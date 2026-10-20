"""Independent raw-parquet to processed-JSONL provenance audit (no src imports)."""
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def audit():
    lock=json.loads((ROOT/'configs/datasets/sources.lock.json').read_text())['files']
    frames={};specs={};errors=[];conflicts=[]
    for spec in lock:
        p=ROOT/spec['path']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=spec['sha256']:errors.append('raw hash: '+spec['key'])
        if spec['source_split']=='validation':
            frames[spec['key']]=pd.read_parquet(p).to_dict('records');specs[spec['key']]=spec
    paths=[p for p in (ROOT/'data/raw_qa').glob('*/*.jsonl') if p.parent.name!='subsets']+[ROOT/'data/raw_qa/subsets/smoke20.jsonl']
    checked=0
    for p in paths:
        for line in p.read_text(encoding='utf-8').splitlines():
            r=json.loads(line);s=r['source'];raw=frames[s['raw_key']][s['raw_row_index']];spec=specs[s['raw_key']]
            gold=raw['answer']['value'] if r['dataset']=='triviaqa' else raw['answer']
            raw_id=raw['question_id'] if r['dataset']=='triviaqa' else raw['id']
            if ' '.join(raw['question'].split())!=r['question'] or ' '.join(gold.split())!=r['gold_answer'] or raw_id!=s['raw_id']:errors.append('raw/processed mismatch: '+r['sample_id'])
            if s['revision']!=spec['revision'] or s['raw_file_sha256']!=spec['sha256']:errors.append('revision/hash provenance: '+r['sample_id'])
            if r['dataset']=='triviaqa':
                answers={frames[s['raw_key']][i]['answer']['value'] for i in s['raw_row_indexes_collapsed']}
                if len(answers)>1:conflicts.append({'sample_id':r['sample_id'],'raw_gold_values':sorted(answers),'retained_gold':r['gold_answer']})
            checked+=1
    return {'passed':not errors,'records_checked':checked,'errors':errors,'canonical_gold_conflicts':conflicts,'source_revisions':{s['key']:s['revision'] for s in lock},'scope':'Raw bytes, every retained question, canonical gold, raw ID and pinned provenance; no model-pretraining contamination claim.'}


if __name__=='__main__':
    result=audit();(ROOT/'reports/raw_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Raw audit:',result['passed'],'records:',result['records_checked'],'canonical answer conflicts:',len(result['canonical_gold_conflicts']))
    raise SystemExit(0 if result['passed'] else 1)
