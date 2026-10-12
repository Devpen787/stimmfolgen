import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "gate0"))
import fitz
import source_probe
import model_probe

class SourceAndModelTests(unittest.TestCase):
    def test_normalize_whitespace_and_soft_hyphen(self):
        self.assertEqual(source_probe.normalize(" AHV\u00ad \n  Rente "), "AHV Rente")

    def test_pdf_magic_rejects_wrong_doc(self):
        with self.assertRaises(Exception):
            source_probe.build_report(b"Not a PDF")

    def test_unverified_quote_is_not_promoted(self):
        report = {"selected_pages":[
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

if __name__=="__main__":
    unittest.main()
