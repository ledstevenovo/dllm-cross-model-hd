"""Deterministic lexical near-duplicate clusters, without embeddings.

Prefix filtering is complete for token-set Jaccard >= threshold. This detects
lexical overlap, not arbitrary semantic paraphrases.
"""
from collections import Counter, defaultdict
import math


def near_pairs(questions, threshold=0.85):
    if not 0 < threshold <= 1:
        raise ValueError('threshold must be in (0,1]')
    sets = [set(q.split()) for q in questions]
    counts = Counter(token for tokens in sets for token in tokens)
    postings = defaultdict(list)
    for i in sorted(range(len(sets)), key=lambda j: (len(sets[j]), j)):
        tokens = sets[i]
        ordered = sorted(tokens, key=lambda token: (counts[token], token))
        prefix = ordered[:len(tokens)-math.ceil(threshold*len(tokens))+1]
        candidates = {j for token in prefix for j in postings[token]
                      if len(sets[j]) >= threshold*len(tokens)}
        for j in sorted(candidates):
            score = len(tokens & sets[j])/len(tokens | sets[j]) if tokens else 1.
            if score >= threshold:
                yield j, i, score
        for token in prefix:
            postings[token].append(i)


def cluster_mapping(records, threshold=0.85):
    parent = {r.cluster_id: r.cluster_id for r in records}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    pairs = []
    for i, j, score in near_pairs([r.question_normalized for r in records], threshold):
        a, b = find(records[i].cluster_id), find(records[j].cluster_id)
        if a != b:
            parent[max(a,b)] = min(a,b)
        pairs.append({'a': records[i].sample_id, 'b': records[j].sample_id, 'jaccard': score})
    return {k: find(k) for k in parent}, pairs
