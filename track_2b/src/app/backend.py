#!/usr/bin/env python3
"""Reviewed evidence app with optional, explicitly configured live Apertus QA."""
import argparse
import json
import os
import ipaddress
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit,parse_qs
TRACK=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(TRACK/'src/gate0'))
from release_guard import clear_gate, human_approvals
from source_probe import download

EVIDENCE=TRACK/'docs/evidence'
PACKET=EVIDENCE/'ahv-semantic-review-2026-10-12'
REVIEWS=EVIDENCE/'ahv-human-review-2026-10-12'
RELEASE=EVIDENCE/'gate0-release-2026-10-14'
TITLES={'P01':'What changes','P02':'Cost at introduction','P03':'Cost after five years','P04':'Financing remains open','P05':'Who makes the budget forecast'}


def load_case(pdf):
    gate=clear_gate(pdf,RELEASE,PACKET,REVIEWS)
    approvals=human_approvals(PACKET,REVIEWS)
    bundle=json.loads((PACKET/'review-bundle.json').read_text())
    cards=[]
    for item in bundle['propositions']:
        ident=item['review_id']
        cards.append({'id':ident,'title':TITLES[ident],'statement':approvals[ident]['accepted_wording'],
            'kind':item['candidate']['kind'],'review_status':'HUMAN_REVIEWED_STATEMENT',
            'origin':'REVIEWED_REFERENCE_CONTEXT' if ident=='P03' else 'REVIEWED_APERTUS_ASSISTED_CASE',
            'citations':item['source_support']})
    return {'case_id':'ch-federal:2024-03-03:ahv13','title':'The 13th AHV pension','mode':'PRE_VOTE',
        'as_of':gate['public_case_as_of'],'content_cutoff':gate['source_content_cutoff'],'available_by':gate['available_by_utc'],
        'vote_date':'2024-03-03','source_sha256':gate['source_sha256'],'cards':cards,'gate':gate,
        'inference_mode':'REVIEWED_RECORDED_CASE','live_inference_performed_for_this_request':False,
        'model':'Apertus v1.5 8B · pinned text-only MLX 4-bit conversion',
        'limitations':['Historical pre-vote booklet, not current pension law','Predictions remain attributed estimates',
                      'Personal financing is unspecified','No voting recommendation','Five-year cost is reviewed reference context']}


def answer_topic(case, topic):
    index={'change':'P01','cost':'P02','future_cost':'P03','personal_cost':'P04','attribution':'P05'}
    if topic not in index:return {'outcome':'INSUFFICIENT_EVIDENCE','text':'This reviewed case does not cover that question. Open the source booklet for more context.','citations':[]}
    card=next(c for c in case['cards'] if c['id']==index[topic])
    return {'outcome':'INSUFFICIENT_EVIDENCE' if topic=='personal_cost' else 'REVIEWED_SOURCE_STATEMENT',
        'text':card['statement'],'personal_financing_chf':None,'citations':card['citations'],
        'missing_facts':['ENACTED_FINANCING_METHOD','ENACTED_FINANCING_RATE'] if topic=='personal_cost' else [],
        'inference_mode':case['inference_mode'],'live_inference_performed_for_this_request':False}


def make_handler(pdf,case,live=None,admission=None,cases=None,source_dir=None):
    cases=cases or {'ahv13':case}
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup();self.connection.settimeout(15)
        def log_message(self,*args):pass  # No questions, voter notes or request bodies in logs.
        def send(self,status,body,kind='application/json; charset=utf-8'):
            data=json.dumps(body,ensure_ascii=False).encode() if isinstance(body,dict) else body
            self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers();self.wfile.write(data)
        def do_GET(self):
            path=urlsplit(self.path).path
            if path=='/api/cases':return self.send(200,cases)
            if path=='/api/case':
                ident=parse_qs(urlsplit(self.path).query).get('case',['ahv13'])[0]
                return self.send(200,cases[ident]) if ident in cases else self.send(404,{'error':'Vote not found'})
            if path=='/api/catalog':return self.send(200,json.loads((TRACK/'src/app/catalog.json').read_text()))
            if path=='/api/live/status':return self.send(200,{'configured':live is not None,'scope':'AHV historical reviewed evidence only','model':live.identity['backing_checkpoint'] if live else None,'provider':'Infomaniak Switzerland' if live and live.hosted_client else 'Your local Mac' if live else None,'private_notes_sent':False,'local_matching_experimental':bool(live and not live.hosted_client)})
            if path=='/api/health':return self.send(200,{'status':'ok','gate0':case['gate']['gate0_status'],'mode':case['inference_mode']})
            if path=='/api/booklet.pdf':
                ident=parse_qs(urlsplit(self.path).query).get('case',['ahv13'])[0]
                if ident not in cases:return self.send(404,{'error':'Vote not found'})
                return self.send(200,pdf if ident=='ahv13' else (Path(source_dir)/(ident+'.pdf')).read_bytes(),'application/pdf')
            allowed={'/':'index.html','/app.js':'app.js','/vault.js':'vault.js','/answer.js':'answer.js','/style.css':'style.css','/local.html':'local.html','/judges.html':'judges.html'}
            if path.startswith('/assets/') and path.removeprefix('/assets/') in {p.name for p in (TRACK/'web/assets').glob('*.svg')}:
                return self.send(200,(TRACK/'web'/path.lstrip('/')).read_bytes(),'image/svg+xml')
            if path in allowed:
                asset=TRACK/'web'/allowed[path]
                if not asset.exists():return self.send(503,{'error':'Frontend not built; backend is ready'})
                kind={'/':'text/html; charset=utf-8','/app.js':'text/javascript; charset=utf-8','/vault.js':'text/javascript; charset=utf-8','/answer.js':'text/javascript; charset=utf-8','/style.css':'text/css; charset=utf-8','/local.html':'text/html; charset=utf-8','/judges.html':'text/html; charset=utf-8'}[path]
                return self.send(200,asset.read_bytes(),kind)
            return self.send(404,{'error':'Not found'})
        def do_POST(self):
            path=urlsplit(self.path).path
            if path=='/api/live/question':
                try:
                    length=int(self.headers.get('Content-Length','0'))
                    if not 0<length<=4096:raise ValueError()
                    origin=self.headers.get('Origin')
                    if origin and urlsplit(origin).netloc!=self.headers.get('Host'):raise ValueError()
                    data=json.loads(self.rfile.read(length))
                    if not isinstance(data,dict) or set(data)!={'question'} or not isinstance(data['question'],str) or not 3<=len(data['question'].strip())<=700:raise ValueError()
                except (ValueError,TypeError):return self.send(400,{'error':'Send one public question (3–700 characters), without private fields.'})
                if parse_qs(urlsplit(self.path).query).get('case',['ahv13'])[0]!='ahv13':return self.send(503,{'error':'Live answers for this vote require the on-premise launcher or online demo.'})
                if live is None:return self.send(503,{'outcome':'SERVICE_UNAVAILABLE','error':'Live Apertus is not configured here. The reviewed explanation remains available.','live_inference_performed_for_this_request':False})
                if admission:
                    address=self.client_address[0]
                    if os.environ.get('TRUST_CADDY_CLIENT_IP')=='1':
                        try:address=str(ipaddress.ip_address(self.headers.get('X-StimmFolgen-Client-IP','')))
                        except ValueError:return self.send(400,{'error':'Invalid proxy client address'})
                    allowed,message=admission.take(address)
                    if not allowed:return self.send(429,{'outcome':'LIMIT_REACHED','error':message,'live_inference_performed_for_this_request':False})
                status,result=live.answer(data['question'].strip())
                return self.send(status,result)
            if path!='/api/question':return self.send(404,{'error':'Not found'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=2048:raise ValueError()
                data=json.loads(self.rfile.read(length))
                if not isinstance(data,dict) or set(data)!={'topic'} or not isinstance(data['topic'],str):raise ValueError()
            except (ValueError,TypeError):return self.send(400,{'error':'Use one supported topic; do not send private notes or salary data'})
            return self.send(200,answer_topic(case,data['topic']))
    return Handler


def serve(pdf,case,host,port,live=None,admission=None,cases=None,source_dir=None):
    print(f'StimmFolgen backend: http://{host}:{port} (live={live is not None})',flush=True)
    ThreadingHTTPServer((host,port),make_handler(pdf,case,live,admission,cases,source_dir)).serve_forever()


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-pdf',type=Path);p.add_argument('--check',action='store_true')
    p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8770)
    p.add_argument('--local-model-dir',type=Path);p.add_argument('--model-url',default='http://127.0.0.1:8766/v1')
    args=p.parse_args();pdf=args.source_pdf.read_bytes() if args.source_pdf else download()
    case=load_case(pdf)
    if args.check:print(json.dumps(case['gate'],indent=2));return
    live=None
    admission=None
    if os.environ.get('INFOMANIAK_PRODUCT_ID'):
        if args.local_model_dir:raise ValueError('Choose one inference provider')
        from live import LiveService
        from hosted import InfomaniakClient
        from admission import Admission
        token_file=Path(os.environ.get('INFOMANIAK_TOKEN_FILE','/run/secrets/infomaniak_token'))
        client=InfomaniakClient(os.environ['INFOMANIAK_PRODUCT_ID'],token_file.read_text().strip())
        live=LiveService(pdf,case,hosted_client=client)
        admission=Admission(os.environ.get('USAGE_DATABASE','/state/usage.sqlite'),int(os.environ.get('DAILY_QUESTION_LIMIT','200')))
    elif args.local_model_dir:
        from live import LiveService
        live=LiveService(pdf,case,args.local_model_dir,args.model_url)
    from case_registry import additional_cases
    source_dir=(args.source_pdf.parent/'sources') if args.source_pdf else TRACK.parent/'.local/local/sources'
    cases={'ahv13':case,**additional_cases(source_dir,download=True)}
    serve(pdf,case,args.host,args.port,live,admission,cases,source_dir)

if __name__=='__main__':main()
