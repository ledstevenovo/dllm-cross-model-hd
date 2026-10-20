"""Independent artifact audit. Deliberately imports no project modules."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import string
import unicodedata

ROOT = Path(__file__).resolve().parents[1]

def normalize(text):
    text = unicodedata.normalize('NFKC',text).lower().translate(str.maketrans({c:' ' for c in string.punctuation}))
    return ' '.join(re.sub(r'\b(a|an|the)\b',' ',text).split())

def audit(root=ROOT):
    manifest=json.loads((root/'data/manifests/build_dataset_latest.json').read_text(encoding='utf-8'))
    errors=[]; records=[]
    for item in manifest['outputs']:
        p=root/item['path']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
            errors.append('hash: '+item['path'])
        if p.suffix=='.jsonl':
            rows=[json.loads(line) for line in p.read_text(encoding='utf-8').splitlines()]
            if len(rows)!=item['records']: errors.append('count: '+item['path'])
            if p.parent.name!='subsets': records.extend(rows)
    smoke=[json.loads(x) for x in (root/'data/raw_qa/subsets/smoke20.jsonl').read_text(encoding='utf-8').splitlines()]
    all_rows=records+smoke
    for key in ['sample_id','question_id']:
        if len({r[key] for r in all_rows})!=len(all_rows): errors.append('duplicate '+key)
    for key in ['cluster_id','question_normalized']:
        groups=defaultdict(set)
        for r in all_rows: groups[r[key]].add(r['split'])
        if any(len(v)>1 for v in groups.values()): errors.append('cross-split '+key)
    for r in all_rows:
        q=r['question']; expected='Answer the question with a short factual answer.\n\nQuestion: '+q.strip()+'\nAnswer:'
        fingerprint='sha256:'+hashlib.sha256(('v1\x1f'+'Answer the question with a short factual answer.\n\nQuestion: {question}\nAnswer:').encode()).hexdigest()
        if r['prompt']!=expected or r['prompt_fingerprint']!=fingerprint: errors.append('prompt: '+r['sample_id'])
        if normalize(q)!=r['question_normalized']: errors.append('normalization: '+r['sample_id'])
        needle=normalize(r['gold_answer']).split();hay=normalize(r['prompt']).split()
        if len(' '.join(needle))>=3 and any(hay[i:i+len(needle)]==needle for i in range(len(hay)-len(needle)+1)): errors.append('copyable canonical gold: '+r['sample_id'])
        if not r['source'] or not r['gold_answer'].strip() or r['gold_answer']=='<unk>': errors.append('provenance/gold: '+r['sample_id'])
    for name,size,split in [('smoke20',20,'smoke'),('small200',200,'test')]:
        subset=[json.loads(x) for x in (root/f'data/raw_qa/subsets/{name}.jsonl').read_text(encoding='utf-8').splitlines()]
        ids=(root/f'data/raw_qa/subsets/{name}.ids.txt').read_text().splitlines()
        lookup={r['sample_id']:r for r in all_rows}
        if len(subset)!=size or ids!=[r['sample_id'] for r in subset]: errors.append('subset size/ids: '+name)
        if any(r['split']!=split or lookup.get(r['sample_id'])!=r for r in subset): errors.append('subset provenance: '+name)
    pilot=root/'data/raw_qa/subsets/pilot200.jsonl'
    if pilot.exists():
        chosen=[json.loads(x) for x in pilot.read_text(encoding='utf-8').splitlines()]
        lookup={r['sample_id']:r for r in all_rows}
        if len(chosen)!=200 or len({r['cluster_id'] for r in chosen})!=200 or any(lookup.get(r['sample_id'])!=r or r['split']=='smoke' for r in chosen): errors.append('pilot200 integrity')
        if dict(Counter(r['split'] for r in chosen))!={'train':120,'validation':30,'test':50}: errors.append('pilot200 counts')
        pm=json.loads((root/'data/manifests/pilot200.json').read_text())
        if hashlib.sha256(pilot.read_bytes()).hexdigest()!=pm['sha256']: errors.append('pilot200 hash')
    return {'passed':not errors,'records':len(all_rows),'split_counts':dict(Counter(r['split'] for r in all_rows)), 'errors':errors,'scope':'Byte hashes, IDs, exact normalized questions, cluster isolation, prompts, provenance and subset membership. Lexical near-duplicates separately audited; arbitrary semantic paraphrases not guaranteed.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output'); args=parser.parse_args()
    report=audit(); text=json.dumps(report,ensure_ascii=False,indent=2)
    if args.output: Path(args.output).write_text(text+'\n',encoding='utf-8')
    print(text); raise SystemExit(0 if report['passed'] else 1)
