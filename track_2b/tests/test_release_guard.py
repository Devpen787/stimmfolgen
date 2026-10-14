"""Release boundary controls against the immutable prepared packet and actual approvals."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
TRACK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TRACK/'src/gate0'))
from release_guard import human_approvals, verify_recorded_identity

class ReleaseReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.reviews=Path(self.temp.name)
        for p in (TRACK/'docs/evidence/ahv-human-review-2026-10-12').glob('P*.json'):shutil.copy(p,self.reviews/p.name)
        self.packet=TRACK/'docs/evidence/ahv-semantic-review-2026-10-12'
    def test_all_five_bound_statement_approvals_required(self):
        self.assertEqual(set(human_approvals(self.packet,self.reviews)),{'P01','P02','P03','P04','P05'})
        (self.reviews/'P04.json').unlink()
        with self.assertRaises(FileNotFoundError):human_approvals(self.packet,self.reviews)
    def test_rejected_or_stale_statement_blocks_release(self):
        p=self.reviews/'P05.json';original=json.loads(p.read_text())
        for key,value in (('decision','REJECT'),('source_sha256','wrong-edition'),('packet_manifest_sha256','wrong-packet'),('accepted_wording','')):
            data=dict(original);data[key]=value;p.write_text(json.dumps(data))
            with self.subTest(key=key),self.assertRaises(ValueError):human_approvals(self.packet,self.reviews)
    def test_original_candidate_cannot_be_relabelled_under_approval(self):
        p=self.reviews/'P02.json';data=json.loads(p.read_text());data['original_candidate']['value']['amount_chf']=5000000000;p.write_text(json.dumps(data))
        with self.assertRaises(ValueError):human_approvals(self.packet,self.reviews)

    def test_recorded_v15_identity_cannot_be_replaced_by_a_verified_flag(self):
        trace=json.loads((TRACK/'docs/evidence/gate0-release-2026-10-14/run-release-v6/direct_provision.json').read_text())
        verify_recorded_identity(trace)
        trace['local_identity']['backing_checkpoint']='swiss-ai/Apertus-8B-Instruct-2509'
        with self.assertRaises(ValueError):verify_recorded_identity(trace)
    def test_recorded_weight_hash_is_required(self):
        trace=json.loads((TRACK/'docs/evidence/gate0-release-2026-10-14/run-release-v6/direct_provision.json').read_text())
        trace['local_identity']['artifacts']['model.safetensors']['sha256']='wrong-weights'
        with self.assertRaises(ValueError):verify_recorded_identity(trace)

if __name__=='__main__':unittest.main()
