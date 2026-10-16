"""Verify historical public availability independently of the printed content cutoff.

The timestamp is an archive observation upper bound, not an exact first-publication
instant or a signed timestamp. Original reports and span identities remain immutable.
"""
import base64
import hashlib
from datetime import datetime, timezone
from source_probe import SOURCE_SHA256, REFERENDUM_DATE

ORIGINAL_URL = 'https://www.admin.ch/dam/gov/de/Dokumentation/Abstimmungen/Marz2024/marzo_DE.pdf.download.pdf/marzo_DE.pdf'
PUBLISHER_PAGE = 'https://www.bsv.admin.ch/de/renteninitiative-ahv-2024'
PUBLISHER_PDF = 'https://www.bsv.admin.ch/dam/de/sd-web/3ulVVyBoZ99F/erlaeuterungen-20240303.pdf'


def verify_capture(pdf, archived_pdf, publisher_pdf, row, headers):
    if any(hashlib.sha256(data).hexdigest() != SOURCE_SHA256 for data in (pdf, archived_pdf, publisher_pdf)):
        raise ValueError('Current/publisher/archive bytes differ from pinned edition')
    if len(row) != 7 or row[2] != ORIGINAL_URL or row[3:5] != ['application/pdf', '200']:
        raise ValueError('Unexpected archive resource or failed capture')
    observed = datetime.strptime(row[1], '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
    if observed >= datetime.fromisoformat(REFERENDUM_DATE+'T00:00:00+01:00'):
        raise ValueError('Archive observation is not pre-vote')
    digest = base64.b32encode(hashlib.sha1(archived_pdf).digest()).decode().rstrip('=')
    if row[5] != digest:
        raise ValueError('CDX payload digest does not match archived PDF')
    header_date = datetime.strptime(headers['memento-datetime'], '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=timezone.utc)
    if header_date != observed or headers['x-archive-orig-date'] != headers['memento-datetime']:
        raise ValueError('Capture timestamp and archived origin date mismatch')
    if headers['content-type'].split(';')[0] != 'application/pdf' or int(headers['content-length']) != len(archived_pdf):
        raise ValueError('Replay is not the complete PDF payload')
    return {'source_sha256': SOURCE_SHA256, 'byte_size': len(pdf),
            'public_availability_verified': True, 'available_by_utc': observed.isoformat(),
            'exact_first_published_at': None, 'basis': 'PRE_VOTE_ARCHIVED_OFFICIAL_PDF_BYTES',
            'archive_timestamp_is_signed': False, 'capture_payload_sha1_base32': digest,
            'original_url': ORIGINAL_URL, 'archive_url': f'https://web.archive.org/web/{row[1]}id_/{ORIGINAL_URL}',
            'referendum_date': REFERENDUM_DATE}


def admit_frame(availability, as_of):
    """Public PRE_VOTE admission; never substitute content cutoff for availability."""
    if availability.get('source_sha256') != SOURCE_SHA256 or availability.get('public_availability_verified') is not True:
        return False
    observed = datetime.fromisoformat(availability['available_by_utc'])
    frame = datetime.fromisoformat(as_of)
    if observed.tzinfo is None or frame.tzinfo is None:
        raise ValueError('Availability and public case frame require explicit time zones')
    return observed <= frame < datetime.fromisoformat(REFERENDUM_DATE+'T00:00:00+01:00')
