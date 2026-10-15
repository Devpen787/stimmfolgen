#!/usr/bin/env python3
"""Real Apertus evidence recorder. Mechanical validity never grants publication."""
import argparse
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from local_model import endpoint_url, is_loopback, validate_identity
from source_probe import normalize, validate_report

ALLOWED_KINDS = {"DIRECT_PROVISION", "ATTRIBUTED_PREDICTION", "COST_PROJECTION", "UNRESOLVED"}
MODEL_IDS = {f"swiss-ai/apertus-v1.5-{s}" for s in ("8b", "70b")} | {f"swiss-ai/apertus-{s}-instruct-2509" for s in ("8b", "70b")}
PROMPT_VERSION = "gate0-v3-schema-and-blocks"

def prompt_for(report, task=None, pages=None):
    selected = [p for p in report["selected_pages"] if pages is None or p["pdf_page"] in pages]
    roles = {str(p["pdf_page"]): p["expected_role"] for p in selected}
    claim_schema = {"type": "object", "required": ["kind", "statement", "pdf_page", "quote", "attribution", "as_of"],
        "properties": {"kind": {"enum": sorted(ALLOWED_KINDS)}, "statement": {"type": "string"},
            "pdf_page": {"enum": [p["pdf_page"] for p in selected]}, "quote": {"type": "string", "maxLength": 240},
            "attribution": {"enum": sorted(set(roles.values()))}, "as_of": {"const": "2023-11-29"}}}
    schema = {"type": "object", "required": ["outcome", "claims", "unknowns", "personal_financing_chf"],
        "properties": {"outcome": {"enum": ["SUPPORTED", "INSUFFICIENT_EVIDENCE"]},
            "claims": {"type": "array", "items": claim_schema},
            "unknowns": {"type": "array", "items": {"type": "string"}}, "personal_financing_chf": {"type": "null"}}}
    excerpts = "\n\n".join(f"SOURCE_PAGE {p['pdf_page']} | attribution={p['expected_role']}:\n{p['text']}" for p in selected)
    return (
        "Historical mode: BEFORE the 3 March 2024 vote, as_of=2023-11-29. No invented page numbers.\n"
        "Extrahiere nur aus den unten stehenden Quellen. Kein späteres Wissen, keine Abstimmungsempfehlung. "
        "Gib ausschließlich EIN JSON-Objekt gemäß dem Schema zurück, nicht das Schema selbst. "
        "Alle Pflichtfelder müssen enthalten sein. Keine Markdown-Blöcke oder Einleitung.\n"
        "statement ist eine kurze Antwort auf die Aufgabe. quote ist ein kurzes, wortgetreu kopiertes "
        "zusammenhängendes Zitat (höchstens 240 Zeichen); niemals getrennte Sätze zusammenkleben. "
        "attribution ist exakt der Identifier zur gewählten Seite aus ROLE_MAP, keine Übersetzung oder Umschreibung. "
        "as_of muss für JEDEN claim 2023-11-29 sein. Vorhersagen/Kostenschätzungen sind keine DIRECT_PROVISION. "
        "Nur belegt Vorhandenes extrahieren: falsche Zitate, falsche Urheber und spätere Entscheidungen nicht bestätigen. "
        "Bei nicht belegbaren Anfragen: outcome=INSUFFICIENT_EVIDENCE und mindestens ein konkreter unknown. "
        "claims darf dann leer sein, oder einen tatsächlich belegten UNRESOLVED Sachverhalt enthalten. "
        "Die Finanzierung ist in der Initiative nicht beschlossen: niemals eine definitive persönliche CHF-Belastung "
        "berechnen, personal_financing_chf bleibt null. Eine hypothetische Finanzierungsoption ist kein Gesetz.\n"
        "ROLE_MAP=" + json.dumps(roles) + "\nJSON_SCHEMA=" + json.dumps(schema) + "\nTASK: "
        + (task or "Extract exactly three short claims: one DIRECT_PROVISION about 13 instead of 12 old-age pension payments, "
                   "one COST_PROJECTION or ATTRIBUTED_PREDICTION, and one UNRESOLVED financing issue. "
                   "Include a concrete unknown about an employed person's precise financing burden; the document leaves financing open.")
        + "\n\n" + excerpts
    )

def parse_response(raw):
    content = raw["choices"][0]["message"]["content"]
    if isinstance(content, list):
        content = "".join(item.get("text", "") for item in content if isinstance(item, dict))
    if not isinstance(content, str):
        raise ValueError("Unexpected completion content format")
    candidate = content.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.I).strip()
    answer = json.loads(candidate)
    if not isinstance(answer, dict):
        raise ValueError("Candidate must be a JSON object")
    return answer

def check_grounding(answer, report):
    reference = {p["pdf_page"]: p for p in report["selected_pages"]}
    claims = answer.get("claims", [])
    if not isinstance(claims, list):
        return []
    checks = []
    for claim in claims:
        if not isinstance(claim, dict):
            checks.append({"schema_valid": False, "publication_state": "WITHHELD"})
            continue
        number, quote, kind = claim.get("pdf_page"), claim.get("quote"), claim.get("kind")
        page = reference.get(number) if type(number) is int else None
        normalized = normalize(quote) if isinstance(quote, str) else ""
        offset = page["text"].find(normalized) if page and 8 <= len(normalized) <= 240 else -1
        checks.append({
            "kind": kind, "pdf_page": number, "page_exists": bool(page), "quote_in_page": offset >= 0,
            "role_matches_page": bool(page and claim.get("attribution") == page["expected_role"]),
            "known_kind": isinstance(kind, str) and kind in ALLOWED_KINDS,
            "statement_present": isinstance(claim.get("statement"), str) and bool(claim["statement"].strip()),
            "quote_length_valid": 8 <= len(normalized) <= 240,
            "as_of_matches": claim.get("as_of") == report["as_of"],
            "role_kind_compatible": bool(page and not (kind == "DIRECT_PROVISION" and page["expected_role"] in {
                "INITIATIVE_COMMITTEE_ARGUMENTS", "FEDERAL_COUNCIL_PARLIAMENT_ARGUMENTS"})),
            "quote_start": offset if offset >= 0 else None,
            "quote_end": offset + len(normalized) if offset >= 0 else None,
            "quote_sha256": hashlib.sha256(normalized.encode()).hexdigest() if offset >= 0 else None,
            "source_sha256": report.get("sha256"), "page_url": page.get("page_url") if page else None,
            "publication_state": "CANDIDATE_UNREVIEWED",
        })
    return checks

def validate_answer(answer, report, require_coverage=True, expected_outcome=None):
    errors = []
    if not isinstance(answer, dict):
        return {"mechanical_pass": False, "errors": ["not_object"], "checks": [], "publication_state": "WITHHELD"}
    if not isinstance(answer.get("claims"), list):
        errors.append("claims_not_array")
    checks = check_grounding(answer, report)
    for i, check in enumerate(checks):
        for field in ("page_exists", "quote_in_page", "quote_length_valid", "role_matches_page", "known_kind", "statement_present", "as_of_matches", "role_kind_compatible"):
            if check.get(field) is not True:
                errors.append(f"claim_{i}:{field}")
    unknowns = answer.get("unknowns")
    if not isinstance(unknowns, list) or not all(isinstance(u, str) and u.strip() for u in unknowns):
        errors.append("unknowns_not_string_array")
    if "personal_financing_chf" not in answer or answer.get("personal_financing_chf") is not None:
        errors.append("unsupported_personal_financing")
    outcome = answer.get("outcome")
    if outcome not in ("SUPPORTED", "INSUFFICIENT_EVIDENCE"):
        errors.append("invalid_outcome")
    if expected_outcome and outcome != expected_outcome:
        errors.append("wrong_outcome")
    if outcome == "SUPPORTED" and not checks:
        errors.append("empty_supported_answer")
    if outcome == "INSUFFICIENT_EVIDENCE" and not unknowns:
        errors.append("abstention_requires_unknown")
    if require_coverage:
        kinds = {c.get("kind") for c in checks if isinstance(c.get("kind"), str)}
        if not ("DIRECT_PROVISION" in kinds and "UNRESOLVED" in kinds and kinds & {"COST_PROJECTION", "ATTRIBUTED_PREDICTION"}):
            errors.append("required_kind_coverage_missing")
        if not unknowns:
            errors.append("financing_unknown_missing")
    return {"mechanical_pass": not errors, "errors": errors, "checks": checks,
            "publication_state": "CANDIDATE_UNREVIEWED" if not errors else "WITHHELD", "semantic_support_verified": False}

def run_inference(report, model_id, base_url, api_key, *, local_identity=None, allow_legacy_diagnostic=False,
                  prompt=None, require_coverage=True, expected_outcome=None, max_tokens=1800, source_pdf_data=None,
                  answer_validator=None, prompt_version=None, output_contract="generated-quotes-v1", system_prompt=None):
    if not base_url:
        raise RuntimeError("LLM_BASE_URL is required; configure a real Apertus endpoint")
    if model_id.lower() not in MODEL_IDS and local_identity is None:
        raise RuntimeError("Gate 0 requires actual Apertus; refuses substitute models or unverified aliases")
    endpoint = endpoint_url(base_url)
    if not api_key and not is_loopback(endpoint):
        raise RuntimeError("LLM_API_KEY required for non-local inference; do not commit secrets")
    if source_pdf_data is None:
        raise ValueError("Original source PDF bytes required to authenticate report excerpts")
    validate_report(report, source_pdf_data)
    identity = validate_identity(local_identity, model_id, endpoint) if local_identity is not None else None
    v1_5 = identity["v1_5_verified"] if identity else model_id.lower().startswith("swiss-ai/apertus-v1.5-")
    if not v1_5 and not allow_legacy_diagnostic:
        raise RuntimeError("Installed checkpoint is not v1.5; use explicit legacy diagnostic mode, never mark Gate 0 passed")
    payload = {"model": model_id, "temperature": 0, "max_tokens": max_tokens,
               "messages": [{"role": "system", "content": system_prompt or "Extract candidate evidence with faithful, attributed citations. No voting advice."},
                            {"role": "user", "content": prompt or prompt_for(report)}]}
    request_bytes = json.dumps(payload, ensure_ascii=False).encode()
    headers = {"Content-Type": "application/json", "User-Agent": "StimmFolgen-Gate0/0.2"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(endpoint + "/chat/completions", data=request_bytes, headers=headers, method="POST")
    result = {
        "evidence_class": "ACTUAL_MODEL_ATTEMPT_UNREVIEWED", "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": model_id, "base_url": endpoint, "local_identity": identity,
        "source_sha256": report["sha256"], "source_url": report["source_url"], "as_of": report["as_of"],
        "source_pdf_reverified": True, "prompt_version": prompt_version or PROMPT_VERSION,
        "output_contract": output_contract, "raw_request": payload,
        "request_sha256": hashlib.sha256(request_bytes).hexdigest(), "generation": {"temperature": 0, "max_tokens": max_tokens},
        "model_inference_performed": False, "human_semantic_reviewed": False, "promoted_to_verified_effect": False,
        "v1_5_verified": v1_5, "gate_status": "REVIEW_REQUIRED" if v1_5 else "BLOCKED_CHECKPOINT_MISMATCH",
    }
    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=240) as response:
            raw_text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw_text = exc.read().decode("utf-8", errors="replace")
        result.update({"transport_error": f"HTTP {exc.code}", "http_status": exc.code,
                       "raw_response_text": raw_text,
                       "response_sha256": hashlib.sha256(raw_text.encode()).hexdigest(),
                       "gate_status": "FAIL_TRANSPORT", "latency_seconds": time.monotonic() - start})
        return result
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        result.update({"transport_error": str(exc), "gate_status": "FAIL_TRANSPORT", "latency_seconds": time.monotonic() - start})
        return result
    result.update({"raw_response_text": raw_text, "response_sha256": hashlib.sha256(raw_text.encode()).hexdigest(),
                   "latency_seconds": time.monotonic() - start})
    try:
        body = json.loads(raw_text)
        result["raw_api_response"] = body
        if not isinstance(body, dict):
            raise ValueError("API response must be an object")
        result["model_inference_performed"] = bool(body.get("choices"))
        if body.get("model") != model_id:
            raise ValueError("Response model does not match requested served alias")
        if body["choices"][0].get("finish_reason") != "stop":
            raise ValueError("Completion did not stop normally (possibly truncated)")
        answer = parse_response(body)
        result["parsed_candidate"] = answer
        validator = answer_validator or validate_answer
        result["validation"] = validator(answer, report, require_coverage, expected_outcome)
        result["mechanical_grounding_checks"] = result["validation"]["checks"]
    except (ValueError, KeyError, TypeError, IndexError) as exc:
        result.update({"parse_error": str(exc), "validation": {"mechanical_pass": False, "errors": ["invalid_completion"], "publication_state": "WITHHELD"}})
    if not result["validation"]["mechanical_pass"] and v1_5:
        result["gate_status"] = "FAIL_MECHANICAL"
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-report", type=Path, required=True)
    p.add_argument("--source-pdf", type=Path, required=True)
    p.add_argument("--local-model-report", type=Path)
    p.add_argument("--allow-legacy-diagnostic", action="store_true")
    p.add_argument("--out", type=Path, default=Path("gate0-model.json"))
    args = p.parse_args()
    identity = json.loads(args.local_model_report.read_text()) if args.local_model_report else None
    result = run_inference(json.loads(args.source_report.read_text()), os.getenv("LLM_NAME", "swiss-ai/Apertus-v1.5-8B"),
        os.getenv("LLM_BASE_URL"), os.getenv("LLM_API_KEY"), local_identity=identity,
        allow_legacy_diagnostic=args.allow_legacy_diagnostic, source_pdf_data=args.source_pdf.read_bytes())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("model", "source_sha256", "gate_status", "model_inference_performed")}, indent=2))
    raise SystemExit(0 if result.get("validation", {}).get("mechanical_pass") and result["v1_5_verified"] else 2)

if __name__ == "__main__":
    main()
