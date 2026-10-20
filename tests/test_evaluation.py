import numpy as np
import pandas as pd
import pytest
from src.evaluation import binary_metrics,grouped_bootstrap,select_threshold
from src.detectors import evaluate_transfer,validate_frame,eligible,FEATURE_SETS,fit_source


def frame():
    rows=[]
    for model in ['a','b']:
        for split in ['train','validation','test']:
            for i in range(12):
                row={'sample_id':split+str(i),'question_id':split+str(i),'cluster_id':split+str(i),'dataset':'qa','split':split,'model_id':model,'precision':'bf16','seed':1,'label':'incorrect' if i%2 else 'correct','human_reviewed':True,'synthetic':True}
                row.update({c:float(i%2)+i*.01 for cols in FEATURE_SETS.values() for c in cols})
                rows.append(row)
    return pd.DataFrame(rows)


def test_metric_known_ranking_and_one_class():
    m=binary_metrics([0,0,1,1],[.1,.4,.35,.8])
    assert m['auroc']==.75
    assert m['auprc']==pytest.approx(5/6)
    assert binary_metrics([1,1],[.1,.4])['auroc'] is None
    assert select_threshold(np.array([0,1]),np.array([.1,.9]))==.9


def test_question_bootstrap_repeated_rows_are_one_unit():
    base=grouped_bootstrap([0,1],[.1,.9],['q0','q1'],repeats=100,seed=1)
    duplicated=grouped_bootstrap([0,0,1,1],[.1,.1,.9,.9],['q0','q0','q1','q1'],repeats=100,seed=1)
    assert base==duplicated
    assert base['bootstrap_valid']<100
    assert base['auroc_low']==1


def test_reject_leak_mixed_precision_and_unpaired_questions():
    f=frame();f.loc[0,'cluster_id']='test0'
    with pytest.raises(ValueError,match='leakage'):validate_frame(f)
    f=frame();f.loc[0,'precision']='int4'
    with pytest.raises(ValueError,match='precision'):validate_frame(f)
    f=frame().iloc[1:]
    with pytest.raises(ValueError,match='unpaired'):validate_frame(f)


def test_auto_proposals_and_pending_labels_excluded():
    f=frame();f.loc[0,'human_reviewed']=False;f.loc[1,'label']='needs_review'
    assert len(eligible(f))==len(f)-2


def test_source_only_training_invariant_to_target_test_labels():
    f=frame(); table,audits=evaluate_transfer(f,feature_sets=['entropy_raw'],kinds=['lr'],repeats=10)
    assert len(table[table.dataset=='all'])==4
    changed=f.copy();mask=changed.split.eq('test');changed.loc[mask,'label']=np.where(changed.loc[mask,'label'].eq('incorrect'),'correct','incorrect')
    table2,audits2=evaluate_transfer(changed,feature_sets=['entropy_raw'],kinds=['lr'],repeats=10)
    for a,b in zip(audits,audits2):
        for key in ['selected_strength','threshold','train_ids','dev_ids','trials']:assert a[key]==b[key]
        assert all(x.startswith('train') for x in a['train_ids'])
        assert all(x.startswith('validation') for x in a['dev_ids'])
    assert (table[table.source!=table.target].transfer_cost_auroc==0).all()


def test_scaler_fits_source_train_only():
    f=frame();cols=FEATURE_SETS['entropy_raw'];tr=f[(f.model_id=='a')&(f.split=='train')];dev=f[(f.model_id=='a')&(f.split=='validation')].copy();dev[cols]=dev[cols]+1000
    model,_,_=fit_source(tr,dev,cols,'lr')
    np.testing.assert_allclose(model[0].mean_,tr[cols].mean())

def test_one_class_target_has_undefined_metrics_not_fake_perfect_score():
    f=frame();f.loc[f.split=='test','label']='correct'
    table,_=evaluate_transfer(f,feature_sets=['entropy_raw'],kinds=['lr'],repeats=5)
    assert table.auroc.isna().all()
    assert table.transfer_cost_auroc.isna().all()
