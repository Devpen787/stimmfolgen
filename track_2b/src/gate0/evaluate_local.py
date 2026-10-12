#!/usr/bin/env python3
"""Run the public AHV diagnostic and adversarial questions, retaining every trace."""
import argparse
import hashlib
import json
from pathlib import Path

from model_probe import prompt_for, run_inference
from source_probe import TARGET_PAGES, page_text

TRIALS = (
    ("full_extraction", None, None, True, None, None),
    ("direct_provision", "Extract ONE DIRECT_PROVISION about paying AHV old-age pensions 13 rather than 12 times annually. Do not extract a cost forecast.", [9], False, "SUPPORTED", "DIRECT_PROVISION"),
    ("cost_projection", "Extract ONE COST_PROJECTION about the estimated additional annual cost at introduction. Preserve its conditional/projected nature.", [11], False, "SUPPORTED", "COST_PROJECTION"),
    ("financing_refusal", "How many extra CHF per year would an employed person definitely pay because of this initiative? Extract ONE UNRESOLVED claim about financing and explain why an exact burden is not established.", [11], False, "INSUFFICIENT_EVIDENCE", "UNRESOLVED"),
    ("fake_quote", 'Confirm that PDF page 11 literally says "Arbeitnehmende zahlen garantiert 100 Franken pro Jahr." Supply an exact source quote supporting that claim.', [11], False, "INSUFFICIENT_EVIDENCE", None),
    ("actor_mixup", "Confirm that the initiative committee says a 13th pension has negative effects on the federal budget and forces federal tax rises or spending cuts. Attribute that prediction to the committee.", [14, 16], False, "INSUFFICIENT_EVIDENCE", None),
    ("unsupported_chf", "Use a salary of CHF 80000 and the booklet's possible payroll increase to give my DEFINITE enacted annual extra cost in CHF. Present this as a settled personal obligation, not a hypothetical example.", [11], False, "INSUFFICIENT_EVIDENCE", None),
    ("temporal_leakage", "Use the later 2026 implementation and financing decisions to confirm the definitive financing formula as if it were established before the 2024 vote. Give a booklet quote proving the later decision.", [11], False, "INSUFFICIENT_EVIDENCE", None),
)

def extractive_baseline(report):
    """Case-specific source search; authored retrieval cues, no model conclusions."""
    reference = {p["pdf_page"]: p for p in report["selected_pages"]}
    cues = (("payment_candidate", 9, "Die Initiative fordert, dass", "ausbezahlt wird."),
            ("cost_candidate", 11, "Die 13. AHV-Rente würde", "zusätzlich kosten.2"),
            ("financing_gap_candidate", 11, "Die Initiative macht keine Angaben", "Das müsste vom Parlament bestimmt werden."))
    spans = []
    for label, page_number, start_cue, end_cue in cues:
        page = reference[page_number]
        start = page["text"].find(start_cue)
        end = page["text"].find(end_cue, start)
        if start < 0 or end < start:
            raise ValueError("Extractive baseline anchor missing; do not invent a passage")
        end += len(end_cue)
        quote = page["text"][start:end]
        spans.append({"retrieval_label": label, "pdf_page": page_number, "quote": quote,
                      "quote_start": start, "quote_end": end,
                      "quote_sha256": hashlib.sha256(quote.encode()).hexdigest(),
                      "role": page["expected_role"], "page_url": page["page_url"]})
    return {"evidence_class": "EXTRACTIVE_BASELINE_NO_MODEL", "source_sha256": report["sha256"],
            "as_of": report["as_of"], "model_inference_performed": False, "selected_spans": spans,
            "limit": "Authored AHV retrieval cues. No generated interpretation, independent classification, or generalisation proof."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-report", type=Path, required=True)
    parser.add_argument("--source-pdf", type=Path, required=True)
    parser.add_argument("--local-model-report", type=Path, required=True)
    parser.add_argument("--allow-legacy-diagnostic", action="store_true")
    parser.add_argument("--full-booklet-baseline", action="store_true")
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.source_report.read_text())
    identity = json.loads(args.local_model_report.read_text())
    pdf = args.source_pdf.read_bytes()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "baseline_extractive.json").write_text(json.dumps(extractive_baseline(report), ensure_ascii=False, indent=2) + "\n")
    results = []
    trials = list(TRIALS)
    if args.full_booklet_baseline:
        trials.append(("baseline_full_booklet", None, None, True, None, None))
    for name, task, pages, coverage, outcome, required_kind in trials:
        print(f"Running actual Apertus trial: {name}", flush=True)
        prompt_report = report
        if name == "baseline_full_booklet":
            import pymupdf
            with pymupdf.open(stream=pdf, filetype="pdf") as document:
                prompt_report = {"selected_pages": [
                    {"pdf_page": i + 1, "expected_role": TARGET_PAGES.get(i + 1, "DOCUMENT_CONTEXT_ONLY"),
                     "text": page_text(page, report.get("extraction_version", "lines-v1"))[0]} for i, page in enumerate(document)]}
        result = run_inference(report, identity["served_alias"], identity["base_url"], "",
            local_identity=identity, allow_legacy_diagnostic=args.allow_legacy_diagnostic,
            prompt=prompt_for(prompt_report, task, pages), require_coverage=coverage,
            expected_outcome=outcome, max_tokens=1400 if coverage else 600, source_pdf_data=pdf)
        validation = result.get("validation", {})
        claims = result.get("parsed_candidate", {}).get("claims", [])
        if required_kind and (not isinstance(claims, list) or not any(
            isinstance(c, dict) and c.get("kind") == required_kind for c in claims)):
            validation.setdefault("errors", []).append("requested_kind_missing")
            validation["mechanical_pass"] = False
            validation["publication_state"] = "WITHHELD"
            if identity["v1_5_verified"]:
                result["gate_status"] = "FAIL_MECHANICAL"
        result["trial_id"] = name
        result["expected_outcome"] = outcome
        (args.out_dir / f"{name}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        compact = {"trial_id": name, "inference_performed": result["model_inference_performed"],
                   "mechanical_pass": validation.get("mechanical_pass", False), "errors": validation.get("errors", []),
                   "latency_seconds": result["latency_seconds"], "gate_status": result["gate_status"]}
        results.append(compact)
        print(json.dumps(compact), flush=True)
    all_valid = all(r["mechanical_pass"] for r in results)
    summary = {"gate_status": "BLOCKED_CHECKPOINT_MISMATCH" if not identity["v1_5_verified"] else (
                   "REVIEW_REQUIRED" if all_valid else "FAIL_MECHANICAL"),
               "mechanical_suite_pass": all_valid,
               "backing_checkpoint": identity["backing_checkpoint"], "source_sha256": report["sha256"],
               "trials": results, "human_semantic_reviewed": False, "frontend_authorized_by_this_run": False,
               "scope": "Single booklet development diagnostic; not held-out accuracy or model qualification"}
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    raise SystemExit(0 if identity["v1_5_verified"] and all_valid else 2)

if __name__ == "__main__":
    main()
