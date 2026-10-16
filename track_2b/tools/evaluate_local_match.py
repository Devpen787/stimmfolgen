#!/usr/bin/env python3
"""Explicit public-question evaluation against actual pinned loopback Apertus."""
import argparse,json,sys
from pathlib import Path
TRACK=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(TRACK/'src/app'),str(TRACK/'src/gate0')]
from backend import load_case
from live import LiveService
p=argparse.ArgumentParser();p.add_argument('--source-pdf',type=Path,required=True);p.add_argument('--model-dir',type=Path,required=True);p.add_argument('--model-url',default='http://127.0.0.1:8766/v1');p.add_argument('--cases',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
cases=json.loads(a.cases.read_text());assert isinstance(cases,list) and 0<len(cases)<=32
assert len({c['id'] for c in cases})==len(cases)
assert all(isinstance(c['question'],str) and 3<=len(c['question'])<=700 and c['id'].replace('_','').replace('-','').isalnum() for c in cases)
pdf=a.source_pdf.read_bytes();svc=LiveService(pdf,load_case(pdf),a.model_dir,a.model_url);a.out.mkdir();passed=0
for c in cases:
 captured={}
 def save(data):
  captured.update(data);(a.out/(c['id']+'.json')).write_text(json.dumps({'evaluation_reference':c,**data},ensure_ascii=False,indent=2)+'\n')
 status,r=svc.answer(c['question'],evidence_sink=save)
 ids=[i for claim in r['claims'] for i in claim['fact_ids']]
 kind=captured.get('traces',[{}])[0].get('parsed_candidate',{}).get('kind')
 ok=status==200 and kind==c['kind'] and sorted(ids)==sorted(c['ids']) and r['outcome'] in ('EVIDENCE_MATCH','INSUFFICIENT_EVIDENCE');passed+=ok
 print(json.dumps({'id':c['id'],'status':status,'outcome':r['outcome'],'ids':ids,'pass':ok}),flush=True)
print(json.dumps({'exact_reference_matches':passed,'total':len(cases),'scope':'Authored development cases, not general model accuracy'}))
raise SystemExit(0 if passed==len(cases) else 2)
