"""Small source-only tuned detectors and paired transfer evaluation."""
import time
import warnings
import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .evaluation import binary_metrics, grouped_bootstrap, select_threshold

FEATURE_SETS = {
    'entropy_raw': ['mean_entropy','early_entropy','middle_entropy','late_entropy','revealing_entropy','entropy_change'],
    'entropy_normalized': ['mean_entropy_vocab_normalized','early_entropy_vocab_normalized','middle_entropy_vocab_normalized','late_entropy_vocab_normalized','revealing_entropy_vocab_normalized','entropy_change_vocab_normalized'],
    'early_only': ['early_entropy'], 'middle_only': ['middle_entropy'], 'late_only': ['late_entropy'],
}
FEATURE_SETS['entropy_confidence'] = FEATURE_SETS['entropy_raw']+['mean_uncertainty']
FEATURE_SETS['absolute_time'] = FEATURE_SETS['entropy_confidence']+['mean_reveal_step','effective_length']
FEATURE_SETS['relative_time'] = FEATURE_SETS['entropy_confidence']+['mean_reveal_progress','revealed_fraction','reveal_progress_entropy']
FEATURE_SETS['relative_normalized'] = FEATURE_SETS['entropy_normalized']+['mean_uncertainty','mean_reveal_progress','revealed_fraction','reveal_progress_entropy_vocab_normalized']
FEATURE_SETS['with_stability'] = FEATURE_SETS['relative_normalized']+['prediction_switch_rate']
BASELINES = ('tre','tre_effective','tre_length_normalized','mean_entropy','revealing_entropy','late_entropy')


def validate_frame(frame):
    required=['sample_id','question_id','cluster_id','dataset','split','model_id','precision','seed','label','human_reviewed','synthetic']
    if set(required)-set(frame): raise ValueError('missing columns: '+str(set(required)-set(frame)))
    if frame.empty: raise ValueError('empty feature table')
    if frame.duplicated(['model_id','sample_id']).any(): raise ValueError('duplicate model/sample IDs')
    if not frame['split'].isin(['train','validation','test','smoke']).all(): raise ValueError('invalid split')
    if frame['synthetic'].nunique()!=1 or not frame['synthetic'].isin([True,False]).all(): raise ValueError('cannot mix synthetic and real')
    for key in ['cluster_id','question_id']:
        if (frame.groupby(key)['split'].nunique()>1).any(): raise ValueError('cross-split leakage: '+key)
    if frame['precision'].nunique()!=1: raise ValueError('mixed precision; use separate experiments')
    if not frame.label.isin(['correct','incorrect','needs_review','refusal_empty','incomplete_truncated','format_failure']).all(): raise ValueError('unknown label')
    for key in ['dataset','cluster_id']:
        if (frame.groupby('question_id')[key].nunique()>1).any(): raise ValueError('question metadata differs across models')
    for model,pool in frame.groupby('model_id'):
        for key in ['checkpoint_revision','tokenizer_revision','gen_length','requested_steps','block_size','temperature','sampling_method']:
            if key in pool and pool[key].nunique()!=1: raise ValueError('mixed generation protocol: '+model+'/'+key)
    models=sorted(frame['model_id'].unique())
    if len(models)!=2: raise ValueError('exactly two backbones required')
    # Pair question sets BEFORE label exclusions; invalid outputs may differ.
    for split in ['train','validation','test']:
        sets=[set(frame[(frame.model_id==m)&(frame.split==split)].question_id) for m in models]
        if not sets[0] or sets[0]!=sets[1]: raise ValueError('unpaired question sets: '+split)
    return models


def eligible(frame):
    # A matcher proposal is not an adjudicated response-level factual label.
    return frame[frame.label.isin(['correct','incorrect']) & frame.human_reviewed.eq(True)].copy()


def fit_source(train, dev, columns, kind, seed=42, scale=True):
    y=train.label.eq('incorrect').astype(int).to_numpy()
    dy=dev.label.eq('incorrect').astype(int).to_numpy()
    if len(np.unique(y))!=2 or len(np.unique(dy))!=2: raise ValueError('source train/dev require both reviewed classes')
    if not np.isfinite(train[columns].to_numpy(dtype=float)).all() or not np.isfinite(dev[columns].to_numpy(dtype=float)).all(): raise ValueError('nonfinite feature')
    best=None; trials=[]
    for strength in ([.1,1.,10.] if kind=='lr' else [.001,.01]):
        estimator=(LogisticRegression(C=strength,max_iter=2000,random_state=seed) if kind=='lr' else
                   MLPClassifier(hidden_layer_sizes=(16,),alpha=strength,solver='lbfgs',max_iter=1000,random_state=seed))
        model=make_pipeline(StandardScaler() if scale else 'passthrough',estimator)
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter('always',ConvergenceWarning)
            started=time.perf_counter();model.fit(train[columns],y);fit_seconds=time.perf_counter()-started
        scores=model.predict_proba(dev[columns])[:,1]
        metric=binary_metrics(dy,scores)['auroc']
        trials.append({'strength':strength,'dev_auroc':metric,'convergence_warning':any(issubclass(w.category,ConvergenceWarning) for w in seen)})
        if best is None or metric>best[0]: best=(metric,model,scores,strength,fit_seconds)
    _,model,score,strength,seconds=best
    return model,select_threshold(dy,score),{'selected_strength':strength,'trials':trials,'fit_seconds':seconds,'train_ids':train.sample_id.tolist(),'dev_ids':dev.sample_id.tolist(),'scale':scale,'columns':columns}


def evaluate_transfer(frame, *, feature_sets=('entropy_raw','relative_normalized'), kinds=('lr','mlp'), repeats=500, seed=42, scale=True, axis='model', predictions=None, fitted_models=None):
    models=validate_frame(frame)
    if axis not in ('model','dataset'): raise ValueError('invalid axis')
    # Only explicit source datasets are used for the separate cross-dataset axis.
    if axis=='dataset' and len(frame.dataset.unique())!=2: raise ValueError('two datasets needed')
    reviewed=eligible(frame); results=[]; audits=[]
    domains=models if axis=='model' else sorted(frame.dataset.unique())
    backbones=[None] if axis=='model' else models
    for backbone in backbones:
        pool=reviewed if backbone is None else reviewed[reviewed.model_id==backbone]
        domain_col='model_id' if axis=='model' else 'dataset'
        for source in domains:
            train=pool[(pool[domain_col]==source)&(pool.split=='train')]
            dev=pool[(pool[domain_col]==source)&(pool.split=='validation')]
            if train.empty or dev.empty: raise ValueError('source has no reviewed training/validation labels')
            for feature_set in feature_sets:
                columns=FEATURE_SETS[feature_set]
                if set(columns)-set(frame): raise ValueError('feature set unavailable: '+feature_set)
                for kind in kinds:
                    model,threshold,audit=fit_source(train,dev,columns,kind,seed,scale)
                    audit.update(source=source,backbone=backbone,feature_set=feature_set,kind=kind,threshold=threshold)
                    audits.append(audit)
                    if fitted_models is not None:
                        fitted_models[(str(backbone),source,feature_set,kind)]=model
                    for target in domains:
                        test=pool[(pool[domain_col]==target)&(pool.split=='test')]
                        if test.empty: raise ValueError('target has no reviewed test labels')
                        # Pooled result plus dataset strata for the cross-model axis.
                        groups=[('all',test)]
                        if axis=='model':groups += list(test.groupby('dataset'))
                        for dataset,group in groups:
                            started=time.perf_counter();score=model.predict_proba(group[columns])[:,1];seconds=time.perf_counter()-started
                            y=group.label.eq('incorrect').astype(int).to_numpy()
                            if dataset=='all' and predictions is not None:
                                predictions.extend({'axis':axis,'source':source,'target':target,'backbone':backbone,'feature_set':feature_set,'kind':kind,'sample_id':sample,'question_id':question,'label':label,'score':float(s),'threshold':threshold}
                                                   for sample,question,label,s in zip(group.sample_id,group.question_id,group.label,score))
                            result={'axis':axis,'source':source,'target':target,'backbone':backbone,'dataset':dataset,'feature_set':feature_set,'kind':kind,'scale':scale,'synthetic':bool(frame.synthetic.iloc[0]),'predict_seconds':seconds,'seed':seed}
                            result.update(binary_metrics(y,score,threshold,True))
                            result.update(grouped_bootstrap(y,score,group.question_id,repeats=repeats,seed=seed))
                            results.append(result)
    table=pd.DataFrame(results)
    # Gap compares two detectors evaluated on exactly the SAME target test set.
    for i,row in table.iterrows():
        reference=table[(table.source==row.target)&(table.target==row.target)&(table.dataset==row.dataset)&(table.feature_set==row.feature_set)&(table.kind==row.kind)]
        if axis=='dataset':reference=reference[reference.backbone==row.backbone]
        reference_value=reference.iloc[0].auroc
        table.loc[i,'transfer_cost_auroc']=(reference_value-row.auroc if pd.notna(reference_value) and pd.notna(row.auroc) else np.nan)
    return table,audits


def evaluate_baselines(frame, repeats=500, seed=42):
    validate_frame(frame); rows=[]
    for (model,dataset),pool in eligible(frame).groupby(['model_id','dataset']):
        test=pool[pool.split=='test']
        if test.empty: continue
        groups=[('all',test)]
        lengths=pd.cut(test.effective_length,[-1,16,32,64,128,256,np.inf])
        groups += [(str(interval), group) for interval,group in test.groupby(lengths,observed=True)]
        for length_bin,group in groups:
            y=group.label.eq('incorrect').astype(int).to_numpy()
            for name in BASELINES:
                rows.append({'model_id':model,'dataset':dataset,'length_bin':length_bin,'method':name,'synthetic':bool(frame.synthetic.iloc[0]),**binary_metrics(y,group[name]),**grouped_bootstrap(y,group[name],group.question_id,repeats=repeats,seed=seed)})
    return pd.DataFrame(rows)
