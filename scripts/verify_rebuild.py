"""Rebuild into a new scratch directory; compare every processed artifact hash."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    stamp=__import__('datetime').datetime.now().strftime('%Y%m%dT%H%M%S')
    target=ROOT/'.tmp'/('rebuild_'+stamp);target.mkdir(parents=True)
    for relative in ['configs/datasets/build.toml','configs/datasets/sources.lock.json','data/raw_download/raw_index.json']:
        out=target/relative;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/relative,out)
    lock=json.loads((ROOT/'configs/datasets/sources.lock.json').read_text())
    for spec in lock['files']:
        out=target/spec['path'];out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/spec['path'],out)
    subprocess.run([sys.executable,str(ROOT/'scripts/build_dataset.py'),'--repo-root',str(target)],check=True)
    expected=json.loads((ROOT/'data/manifests/build_dataset_latest.json').read_text())
    actual=json.loads((target/'data/manifests/build_dataset_latest.json').read_text())
    comparison=[{'path':a['path'],'expected_sha256':a['sha256'],'actual_sha256':b['sha256'],'equal':a['path']==b['path'] and a['sha256']==b['sha256']} for a,b in zip(expected['outputs'],actual['outputs'])]
    passed=len(expected['outputs'])==len(actual['outputs']) and all(r['equal'] for r in comparison)
    report={'passed':passed,'scratch':str(target),'artifacts':comparison,'scope':'Fresh parquet-to-JSONL rebuild in a separate directory; timestamps and git context excluded from byte identity.'}
    (ROOT/'reports/reproducibility.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Fresh rebuild identical:',passed)
    raise SystemExit(0 if passed else 1)

if __name__=='__main__':main()
