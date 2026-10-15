"""Admit additional cases only with matching source bytes and explicit owner review."""
import hashlib,json
from pathlib import Path
from urllib.request import Request,urlopen
TRACK=Path(__file__).resolve().parents[2]

def additional_cases(source_dir=None,download=False):
 cases={}
 for p in (TRACK/'data/cases').glob('*.json'):
  c=json.loads(p.read_text());review=c.get('gate',{}).get('human_review',{})
  if review.get('decision')!='ACCEPT' or review.get('reviewer_kind')!='HUMAN_USER':raise ValueError('Additional case requires explicit human review')
  wording=hashlib.sha256(json.dumps([x['statement'] for x in c['cards']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
  if review.get('wording_sha256')!=wording:raise ValueError('Case wording differs from accepted review')
  target=Path(source_dir)/ (p.stem+'.pdf') if source_dir else None
  data=target.read_bytes() if target and target.exists() else None
  if data is None and download:
   with urlopen(Request(c['source_url'],headers={'User-Agent':'StimmFolgen/0.5'}),timeout=30) as r:data=r.read(8*1024*1024+1)
  if data is None:raise ValueError('Additional case source PDF required')
  if len(data)>8*1024*1024 or hashlib.sha256(data).hexdigest()!=c['source_sha256']:raise ValueError('Additional case PDF authentication failed')
  import pymupdf
  from source_probe import page_text
  pdf=pymupdf.open(stream=data,filetype='pdf')
  for card in c['cards']:
   if card['review_status']!='HUMAN_REVIEWED_STATEMENT':raise ValueError('Statement review missing')
   for ref in card['citations']:
    text,_=page_text(pdf[ref['pdf_page']-1],'blocks-v3');quote=text[ref['start_char']:ref['end_char']]
    if quote!=ref['text'] or hashlib.sha256(quote.encode()).hexdigest()!=ref['text_sha256'] or ref['source_sha256']!=c['source_sha256']:raise ValueError('Additional case source span mismatch')
  if target and not target.exists():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  cases[p.stem]=c
 return cases
