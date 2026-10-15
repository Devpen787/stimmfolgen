#!/usr/bin/env python3
"""Compose a captioned walkthrough from actual browser captures and local narration."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent / '.local/submission-final/render'


def run(args):
    return subprocess.check_output(args, text=True).strip()


def seconds(path):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                      '-of', 'default=nw=1:nk=1', str(path)]))


def timestamp(value, separator=','):
    millis = round(value * 1000)
    return f'{millis//3600000:02}:{millis//60000%60:02}:{millis//1000%60:02}{separator}{millis%1000:03}'


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    story = json.loads((ROOT / 'demo/tracker-storyboard.json').read_text())
    chapters, segments, captions, elapsed = [], [], [], 0.0
    for i, chapter in enumerate(story['chapters']):
        text = WORK / f'{i}.txt'
        text.write_text(chapter['narration'])
        audio, clip = WORK / f'{i}.aiff', WORK / f'{i}.mp4'
        subprocess.run(['/usr/bin/say', '-v', story['voice'], '-r', str(story['rate']),
                        '-f', str(text), '-o', str(audio)], check=True)
        duration = seconds(audio) + .35
        source = ROOT / 'demo/tracker-captures' / chapter['capture']
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', str(source),
                        '-i', str(audio), '-vf',
                        'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:white',
                        '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11,apad', '-t', str(duration),
                        '-r', '24', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', str(clip)], check=True)
        actual = seconds(clip)
        words = chapter['narration'].split()
        for start in range(0, len(words), 10):
            a, b = elapsed + actual * start / len(words), elapsed + actual * min(start+10, len(words)) / len(words)
            captions.append(f'{len(captions)+1}\n{timestamp(a)} --> {timestamp(b)}\n'+ ' '.join(words[start:start+10])+'\n')
        chapters.append({**chapter, 'start_seconds': round(elapsed, 3), 'duration_seconds': actual,
                         'capture_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        elapsed += actual
        segments.append(clip)
    listing = WORK / 'concat.txt'
    listing.write_text(''.join("file '" + str(p) + "'\n" for p in segments))
    output = ROOT / 'demo/StimmFolgen_Tracker_Demo.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                    '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', str(output)], check=True)
    duration = seconds(output)
    if duration > 120:
        raise RuntimeError(f'Video exceeds the official limit: {duration}')
    (ROOT / 'demo/StimmFolgen_Tracker_Demo.srt').write_text('\n'.join(captions))
    metadata = {'kind': 'NARRATED_ACTUAL_BROWSER_CAPTURE_WALKTHROUGH',
                'continuous_screen_recording': False, 'fresh_web_inference': False,
                'private_data': 'SYNTHETIC_ONLY', 'duration_seconds': duration,
                'resolution': '1280x720', 'video_codec': 'H264', 'audio_codec': 'AAC',
                'voice': 'local macOS '+story['voice'], 'audio_trimmed': False,
                'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'chapters': chapters}
    (ROOT / 'demo/tracker-metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(json.dumps({'video': str(output), 'duration_seconds': duration, 'bytes': output.stat().st_size}))


if __name__ == '__main__':
    main()
