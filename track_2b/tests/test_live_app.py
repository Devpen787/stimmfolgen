"""Adversarial service/HTTP contracts. Fixtures below are NOT inference evidence."""
import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/app'))
from backend import make_handler
from admission import Admission
from hosted import InfomaniakClient, MODEL, NoRedirect
from live import LiveService, validate_selection, validate_match_review, compose_answer
from http.server import ThreadingHTTPServer

CASE={'as_of':'2024-03-02T23:59:59+01:00','source_sha256':'test-only',
      'cards':[{'id':'P01','kind':'DIRECT_PROVISION','statement':'Fixture, not AHV proof.',
                'citations':[{'span_id':'sp-fixture','actor':'GOVERNMENT','pdf_page':9,'text':'Fixture source'}]}]}
CANDIDATE={'kind':'EVIDENCE','fact_ids':['P01']}
REVIEW={'fact_ids':['P01']}

class FakeHosted:
    identity={'backing_checkpoint':MODEL,'v1_5_verified':True}
    def __init__(self, answers):self.answers=iter(answers);self.prompts=[]
    def call(self,prompt,validator,version,max_tokens,**kwargs):
        self.prompts.append(prompt)
        answer=next(self.answers)
        return {'model_inference_performed':True,'parsed_candidate':answer,'validation':validator(answer)}

class LiveContractTests(unittest.TestCase):
    def service(self,answers):
        client=FakeHosted(answers)
        with patch('live.build_report',return_value={}):service=LiveService(b'fixture',CASE,hosted_client=client)
        return service,client
    def test_untrusted_reference_and_generated_fields_are_rejected(self):
        for candidate in [dict(CANDIDATE,notes='private'),dict(CANDIDATE,text='invented factual wording'),
                          {'kind':'EVIDENCE','fact_ids':['invented']},{'kind':'EVIDENCE','fact_ids':[]},{'kind':[],'fact_ids':[]}]:
            self.assertTrue(validate_selection(candidate,CASE))
    def test_relevance_check_cannot_add_an_unselected_fact(self):
        service,_=self.service([CANDIDATE,{'fact_ids':['invented']}])
        code,result=service.answer('Public fixture question')
        self.assertEqual(code,200);self.assertEqual(result['outcome'],'WITHHELD');self.assertEqual(result['claims'],[])
        self.assertTrue(result['live_inference_performed_for_this_request']);self.assertFalse(result['human_reviewed'])
    def test_review_can_remove_unrelated_context_without_fabricating_a_claim(self):
        service,_=self.service([CANDIDATE,{'fact_ids':[]}])
        _,result=service.answer('Public fixture question')
        self.assertEqual(result['outcome'],'INSUFFICIENT_EVIDENCE');self.assertFalse(result['claims'])
    def test_service_refusal_needs_no_generated_fact_or_impossible_entailment_check(self):
        service,client=self.service([{'kind':'VOTING_ADVICE','fact_ids':[]}])
        _,result=service.answer('Public fixture question')
        self.assertEqual(result['answer_mode'],'SERVICE_LIMIT');self.assertEqual(len(client.prompts),1)
        self.assertFalse(result['claims']);self.assertIn('does not recommend',result['unknowns'][0])
    def test_returned_sources_come_from_authenticated_case_not_generated_text(self):
        service,client=self.service([CANDIDATE,REVIEW])
        code,result=service.answer('Public fixture question')
        self.assertEqual(result['claims'][0]['citations'],CASE['cards'][0]['citations'])
        self.assertEqual(result['claims'][0]['text'],CASE['cards'][0]['statement'])
        self.assertEqual(result['answer_mode'],'REVIEWED_EVIDENCE');self.assertTrue(result['statements_human_reviewed'])
        self.assertEqual(len(client.prompts),2);self.assertFalse(result['human_reviewed'])
        self.assertEqual(result['model_identity_basis'],'PROVIDER_REPORTED_NOT_WEIGHT_ATTESTED')
    def test_relevance_rejects_malformed_or_generated_fields(self):
        for value in [[],[['P01']],{'fact_ids':['P01'],'text':'invented'}, {'fact_ids':['P01','P01']}, {'fact_ids':['unknown']}, {'fact_ids':None}]:
            self.assertTrue(validate_match_review(value,CANDIDATE))
    def test_all_factual_wording_is_pinned_even_for_arbitrary_valid_selection(self):
        case=json.loads((Path(__file__).resolve().parents[1]/'hosted/public-bundle.json').read_text())['case']
        for c in case['cards']:
            selection={'kind':'EVIDENCE','fact_ids':[c['id']]}
            result=compose_answer(case,selection,[c['id']])
            self.assertEqual(result['claims'][0]['text'],c['statement'])
            self.assertEqual(result['claims'][0]['citations'],c['citations'])
            self.assertEqual(result['claims'][0]['evidence_kinds'],[c['kind']])
    def test_transport_failure_cannot_replay_an_answer(self):
        service,client=self.service([])
        with patch.object(client,'call',side_effect=OSError('synthetic unavailable')):
            code,result=service.answer('Public fixture question')
        self.assertEqual(code,503);self.assertEqual(result['claims'],[]);self.assertFalse(result['live_inference_performed_for_this_request'])
    def test_busy_request_cannot_start_a_second_completion(self):
        service,client=self.service([])
        service.lock.acquire()
        try:self.assertEqual(service.answer('Public question')[0],429)
        finally:service.lock.release()
        self.assertEqual(client.prompts,[])

class AdmissionTests(unittest.TestCase):
    def test_daily_budget_survives_restart_without_questions_or_addresses(self):
        with tempfile.TemporaryDirectory() as temp:
            path=str(Path(temp)/'usage.sqlite');admission=Admission(path,daily_limit=1)
            self.assertTrue(admission.take('192.0.2.1')[0]);admission.db.close()
            admission=Admission(path,daily_limit=1)
            self.assertFalse(admission.take('192.0.2.2')[0]);admission.db.close()
            self.assertNotIn(b'192.0.2',Path(path).read_bytes())
    def test_network_rate_limit_and_expiry(self):
        now=[0];a=Admission(':memory:',100,lambda:now[0])
        for _ in range(6):self.assertTrue(a.take('192.0.2.1')[0])
        self.assertFalse(a.take('192.0.2.1')[0]);self.assertTrue(a.take('192.0.2.2')[0])
        now[0]=301;self.assertTrue(a.take('192.0.2.1')[0]);a.db.close()

class HostedIdentityTests(unittest.TestCase):
    def test_unadvertised_model_fails_before_generation(self):
        with patch.object(InfomaniakClient,'request',return_value={'data':[{'id':'different-model'}]}):
            with self.assertRaises(ValueError):InfomaniakClient('12345','synthetic-not-a-key')
    def test_token_cannot_change_endpoint_or_add_header(self):
        for product,token in [('https://other.test','x'),('1','x\nAuthorization: other')]:
            with self.assertRaises(ValueError):InfomaniakClient(product,token)
    def test_mismatched_response_and_truncation_cannot_pass(self):
        with patch.object(InfomaniakClient,'request',return_value={'data':[{'id':MODEL}]}):client=InfomaniakClient('12345','synthetic-not-a-key')
        for model,reason in [('other-model','stop'),(MODEL,'length')]:
            with patch.object(client,'request',return_value={'model':model,'choices':[{'finish_reason':reason}]}):
                with self.assertRaises(ValueError):client.call('public prompt',lambda *a:None,'test',100)
    def test_malformed_provider_shape_fails_closed(self):
        with patch.object(InfomaniakClient,'request',return_value={'data':[{'id':MODEL}]}):client=InfomaniakClient('12345','synthetic-not-a-key')
        for response in [[],{}, {'choices':[]}, {'choices':['invalid']}]:
            with patch.object(client,'request',return_value=response):
                with self.assertRaises(ValueError):client.call('public prompt',lambda *a:None,'test',100)
    def test_redirect_does_not_forward_credentials(self):
        with self.assertRaises(ValueError):NoRedirect().redirect_request(None,None,302,'',{},'https://other.test')

class LiveHttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(b'fixture',CASE))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def post(self,payload,origin=None):
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=origin
        req=urllib.request.Request(self.url+'/api/live/question',json.dumps(payload).encode(),headers)
        try:response=urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:response=e
        with response:return response.status,json.loads(response.read())
    def test_no_live_service_is_honest(self):
        status,result=self.post({'question':'What changes?'})
        self.assertEqual(status,503);self.assertFalse(result['live_inference_performed_for_this_request'])
    def test_notes_choice_salary_and_cross_origin_are_rejected_before_inference(self):
        for field in ['notes','choice','salary','history']:
            self.assertEqual(self.post({'question':'What changes?',field:'synthetic private field'})[0],400)
        self.assertEqual(self.post({'question':'What changes?'},'https://other.test')[0],400)
        self.assertEqual(self.post({'question':'x'*701})[0],400)
        self.assertEqual(self.post({'question':['What changes?']})[0],400)

if __name__=='__main__':unittest.main()
