"""Public metadata boundaries, distinct from the reviewed original AHV case."""
import hashlib,json,unittest
from pathlib import Path
from urllib.parse import urlsplit
CATALOG=json.loads((Path(__file__).resolve().parents[1]/'src/app/catalog.json').read_text())
class CatalogTests(unittest.TestCase):
 def test_metadata_sources_are_official_and_hash_the_declared_excerpt_only(self):
  for source in CATALOG['sources'].values():
   self.assertIn(urlsplit(source['url']).hostname,{'www.admin.ch','www.bsv.admin.ch','www.bk.admin.ch','www.efd.admin.ch'})
   self.assertEqual(source['excerpt_sha256'],hashlib.sha256(source['excerpt'].encode()).hexdigest())
   self.assertIsNone(source['original_html_sha256'])
   self.assertIn(source['snapshot_kind'],{'MANUAL_PRIMARY_WEB_EXCERPT','AUTHENTICATED_PDF'})
   if source['snapshot_kind']=='AUTHENTICATED_PDF':self.assertRegex(source['source_sha256'],r'^[a-f0-9]{64}$')
 def test_only_original_case_claims_reviewed_apertus_analysis(self):
  reviewed=[v for v in CATALOG['votes'] if v['analysis_case_id']]
  admitted={'ahv13'}|{p.stem for p in (Path(__file__).resolve().parents[1]/'data/cases').glob('*.json') if json.loads(p.read_text()).get('gate',{}).get('human_review',{}).get('decision')=='ACCEPT'}
  self.assertEqual({v['id'] for v in reviewed},admitted)
  self.assertEqual(next(v for v in reviewed if v['id']=='ahv13')['analysis_as_of'],'2024-03-02T23:59:59+01:00')
  for v in CATALOG['votes']:
   self.assertRegex(v['date'],r'^20[0-9]{2}-[0-9]{2}-[0-9]{2}$')
   for source in v['sources']:self.assertIn(source,CATALOG['sources'])
 def test_updates_and_relationships_keep_their_dates_and_source_identity(self):
  ids={v['id'] for v in CATALOG['votes']}
  for v in CATALOG['votes']:
   for u in v['updates']:
    self.assertEqual(u['kind'],'OFFICIAL_SOURCE_UPDATE_NOT_MODEL_ANALYSIS')
    self.assertEqual(u['date'],CATALOG['sources'][u['source']]['published_at'])
    # Official results may be published on polling day; all updates stay outside booklet reasoning.
    self.assertGreaterEqual(u['date'],v['date'])
   for r in v['related']:self.assertIn(r['id'],ids);self.assertIn(r['source'],CATALOG['sources']);self.assertTrue(r['reason'])
if __name__=='__main__':unittest.main()
