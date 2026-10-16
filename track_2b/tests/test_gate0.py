import io
import json
import hashlib
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "gate0"))
import pymupdf as fitz
import source_probe
import model_probe
import local_model

class SourceAndModelTests(unittest.TestCase):
    def test_normalize_whitespace_and_soft_hyphen(self):
        self.assertEqual(source_probe.normalize(" AHV\u00ad \n  Rente "), "AHV Rente")

    def test_soft_hyphen_line_break_is_joined(self):
        self.assertEqual(source_probe.normalize("zusätz\u00ad\nlichen Ausgaben"), "zusätzlichen Ausgaben")

    def test_blocks_keep_sidebar_out_of_body_sentence(self):
        page = mock.Mock()
        page.get_text.return_value = [
            (0, 0, 20, 20, "Initiative will eine\n13. AHV-Rente\n", 0, 0),
            (100, 0, 300, 40, "Die Initiative fordert, dass die Rente\n13 Mal ausbezahlt wird.\n", 1, 0)]
        text, blocks = source_probe.page_text(page, "blocks-v2")
        self.assertIn("Die Initiative fordert, dass die Rente 13 Mal ausbezahlt wird.", text)
        self.assertEqual(blocks[1]["bbox"], [100, 0, 300, 40])
        self.assertEqual(blocks[1]["raw_text"], page.get_text.return_value[1][4])

    def test_legacy_normalization_preserved_for_old_traces(self):
        self.assertEqual(source_probe.normalize_legacy("zusätz\u00ad\nlichen"), "zusätz lichen")

    def test_pdf_magic_rejects_wrong_doc(self):
        with self.assertRaises(Exception):
            source_probe.build_report(b"Not a PDF")

    def test_unverified_quote_is_not_promoted(self):
        report = {"as_of":"2023-11-29", "selected_pages":[
            {"pdf_page":11,"expected_role":"FEDERAL_COUNCIL_DETAIL_FINANCING",
            "text":"Die Initiative macht keine Angaben zur Finanzierung der Ausgaben."}
        ]}
        answer = {"claims":[
            {"kind":"UNRESOLVED","pdf_page":11,"quote":"Die Initiative macht keine Angaben","attribution":"FEDERAL_COUNCIL_DETAIL_FINANCING"},
            {"kind":"DIRECT_PROVISION","pdf_page":11,"quote":"Arbeitnehmer zahlen 100 Franken","attribution":"FEDERAL_COUNCIL_DETAIL_FINANCING"}]}
        checks=model_probe.check_grounding(answer,report)
        self.assertTrue(checks[0]["quote_in_page"])
        self.assertFalse(checks[1]["quote_in_page"])
        self.assertTrue(all(x["publication_state"]=="CANDIDATE_UNREVIEWED" for x in checks))

    def test_unallowed_model_rejected_before_network(self):
        with self.assertRaisesRegex(RuntimeError, "actual Apertus"):
            model_probe.run_inference({}, "gpt-4o", "https://api.example.org/v1", "x")

    def test_nonlocal_without_api_key_fails_before_network(self):
        with self.assertRaisesRegex(RuntimeError, "LLM_API_KEY"):
            model_probe.run_inference({}, "swiss-ai/Apertus-v1.5-8B", "https://api.example.org/v1", "")

    def test_prompt_protects_temporal_boundary(self):
        report={"selected_pages":[{"pdf_page":11,"expected_role":"FEDERAL_COUNCIL_DETAIL_FINANCING","text":"financing remains open"}]}
        prompt=model_probe.prompt_for(report)
        self.assertIn("BEFORE the 3 March 2024",prompt)
        self.assertIn("financing open",prompt)
        self.assertIn("No invented page numbers",prompt)

class FailClosedTests(unittest.TestCase):
    """Synthetic unit controls, never represented as model inference."""
    def setUp(self):
        self.report = {"as_of": "2023-11-29", "sha256": "fixture-only", "source_url": "https://example.invalid/fixture", "selected_pages": [
            {"pdf_page": 11, "expected_role": "FEDERAL_COUNCIL_DETAIL_FINANCING",
             "text": "Die Initiative macht keine Angaben zur Finanzierung der Ausgaben."}]}
        self.answer = {"outcome": "INSUFFICIENT_EVIDENCE", "personal_financing_chf": None,
                       "unknowns": ["The enacted financing formula is missing."], "claims": [
            {"kind": "UNRESOLVED", "statement": "Financing is unspecified.", "pdf_page": 11,
             "quote": "Die Initiative macht keine Angaben", "attribution": "FEDERAL_COUNCIL_DETAIL_FINANCING",
             "as_of": "2023-11-29"}]}

    def check(self, answer=None):
        return model_probe.validate_answer(answer if answer is not None else self.answer,
            self.report, require_coverage=False, expected_outcome="INSUFFICIENT_EVIDENCE")

    def test_valid_candidate_still_requires_semantic_review(self):
        result = self.check()
        self.assertTrue(result["mechanical_pass"])
        self.assertFalse(result["semantic_support_verified"])
        self.assertEqual(result["publication_state"], "CANDIDATE_UNREVIEWED")

    def test_fake_quote_rejected(self):
        self.answer["claims"][0]["quote"] = "Employees must pay 100 francs"
        self.assertIn("claim_0:quote_in_page", self.check()["errors"])

    def test_case_changed_quote_rejected(self):
        self.answer["claims"][0]["quote"] = self.answer["claims"][0]["quote"].upper()
        self.assertFalse(self.check()["mechanical_pass"])

    def test_actor_mixup_rejected(self):
        self.answer["claims"][0]["attribution"] = "INITIATIVE_COMMITTEE_ARGUMENTS"
        self.assertIn("claim_0:role_matches_page", self.check()["errors"])

    def test_unsupported_chf_rejected(self):
        self.answer["personal_financing_chf"] = 280
        self.assertIn("unsupported_personal_financing", self.check()["errors"])

    def test_temporal_leakage_rejected(self):
        self.answer["claims"][0]["as_of"] = "2026-10-12"
        self.assertIn("claim_0:as_of_matches", self.check()["errors"])

    def test_empty_claims_do_not_pass_full_gate(self):
        self.answer["claims"] = []
        result = model_probe.validate_answer(self.answer, self.report)
        self.assertFalse(result["mechanical_pass"])

    def test_malformed_claims_fail_without_crashing(self):
        for value in (None, "text", [{}], [None], [{"pdf_page": [], "kind": []}]):
            with self.subTest(value=value):
                self.answer["claims"] = value
                self.assertFalse(self.check()["mechanical_pass"])

    def test_known_prefix_does_not_allow_invented_model(self):
        with self.assertRaisesRegex(RuntimeError, "actual Apertus"):
            model_probe.run_inference({}, "swiss-ai/apertus-fake", "http://127.0.0.1:8766/v1", "")

    def test_loopback_is_hostname_not_substring(self):
        for url in ("https://localhost.evil.example/v1", "https://evil.example/localhost", "https://127.0.0.1.evil.example/v1"):
            with self.subTest(url=url):
                with self.assertRaises((ValueError, RuntimeError)):
                    model_probe.run_inference({}, "swiss-ai/Apertus-v1.5-8B", url, "")

    def test_credentials_in_url_rejected(self):
        with self.assertRaises(ValueError):
            local_model.endpoint_url("http://secret@127.0.0.1:8766/v1")

    def test_unverified_local_alias_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "unverified aliases"):
            model_probe.run_inference({}, "default_model", "http://127.0.0.1:8766/v1", "")

    def test_stale_local_identity_endpoint_rejected_before_inspection(self):
        with self.assertRaisesRegex(RuntimeError, "mismatch"):
            local_model.validate_identity({"served_alias": "default_model", "backing_checkpoint": local_model.CHECKPOINT}, "default_model", "http://127.0.0.1:9999/v1")

    def test_wrong_source_edition_rejected_before_network(self):
        with self.assertRaisesRegex(ValueError, "edition"):
            model_probe.run_inference({}, "swiss-ai/Apertus-v1.5-8B", "http://127.0.0.1:8766/v1", "", source_pdf_data=b"fixture")

    def test_no_source_pdf_fails_before_network(self):
        with self.assertRaisesRegex(ValueError, "PDF bytes"):
            model_probe.run_inference({}, "swiss-ai/Apertus-v1.5-8B", "http://127.0.0.1:8766/v1", "")

    def test_truncated_response_preserves_raw_trace(self):
        body = {"model": "swiss-ai/Apertus-v1.5-8B", "choices": [{"finish_reason": "length", "message": {"content": "{"}}]}
        with mock.patch.object(model_probe, "validate_report"), mock.patch.object(
                model_probe.urllib.request, "urlopen") as opening:
            opening.return_value.__enter__.return_value.read.return_value = json.dumps(body).encode()
            result = model_probe.run_inference(self.report, body["model"], "http://127.0.0.1:8766/v1", "", source_pdf_data=b"fixture")
        self.assertFalse(result["validation"]["mechanical_pass"])
        self.assertEqual(json.loads(result["raw_response_text"]), body)

    def test_missing_direct_projection_and_unknown_is_failure(self):
        result = model_probe.validate_answer(self.answer, self.report)
        self.assertIn("required_kind_coverage_missing", result["errors"])

    def test_legacy_manifest_cannot_claim_v15(self):
        identity = {"backing_checkpoint": local_model.CHECKPOINT, "model_id": local_model.MODEL_ID,
            "source_revision": local_model.REVISION, "served_alias": "default_model",
            "base_url": "http://127.0.0.1:8766/v1", "evidence_class": "LOCAL_MODEL_INSPECTION",
            "v1_5_verified": True}
        with self.assertRaisesRegex(RuntimeError, "mismatch"):
            local_model.validate_identity(identity, "default_model", identity["base_url"])

    def test_v15_manifest_with_wrong_weights_is_rejected(self):
        checkpoint = "swiss-ai/Apertus-v1.5-8B"
        profile = local_model.SUPPORTED[checkpoint]
        identity = {"backing_checkpoint": checkpoint, "model_id": profile["model_id"],
            "source_revision": profile["revision"], "served_alias": "default_model",
            "base_url": "http://127.0.0.1:8766/v1", "evidence_class": "LOCAL_MODEL_INSPECTION",
            "v1_5_verified": True, "artifacts": {"model.safetensors": {"sha256": local_model.WEIGHTS_SHA256}}}
        with self.assertRaisesRegex(RuntimeError, "pinned Apertus weights"):
            local_model.validate_identity(identity, "default_model", identity["base_url"])

    def test_matching_quote_does_not_prove_interpretation(self):
        self.answer["claims"][0]["statement"] = "Every employee has an enacted CHF 280 obligation."
        result = self.check()
        self.assertTrue(result["mechanical_pass"])
        self.assertFalse(result["semantic_support_verified"])
        self.assertEqual(result["publication_state"], "CANDIDATE_UNREVIEWED")

    def test_quote_length_limit_is_enforced(self):
        self.report["selected_pages"][0]["text"] = "A" * 300
        self.answer["claims"][0]["quote"] = "A" * 241
        self.assertIn("claim_0:quote_length_valid", self.check()["errors"])


    def test_non_object_api_response_is_recorded_as_failure(self):
        with mock.patch.object(model_probe, "validate_report"), mock.patch.object(
                model_probe.urllib.request, "urlopen") as opening:
            opening.return_value.__enter__.return_value.read.return_value = b"[]"
            result = model_probe.run_inference(self.report, "swiss-ai/Apertus-v1.5-8B",
                "http://127.0.0.1:8766/v1", "", source_pdf_data=b"fixture")
        self.assertFalse(result["validation"]["mechanical_pass"])
        self.assertEqual(result["raw_response_text"], "[]")

class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.report = {"evidence_class": "SOURCE", "source_url": source_probe.SOURCE_URL,
            "sha256": source_probe.SOURCE_SHA256, "as_of": source_probe.EDITORIAL_CUTOFF,
            "editorial_cutoff": source_probe.EDITORIAL_CUTOFF, "referendum_date": source_probe.REFERENDUM_DATE,
            "page_count": 32, "model_inference_performed": False, "selected_pages": [
                {"pdf_page": number, "expected_role": role, "text": "Synthetic unit text",
                 "text_sha256": hashlib.sha256(b"Synthetic unit text").hexdigest(),
                 "available_at": source_probe.EDITORIAL_CUTOFF}
                for number, role in source_probe.TARGET_PAGES.items()]}

    def test_consistent_report_without_pdf_is_not_authenticated(self):
        # Consistency alone accepts this synthetic text; production inference requires PDF bytes.
        self.assertIs(source_probe.validate_report(self.report), self.report)
        with self.assertRaisesRegex(ValueError, "pinned"):
            source_probe.validate_report(self.report, b"synthetic PDF bytes")

    def test_changed_excerpt_hash_rejected(self):
        self.report["selected_pages"][0]["text"] = "Altered text"
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            source_probe.validate_report(self.report)

    def test_later_source_availability_rejected(self):
        self.report["selected_pages"][0]["available_at"] = "2026-10-12"
        with self.assertRaisesRegex(ValueError, "temporal leakage"):
            source_probe.validate_report(self.report)

    def test_duplicate_page_rejected(self):
        self.report["selected_pages"][1] = self.report["selected_pages"][0]
        with self.assertRaisesRegex(ValueError, "page set"):
            source_probe.validate_report(self.report)

    def test_wrong_actor_in_source_report_rejected(self):
        self.report["selected_pages"][0]["expected_role"] = "INITIATIVE_COMMITTEE_ARGUMENTS"
        with self.assertRaisesRegex(ValueError, "metadata"):
            source_probe.validate_report(self.report)

    def test_wrong_edition_hash_rejected(self):
        self.report["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "edition"):
            source_probe.validate_report(self.report)

    def test_editorial_cutoff_cannot_be_claimed_as_publication_date(self):
        self.report.update({"extraction_version": "blocks-v3", "published_at": None,
            "public_availability_verified": False,
            "temporal_basis": "PRINTED_EDITORIAL_CUTOFF_NOT_PUBLICATION_DATE"})
        for page in self.report["selected_pages"]:
            page.update({"available_at": None, "knowledge_cutoff_at": source_probe.EDITORIAL_CUTOFF})
        source_probe.validate_report(self.report)
        self.report["published_at"] = source_probe.EDITORIAL_CUTOFF
        with self.assertRaisesRegex(ValueError, "frame mismatch"):
            source_probe.validate_report(self.report)

if __name__=="__main__":
    unittest.main()
