import numpy as np
import pytest
from src.trace_schema import REQUIRED,save_trace,load_trace,extract_features,validate_trace,summarize_logits

def fixture():
    meta={k:'fixture' for k in REQUIRED}; meta.update(gen_length=2,effective_length=2,steps=2,vocab_size=100,split="train",environment={"python":"fixture"},temperature=0.0,block_size=2,seed=1)
    arrays={'entropy':np.array([[2.,4.],[1.,3.]]),'top1_probability':np.full((2,2),.5),'mask_before':np.array([[True,True],[False,True]]),'revealed':np.array([[True,False],[False,True]]),'final_tokens':np.array([10,11])}
    return meta,arrays

def test_hand_calculated_scores():
    m,a=fixture(); f=extract_features(m,a)
    assert f['tre']==4 # .5*2 + 1*3
    assert f['tre_length_normalized']==2
    assert f['mean_entropy']==2.5
    assert f['revealing_entropy']==2.5
    assert f['late_entropy']==2

def test_roundtrip(tmp_path):
    m,a=fixture(); p=tmp_path/'sample.npz';save_trace(p,m,a)
    got,b=load_trace(p)
    assert got['sample_id']==m['sample_id']
    np.testing.assert_array_equal(a['entropy'],b['entropy'])

def test_invalid_transition():
    m,a=fixture();a['mask_before'][1,0]=True
    with pytest.raises(ValueError,match='transition'):validate_trace(m,a)

def test_nan_rejected():
    m,a=fixture();a['entropy'][0,0]=np.nan
    with pytest.raises(ValueError,match='entropy'):validate_trace(m,a)

def test_logits_entropy_and_extremes():
    s=summarize_logits(np.array([[0.,0.],[1000.,-1000.]]))
    np.testing.assert_allclose(s['entropy'],[np.log(2),0],atol=1e-6)
    np.testing.assert_allclose(s['top1_probability'],[.5,1.])

def test_effective_length_excludes_padding_but_full_tre_does_not():
    m,a=fixture();m['effective_length']=1
    f=extract_features(m,a)
    assert f['tre']==4
    assert f['tre_effective']==1

def test_unrevealed_effective_answer_and_full_logits_rejected():
    m,a=fixture();a['revealed'][-1,-1]=False
    with pytest.raises(ValueError,match='unrevealed'):validate_trace(m,a)
    m,a=fixture();a['logits']=np.zeros((2,2,100))
    with pytest.raises(ValueError,match='full logits'):validate_trace(m,a)
