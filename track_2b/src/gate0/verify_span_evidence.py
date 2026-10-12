#!/usr/bin/env python3
"""Reauthenticate committed span traces against original PDF bytes, without inference."""
import argparse
import hashlib
import json
from pathlib import Path
from source_probe import validate_report
from source_spans import authenticate_catalog, digest
from semantic_eval import validate_reference, evaluate_semantics
from model_probe import parse_response
from span_probe import adapt_answer, compare_attribution, TRIALS


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
    semantic_replays = 0
    for run in sorted(root.glob('run-*')):
        catalog = json.loads((run / 'source-spans.json').read_text())
        authenticate_catalog(catalog, report, pdf)
        reference = json.loads((run / 'semantic-reference-used.json').read_text())
        validate_reference(reference, catalog)
        for path in run.glob('*.json'):
            trace = json.loads(path.read_text())
            if trace.get('evidence_class') == 'POLICY_COMPARISON_OF_TWO_ACTUAL_MODEL_COMPLETIONS':
                name=trace['trial_id']
                grounding=json.loads((run/(name+'-grounding.json')).read_text())
                intent=json.loads((run/(name+'-intent.json')).read_text())
                trial=next(t for t in TRIALS if t[0]==name)
                target=(trial[6] or trial[4])[0]
                expected=compare_attribution(grounding.get('parsed_candidate'),intent.get('parsed_candidate'),catalog,target)
                canonical=adapt_answer(expected,catalog,target,name) if expected else None
                if trace.get('policy_candidate') != expected or trace.get('canonical_candidate') != canonical:
                    raise ValueError('Policy changed extracted source actor/spans or requested actor')
                if trace['component_response_sha256'] != {'grounding':grounding.get('response_sha256'),'intent':intent.get('response_sha256')}:
                    raise ValueError('Policy component response hashes mismatch')
            if trace.get('prompt_version') == 'gate0-span-selection-v5-source-actor-comparison' and trace.get('canonical_candidate') is not None:
                trial=next(t for t in TRIALS if t[0]==trace['trial_id'])
                semantic=evaluate_semantics(trace['canonical_candidate'],catalog,reference,
                    expected_outcomes=trial[3],required_predicates=trial[4],required_missing=trial[5],allowed_predicates=trial[6],
                    required_values=reference['cases'][trace['trial_id']]['required_values'])
                if trace.get('semantic_evaluation') != semantic:
                    raise ValueError('Stored semantic verdict differs from independent reference replay')
                if trace['bounded_machine_test_pass'] != bool(trace['validation']['mechanical_pass'] and semantic['semantic_reference_pass']):
                    raise ValueError('Stored bounded pass flag mismatch')
                semantic_replays+=1
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
            if trace.get('prompt_version') in ('gate0-span-selection-v3-flat-task-contract', 'gate0-span-selection-v4-neutral-attribution', 'gate0-span-selection-v5-source-actor-comparison'):
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
            'file_count': len(actual), 'bounded_reference_replays': semantic_replays,
            'model_inference_performed_by_verifier': False,
            'semantic_accuracy_or_human_review_proven_by_verifier': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence-dir', type=Path, required=True)
    parser.add_argument('--source-pdf', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.evidence_dir, args.source_pdf.read_bytes()), indent=2))


if __name__ == '__main__':
    main()
