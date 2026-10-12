"""Synthetic temporal controls; live archive-byte evidence is separately retained."""
import base64
import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/gate0'))
import publication_availability as p

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.data=b'synthetic-pdf-not-real-inference'
        self.sha=hashlib.sha256(self.data).hexdigest()
        self.row=['fixture','20240111121117',p.ORIGINAL_URL,'application/pdf','200',
                  base64.b32encode(hashlib.sha1(self.data).digest()).decode().rstrip('='),'irrelevant-WARC-length']
        self.headers={'memento-datetime':'Thu, 11 Jan 2024 12:11:17 GMT','x-archive-orig-date':'Thu, 11 Jan 2024 12:11:17 GMT',
                      'content-type':'application/pdf','content-length':str(len(self.data))}

    def test_archive_timestamp_is_upper_bound_not_first_publication(self):
        with patch.object(p,'SOURCE_SHA256',self.sha):
            result=p.verify_capture(self.data,self.data,self.data,self.row,self.headers)
        self.assertTrue(result['public_availability_verified'])
        self.assertIsNone(result['exact_first_published_at'])
        self.assertFalse(result['archive_timestamp_is_signed'])

    def test_changed_edition_is_rejected(self):
        with patch.object(p,'SOURCE_SHA256',self.sha),self.assertRaises(ValueError):
            p.verify_capture(self.data,self.data+b'changed',self.data,self.row,self.headers)

    def test_changed_resource_failed_capture_and_payload_digest_rejected(self):
        for index,value in ((2,'https://example.invalid/booklet.pdf'),(4,'404'),(5,'made-up-digest')):
            row=list(self.row);row[index]=value
            with self.subTest(index=index),patch.object(p,'SOURCE_SHA256',self.sha),self.assertRaises(ValueError):
                p.verify_capture(self.data,self.data,self.data,row,self.headers)

    def test_after_vote_capture_cannot_establish_pre_vote_availability(self):
        row=list(self.row);row[1]='20240304121117'
        with patch.object(p,'SOURCE_SHA256',self.sha),self.assertRaises(ValueError):
            p.verify_capture(self.data,self.data,self.data,row,self.headers)

    def test_header_timestamp_mismatch_rejected(self):
        self.headers['memento-datetime']='Fri, 12 Jan 2024 12:11:17 GMT'
        with patch.object(p,'SOURCE_SHA256',self.sha),self.assertRaises(ValueError):
            p.verify_capture(self.data,self.data,self.data,self.row,self.headers)

    def test_content_cutoff_is_not_a_public_as_of(self):
        evidence={'source_sha256':p.SOURCE_SHA256,'public_availability_verified':True,'available_by_utc':'2024-01-11T12:11:17+00:00'}
        self.assertFalse(p.admit_frame(evidence,'2023-11-29T23:59:59+01:00'))
        self.assertTrue(p.admit_frame(evidence,'2024-03-02T23:59:59+01:00'))
        self.assertFalse(p.admit_frame(evidence,'2024-03-03T00:00:00+01:00'))
        self.assertFalse(p.admit_frame(evidence,'2024-03-02T23:00:00+00:00'))
        evidence['public_availability_verified']=False
        self.assertFalse(p.admit_frame(evidence,'2024-03-02T23:59:59+01:00'))

    def test_naive_frame_is_rejected(self):
        evidence={'source_sha256':p.SOURCE_SHA256,'public_availability_verified':True,'available_by_utc':'2024-01-11T12:11:17+00:00'}
        with self.assertRaises(ValueError):p.admit_frame(evidence,'2024-03-02')

if __name__=='__main__': unittest.main()
