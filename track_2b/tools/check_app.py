#!/usr/bin/env python3
"""Actual-container HTTP smoke checks; no synthetic model pass or inference claim."""
import argparse
import json
import time
import urllib.request
import urllib.error
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8770');args=p.parse_args()
def get(path):
    with urllib.request.urlopen(args.url+path,timeout=5) as r:return r.read()
for attempt in range(30):
    try:health=json.loads(get('/api/health'));break
    except (OSError,urllib.error.URLError):time.sleep(1)
else:raise SystemExit('Backend did not become healthy')
assert health['gate0']=='PASS_BOUNDED_AHV'
case=json.loads(get('/api/case'))
assert case['inference_mode']=='REVIEWED_RECORDED_CASE'
assert case['live_inference_performed_for_this_request'] is False
assert {c['id'] for c in case['cards']}=={'P01','P02','P03','P04','P05'}
assert case['as_of']=='2024-03-02T23:59:59+01:00'
assert all(c['citations'] and c['review_status']=='HUMAN_REVIEWED_STATEMENT' for c in case['cards'])
assert b'no live generation' in get('/')
assert get('/api/booklet.pdf').startswith(b'%PDF')
def post(body):
    request=urllib.request.Request(args.url+'/api/question',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=5) as r:return json.loads(r.read())
a=post({'topic':'personal_cost'});assert a['personal_financing_chf'] is None and a['outcome']=='INSUFFICIENT_EVIDENCE'
assert a['live_inference_performed_for_this_request'] is False
assert post({'topic':'recommend my vote'})['outcome']=='INSUFFICIENT_EVIDENCE'
try:post({'topic':'cost','notes':'SYNTHETIC privacy negative control'})
except urllib.error.HTTPError as e:assert e.code==400;e.close()
else:raise AssertionError('Private fields accepted')
print(json.dumps({'status':'PASS','gate0':health['gate0'],'cards':5,'personal_cost':'UNKNOWN','private_payload':'REJECTED','web_live_inference':False}))
