#!/usr/bin/env python3
"""Check current-tree hygiene and immutable evidence; not a history or OCR scan."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'track_2b/docs/evidence'


def main():
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    forbidden = re.compile(r'(^|/)(\.local|node_modules|\.env(?:\..*)?|blueprint|adr)(/|$)|\.(safetensors|gguf|ckpt)$')
    private_text = re.compile(r'/(?:Users|home)/[^/\s]+/|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{30,}')
    errors = []
    for name in filter(None, tracked):
        path = ROOT / name
        if not path.is_file():
            continue
        if forbidden.search(name):
            errors.append(f'Private or retired working path: {name}')
        if path.suffix in {'.md', '.json', '.jsonl', '.yaml', '.yml', '.toml', '.txt', '.html'}:
            value = path.read_text(errors='replace')
            if private_text.search(value):
                errors.append(f'Private path or credential pattern: {name}')
            emails = re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', value)
            if any(e != 'hello@hackapertus.ch' and not e.endswith('@users.noreply.github.com') for e in emails):
                errors.append(f'Unexpected email address: {name}')
    manifest = json.loads((EVIDENCE / 'preserved-files.json').read_text())
    for name, expected in manifest['sha256'].items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f'Preserved file changed: {name}')
    selected = EVIDENCE / 'local-hosted-verification'
    for entry in json.loads((selected / 'trace-provenance.json').read_text())['records']:
        path = selected / entry['file']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            errors.append(f'Selected trace changed: {entry["file"]}')
    # Frozen historical packets and submitted report retain their original links.
    docs = [ROOT / 'README.md', ROOT / 'track_2b/README.md', ROOT / 'track_2b/hosted/README.md',
            ROOT / 'track_2b/src/gate0/README.md', ROOT / 'track_2b/demo/README.md',
            *list((ROOT / 'track_2b/docs').glob('*.md')), EVIDENCE / 'README.md',
            selected / 'README.md', EVIDENCE / 'property-tax-2026-10-15/README.md']
    for doc in docs:
        for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:', target) or target.startswith('#'):
                continue
            if not (doc.parent / target.split('#')[0]).exists():
                errors.append(f'Broken local link: {doc.relative_to(ROOT)} -> {target}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(json.dumps({'current_tree_hygiene': 'PASS', 'preserved_files': len(manifest['sha256']),
                      'selected_trace_integrity': 'PASS', 'curated_document_links': 'PASS',
                      'scope': 'Current tracked text and selected hashes; excludes history and binary OCR'}))


if __name__ == '__main__':
    main()
