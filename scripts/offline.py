"""CPU-only commands: extract, evaluate, label proposals, and synthetic demo."""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.tmp/matplotlib'))
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
from src.trace_schema import save_trace,load_trace,extract_features
from src.detectors import FEATURE_SETS,evaluate_transfer,evaluate_baselines
from src.labeling import classify_generation


def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x.strip()]


def write_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def questions(path=None):
    if path:return read_jsonl(path)
    return [r for p in sorted((ROOT/'data/raw_qa').glob('*/*.jsonl')) if p.parent.name!='subsets' for r in read_jsonl(p)]


def extract(trace_dir,label_file,output,question_file=None):
    qa={r['question_id']:r for r in questions(question_file)}
    labels={}
    for r in read_jsonl(label_file):
        key=(r['model_id'],r['sample_id'])
        if key in labels:raise ValueError('duplicate label ID')
        if not isinstance(r.get('human_reviewed'),bool):raise ValueError('label requires explicit human_reviewed boolean')
        if not r.get('label_source'):raise ValueError('label source required')
        labels[key]=r
    rows=[]; seen=set();start=time.perf_counter()
    traces=sorted(Path(trace_dir).rglob('*.npz'))
    for path in traces:
        meta,arrays=load_trace(path);key=(meta['model_id'],meta['sample_id'])
        if key in seen:raise ValueError('duplicate trace')
        seen.add(key)
        q=qa[meta['question_id']]
        if any(meta[k]!=q[k] for k in ['dataset','split','prompt']):raise ValueError('trace/QA metadata mismatch')
        label=labels[key]
        if label.get('question_id')!=meta['question_id']:raise ValueError('label question mismatch')
        if label['human_reviewed'] and not meta.get('synthetic',False) and not label['label_source'].startswith('human:'):
            raise ValueError('reviewed real labels require label_source=human:<reviewer/run>')
        row={k:meta[k] for k in ['sample_id','question_id','dataset','split','model_id','precision','seed','checkpoint_revision','tokenizer_revision','gen_length','steps','block_size','temperature','sampling_method','termination']}
        if 'requested_steps' in meta:row['requested_steps']=meta['requested_steps']
        row.update(cluster_id=q['cluster_id'],synthetic=meta.get('synthetic',False),label=label['label'],human_reviewed=label['human_reviewed'],label_source=label['label_source'])
        row.update(extract_features(meta,arrays));rows.append(row)
    if not rows or seen!=set(labels):raise ValueError('trace/label coverage mismatch or empty input')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_parquet(output,index=False)
    write_json(output.with_suffix('.manifest.json'),{'feature_version':'features-v1','trace_count':len(traces),'label_sha256':sha(label_file),'output_sha256':sha(output),'elapsed_seconds':time.perf_counter()-start,'synthetic':all(r['synthetic'] for r in rows),'traces':[{'path':str(p),'sha256':sha(p)} for p in traces]})
    return output


def plot_results(frame,results,output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    synthetic=bool(frame.synthetic.iloc[0]);prefix='SYNTHETIC PIPELINE CHECK — ' if synthetic else ''
    base=results[(results.dataset=='all')&(results.feature_set==results.feature_set.iloc[0])]
    fig,axes=plt.subplots(1,2,figsize=(14,6),layout='constrained')
    for ax,metric in zip(axes,['auroc','auprc']):
        for i,(_,row) in enumerate(base.iterrows()):
            score=row[metric];low=row[metric+'_low'];high=row[metric+'_high']
            if any(pd.isna(x) for x in [score,low,high]):continue
            ax.errorbar(i,score,yerr=np.array([[max(0,score-low)],[max(0,high-score)]]),fmt='o',capsize=4)
        ax.set_xticks(range(len(base)),[f'{r.source}→{r.target}\n{r.kind}' for r in base.itertuples()],rotation=45,ha='right',fontsize=8)
        ax.set_ylim(0,1.05);ax.set_ylabel(metric.upper()+', question-bootstrap 95% CI')
    fig.suptitle(prefix+'Transfer matrix')
    fig.savefig(output/'transfer.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    for (model,label),pool in frame[frame.split=='test'].groupby(['model_id','label']):
        for ax,col in zip(axes,['mean_entropy','mean_reveal_progress']):
            ax.hist(pool[col],bins=15,alpha=.4,density=True,label=model+' / '+label);ax.set_xlabel(col);ax.set_ylabel('Density');ax.legend(fontsize=7)
    fig.suptitle(prefix+'Target feature distributions')
    fig.savefig(output/'feature_distributions.png',dpi=160);plt.close(fig)


def evaluate(feature_file,output,sets,kinds,repeats,seed,scale=True,axis='model',allow_nonbf16=False):
    frame=pd.read_parquet(feature_file)
    if not bool(frame.synthetic.all()) and not allow_nonbf16 and not frame.precision.isin(['bf16','bfloat16']).all():raise ValueError('formal evaluation requires BF16; isolate debug/quantized experiments with --allow-nonbf16')
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    predictions=[];models={}
    results,audits=evaluate_transfer(frame,feature_sets=sets,kinds=kinds,repeats=repeats,seed=seed,scale=scale,axis=axis,predictions=predictions,fitted_models=models)
    import joblib
    joblib.dump(models,output/'detectors.joblib')
    pd.DataFrame(predictions).to_csv(output/'predictions.csv',index=False)
    results.to_csv(output/'transfer_matrix.csv',index=False)
    results.to_csv(output/'ablation.csv',index=False)
    evaluate_baselines(frame,repeats,seed).to_csv(output/'tre_baselines.csv',index=False)
    write_json(output/'training_audit.json',audits)
    from src.detectors import eligible
    counts=[]
    for (model,dataset,split),pool in frame.groupby(['model_id','dataset','split']):
        counts.append({'model_id':model,'dataset':dataset,'split':split,'total':len(pool),'eligible':len(eligible(pool)),'label_counts':dict(Counter(pool.label))})
    write_json(output/'coverage.json',counts)
    plot_results(frame,results,output)
    git=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    code_hashes={str(p.relative_to(ROOT)):sha(p) for folder in ['src','scripts','configs'] for p in sorted((ROOT/folder).rglob('*')) if p.is_file() and p.suffix in ['.py','.toml','.json']}
    manifest={'synthetic':bool(frame.synthetic.all()),'git_commit':git,'code_hashes':code_hashes,'feature_sha256':sha(feature_file),'feature_file':str(feature_file),'seed':seed,'bootstrap_repeats':repeats,'feature_sets':list(sets),'kinds':list(kinds),'scale':scale,'axis':axis,'allow_nonbf16':allow_nonbf16,'precision':sorted(frame.precision.unique()),'elapsed_seconds':time.perf_counter()-start,'environment':{name:importlib.metadata.version(name) for name in ['numpy','pandas','pyarrow','scikit-learn','matplotlib']},'outputs':{p.name:sha(p) for p in output.iterdir() if p.suffix in ['.csv','.png','.json','.joblib'] and p.name!='manifest.json'}}
    write_json(output/'manifest.json',manifest)
    title='Synthetic pipeline verification ONLY' if manifest['synthetic'] else 'Offline evaluation'
    (output/'report.md').write_text('# '+title+'\n\nInputs, code hashes, precision and runtime: manifest.json. Source-only fit/tuning/threshold IDs: training_audit.json. Label exclusions: coverage.json. Four-direction results and target-trained references: transfer_matrix.csv. Feature ablations: ablation.csv.\n\nA small confidence interval here is not evidence for a real research hypothesis when synthetic=true. Raw TRE scores have no probability calibration interpretation. AUROC/AUPRC are undefined (empty cells) for one-class strata. Bootstrap is grouped by question_id; invalid one-class draws and valid counts are recorded.\n',encoding='utf-8')
    print(title, 'rows:',len(results),'output:',output,flush=True)
    return results


def demo(output,repeats=100):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    qa=read_jsonl(ROOT/'data/raw_qa/subsets/pilot200.jsonl')
    rng=np.random.default_rng(42);labels=[]
    for model_index,model in enumerate(['fixture-llada','fixture-dream']):
        for i,q in enumerate(qa):
            y=i%2
            # Artificial label signal tests the pipeline, never model behavior.
            h=np.clip(rng.normal(1+y*.6+model_index*.2,.25,size=(4,8)),.01,3.)
            r=np.zeros((4,8),dtype=bool)
            for t in range(4):r[t,2*t:2*t+2]=True
            mask=np.ones((4,8),dtype=bool)
            for t in range(1,4):mask[t]=mask[t-1]&~r[t-1]
            meta={'sample_id':q['sample_id'],'question_id':q['question_id'],'dataset':q['dataset'],'split':q['split'],'model_id':model,'checkpoint_revision':'synthetic-no-model','tokenizer_revision':'synthetic-no-tokenizer','code_commit':'synthetic-fixture-v1','environment':{'generator':'numpy fixture'},'prompt':q['prompt'],'seed':42,'gen_length':8,'steps':4,'block_size':8,'temperature':0.,'sampling_method':'synthetic','precision':'float32','generated_text':'SYNTHETIC FIXTURE','termination':'complete','effective_length':8,'vocab_size':100,'synthetic':True}
            arrays={'entropy':h,'top1_probability':np.full((4,8),.5),'mask_before':mask,'revealed':r,'final_tokens':np.arange(8),'top1_token':rng.integers(0,100,(4,8))}
            save_trace(output/'traces'/model/(q['sample_id']+'.npz'),meta,arrays)
            labels.append({'model_id':model,'sample_id':q['sample_id'],'question_id':q['question_id'],'label':'incorrect' if y else 'correct','human_reviewed':True,'label_source':'synthetic_fixture_NOT_human_review'})
    label_path=output/'synthetic_labels.jsonl'
    label_path.write_text(''.join(json.dumps(r)+'\n' for r in labels),encoding='utf-8')
    feature_path=extract(output/'traces',label_path,output/'features.parquet',ROOT/'data/raw_qa/subsets/pilot200.jsonl')
    evaluate(feature_path,output/'evaluation',list(FEATURE_SETS),['lr','mlp'],repeats,42)


def main():
    parser=argparse.ArgumentParser(__doc__);sub=parser.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('extract');p.add_argument('--traces',required=True);p.add_argument('--labels',required=True);p.add_argument('--output',required=True);p.add_argument('--questions')
    p=sub.add_parser('evaluate');p.add_argument('--features',required=True);p.add_argument('--output',required=True);p.add_argument('--feature-sets',nargs='+',choices=list(FEATURE_SETS),default=['entropy_raw','relative_normalized']);p.add_argument('--kinds',nargs='+',choices=['lr','mlp'],default=['lr','mlp']);p.add_argument('--bootstrap',type=int,default=500);p.add_argument('--seed',type=int,default=42);p.add_argument('--no-scale',action='store_true');p.add_argument('--axis',choices=['model','dataset'],default='model');p.add_argument('--allow-nonbf16',action='store_true')
    p=sub.add_parser('label');p.add_argument('--generations',required=True);p.add_argument('--output',required=True);p.add_argument('--questions')
    p=sub.add_parser('demo');p.add_argument('--output',default='results/synthetic_demo');p.add_argument('--bootstrap',type=int,default=100)
    a=parser.parse_args()
    if a.cmd=='extract':extract(a.traces,a.labels,a.output,a.questions)
    elif a.cmd=='evaluate':evaluate(a.features,a.output,a.feature_sets,a.kinds,a.bootstrap,a.seed,not a.no_scale,a.axis,a.allow_nonbf16)
    elif a.cmd=='demo':demo(a.output,a.bootstrap)
    else:
        qa={r['question_id']:r for r in questions(a.questions)};rows=[]
        for g in read_jsonl(a.generations):
            q=qa[g['question_id']]
            proposal=classify_generation(g['generated_text'],q['gold_answer'],q['gold_aliases'],question=q['question'],hit_max_length=g.get('hit_max_length',False)).to_dict()
            rows.append({**proposal,**{k:g[k] for k in ['model_id','sample_id','question_id']},'human_reviewed':False})
        dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')


if __name__=='__main__':main()
