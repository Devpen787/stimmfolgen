#!/usr/bin/env python3
"""Reproduce a bounded second-case source packet; never grant human approval."""
from pathlib import Path
import argparse,hashlib,json,sys
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/gate0'))
from source_probe import page_text
import pymupdf
URL='https://www.bk.admin.ch/dam/de/sd-web/6DaWglL-N7NM/2025-09-28_erlaeuterungen_des_bundesrates.pdf'
SHA='39c020145299913685e4d0b6899fa23bb1f94938652a417e0c1da08d316ade8a'
DEFINITIONS=[
 ('H01','What changes for homeowners','DIRECT_PROVISION',10,'Das Bundesgesetz über den Systemwechsel','Neue Schuldzinsen', 'The linked reform would abolish imputed-rental-income taxation for owner-occupied homes and restrict deductions, including maintenance costs.'),
 ('H02','Cantonal tax on second homes','CONDITIONAL_APPLICABILITY',10,'Die neue Verfassungsbestimmung erlaubt',None,'Cantons could introduce a special tax on predominantly owner-occupied second homes. This would not happen automatically in every canton.'),
 ('H03','Renters and interest deductions','CONDITIONAL_APPLICABILITY',12,'Da im geltenden Recht alle Arten von Schuldzinsen','5 Verteilungswirkungen','Renters could also be affected by restrictions on interest deductions. The booklet says they would generally no longer deduct interest.'),
 ('H04','Personal tax savings remain conditional','UNRESOLVED',12,'Unmittelbar betrifft die Reform','Für weitere Personen','The booklet does not establish one definite personal saving. Effects depend on residence, imputed rental value, deductions, taxable income, mortgage rates and any second-home tax.')]

def build(data):
 if hashlib.sha256(data).hexdigest()!=SHA:raise ValueError('Second-case source hash mismatch')
 pdf=pymupdf.open(stream=data,filetype='pdf')
 if len(pdf)!=48:raise ValueError('Second-case page count mismatch')
 cards=[]
 for id,title,kind,page,start,end,statement in DEFINITIONS:
  text,_=page_text(pdf[page-1],'blocks-v3');a=text.find(start)
  if a<0:raise ValueError('Source anchor missing: '+id)
  z=text.find(end,a+len(start)) if end else len(text)
  if z<0:z=len(text)
  quote=text[a:z].strip()
  citation={'span_id':'home-tax:'+id,'pdf_page':page,'printed_page':page,'start_char':a,'end_char':a+len(quote),'text':quote,'text_sha256':hashlib.sha256(quote.encode()).hexdigest(),'actor':'GOVERNMENT','page_url':URL+'#page='+str(page),'source_sha256':SHA}
  cards.append({'id':id,'title':title,'kind':kind,'statement':statement,'review_status':'PENDING_HUMAN_REVIEW','origin':'APERTUS_PASSAGE_SELECTION_WITH_INDEPENDENT_SOURCE_CHECK','citations':[citation]})
 return {'case_id':'ch-federal:2025-09-28:home-tax','title':'Homeownership tax reform','mode':'DOCUMENT_EXPLANATION','as_of':'2025-06-20T23:59:59+02:00','content_cutoff':'2025-06-20','available_by':datetime.now(timezone.utc).isoformat(),'vote_date':'2025-09-28','source_sha256':SHA,'source_url':URL,'cards':cards,'gate':{'status':'PENDING_HUMAN_REVIEW','source_bytes_verified':True,'historical_public_availability_claimed':False},'inference_mode':'SOURCE_CHECKED_CANDIDATE','live_inference_performed_for_this_request':False,'model':'Apertus v1.5 8B','limitations':['Describes the 2025 proposal, not current tax advice','Exact-byte historical publication date not independently established; source inspected in October 2026','No definite personal tax calculation','Human wording review pending'],'questions':['What changes for homeowners?','Does every canton have to introduce the second-home tax?','Can renters also be affected?'],'primary_cards':['H01','H04'],'perspectives':{'groups':[{'id':'owner','label':'Own and live in a home','fact_ids':['H01','H04']},{'id':'renter','label':'Rent a home','fact_ids':['H03']},{'id':'second-home','label':'Own a second home','fact_ids':['H02']}],'nation':{'title':'Different choices across cantons','fact_ids':['H02','H04']}}}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-pdf',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();case=build(a.source_pdf.read_bytes());a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(case,ensure_ascii=False,indent=2)+'\n');print('Prepared four source-bound candidates, without granting human approval.')
