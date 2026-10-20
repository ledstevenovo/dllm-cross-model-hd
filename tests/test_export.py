import pytest
from scripts.offline import extract
from tests.test_trace import fixture
from src.trace_schema import save_trace
import json


def test_feature_export_rejects_wrong_split_and_unattributed_review(tmp_path):
    m,a=fixture();m.update(synthetic=False,model_id='model',sample_id='s',question_id='q',dataset='triviaqa',split='train',prompt='Q')
    q={'question_id':'q','sample_id':'q','dataset':'triviaqa','split':'test','prompt':'Q','cluster_id':'q'}
    qp=tmp_path/'qa.jsonl';qp.write_text(json.dumps(q)+'\n')
    labels=tmp_path/'labels.jsonl';labels.write_text(json.dumps({'model_id':'model','sample_id':'s','question_id':'q','label':'correct','human_reviewed':True,'label_source':'auto'})+'\n')
    save_trace(tmp_path/'traces'/'s.npz',m,a)
    with pytest.raises(ValueError,match='metadata mismatch'):extract(tmp_path/'traces',labels,tmp_path/'out.parquet',qp)
    q['split']='train';qp.write_text(json.dumps(q)+'\n')
    with pytest.raises(ValueError,match='label_source'):extract(tmp_path/'traces',labels,tmp_path/'out.parquet',qp)
