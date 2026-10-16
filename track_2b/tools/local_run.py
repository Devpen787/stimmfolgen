#!/usr/bin/env python3
"""Start verified loopback-only model and app; clean up only owned subprocesses."""
import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'track_2b/src/gate0'))
from local_model import inspect
from local_setup import hardware


def port_open(port):
    with socket.socket() as sock:return sock.connect_ex(('127.0.0.1',port))==0


def stop_owned(*_):
    raise KeyboardInterrupt


def main():
    p=argparse.ArgumentParser();p.add_argument('--model-dir',type=Path,default=ROOT/'.local/models/apertus-v1.5-8b-mlx-4bit')
    p.add_argument('--model-python',type=Path,default=Path(sys.executable));p.add_argument('--port',type=int,default=8770);p.add_argument('--model-port',type=int,default=8766)
    p.add_argument('--source-pdf',type=Path,default=ROOT/'.local/local/booklet.pdf');p.add_argument('--check',action='store_true')
    args=p.parse_args();signal.signal(signal.SIGTERM,stop_owned);print(json.dumps(hardware(),indent=2),flush=True)
    if not all(1024<=v<=65535 for v in (args.port,args.model_port)) or args.port==args.model_port:raise ValueError('Use two distinct ports between 1024 and 65535')
    if port_open(args.port):raise RuntimeError(f'App port {args.port} is busy. Choose APP_PORT=8783; no existing service was changed.')
    if not args.source_pdf.exists():raise RuntimeError('Source booklet missing. Run make local-setup first or supply --source-pdf.')
    model_dir=args.model_dir.expanduser().resolve(strict=True);base=f'http://127.0.0.1:{args.model_port}/v1'
    owned=[];log=None
    try:
        if not port_open(args.model_port):
            logdir=ROOT/'.local/local';logdir.mkdir(parents=True,exist_ok=True);log=(logdir/'model-server.log').open('ab')
            env={**os.environ,'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1','PYTHONDONTWRITEBYTECODE':'1'}
            command=[str(args.model_python),'-m','mlx_lm','server','--model',str(model_dir),'--host','127.0.0.1','--port',str(args.model_port),'--temp','0','--max-tokens','850','--chat-template-args','{"enable_thinking":false}','--decode-concurrency','1','--prompt-concurrency','1','--prompt-cache-size','1','--prefill-step-size','256']
            process=subprocess.Popen(command,stdout=log,stderr=log,env=env);owned.append(process)
            deadline=time.monotonic()+120
            while not port_open(args.model_port):
                if process.poll() is not None or time.monotonic()>deadline:raise RuntimeError('Model did not start. Inspect .local/local/model-server.log.')
                time.sleep(.5)
        identity=inspect(model_dir,base)
        if not identity['v1_5_verified']:raise RuntimeError('Requires pinned Apertus v1.5')
        print('Verified local Apertus v1.5. Questions stay on this Mac. No API key needed.',flush=True)
        if args.check:return
        env={**os.environ,'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1'}
        # Hosted credentials/config cannot silently switch this local installation.
        for key in list(env):
            if key.startswith(('INFOMANIAK_','PUBLICAI_','LLM_')):env.pop(key)
        command=[sys.executable,str(ROOT/'track_2b/src/app/backend.py'),'--source-pdf',str(args.source_pdf),'--local-model-dir',str(model_dir),'--model-url',base,'--host','127.0.0.1','--port',str(args.port)]
        app=subprocess.Popen(command,env=env);owned.append(app)
        print(f'Open http://127.0.0.1:{args.port}/ — Ctrl+C stops this installation.',flush=True)
        app.wait()
    finally:
        for process in reversed(owned):
            if process.poll() is None:
                process.terminate()
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:process.kill();process.wait()
        if log:log.close()

if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:pass
