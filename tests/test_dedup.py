import itertools
import random
from src.dedup import near_pairs

def test_prefix_join_matches_brute_force():
    rng=random.Random(42)
    questions=[' '.join(rng.sample(list('abcdefghijklmnop'),rng.randint(2,12))) for _ in range(100)]
    for threshold in [.5,.85,1.]:
        actual={frozenset((i,j)) for i,j,_ in near_pairs(questions,threshold)}
        tokens=[set(q.split()) for q in questions]
        expected={frozenset((i,j)) for i,j in itertools.combinations(range(len(tokens)),2) if len(tokens[i]&tokens[j])/len(tokens[i]|tokens[j])>=threshold}
        assert actual==expected
