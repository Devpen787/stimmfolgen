#!/usr/bin/env python3
"""Real-source release guard negative controls using temporary, explicitly mutated copies.

No new inference and no alteration of archived evidence; mutations are not model outputs.
"""
import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
TRACK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TRACK/'src/gate0'))
from release_guard import clear_gate
p=argparse.ArgumentParser();p.add_argument('--source-pdf',type=Path,required=True);args=p.parse_args()
evidence=TRACK/'docs/evidence/gate0-release-2026-10-14'
packet=TRACK/'docs/evidence/ahv-semantic-review-2026-10-12'
reviews=TRACK/'docs/evidence/ahv-human-review-2026-10-12'
pdf=args.source_pdf.read_bytes()
assert clear_gate(pdf,evidence,packet,reviews)['gate0_status']=='PASS_BOUNDED_AHV'
results={}
def reject(label,callback):
    try:callback()
    except (ValueError,FileNotFoundError):results[label]='BLOCKED_AS_REQUIRED'
    else:raise AssertionError('Release did not reject '+label)
reject('source_byte_mismatch',lambda:clear_gate(pdf+b'changed',evidence,packet,reviews))
with tempfile.TemporaryDirectory() as tmp:
    temp=Path(tmp)
    r=temp/'reviews';shutil.copytree(reviews,r);(r/'P04.json').unlink()
    reject('missing_human_approval',lambda:clear_gate(pdf,evidence,packet,r))
    shutil.copy(reviews/'P04.json',r/'P04.json')
    d=json.loads((r/'P04.json').read_text());d['decision']='REJECT';(r/'P04.json').write_text(json.dumps(d))
    reject('rejected_human_statement',lambda:clear_gate(pdf,evidence,packet,r))
    e=temp/'evidence';shutil.copytree(evidence,e)
    def mutate(relative,callback):
        target=e/relative;data=json.loads(target.read_text());callback(data);target.write_text(json.dumps(data))
        manifest=json.loads((e/'manifest.json').read_text())
        manifest['files'][relative]['bytes']=target.stat().st_size
        manifest['files'][relative]['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        (e/'manifest.json').write_text(json.dumps(manifest))
    mutate('run-release-v6/summary.json',lambda d:d.update(public_case_as_of='2023-11-29T23:59:59+01:00'))
    reject('premature_public_frame_even_with_valid_manifest',lambda:clear_gate(pdf,e,packet,reviews))
    shutil.rmtree(e);shutil.copytree(evidence,e)
    mutate('run-release-v6/direct_provision.json',lambda d:d['local_identity'].update(backing_checkpoint='swiss-ai/Apertus-8B-Instruct-2509'))
    reject('checkpoint_substitution_even_with_valid_manifest',lambda:clear_gate(pdf,e,packet,reviews))
print(json.dumps({'status':'PASS','model_inference_performed':False,'negative_controls':results},indent=2))
