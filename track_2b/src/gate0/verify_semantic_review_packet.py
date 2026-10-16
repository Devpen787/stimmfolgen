#!/usr/bin/env python3
"""Authenticate a prepared review packet; never turn pending decisions into approval."""
import argparse
import hashlib
import json
from pathlib import Path
from publication_availability import verify_capture, admit_frame, PUBLISHER_PAGE, PUBLISHER_PDF
from source_spans import authenticate_catalog, digest


def verify(root, pdf):
    manifest=json.loads((root/'manifest.json').read_text())
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='manifest.json'}
    if actual!=set(manifest['files']):raise ValueError('Review packet file set mismatch')
    for name,expected in manifest['files'].items():
        data=(root/name).read_bytes()
        if len(data)!=expected['bytes'] or hashlib.sha256(data).hexdigest()!=expected['sha256']:
            raise ValueError('Review packet hash mismatch: '+name)
    availability=json.loads((root/'publication-availability.json').read_text())
    # Offline witness replay: CDX SHA-1 is checked against original pinned bytes.
    # Live archived/current/publisher byte equality was separately observed during acquisition.
    replay=verify_capture(pdf,pdf,pdf,availability['cdx_capture'],availability['archive_replay_headers'])
    if any(availability.get(k)!=v for k,v in replay.items()):raise ValueError('Availability witness mismatch')
    if (availability['publisher_page_url']!=PUBLISHER_PAGE or availability['publisher_download_url']!=PUBLISHER_PDF or
        availability['publisher_anchor']['href']!=PUBLISHER_PDF):raise ValueError('Publisher resource mismatch')
    if not admit_frame(availability,availability['review_case_as_of']):raise ValueError('Proposed public frame is inadmissible')
    if admit_frame(availability,'2023-11-29T23:59:59+01:00'):raise ValueError('Editorial cutoff admitted as publication date')
    evidence=root.parent
    base=evidence/'gate0-attribution-2026-10-12'
    run=base/'run-attribution-v5-repeat'
    source=json.loads((base/'source.json').read_text());catalog=json.loads((run/'source-spans.json').read_text())
    authenticate_catalog(catalog,source,pdf)
    reference=json.loads((run/'semantic-reference-used.json').read_text())
    bundle=json.loads((root/'review-bundle.json').read_text())
    if (bundle['source_sha256']!=source['sha256'] or bundle['catalog_sha256']!=catalog['catalog_sha256'] or
        bundle['semantic_reference_sha256']!=digest(reference)):raise ValueError('Review source/reference binding mismatch')
    if len(bundle['propositions'])!=len(reference['facts']) or len(bundle['trials'])!=7:raise ValueError('Incomplete review scope')
    by_id={s['span_id']:s for s in catalog['spans']}
    for item,fact in zip(bundle['propositions'],reference['facts']):
        if item['candidate']!={k:fact[k] for k in ('predicate','kind','actor','value')}:raise ValueError('Reference proposition changed')
        for support in item['source_support']:
            span=by_id[support['span_id']]
            if any(span[k]!=v for k,v in support.items()):raise ValueError('Review source span changed')
        if item['decision']!='PENDING':raise ValueError('Prepared packet claims human decision')
    for item in bundle['trials']:
        path=(evidence/item['trace']).resolve()
        if not path.is_relative_to(base.resolve()):raise ValueError('Review trace escapes evidence scope')
        data=path.read_bytes();trace=json.loads(data)
        if hashlib.sha256(data).hexdigest()!=item['trace_file_sha256'] or trace['canonical_candidate']!=item['candidate']:
            raise ValueError('Model candidate differs from immutable recorded trace')
        if item['decision']!='PENDING':raise ValueError('Prepared trial claims human decision')
    template=json.loads((root/'review-response.template.json').read_text())
    if (template['reviewer_name'] is not None or template['reviewed_at'] is not None or template['overall_decision']!='PENDING' or
        any(i['decision']!='PENDING' for i in template['decisions'])):raise ValueError('Template is not pending')
    if bundle['human_semantic_reviewed'] or bundle['frontend_authorized']:raise ValueError('Packet authorises release')
    return {'packet_integrity_pass':True,'publication_witness_replay_pass':True,'public_frame_admitted':True,
            'editorial_cutoff_as_public_frame_admitted':False,'human_semantic_reviewed':False,'frontend_authorized':False,
            'new_network_archive_verification_performed':False,'model_inference_performed':False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet-dir',type=Path,required=True)
    parser.add_argument('--source-pdf',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(verify(args.packet_dir,args.source_pdf.read_bytes()),indent=2))

if __name__=='__main__':main()
