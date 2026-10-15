#!/usr/bin/env python3
import argparse,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/app'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/gate0'))
from case_registry import additional_cases
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);p.add_argument('--download',action='store_true');a=p.parse_args();print(json.dumps({'admitted_cases':list(additional_cases(a.source_dir,a.download))}))
