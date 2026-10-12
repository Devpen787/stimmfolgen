#!/usr/bin/env python3
"""Gate 0: independently fetch the official March 2024 voting PDF and record provenance.

This is SOURCE proof, not Apertus inference or semantic policy verification.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = "https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf"
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

def inspect_pdf(data):
    import fitz  # PyMuPDF
    pdf = fitz.open(stream=data, filetype="pdf")
    if len(pdf) < 18:
        raise AssertionError("Unexpectedly short voting booklet")
    pages = []
    for number, expected_role in TARGET_PAGES.items():
        txt = normalize(pdf[number - 1].get_text("text", sort=True))
        if len(txt) < 150:
            raise AssertionError(f"Page {number} missing extractable text (possibly scanned)")
        pages.append({"pdf_page": number, "expected_role": expected_role, "text": txt})
    # These are guardrails to catch a changed PDF/wrong document, not semantic validation.
    by_page = {p["pdf_page"]: p["text"].casefold() for p in pages}
    if "13. ahv" not in by_page[4] or "finanzierung" not in by_page[11]:
        raise AssertionError("Expected first-referendum anchors not found")
    return {"page_count": len(pdf), "selected_pages": pages}

def build_report(data):
    return {
        "evidence_class": "SOURCE",
        "source_url": SOURCE_URL,
        "sha256": hashlib.sha256(data).hexdigest(),
        "byte_size": len(data),
        "language": "de",
        "publisher": "Swiss Federal Chancellery (Bundeskanzlei)",
        "referendum_date": REFERENDUM_DATE,
        "editorial_cutoff": EDITORIAL_CUTOFF,
        "as_of": EDITORIAL_CUTOFF,
        "model_inference_performed": False,
        **inspect_pdf(data),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", type=Path, help="Use a manually acquired official PDF, instead of download")
    p.add_argument("--out", type=Path, default=Path("gate0-source.json"))
    args = p.parse_args()
    if args.pdf:
        data = args.pdf.read_bytes()
        if not data.startswith(b"%PDF-"):
            raise ValueError("Input is not a PDF")
    else:
        data = download()
    report = build_report(data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
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
