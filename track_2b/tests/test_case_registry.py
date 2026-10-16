"""Synthetic admission negatives; these never grant a real case approval."""
import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
TRACK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TRACK/'src/app'))
from case_registry import additional_cases
class CaseAdmissionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'data/cases').mkdir(parents=True);self.path=self.root/'data/cases/fictional.json'
  self.card={'statement':'Synthetic fixed wording','review_status':'HUMAN_REVIEWED_STATEMENT','citations':[]}
  digest=hashlib.sha256(json.dumps([self.card['statement']],separators=(',',':')).encode()).hexdigest()
  self.case={'gate':{'human_review':{'decision':'ACCEPT','reviewer_kind':'HUMAN_USER','wording_sha256':digest}},'cards':[self.card],'source_sha256':'a'*64}
 def tearDown(self):self.tmp.cleanup()
 def check_rejected(self,pattern):
  self.path.write_text(json.dumps(self.case))
  with patch('case_registry.TRACK',self.root),self.assertRaisesRegex(ValueError,pattern):additional_cases(self.root/'sources')
 def test_model_only_or_pending_review_is_not_publishable(self):
  self.case['gate']['human_review']['decision']='PENDING';self.check_rejected('explicit human review')
 def test_wording_cannot_change_after_acceptance(self):
  self.card['statement']='Synthetic changed wording';self.check_rejected('wording differs')
 def test_source_bytes_required_even_with_a_synthetic_accepted_record(self):
  self.check_rejected('source PDF required')
 def test_changed_source_bytes_rejected(self):
  (self.root/'sources').mkdir();(self.root/'sources/fictional.pdf').write_bytes(b'synthetic wrong source');self.check_rejected('PDF authentication failed')
if __name__=='__main__':unittest.main()
