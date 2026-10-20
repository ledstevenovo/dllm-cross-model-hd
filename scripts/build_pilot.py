"""Select a 200-question train/dev/test collection plan without changing global splits."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.splitting import select_stratified


def build(root=ROOT):
    selected=[]
    for split,count in [('train',120),('validation',30),('test',50)]:
        rows=[json.loads(x) for p in sorted((root/'data/raw_qa').glob('*/'+split+'.jsonl')) for x in p.read_text(encoding='utf-8').splitlines()]
        by_cluster={}
        for r in sorted(rows,key=lambda r:r['sample_id']):by_cluster.setdefault(r['cluster_id'],r)
        strata={}
        for cid,r in by_cluster.items():
            stratum=r['dataset']+':'+r['answer_type'] if r['dataset']=='hotpotqa' else r['dataset']
            strata.setdefault(stratum,[]).append(cid)
        picked=select_stratified(strata,count,seed=20261020,salt='pilot200-v1-'+split)
        selected.extend(by_cluster[cid] for ids in picked.values() for cid in ids)
    selected.sort(key=lambda r:(r['split'],r['sample_id']))
    p=root/'data/raw_qa/subsets/pilot200.jsonl'
    p.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in selected),encoding='utf-8',newline='\n')
    manifest={'name':'pilot200-v1','purpose':'same collection questions for both backbones; not a statistically powered final experiment','counts':{s:sum(r['split']==s for r in selected) for s in ['train','validation','test']},'source_manifest_sha256':hashlib.sha256((root/'data/manifests/build_dataset_latest.json').read_bytes()).hexdigest(),'path':str(p.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'question_ids':[r['question_id'] for r in selected]}
    (root/'data/manifests/pilot200.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(manifest['counts'])
    return selected

if __name__=='__main__':build()
