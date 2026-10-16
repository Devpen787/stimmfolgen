#!/usr/bin/env python3
"""Opt-in local installation for Apple Silicon; never uses a hosted AI API."""
import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MODEL_REPO='tokimoa/apertus-v1.5-8b-mlx-4bit'
MODEL_REVISION='f08ed532a657bef7d322bd0cbca43dac13a9d0a3'
REQUIREMENTS=['mlx==0.32.0','mlx-lm==0.31.3','transformers==5.15.0','pymupdf==1.28.2','huggingface_hub==1.27.0']


def hardware():
    if platform.system()!='Darwin' or platform.machine()!='arm64':
        raise RuntimeError('This local AI package supports Apple Silicon Macs only. Windows/Linux and Intel are not verified.')
    ram=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True))
    return {'os':platform.mac_ver()[0],'architecture':platform.machine(),'ram_gib':round(ram/1024**3,1),'tested_machine_ram_gib':18}


def main():
    p=argparse.ArgumentParser(description='Install the local runtime; --download explicitly permits the ~4.6 GB model download.')
    p.add_argument('--download',action='store_true');p.add_argument('--model-dir',type=Path,default=ROOT/'.local/models/apertus-v1.5-8b-mlx-4bit')
    args=p.parse_args();args.model_dir=args.model_dir.expanduser().resolve();print(json.dumps(hardware(),indent=2))
    if sys.version_info<(3,11):raise RuntimeError('Use Python 3.11 or newer.')
    if shutil.disk_usage(ROOT).free<8*1024**3:raise RuntimeError('Keep at least 8 GiB free for runtime/model setup.')
    runtime=ROOT/'.local/runtime';python=runtime/'bin/python'
    if not python.exists():subprocess.run([sys.executable,'-m','venv',str(runtime)],check=True)
    subprocess.run([str(python),'-m','pip','install',*REQUIREMENTS],check=True)
    if not (args.model_dir/'model.safetensors').exists():
        if not args.download:raise RuntimeError('Model not installed. Rerun with --download to fetch the pinned ~4.6 GB model.')
        subprocess.run([str(python),'-c','from huggingface_hub import snapshot_download; import sys; snapshot_download(repo_id=sys.argv[1],revision=sys.argv[2],local_dir=sys.argv[3])',MODEL_REPO,MODEL_REVISION,str(args.model_dir.resolve())],check=True)
    sys.path.insert(0,str(ROOT/'track_2b/src/gate0'))
    # Source import/extraction uses the installed runtime, never system-package mutation.
    subprocess.run([str(python),str(ROOT/'track_2b/src/gate0/source_probe.py'),'--out',str(ROOT/'.local/local/source.json'),'--pdf-out',str(ROOT/'.local/local/booklet.pdf')],check=True)
    print('Installed. Run make local-run. No external inference service is used.')

if __name__=='__main__':main()
