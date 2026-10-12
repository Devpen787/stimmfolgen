#!/usr/bin/env python3
"""Gate 0: call a REAL Apertus OpenAI-compatible endpoint on verified source text.

No silent model substitution, no fixture result advertised as a run,
no policy conclusion auto-promoted beyond unreviewed CANDIDATE.
"""
import argparse
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from source_probe import normalize

ALLOWED_KINDS = {"DIRECT_PROVISION", "ATTRIBUTED_PREDICTION", "COST_PROJECTION", "UNRESOLVED"}
SOURCE_ROLES = {
    "FEDERAL_COUNCIL_SUMMARY",
    "FEDERAL_COUNCIL_DETAIL",
    "FEDERAL_COUNCIL_DETAIL_FINANCING",
    "INITIATIVE_COMMITTEE_ARGUMENTS",
    "FEDERAL_COUNCIL_PARLIAMENT_ARGUMENTS",
}

def prompt_for(report):
    excerpts = "\n\n".join(
        f"PDF PAGE {p['pdf_page']} — {p['expected_role']}:\n{p['text'][:3400]}"
        for p in report["selected_pages"]
    )
    return (
        "You are extracting CANDIDATE statements from an archived Swiss referendum booklet, "
        "as it was known BEFORE the 3 March 2024 vote. Do not use later information. "
        "Never recommend a voting choice or assert a specific future personal CHF cost "
        "unless its financing formula is established by the passage. Distinguish the committee's "
        "predictions from the federal government's explanations and proposed law. "
        "Return ONLY a JSON object with claims array and unknowns array. "
        "Each claim: kind (DIRECT_PROVISION, ATTRIBUTED_PREDICTION, COST_PROJECTION, UNRESOLVED), "
        "statement (plain English), pdf_page (1-indexed integer), "
        "quote (short EXACT verbatim substring from that page), "
        "attribution (the ROLE tag for that page). "
        "Include at least one unknown about an exact employed person's future financing burden "
        "if the document leaves the actual financing open. "
        "Quotes must be copied EXACTLY from the supplied page text. "
        "No invented page numbers. No speculation as established facts.\n\n"
        + excerpts
    )

def parse_response(raw):
    content = raw["choices"][0]["message"]["content"]
    if isinstance(content, list):
        content = "".join(item.get("text", "") for item in content if isinstance(item, dict))
    if not isinstance(content, str):
        raise ValueError("Unexpected completion content format")
    candidate = content.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^\`\`\`(?:json)?\s*|\s*\`\`\`$", "", candidate, flags=re.I).strip()
    return json.loads(candidate)

def check_grounding(answer, report):
    reference = {p["pdf_page"]: p for p in report["selected_pages"]}
    checks = []
    for claim in answer.get("claims", []):
        page = reference.get(claim.get("pdf_page"))
        quote = claim.get("quote")
        kind = claim.get("kind")
        attr = claim.get("attribution")
        checks.append({
            "kind": kind,
            "pdf_page": claim.get("pdf_page"),
            "page_exists": bool(page),
            "quote_in_page": bool(page and isinstance(quote, str) and
                                  len(quote.strip()) >= 8 and
                                  normalize(quote).casefold() in page["text"].casefold()),
            "role_matches_page": bool(page and attr == page["expected_role"]),
            "known_kind": kind in ALLOWED_KINDS,
            "publication_state": "CANDIDATE_UNREVIEWED",
        })
    return checks

def run_inference(report, model_id, base_url, api_key):
    if not base_url:
        raise RuntimeError("LLM_BASE_URL is required; configure a real Apertus endpoint")
    if not model_id.lower().startswith("swiss-ai/apertus"):
        raise RuntimeError("Gate 0 requires actual Apertus; refuses substitute models")
    if not api_key and not any(h in base_url for h in ("localhost", "127.0.0.1", "host.docker.internal")):
        raise RuntimeError("LLM_API_KEY required for non-local inference; do not commit secrets")
    endpoint = base_url.rstrip("/")
    if not endpoint.endswith("/v1"):
        endpoint += "/v1"
    payload = {
        "model": model_id, "temperature": 0.1, "max_tokens": 1800,
        "messages": [
            {"role": "system", "content": "Extract candidate evidence with faithful, attributed citations. No voting advice."},
            {"role": "user", "content": prompt_for(report)},
        ],
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(
        endpoint + "/chat/completions", data=json.dumps(payload).encode(),
        headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        body = json.load(response)
    answer = parse_response(body)
    checks = check_grounding(answer, report)
    return {
        "evidence_class": "ACTUAL_MODEL_ATTEMPT_UNREVIEWED",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": model_id,
        "base_url": endpoint,  # NEVER include authentication
        "source_sha256": report["sha256"],
        "source_url": report["source_url"],
        "as_of": report["as_of"],
        "generation": {"temperature": 0.1, "max_tokens": 1800},
        "raw_api_response": body,
        "parsed_candidate": answer,
        "mechanical_grounding_checks": checks,
        "model_inference_performed": True,
        "human_semantic_reviewed": False,
        "promoted_to_verified_effect": False,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-report", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("gate0-model.json"))
    args = p.parse_args()
    report = json.loads(args.source_report.read_text())
    if report.get("model_inference_performed") is not False or not report.get("selected_pages"):
        raise ValueError("Need unmodified source report; no verified pages")
    result = run_inference(report, os.getenv("LLM_NAME", "swiss-ai/Apertus-v1.5-8B"),
                           os.getenv("LLM_BASE_URL"), os.getenv("LLM_API_KEY"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "model": result["model"], "source_sha256": result["source_sha256"],
        "candidate_claims": len(result["mechanical_grounding_checks"]),
        "quotes_found": sum(x["quote_in_page"] for x in result["mechanical_grounding_checks"]),
        "human_semantic_reviewed": False
    }, indent=2))

if __name__ == "__main__":
    main()
