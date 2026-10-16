#!/usr/bin/env python3
"""Gate 0: independently fetch the official March 2024 voting PDF and record provenance.

This is SOURCE proof, not Apertus inference or semantic policy verification.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = "https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf"
SOURCE_SHA256 = "53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e"
EDITORIAL_CUTOFF = "2023-11-29"  # printed page 2
REFERENDUM_DATE = "2024-03-03"
# 1-indexed PDF pages; clearly distinct from source's 2nd initiative.
TARGET_PAGES = {
    4: "FEDERAL_COUNCIL_SUMMARY",
    9: "FEDERAL_COUNCIL_DETAIL",
    11: "FEDERAL_COUNCIL_DETAIL_FINANCING",
    14: "INITIATIVE_COMMITTEE_ARGUMENTS",
    16: "FEDERAL_COUNCIL_PARLIAMENT_ARGUMENTS",
}

def normalize(text):
    # Join only actual soft-hyphen line continuations; keep ordinary word boundaries.
    text = re.sub(r"[\u00ad\u0002]\n[ \t]*(?=[a-zäöüß])", "", text)
    return re.sub(r"\s+", " ", text.replace("\u00ad", "").replace("\u0002", "")).strip()

def normalize_legacy(text):
    return re.sub(r"\s+", " ", text.replace("\u00ad", "").replace("\u0002", "")).strip()

def download(url=SOURCE_URL, timeout=30):
    if url != SOURCE_URL:
        raise ValueError("This probe only downloads the explicitly allowlisted federal source URL")
    request = Request(url, headers={"User-Agent": "StimmFolgen-SourceVerification/0.1"})
    with urlopen(request, timeout=timeout) as response:
        content = response.read(8 * 1024 * 1024 + 1)
        if len(content) > 8 * 1024 * 1024:
            raise RuntimeError("Source exceeds 8 MB acquisition cap")
        if not content.startswith(b"%PDF-"):
            raise RuntimeError("Official URL did not return PDF bytes")
    return content

def page_text(page, extraction_version):
    if extraction_version == "lines-v1":
        return normalize_legacy(page.get_text("text", sort=True)), None
    if extraction_version not in {"blocks-v2", "blocks-v3"}:
        raise ValueError("Unsupported source extraction version")
    # Preserve complete text blocks: line sorting interleaves left-hand headings with body sentences.
    blocks = [{"bbox": list(block[:4]), "block_number": block[5], "raw_text": block[4]}
              for block in page.get_text("blocks", sort=True) if block[6] == 0]
    return normalize("\n".join(block["raw_text"] for block in blocks)), blocks

def inspect_pdf(data, extraction_version="blocks-v3"):
    import pymupdf as fitz
    pdf = fitz.open(stream=data, filetype="pdf")
    if len(pdf) != 32:
        raise AssertionError("Unexpected voting booklet pagination")
    if "Redaktionsschluss: 29. November 2023" not in normalize(pdf[1].get_text()):
        raise AssertionError("Editorial cutoff does not match the printed booklet")
    pages = []
    for number, expected_role in TARGET_PAGES.items():
        txt, blocks = page_text(pdf[number - 1], extraction_version)
        if len(txt) < 150:
            raise AssertionError(f"Page {number} missing extractable text (possibly scanned)")
        pages.append({"pdf_page": number, "printed_page": number,
                      "expected_role": expected_role, "text": txt,
                      "text_sha256": hashlib.sha256(txt.encode()).hexdigest(),
                      "available_at": EDITORIAL_CUTOFF,
                      "page_url": f"{SOURCE_URL}#page={number}"})
        if blocks is not None:
            pages[-1]["raw_text_blocks"] = blocks
        if extraction_version == "blocks-v3":
            # The printed editorial cutoff is a knowledge basis, not a proven publication date.
            pages[-1]["available_at"] = None
            pages[-1]["knowledge_cutoff_at"] = EDITORIAL_CUTOFF
    # These are guardrails to catch a changed PDF/wrong document, not semantic validation.
    by_page = {p["pdf_page"]: p["text"].casefold() for p in pages}
    if "13. ahv" not in by_page[4] or "finanzierung" not in by_page[11]:
        raise AssertionError("Expected first-referendum anchors not found")
    return {"page_count": len(pdf), "selected_pages": pages}

def build_report(data, extraction_version="blocks-v3"):
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise ValueError("PDF bytes do not match the pinned March 2024 edition")
    report = {
        "evidence_class": "SOURCE",
        "source_url": SOURCE_URL,
        "sha256": hashlib.sha256(data).hexdigest(),
        "byte_size": len(data),
        "language": "de",
        "publisher": "Swiss Federal Chancellery (Bundeskanzlei)",
        "referendum_date": REFERENDUM_DATE,
        "editorial_cutoff": EDITORIAL_CUTOFF,
        "as_of": EDITORIAL_CUTOFF,
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
        "model_inference_performed": False,
        **inspect_pdf(data, extraction_version),
    }
    if extraction_version != "lines-v1":
        report["extraction_version"] = extraction_version
    if extraction_version == "blocks-v3":
        report.update({"temporal_basis": "PRINTED_EDITORIAL_CUTOFF_NOT_PUBLICATION_DATE",
                       "public_availability_verified": False, "published_at": None})
    return report

def validate_report(report, pdf_data=None):
    """Reject changed editions, hindsight frames and malformed page metadata.

    With pdf_data, also re-extract the pinned bytes and compare every page.
    Without it this validates report consistency, not authenticity of excerpts.
    """
    if not isinstance(report, dict):
        raise ValueError("Source report must be an object")
    expected = {"evidence_class": "SOURCE", "source_url": SOURCE_URL,
                "sha256": SOURCE_SHA256, "as_of": EDITORIAL_CUTOFF,
                "editorial_cutoff": EDITORIAL_CUTOFF,
                "referendum_date": REFERENDUM_DATE, "page_count": 32,
                "model_inference_performed": False}
    if report.get("extraction_version") == "blocks-v3":
        expected.update({"temporal_basis": "PRINTED_EDITORIAL_CUTOFF_NOT_PUBLICATION_DATE",
                         "public_availability_verified": False, "published_at": None})
    if any(report.get(k) != v for k, v in expected.items()):
        raise ValueError("Source edition or pre-vote frame mismatch")
    pages = report.get("selected_pages")
    if not isinstance(pages, list) or len(pages) != len(TARGET_PAGES):
        raise ValueError("Expected five unique source pages")
    if {p.get("pdf_page") for p in pages if isinstance(p, dict)} != set(TARGET_PAGES):
        raise ValueError("Source page set mismatch")
    for page in pages:
        temporal_ok = (page.get("available_at") is None and page.get("knowledge_cutoff_at") == EDITORIAL_CUTOFF
                       if report.get("extraction_version") == "blocks-v3"
                       else page.get("available_at") == EDITORIAL_CUTOFF)
        if (type(page.get("pdf_page")) is not int or
            page.get("expected_role") != TARGET_PAGES.get(page["pdf_page"]) or
            not temporal_ok or
            not isinstance(page.get("text"), str) or
            page.get("text_sha256") != hashlib.sha256(page["text"].encode()).hexdigest()):
            raise ValueError("Source page metadata/hash mismatch or temporal leakage")
    if pdf_data is not None:
        rebuilt = build_report(pdf_data, report.get("extraction_version", "lines-v1"))
        if report["selected_pages"] != rebuilt["selected_pages"]:
            raise ValueError("Report excerpts do not match re-extracted official PDF bytes")
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", type=Path, help="Use a manually acquired official PDF, instead of download")
    p.add_argument("--out", type=Path, default=Path("gate0-source.json"))
    p.add_argument("--pdf-out", type=Path, help="Cache the exact source bytes for model verification")
    p.add_argument("--extraction-version", choices=("lines-v1", "blocks-v2", "blocks-v3"), default="blocks-v3")
    p.add_argument("--spans-out", type=Path, help="Compile immutable spans authenticated against original bytes")
    args = p.parse_args()
    if args.pdf:
        data = args.pdf.read_bytes()
        if not data.startswith(b"%PDF-"):
            raise ValueError("Input is not a PDF")
    else:
        data = download()
    report = build_report(data, args.extraction_version)
    if args.pdf_out:
        args.pdf_out.parent.mkdir(parents=True, exist_ok=True)
        args.pdf_out.write_bytes(data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if args.spans_out:
        from source_spans import build_catalog
        from semantic_eval import validate_reference
        catalog = build_catalog(report, data)
        reference = json.loads((Path(__file__).resolve().parents[2] / "tests/references/ahv13_semantics.json").read_text())
        validate_reference(reference, catalog)
        args.spans_out.parent.mkdir(parents=True, exist_ok=True)
        args.spans_out.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "evidence_class": "SOURCE",
        "sha256": report["sha256"],
        "bytes": report["byte_size"],
        "page_count": report["page_count"],
        "selected_pdf_pages": [r["pdf_page"] for r in report["selected_pages"]],
        "model_inference_performed": False
    }, indent=2))

if __name__ == "__main__":
    main()
