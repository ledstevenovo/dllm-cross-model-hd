"""Independent lexical overlap check with lexicographic prefix enumeration.
Does not import the production clustering implementation.
"""
from collections import defaultdict
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def audit(root=ROOT,threshold=.85):
    paths=[p for p in (root/'data/raw_qa').glob('*/*.jsonl') if p.parent.name!='subsets']+[root/'data/raw_qa/subsets/smoke20.jsonl']
    rows=[json.loads(line) for p in paths for line in p.read_text(encoding='utf-8').splitlines()]
    rows.sort(key=lambda r:r['sample_id']);sets=[set(r['question_normalized'].split()) for r in rows]
    index=defaultdict(list);pairs=[];violations=[]
    for i in sorted(range(len(rows)),key=lambda j:(len(sets[j]),j)):
        prefix=sorted(sets[i])[:len(sets[i])-math.ceil(threshold*len(sets[i]))+1]
        candidates={j for token in prefix for j in index[token] if len(sets[j])>=threshold*len(sets[i])}
        for j in candidates:
            score=len(sets[i]&sets[j])/len(sets[i]|sets[j])
            if score>=threshold:
                pair={'a':rows[j]['sample_id'],'b':rows[i]['sample_id'],'jaccard':score,'same_split':rows[j]['split']==rows[i]['split'],'same_cluster':rows[j]['cluster_id']==rows[i]['cluster_id']}
                pairs.append(pair)
                if not pair['same_split'] or not pair['same_cluster']:violations.append(pair)
        for token in prefix:index[token].append(i)
    return {'passed':not violations,'threshold':threshold,'records':len(rows),'pair_count':len(pairs),'pairs':sorted(pairs,key=lambda p:(p['a'],p['b'])),'violations':violations,'limitation':'Lexical token-set overlap, not complete semantic paraphrase detection.'}

if __name__=='__main__':
    result=audit();(ROOT/'reports/near_duplicate_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('near pairs:',result['pair_count'],'violations:',len(result['violations']))
    raise SystemExit(0 if result['passed'] else 1)
