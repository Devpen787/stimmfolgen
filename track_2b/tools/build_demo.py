#!/usr/bin/env python3
"""Narrated actual-app capture walkthrough; not a continuous live screen recording."""
import json
import re
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
work=root.parent/'.local/gate0/demo-build';work.mkdir(parents=True,exist_ok=True)
captures=root/'docs/evidence/app-release-2026-10-14'
parts=re.findall(r'^### ([\w-]+)\n(.+?)(?=\n### |\Z)',(root/'demo/DEMO.md').read_text(),re.M|re.S)
clips=[];durations=[]
for i,(image_name,text) in enumerate(parts):
    script=work/f'part-{i}.txt';script.write_text(text.strip())
    audio=work/f'part-{i}.aiff'
    subprocess.run(['/usr/bin/say','-v','Samantha','-r','215','-f',str(script),'-o',str(audio)],check=True)
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)]))+1
    clip=work/f'part-{i}.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',str(captures/(image_name+'.jpg')),'-i',str(audio),
        '-vf','scale=1280:898:force_original_aspect_ratio=decrease,pad=1280:900:(ow-iw)/2:(oh-ih)/2:color=0xf4f5f2',
        '-af','apad','-t',str(duration),'-r','30','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','96k',str(clip)],check=True)
    clips.append(clip);durations.append(duration)
listing=work/'concat.txt';listing.write_text(''.join("file '"+str(c)+"'\n" for c in clips))
out=root/'demo/StimmFolgen_Demo.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(out)],check=True)
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(out)]))
assert duration<=120,f'Demo too long: {duration}'
(root/'demo/metadata.json').write_text(json.dumps({'kind':'NARRATED_ACTUAL_BROWSER_CAPTURE_WALKTHROUGH','continuous_screen_recording':False,
    'fresh_web_inference':False,'duration_seconds':duration,'local_voice':'macOS Samantha','chapters':[{'capture':n+'.jpg','duration_seconds':d} for (n,_),d in zip(parts,durations)]},indent=2)+'\n')
print('Demo seconds:',duration)
