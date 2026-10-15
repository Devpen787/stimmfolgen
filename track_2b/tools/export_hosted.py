#!/usr/bin/env python3
"""Rebuild deployable public JSON only after the native Gate authenticates evidence."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
TRACK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TRACK/'src/app'))
from backend import load_case
from live import generation_prompt, review_prompt, CONTRACT, SELECT_SYSTEM, MATCH_SYSTEM


def export(pdf):
    case=load_case(pdf)
    query=json.loads((TRACK/'hosted/query-contract.json').read_text())
    query['planner_template']='QUESTION="__QUESTION__"\nOPEN_PROPOSAL='+json.dumps(case['title'])+'\nEVIDENCE_AS_OF='+json.dumps(case['as_of'])
    return {'case':case,'catalog':json.loads((TRACK/'src/app/catalog.json').read_text()),
        'contract':CONTRACT,
        'hosted_query':query,
        'generation_template':generation_prompt(case,'__QUESTION__'),
        'review_template':review_prompt(case,'__QUESTION__',{'__CANDIDATE__':True}),
        'source_url':case['cards'][0]['citations'][0]['page_url'].split('#')[0],
        'generator_system':SELECT_SYSTEM, 'review_system':MATCH_SYSTEM}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-pdf',type=Path,required=True);p.add_argument('--check',action='store_true');args=p.parse_args()
    data=json.dumps(export(args.source_pdf.read_bytes()),ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n'
    out=TRACK/'hosted/public-bundle.json'
    if args.check:
        expected='export default '+json.dumps(hashlib.sha256(data.encode()).hexdigest())+';\n'
        if out.read_text()!=data or (TRACK/'hosted/bundle-hash.mjs').read_text()!=expected:raise SystemExit('Hosted bundle differs from authenticated native evidence/prompts. Re-export it.')
        print('Hosted bundle matches authenticated native evidence and prompt contract.');raise SystemExit(0)
    out.write_text(data)
    (TRACK/'hosted/bundle-hash.mjs').write_text('export default '+json.dumps(hashlib.sha256(data.encode()).hexdigest())+';\n')
    print('Exported authenticated public bundle:',hashlib.sha256(data.encode()).hexdigest())
