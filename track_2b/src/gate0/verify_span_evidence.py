#!/usr/bin/env python3
"""Reauthenticate committed span traces against original PDF bytes, without inference."""
import argparse
import hashlib
import json
from pathlib import Path
from source_probe import validate_report
from source_spans import authenticate_catalog, digest
from semantic_eval import validate_reference
from model_probe import parse_response
from span_probe import adapt_answer, TRIALS


def verify(root, pdf):
    manifest = json.loads((root / 'manifest.json').read_text())
    actual = {str(p.relative_to(root)) for p in root.rglob('*.json') if p.name != 'manifest.json'}
    if actual != set(manifest['files']):
        raise ValueError('Manifest file set mismatch')
    for name, expected in manifest['files'].items():
        data = (root / name).read_bytes()
        if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
            raise ValueError('Evidence hash/size mismatch: ' + name)
    report = json.loads((root / 'source.json').read_text())
    validate_report(report, pdf)
    count = 0
    for run in sorted(root.glob('run-*')):
        catalog = json.loads((run / 'source-spans.json').read_text())
        authenticate_catalog(catalog, report, pdf)
        reference = json.loads((run / 'semantic-reference-used.json').read_text())
        validate_reference(reference, catalog)
        for path in run.glob('*.json'):
            trace = json.loads(path.read_text())
            if 'raw_request' not in trace:
                continue  # derived aggregates are explicitly not model completions
            raw_request = json.dumps(trace['raw_request'], ensure_ascii=False).encode()
            if hashlib.sha256(raw_request).hexdigest() != trace['request_sha256']:
                raise ValueError('Request hash mismatch: ' + str(path))
            response = trace['raw_response_text']
            if hashlib.sha256(response.encode()).hexdigest() != trace['response_sha256']:
                raise ValueError('Response hash mismatch: ' + str(path))
            if json.loads(response) != trace['raw_api_response']:
                raise ValueError('Parsed HTTP response mismatch: ' + str(path))
            if 'parsed_candidate' in trace and parse_response(trace['raw_api_response']) != trace['parsed_candidate']:
                raise ValueError('Candidate differs from recorded model output: ' + str(path))
            if trace.get('prompt_version') == 'gate0-span-selection-v3-flat-task-contract':
                trial = next(t for t in TRIALS if t[0] == trace['trial_id'])
                target = (trial[6] or trial[4])[0]
                if adapt_answer(trace.get('parsed_candidate'), catalog, target, trace['trial_id']) != trace.get('canonical_candidate'):
                    raise ValueError('Adapter changed raw model values/IDs')
            if trace['source_sha256'] != report['sha256'] or trace['catalog_sha256'] != catalog['catalog_sha256']:
                raise ValueError('Trace source/catalog mismatch')
            if trace['semantic_reference_sha256'] != digest(reference):
                raise ValueError('Trace reference snapshot mismatch')
            count += 1
    return {'evidence_integrity_pass': True, 'authenticated_actual_inference_traces': count,
            'file_count': len(actual), 'model_inference_performed_by_verifier': False,
            'semantic_accuracy_or_human_review_proven_by_verifier': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence-dir', type=Path, required=True)
    parser.add_argument('--source-pdf', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.evidence_dir, args.source_pdf.read_bytes()), indent=2))


if __name__ == '__main__':
    main()
