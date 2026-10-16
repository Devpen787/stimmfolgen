#!/usr/bin/env python3
"""Public HTTP smoke for either mode. Does not imply remote/phone inference."""
import argparse,json,urllib.request,urllib.error
p=argparse.ArgumentParser();p.add_argument('--url',required=True);a=p.parse_args();base=a.url.rstrip('/')

def get(path):
 with urllib.request.urlopen(urllib.request.Request(base+path,headers={'User-Agent':'StimmFolgen-ReleaseCheck/1.0'}),timeout=15) as r:return json.load(r)

def post(data,origin=None):
 h={'Content-Type':'application/json','User-Agent':'StimmFolgen-ReleaseCheck/1.0'}
 if origin:h['Origin']=origin
 req=urllib.request.Request(base+'/api/live/question',data=json.dumps(data).encode(),headers=h)
 try:r=urllib.request.urlopen(req,timeout=15)
 except urllib.error.HTTPError as e:r=e
 with r:return r.status,json.load(r)
case=get('/api/case');status=get('/api/live/status');catalog=get('/api/catalog')
assert case['gate']['gate0_status']=='PASS_BOUNDED_AHV' and len(case['cards'])==5 and len(catalog['votes'])==5
for field in ['notes','choice','salary','history']:
 assert post({'question':'What changes?',field:'synthetic private field'})[0]==400
assert post({'question':'What changes?'},'https://other.test')[0]==400
print(json.dumps({'status':'PASS','live_configured':status['configured'],'model':status['model'],'evidence_class':'ACTUAL_HTTP_BOUNDARIES_NOT_INFERENCE','origin':base}))
