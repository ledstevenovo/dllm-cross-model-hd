"""Binary metrics and question-ID grouped (not row-wise) bootstrap."""
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, brier_score_loss


def select_threshold(y, score):
    if len(np.unique(y)) != 2:
        raise ValueError('source validation requires both classes')
    candidates = np.unique(np.r_[score, np.nextafter(max(score), np.inf)])
    return float(max(candidates, key=lambda t: (f1_score(y, score >= t), t)))


def binary_metrics(y, score, threshold=None, probability=False):
    y, score = np.asarray(y), np.asarray(score, dtype=float)
    if len(y) != len(score) or not len(y) or not np.isfinite(score).all():
        raise ValueError('invalid scores')
    if not np.isin(y, [0,1]).all(): raise ValueError('nonbinary labels')
    both = len(np.unique(y)) == 2
    result = {'n': len(y), 'positive': int(y.sum()), 'negative': int((1-y).sum()),
              'positive_rate': float(y.mean()),
              'auroc': float(roc_auc_score(y, score)) if both else None,
              'auprc': float(average_precision_score(y, score)) if both else None}
    if threshold is not None:
        result['f1'] = float(f1_score(y, score >= threshold, zero_division=0))
        result['threshold'] = float(threshold)
    if probability:
        if ((score<0)|(score>1)).any(): raise ValueError('probability outside [0,1]')
        result['brier'] = float(brier_score_loss(y, score))
        bins = np.minimum((score*10).astype(int),9)
        result['ece'] = float(sum(np.mean(bins==b)*abs(y[bins==b].mean()-score[bins==b].mean())
                                  for b in range(10) if (bins==b).any()))
    return result


def grouped_bootstrap(y, score, question_ids, *, repeats=500, seed=42):
    y, score, ids = np.asarray(y), np.asarray(score), np.asarray(question_ids)
    if repeats < 1 or not len(y) or len(y)!=len(score) or len(y)!=len(ids):
        raise ValueError('invalid bootstrap input')
    groups = [np.flatnonzero(ids==key) for key in sorted(set(ids))]
    rng = np.random.default_rng(seed)
    values = {'auroc': [], 'auprc': []}
    for _ in range(repeats):
        ix = np.concatenate([groups[i] for i in rng.integers(len(groups),size=len(groups))])
        if len(np.unique(y[ix])) < 2: continue
        values['auroc'].append(roc_auc_score(y[ix],score[ix]))
        values['auprc'].append(average_precision_score(y[ix],score[ix]))
    result = {'bootstrap_attempts': repeats, 'bootstrap_valid': len(values['auroc']), 'bootstrap_unit':'question_id'}
    for name, vals in values.items():
        bounds = np.quantile(vals,[.025,.975]).tolist() if len(vals)>=2 else [None,None]
        result[name+'_low'], result[name+'_high'] = bounds
    return result
