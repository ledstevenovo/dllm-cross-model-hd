"""Full CPU collector acceptance: actual sampler paths, 20 questions each, resume.

Run with the separate torch/transformers CPU test environment. No weights or GPU.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.trace_schema import load_trace,extract_features
from src.collection_store import file_hash


def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--output',default='results/collectors_cpu');a=p.parse_args()
    output=Path(a.output).resolve();output.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,HF_HOME=str(ROOT/'.tmp/hf-collector-tests'),PYTHONIOENCODING='utf-8')
    checks=[];models=[];started=time.perf_counter()
    for family in ['llada','dream']:
        root=output/family
        args=[sys.executable,str(ROOT/f'scripts/collect_{family}.py'),'--fixture','--questions',str(ROOT/'data/raw_qa/subsets/smoke20.jsonl'),'--output',str(root),'--verify-observer']
        # A prior completed fixture run must be explicitly resumable, not overwritten.
        if (root/'manifest.json').exists():args+=['--resume']
        for command in [args,args if '--resume' in args else args+['--resume']]:
            run=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
            checks.append({'command':command,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
            if run.returncode:
                print(run.stdout,run.stderr);raise RuntimeError('collector CLI failed')
        manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
        assert manifest['status']=='completed' and len(manifest['samples'])==20
        qids=set()
        for sample,entry in manifest['samples'].items():
            path=root/entry['path'];assert file_hash(path)==entry['sha256']
            meta,arrays=load_trace(path);features=extract_features(meta,arrays)
            assert meta['synthetic'] and meta['observer_verified'] and meta['actual_forward_count']==64
            assert arrays['entropy'].shape==(64,64) and arrays['revealed'].sum()==64
            assert meta['collection_fingerprint']==manifest['fingerprint']
            assert all(__import__('math').isfinite(v) for v in features.values())
            qids.add(meta['question_id'])
        expected={json.loads(line)['question_id'] for line in (ROOT/'data/raw_qa/subsets/smoke20.jsonl').read_text(encoding='utf-8').splitlines()}
        assert qids==expected
        assert len((root/'generations.jsonl').read_text(encoding='utf-8').splitlines())==20
        models.append({'family':family,'traces':20,'steps':64,'length':64,'manifest_sha256':file_hash(root/'manifest.json')})
    report={'passed':True,'synthetic':True,'scope':'CPU fixture models execute real collection paths; pinned native Dream sampler; NOT real model/GPU acceptance.', 'models':models,'checks':checks,'elapsed_seconds':time.perf_counter()-started,'environment':{k:importlib.metadata.version(k) for k in ['torch','transformers','numpy','pytest']},'source_hashes':{str(path.relative_to(ROOT)):file_hash(path) for folder in ['src','scripts','tests/fixtures','configs'] for path in sorted((ROOT/folder).rglob('*')) if path.is_file() and path.suffix in ['.py','.json','.toml']}}
    dest=ROOT/'reports/phase2_cpu_verification.json';dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: 40 synthetic traces, 64x64, native paths, observer comparisons, resume and feature extraction.')

if __name__=='__main__':main()
