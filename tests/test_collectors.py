import numpy as np
import pytest
torch=pytest.importorskip('torch')
from src.collectors import DecodeConfig,collect,align_generation_logits,logits_statistics
from tests.fixtures.collector_models import PositionModel,DreamPositionModel,Tokenizer
from src.trace_schema import summarize_logits


def test_shift_mapping_raw_and_native_hook_are_identical():
    raw=torch.arange(7*5,dtype=torch.float32).reshape(1,7,5)
    shifted=torch.cat([raw[:,:1],raw[:,:-1]],dim=1)
    direct=align_generation_logits(raw,3,4,'dream',already_shifted=False)
    hook=align_generation_logits(shifted,3,4,'dream',already_shifted=True)
    torch.testing.assert_close(direct,raw[:,2:6])
    torch.testing.assert_close(hook,direct)
    torch.testing.assert_close(align_generation_logits(raw,3,4,'llada'),raw[:,3:7])


def test_fp32_entropy_matches_reference_and_does_not_mutate():
    x=torch.tensor([[[0.,0.,0.],[1000.,-1000.,0.],[-5.,3.,2.]]],dtype=torch.float16)
    original=x.clone();s=logits_statistics(x,chunk_size=1);expected=summarize_logits(x.numpy()[0])
    for key in expected:np.testing.assert_allclose(s[key],expected[key],atol=1e-6)
    torch.testing.assert_close(x,original)
    with pytest.raises(ValueError):logits_statistics(torch.full((1,1,3),float('nan')))


@pytest.mark.parametrize('family,model_type',[('llada',PositionModel),('dream',DreamPositionModel)])
def test_collector_observer_and_real_sampler_tokens_agree(family,model_type):
    ids=torch.tensor([[1,5,6]]);cfg=DecodeConfig(gen_length=4,steps=4,block_size=4)
    observed,arrays=collect(model_type(),ids,cfg,family,31)
    baseline,_=collect(model_type(),ids,cfg,family,31,observe=False)
    torch.testing.assert_close(observed,baseline)
    assert arrays['entropy'].shape==(4,4)
    assert arrays['revealed'].sum()==4
    np.testing.assert_array_equal(arrays['mask_before'][1:],arrays['mask_before'][:-1]&~arrays['revealed'][:-1])
    expected=np.arange(3,7)+3 if family=='llada' else np.arange(2,6)+3
    np.testing.assert_array_equal(arrays['top1_token'][0],expected)
    np.testing.assert_array_equal(arrays['final_tokens'],expected)


def test_llada_matches_independent_upstream_loop(monkeypatch):
    from tests.fixtures import llada_generate_reference as upstream
    monkeypatch.setattr(upstream,'sleep',lambda _:None)
    ids=torch.tensor([[1,5,6]]);cfg=DecodeConfig(gen_length=8,steps=8,block_size=4)
    actual,arrays=collect(PositionModel(),ids,cfg,'llada',31)
    expected=upstream.generate(PositionModel(),ids,steps=8,gen_length=8,block_length=4,mask_id=31,tokenizer=Tokenizer())
    torch.testing.assert_close(actual,expected)
    assert arrays['entropy'].shape==(8,8)


def test_unsupported_decoding_rejected_before_forward():
    m=PositionModel()
    with pytest.raises(ValueError):collect(m,torch.tensor([[1]]),DecodeConfig(gen_length=4,steps=5,block_size=4),'llada',31)
    assert m.calls==0

def test_dream_fp16_native_entropy_nan_is_rejected_not_silently_collected():
    from tests.fixtures.dream_generation_utils import sample_tokens
    logits=torch.tensor([[3.,0.,-1.],[0.,0.,-30.]],dtype=torch.float16)
    confidence,_=sample_tokens(logits,neg_entropy=True)
    assert torch.isnan(confidence[1]), 'Pinned native FP16 epsilon underflows to zero'
    class HalfModel(DreamPositionModel):
        def forward(self,*args,**kwargs):
            out=super().forward(*args,**kwargs);out.logits=out.logits.half();return out
    with pytest.raises(ValueError,match='FP16'):
        collect(HalfModel(),torch.tensor([[1,5,6]]),DecodeConfig(4,4,4),'dream',31)
