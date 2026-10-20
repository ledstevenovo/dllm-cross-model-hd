"""Independent verification of synthetic end-to-end output artifacts.

Uses saved model pipelines and direct rank arithmetic; does not import src.
Only run against this project's self-generated trusted joblib files.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
ROOT=Path(__file__).resolve().parents[1]


def audit():
    folder=ROOT/'results/synthetic_demo/evaluation'
    features=pd.read_parquet(ROOT/'results/synthetic_demo/features.parquet')
    predictions=pd.read_csv(folder/'predictions.csv')
    table=pd.read_csv(folder/'transfer_matrix.csv')
    audits=json.loads((folder/'training_audit.json').read_text())
    models=joblib.load(folder/'detectors.joblib')
    errors=[]
    assert features.synthetic.all(), 'This checker is for synthetic evidence only'
    for item in audits:
        source=features[features.model_id==item['source']]
        train=source[source.split=='train'];dev=source[source.split=='validation']
        if set(item['train_ids'])!=set(train.sample_id) or set(item['dev_ids'])!=set(dev.sample_id):errors.append('source IDs')
        key=(str(item['backbone']),item['source'],item['feature_set'],item['kind'])
        pipeline=models[key]
        if item['scale'] and not np.allclose(pipeline[0].mean_,train[item['columns']].mean()):errors.append('source scaler')
        for target in features.model_id.unique():
            target_rows=features[(features.model_id==target)&(features.split=='test')].sort_values('sample_id')
            saved=predictions[(predictions.source==item['source'])&(predictions.target==target)&(predictions.feature_set==item['feature_set'])&(predictions.kind==item['kind'])].sort_values('sample_id')
            if saved.sample_id.tolist()!=target_rows.sample_id.tolist():errors.append('target prediction IDs')
            score=pipeline.predict_proba(target_rows[item['columns']])[:,1]
            if not np.allclose(score,saved.score):errors.append('frozen predictions')
            y=target_rows.label.eq('incorrect').to_numpy();pos=int(y.sum());neg=len(y)-pos
            auroc=(pd.Series(score).rank().to_numpy()[y].sum()-pos*(pos+1)/2)/(pos*neg)
            row=table[(table.source==item['source'])&(table.target==target)&(table.feature_set==item['feature_set'])&(table.kind==item['kind'])&(table.dataset=='all')].iloc[0]
            if not np.isclose(auroc,row.auroc):errors.append('AUROC rank arithmetic')
    for r in table[table.dataset=='all'].itertuples():
        ref=table[(table.source==r.target)&(table.target==r.target)&(table.feature_set==r.feature_set)&(table.kind==r.kind)&(table.dataset=='all')].iloc[0]
        if not np.isclose(r.transfer_cost_auroc,ref.auroc-r.auroc):errors.append('target-reference gap')
    result={'passed':not errors,'errors':errors,'trained_detectors':len(audits),'saved_predictions':len(predictions),'matrix_rows':len(table),'scope':'Source-only IDs/scaler, frozen saved-model predictions, independent rank AUROC and same-target gap; SYNTHETIC only.'}
    (ROOT/'reports/offline_artifact_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result)
    return result

if __name__=='__main__':raise SystemExit(0 if audit()['passed'] else 1)
