#!/usr/bin/env python3
"""Local backend serving a reviewed Apertus-assisted case; no invented live inference."""
import argparse
import json
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
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


def make_handler(pdf,case):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass  # No questions, voter notes or request bodies in logs.
        def send(self,status,body,kind='application/json; charset=utf-8'):
            data=json.dumps(body,ensure_ascii=False).encode() if isinstance(body,dict) else body
            self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers();self.wfile.write(data)
        def do_GET(self):
            path=urlsplit(self.path).path
            if path=='/api/case':return self.send(200,case)
            if path=='/api/catalog':return self.send(200,json.loads((TRACK/'src/app/catalog.json').read_text()))
            if path=='/api/health':return self.send(200,{'status':'ok','gate0':case['gate']['gate0_status'],'mode':case['inference_mode']})
            if path=='/api/booklet.pdf':return self.send(200,pdf,'application/pdf')
            allowed={'/':'index.html','/app.js':'app.js','/vault.js':'vault.js','/style.css':'style.css'}
            if path.startswith('/assets/') and path.removeprefix('/assets/') in {p.name for p in (TRACK/'web/assets').glob('*.svg')}:
                return self.send(200,(TRACK/'web'/path.lstrip('/')).read_bytes(),'image/svg+xml')
            if path in allowed:
                asset=TRACK/'web'/allowed[path]
                if not asset.exists():return self.send(503,{'error':'Frontend not built; backend is ready'})
                kind={'/':'text/html; charset=utf-8','/app.js':'text/javascript; charset=utf-8','/vault.js':'text/javascript; charset=utf-8','/style.css':'text/css; charset=utf-8'}[path]
                return self.send(200,asset.read_bytes(),kind)
            return self.send(404,{'error':'Not found'})
        def do_POST(self):
            if urlsplit(self.path).path!='/api/question':return self.send(404,{'error':'Not found'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=2048:raise ValueError()
                data=json.loads(self.rfile.read(length))
                if not isinstance(data,dict) or set(data)!={'topic'} or not isinstance(data['topic'],str):raise ValueError()
            except (ValueError,TypeError):return self.send(400,{'error':'Use one supported topic; do not send private notes or salary data'})
            return self.send(200,answer_topic(case,data['topic']))
    return Handler


def serve(pdf,case,host,port):
    print(f'StimmFolgen reviewed-case backend: http://{host}:{port}',flush=True)
    ThreadingHTTPServer((host,port),make_handler(pdf,case)).serve_forever()


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-pdf',type=Path);p.add_argument('--check',action='store_true')
    p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8770)
    args=p.parse_args();pdf=args.source_pdf.read_bytes() if args.source_pdf else download()
    case=load_case(pdf)
    if args.check:print(json.dumps(case['gate'],indent=2));return
    serve(pdf,case,args.host,args.port)

if __name__=='__main__':main()
