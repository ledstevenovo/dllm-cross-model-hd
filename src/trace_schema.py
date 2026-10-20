"""Compact, pre-reveal trace contract and CPU-only feature extraction.

TRE: local 2607.22661_TRE.pdf sections 4.1/4.2 eqs. (3)/(4), Appendix
B eqs. (58)/(59): sum_t (t/T) sum_{newly revealed i} H[t,i]. Natural log.
The full-position score and effective-answer variant are separate columns.
"""
import json
from pathlib import Path
import numpy as np

REQUIRED = ('sample_id','question_id','dataset','split','model_id','checkpoint_revision','tokenizer_revision','code_commit','environment','prompt','seed','gen_length','steps','block_size','temperature','sampling_method','precision','generated_text','termination','effective_length','vocab_size')


def summarize_logits(logits):
    """Numerically stable FP32 statistics; collectors can implement on GPU."""
    z=np.asarray(logits,dtype=np.float32)
    if not np.isfinite(z).all(): raise ValueError('nonfinite logits')
    z=z-z.max(axis=-1,keepdims=True)
    logp=z-np.log(np.exp(z).sum(axis=-1,keepdims=True))
    p=np.exp(logp)
    return {'entropy':-(p*logp).sum(axis=-1),'top1_probability':p.max(axis=-1),'top1_token':p.argmax(axis=-1)}


def validate_trace(meta, arrays):
    allowed={"entropy","top1_probability","mask_before","revealed","final_tokens","top1_token","reveal_step"}
    if set(arrays)-allowed: raise ValueError("unsupported arrays; full logits must not be stored")
    missing=[k for k in REQUIRED if k not in meta]
    if missing: raise ValueError('missing metadata: '+', '.join(missing))
    if not isinstance(meta.get('synthetic',False),bool): raise ValueError('synthetic must be boolean')
    for key in ('sample_id','question_id','dataset','model_id','checkpoint_revision','tokenizer_revision','code_commit','precision','prompt','termination'):
        if not isinstance(meta[key],str) or not meta[key].strip(): raise ValueError('invalid metadata '+key)
    if meta['split'] not in ('train','validation','test','smoke'): raise ValueError('invalid split')
    if not isinstance(meta['environment'],dict) or not meta['environment']: raise ValueError('environment must be recorded')
    for key in ('seed','gen_length','steps','block_size','effective_length','vocab_size'):
        if not isinstance(meta[key],int): raise ValueError(key+' must be integer')
    if meta['vocab_size']<2 or meta['block_size']<1 or not np.isfinite(meta['temperature']) or meta['temperature']<0: raise ValueError('invalid decoding metadata')
    if not isinstance(meta['generated_text'],str): raise ValueError('generated_text must be string')
    h=np.asarray(arrays['entropy']); p=np.asarray(arrays['top1_probability'])
    mask=np.asarray(arrays['mask_before']); reveal=np.asarray(arrays['revealed'])
    if h.ndim!=2 or not h.size or any(x.shape!=h.shape for x in (p,mask,reveal)): raise ValueError('expected matching nonempty T x L arrays')
    if mask.dtype!=bool or reveal.dtype!=bool: raise ValueError('mask/revealed must be bool')
    if not np.isfinite(h).all() or (h<0).any() or (h>np.log(meta['vocab_size'])+1e-4).any() or not np.isfinite(p).all() or ((p<0)|(p>1)).any(): raise ValueError('invalid entropy/probability')
    if not mask[0].all(): raise ValueError('trace-v1 requires initially masked generation positions')
    if (reveal & ~mask).any() or (reveal.sum(axis=0)>1).any(): raise ValueError('invalid reveal sets; remasking is outside v1')
    if not np.array_equal(mask[1:],mask[:-1]&~reveal[:-1]): raise ValueError('mask transition mismatch')
    tokens=np.asarray(arrays['final_tokens'])
    if tokens.shape!=(h.shape[1],) or not np.issubdtype(tokens.dtype,np.integer): raise ValueError('final_tokens must be integer L vector')
    if ((tokens<0)|(tokens>=meta['vocab_size'])).any(): raise ValueError('invalid token IDs')
    length=meta['effective_length']
    if meta['gen_length']!=h.shape[1] or not 0<=length<=h.shape[1]: raise ValueError('invalid effective length')
    if (mask[-1,:length]&~reveal[-1,:length]).any(): raise ValueError('effective answer contains unrevealed positions')
    if meta['steps']!=h.shape[0]: raise ValueError('steps must record actual observed T')
    if 'top1_token' in arrays:
        tok=np.asarray(arrays['top1_token'])
        if tok.shape!=h.shape or not np.issubdtype(tok.dtype,np.integer) or ((tok<0)|(tok>=meta['vocab_size'])).any(): raise ValueError('invalid top1_token')
    if 'reveal_step' in arrays:
        expected=np.where(reveal.any(axis=0),reveal.argmax(axis=0)+1,-1)
        if not np.array_equal(arrays['reveal_step'],expected): raise ValueError('reveal_step mismatch')


def save_trace(path, meta, arrays):
    validate_trace(meta,arrays)
    arrays=dict(arrays)
    r=arrays['revealed']
    arrays['reveal_step']=np.where(r.any(axis=0),r.argmax(axis=0)+1,-1)
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    partial=path.with_suffix(path.suffix+'.partial')
    with partial.open('wb') as f:
        np.savez_compressed(f, metadata=np.array(json.dumps({**meta,'trace_schema':'trace-v1'})), **arrays)
    partial.replace(path)


def load_trace(path):
    with np.load(path,allow_pickle=False) as z:
        meta=json.loads(str(z['metadata'])); arrays={k:z[k] for k in z.files if k!='metadata'}
    if meta.get('trace_schema')!='trace-v1': raise ValueError('unknown trace version')
    validate_trace(meta,arrays)
    return meta,arrays


def extract_features(meta, arrays):
    validate_trace(meta,arrays)
    full=arrays['entropy']; full_r=arrays['revealed']; t=full.shape[0]
    length=meta['effective_length']; h=full[:,:length]; r=full_r[:,:length]
    p=arrays['top1_probability'][:,:length]; u=np.arange(1,t+1)/t
    tre=float((full*full_r*u[:,None]).sum())
    safe_length=max(length,1)
    weighted=float((h*r*u[:,None]).sum())
    revealed=h[r]
    features={'tre':tre, 'tre_effective':weighted,'tre_length_normalized':weighted/safe_length,
              'mean_entropy':float(h.mean()) if length else 0.,
              'revealing_entropy':float(revealed.mean()) if revealed.size else 0.,
              'mean_uncertainty':float(1-p.mean()) if length else 0.,
              'entropy_change':float((h[-1]-h[0]).mean()) if length else 0.,
              'effective_length':float(length),'revealed_fraction':float(r.sum()/safe_length)}
    reveal_times=np.nonzero(r)[0]+1
    features['mean_reveal_step']=float(reveal_times.mean()) if reveal_times.size else 0.
    features['mean_reveal_progress']=features['mean_reveal_step']/t
    # Revealed proportion before each forward, weighted by reveal-boundary entropy.
    progress=(~arrays['mask_before'][:,:length]).sum(axis=1)/safe_length
    features['reveal_progress_entropy']=float((h*r*progress[:,None]).sum()/safe_length)
    for name, idx in zip(('early','middle','late'),np.array_split(np.arange(t),3)):
        features[name+'_entropy']=float((h[idx] if idx.size else h[-1:]).mean()) if length else 0.
    for key in list(features):
        if 'entropy' in key or key.startswith('tre'):
            features[key+'_vocab_normalized']=features[key]/np.log(meta['vocab_size'])
    if 'top1_token' in arrays:
        tok=arrays['top1_token'][:,:length]
        features['prediction_switch_rate']=float((tok[1:]!=tok[:-1]).mean()) if t>1 and length else 0.
    return features
