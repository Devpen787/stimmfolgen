"""HTTP/privacy boundary tests with an explicit routing fixture, not model evidence."""
import json
import sys
import threading
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/app'))
from backend import make_handler

class BackendBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture={'cards':[{'id':f'P{i:02}', 'statement':'Routing fixture only', 'citations':[]} for i in range(1,6)],
                 'gate':{'gate0_status':'TEST_ROUTING_FIXTURE'},'inference_mode':'REVIEWED_RECORDED_CASE'}
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(b'%PDF routing fixture',fixture))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def post(self,body):
        request=urllib.request.Request(self.url+'/api/question',data=body,headers={'Content-Type':'application/json'})
        try:r=urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:r=e
        with r:return r.status,json.loads(r.read()),r.headers
    def test_personal_cost_is_unknown_and_never_zero(self):
        status,data,headers=self.post(b'{"topic":"personal_cost"}')
        self.assertEqual(status,200);self.assertEqual(data['outcome'],'INSUFFICIENT_EVIDENCE')
        self.assertIsNone(data['personal_financing_chf']);self.assertFalse(data['live_inference_performed_for_this_request'])
        self.assertEqual(set(data['missing_facts']),{'ENACTED_FINANCING_METHOD','ENACTED_FINANCING_RATE'})
        self.assertIn("connect-src 'self'",headers['Content-Security-Policy'])
    def test_unknown_topic_abstains(self):
        self.assertEqual(self.post(b'{"topic":"tell me how to vote"}')[1]['outcome'],'INSUFFICIENT_EVIDENCE')
    def test_private_payload_and_malformed_requests_are_rejected(self):
        for body in (b'{"topic":"cost","notes":"synthetic private field"}',b'{"topic":"cost","salary":8000}',
                     b'[]',b'null',b'{"topic":9}',b'{',b'x'*2049):
            with self.subTest(body=body[:60]):self.assertEqual(self.post(body)[0],400)
    def test_public_provision_is_reviewed_recorded(self):
        status,data,_=self.post(b'{"topic":"change"}')
        self.assertEqual(status,200);self.assertEqual(data['outcome'],'REVIEWED_SOURCE_STATEMENT')
        self.assertFalse(data['live_inference_performed_for_this_request'])
    def test_source_and_assets_are_allowlisted(self):
        with urllib.request.urlopen(self.url+'/api/booklet.pdf') as r:self.assertEqual(r.headers['Content-Type'],'application/pdf')
        for path in ('/.env','/../Dockerfile','/docs/evidence/manifest.json'):
            with self.subTest(path=path),self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(self.url+path)
            self.assertEqual(error.exception.code,404);error.exception.close()

if __name__=='__main__':unittest.main()
