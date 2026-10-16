#!/usr/bin/env python3
"""Verify local deliverable limits without claiming owner/legal/submission clearance."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parents[2]


def inspect():
    report = ROOT / 'track_2b/StimmFolgen_Report.pdf'
    video = ROOT / 'track_2b/demo/StimmFolgen_Live_Demo.mp4'
    metadata = json.loads((ROOT / 'track_2b/demo/StimmFolgen_Live_Demo-metadata.json').read_text())
    media = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
        'format=duration,size:stream=codec_name,width,height', '-of', 'json', str(video)], text=True))
    pages = len(pymupdf.open(report))
    duration = float(media['format']['duration'])
    tracks = [p.name for p in ROOT.glob('track_*') if p.is_dir()]
    data_bytes = sum(p.stat().st_size for p in (ROOT / 'track_2b/data').rglob('*') if p.is_file())
    assert pages <= 6, f'Report exceeds 6 pages: {pages}'
    assert 0 < duration <= 120, f'Invalid demo duration: {duration}'
    assert {'h264', 'aac'} <= {s['codec_name'] for s in media['streams']}
    assert tracks == ['track_2b'], f'Unexpected challenge directories: {tracks}'
    assert data_bytes <= 100_000_000
    digest = hashlib.sha256(video.read_bytes()).hexdigest()
    assert digest == metadata['sha256'], 'Video metadata does not match the final file'
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    forbidden = [p for p in tracked if re.search(r'(^|/)(\.env(?:\.|$)|\.local/|node_modules/)', p)
                 or p.endswith(('.safetensors', '.gguf', '.ckpt'))]
    assert not forbidden, f'Forbidden local/secret/model file paths: {forbidden}'
    return {'technical_artifacts': 'PASS', 'report_pages': pages,
            'video_seconds': duration, 'video_bytes': int(media['format']['size']),
            'video_sha256': digest, 'data_directory_bytes': data_bytes,
            'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
            'new_inference_performed': False,
            'submission_status': 'NOT_VERIFIED_BY_THIS_TOOL',
            'video_scope': 'See track_2b/demo/README.md and metadata for narration provenance',
            'remaining_review_limits': ['source material rights', 'organiser acceptance of post-deadline changes'],
            'secret_scan_scope': 'tracked path scan only; no claim of exhaustive secret detection'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = inspect()
    text = json.dumps(result, indent=2) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    print(text)
