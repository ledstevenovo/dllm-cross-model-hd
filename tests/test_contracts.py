import pytest
from src.labeling import classify_generation, match_answer
from src.prompts import render_prompt, prompt_fingerprint, answer_in_prompt
from src.splitting import assign_splits, select_stratified
from src.schema import QARecord, validate_records

@pytest.mark.parametrize('answer,gold,expected', [('Paris','Paris',True),('Paris, Texas','Paris',False),('-3.5','3.5',False),('-3.5','-3.50',True),('1,234','1234',True),('12%','12',False),('true','yes',True)])
def test_matching(answer,gold,expected):
    assert match_answer(answer,gold)[0] is expected

def test_large_numeric_answers_do_not_round_to_same_float():
    assert not match_answer('9007199254740992','9007199254740993')[0]

@pytest.mark.parametrize('text,label', [('', 'refusal_empty'), (None,'format_failure'), ("I don\'t know.",'refusal_empty'), ('London','needs_review'), ('Paris','correct'), ('Paris\nIt is in Germany.','needs_review')])
def test_labels(text,label):
    assert classify_generation(text,'Paris').label == label

def test_truncation_is_not_verified_correct():
    assert classify_generation('Paris','Paris',hit_max_length=True).label == 'needs_review'
    assert classify_generation('Lon','Paris',hit_max_length=True).label == 'incomplete_truncated'

def test_frozen_prompt():
    assert prompt_fingerprint() == 'sha256:0de959aec7090589f83e17ef5ac034a76266f87f2452449bc94a8ff35753356b'
    assert 'Question: Where?' in render_prompt('Where?')
    assert not answer_in_prompt('Bulldog', 'Bull')
    assert answer_in_prompt('The Bull?', 'Bull')

def test_split_stable_assignments_not_subset_membership():
    ratios=[('train',.6),('validation',.15),('test',.25)]
    a=assign_splits(['one','two'],ratios,seed=1,salt='v1')
    b=assign_splits(['one','two','three'],ratios,seed=1,salt='v1')
    assert all(b[k]==v for k,v in a.items())
    with pytest.raises(ValueError):
        assign_splits(['one'],[('train',.8)],seed=1,salt='v1')
    assert sum(map(len,select_stratified({'a':['1','2'],'b':['3']},2,seed=1,salt='v1').values()))==2

def test_schema_and_duplicate():
    r=QARecord('id','id','c','triviaqa','train','Capital of France?','Paris',source={'split':'validation'}).finalize()
    assert not r.problems()
    assert validate_records([r,r])['duplicate_sample_ids']==['id']
