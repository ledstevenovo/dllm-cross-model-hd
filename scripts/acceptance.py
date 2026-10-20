"""CPU acceptance runner. Never downloads model weights or runs GPU inference."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]


def main():
    stages=[
        ['scripts/download_raw.py'],
        ['scripts/build_dataset.py'],
        ['scripts/build_pilot.py'],
        ['scripts/verify_rebuild.py'],
        ['scripts/audit_dataset.py','--output','reports/dataset_audit.json'],
        ['scripts/audit_raw.py'],
        ['scripts/audit_near_duplicates.py'],
        ['-m','pytest'],
        ['scripts/offline.py','demo','--output','results/synthetic_demo','--bootstrap','100'],
        ['scripts/audit_offline_artifacts.py'],
        ['scripts/offline.py','evaluate','--features','results/synthetic_demo/features.parquet','--output','results/synthetic_cross_dataset','--axis','dataset','--feature-sets','entropy_raw','--bootstrap','30'],
        ['scripts/offline.py','evaluate','--features','results/synthetic_demo/features.parquet','--output','results/synthetic_no_scale','--feature-sets','entropy_raw','--no-scale','--seed','7','--bootstrap','30'],
    ]
    report={'started_utc':datetime.now(timezone.utc).isoformat(),'scope':'CPU-only engineering acceptance. Synthetic results never prove empirical research hypotheses.','checks':[],'completed':False,'passed':False}
    dest=ROOT/'reports/acceptance.json'
    for args in stages:
        print('[START]', ' '.join(args),flush=True);start=time.perf_counter()
        process=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        report['checks'].append({'command':[sys.executable,*args],'returncode':process.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout':process.stdout[-6000:],'stderr':process.stderr[-3000:]})
        report['checks_passed_so_far']=all(c['returncode']==0 for c in report['checks'])
        dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('[PASS]' if not process.returncode else '[FAIL]',args[0],flush=True)
        if process.returncode:
            print(process.stdout,process.stderr);return process.returncode
    import pandas as pd
    table=pd.read_csv(ROOT/'results/synthetic_demo/evaluation/transfer_matrix.csv')
    counts={'transfer_result_rows':len(table),'feature_sets':table.feature_set.nunique(),'detector_kinds':table.kind.nunique(),'directions':len(table[['source','target']].drop_duplicates())}
    if counts!={'transfer_result_rows':240,'feature_sets':10,'detector_kinds':2,'directions':4}:raise AssertionError(counts)
    report['synthetic_outputs']=counts
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    report['completed']=True
    report['passed']=True
    report['artifacts']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'reports/dataset_audit.json',ROOT/'reports/raw_audit.json',ROOT/'reports/near_duplicate_audit.json',ROOT/'reports/reproducibility.json',ROOT/'results/synthetic_demo/evaluation/manifest.json']}
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('ALL CPU ACCEPTANCE CHECKS PASSED',flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
