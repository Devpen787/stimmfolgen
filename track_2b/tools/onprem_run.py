#!/usr/bin/env python3
"""Own a loopback MLX process and Docker app; never touch unrelated services."""
import argparse,json,os,signal,socket,subprocess,sys,time,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'track_2b/src/gate0'))
from local_model import inspect
from local_setup import hardware

def open_port(port):
 with socket.socket() as s:return s.connect_ex(('127.0.0.1',port))==0

def main():
 p=argparse.ArgumentParser();p.add_argument('--model-dir',type=Path,required=True);p.add_argument('--port',type=int,default=8770);p.add_argument('--no-cache',action='store_true');a=p.parse_args()
 if not 1024<=a.port<=65535 or a.port==8768:raise ValueError('Choose an app port distinct from 8768')
 print(json.dumps(hardware()),flush=True)
 if open_port(a.port) or open_port(8768):raise RuntimeError('A required local port is busy. Existing services were not changed.')
 model=a.model_dir.expanduser().resolve(strict=True);directory=ROOT/'.local/onprem';directory.mkdir(parents=True,exist_ok=True)
 name='stimmfolgen-onprem-'+uuid.uuid4().hex[:10];process=None;container=None
 def interrupt(*_):raise KeyboardInterrupt
 signal.signal(signal.SIGTERM,interrupt)
 try:
  env={**os.environ,'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1'}
  with (directory/'model.log').open('ab') as log:
   process=subprocess.Popen([sys.executable,'-m','mlx_lm','server','--model',str(model),'--host','127.0.0.1','--port','8768','--temp','0','--max-tokens','850','--chat-template-args','{"enable_thinking":false}','--decode-concurrency','1','--prompt-concurrency','1','--prompt-cache-size','1','--prefill-step-size','256'],stdout=log,stderr=log,env=env)
   deadline=time.monotonic()+120
   while not open_port(8768):
    if process.poll() is not None or time.monotonic()>deadline:raise RuntimeError('Apertus did not start. Inspect .local/onprem/model.log')
    time.sleep(.5)
   identity=inspect(model,'http://127.0.0.1:8768/v1')
   if not identity['v1_5_verified']:raise RuntimeError('Apertus v1.5 required')
   identity_file=directory/'identity.json';identity_file.write_text(json.dumps(identity,indent=2));identity_file.chmod(0o600)
   common=['docker','build']+(['--no-cache'] if a.no_cache else [])
   subprocess.run(common+['-t','stimmfolgen:local','.'],cwd=ROOT,check=True)
   subprocess.run(common+['-f','Dockerfile.onprem','-t','stimmfolgen:onprem','.'],cwd=ROOT,check=True)
   command=['docker','run','--rm','--name',name,'--read-only','--tmpfs','/tmp:rw,noexec,nosuid,size=16m','-p',f'127.0.0.1:{a.port}:8770','--mount',f'type=bind,source={identity_file},target=/run/local-identity.json,readonly','stimmfolgen:onprem']
   container=subprocess.Popen(command,cwd=ROOT)
   print(f'Open http://127.0.0.1:{a.port}/ . Apertus runs locally; no API key or hosted inference. Ctrl+C stops only this installation.',flush=True)
   container.wait()
 finally:
  if container is not None and container.poll() is None:
   subprocess.run(['docker','stop','--time','5',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);container.wait(timeout=15)
  if process is not None and process.poll() is None:
   process.terminate()
   try:process.wait(timeout=10)
   except subprocess.TimeoutExpired:process.kill();process.wait()

if __name__=='__main__':
 try:main()
 except KeyboardInterrupt:pass
