import json
from pathlib import Path
import pytest
pytest.importorskip('torch')
from src.collection_cli import run_collection
from src.trace_schema import load_trace
ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('family',['llada','dream'])
def test_cli_fixture_full_path_resume_and_code_provenance(tmp_path,family):
    args=['--fixture','--questions',str(ROOT/'data/raw_qa/subsets/smoke20.jsonl'),'--output',str(tmp_path),'--limit','2','--gen-length','4','--steps','4','--block-size','4']
    assert run_collection(family,args)==0
    manifest=json.loads((tmp_path/'manifest.json').read_text())
    assert manifest['status']=='completed'
    assert len(manifest['samples'])==2
    snapshot={p.name:p.read_bytes() for p in (tmp_path/'traces').glob('*.npz')}
    for entry in manifest['samples'].values():
        meta,arrays=load_trace(tmp_path/entry['path'])
        assert meta['synthetic'] is True and meta['steps']==4
        assert meta['precision']=='float32'
        assert meta['prompt_token_ids']==[1,5,6]
        assert meta['collection_fingerprint']==manifest['fingerprint']
        assert meta['actual_forward_count']==4
    assert run_collection(family,args+['--resume'])==0
    assert snapshot=={p.name:p.read_bytes() for p in (tmp_path/'traces').glob('*.npz')}
    assert len((tmp_path/'generations.jsonl').read_text().splitlines())==2
    with pytest.raises(ValueError,match='config'):
        run_collection(family,args+['--resume','--seed','99'])


def test_real_and_fixture_output_cannot_mix(tmp_path):
    args=['--fixture','--output',str(tmp_path),'--questions',str(ROOT/'data/raw_qa/subsets/smoke20.jsonl'),'--limit','1','--gen-length','4','--steps','4','--block-size','4']
    run_collection('llada',args)
    with pytest.raises(FileExistsError):run_collection('llada',args)


def test_dream_native_source_is_revision_guarded():
    from src.collection_cli import verify_dream_source
    from tests.fixtures.collector_models import DreamPositionModel
    verify_dream_source(DreamPositionModel(),ROOT/'configs/collection_sources.json')

def test_end_of_turn_is_not_mislabeled_as_length_budget():
    from src.collection_cli import completion_boundary
    from types import SimpleNamespace
    from tests.fixtures.collector_models import Tokenizer
    boundary=completion_boundary(SimpleNamespace(eos_token_id=2),Tokenizer(),'llada',[6,7,8,2])
    assert boundary['effective_length']==1
    assert boundary['termination']=='eot'
    assert boundary['stop_positions']==[1,3]


def test_actual_torch_forward_counter_and_handle_cleanup():
    from src.collectors import count_forward_calls,collect,DecodeConfig
    from tests.fixtures.collector_models import PositionModel
    import torch
    model=PositionModel()
    with count_forward_calls(model) as counter:
        collect(model,torch.tensor([[1,5,6]]),DecodeConfig(4,4,4),'llada',31)
        assert counter['count']==4
    model(torch.tensor([[1]]))
    assert counter['count']==4

def test_loader_uses_pinned_revision_and_explicit_dtype_without_download(monkeypatch):
    import transformers,torch
    from src.collection_cli import load_components
    from tests.fixtures.collector_models import PositionModel,Tokenizer
    seen={}
    def model_loader(name,**kwargs):seen['model']=(name,kwargs);return PositionModel()
    def token_loader(name,**kwargs):seen['tokenizer']=(name,kwargs);return Tokenizer()
    monkeypatch.setattr(transformers.AutoModel,'from_pretrained',model_loader)
    monkeypatch.setattr(transformers.AutoTokenizer,'from_pretrained',token_loader)
    config={'model_id':'test/model','checkpoint_revision':'a'*40,'tokenizer_revision':'b'*40}
    load_components('llada',config,'float32','cpu')
    assert seen['model'][1]['revision']=='a'*40
    assert seen['model'][1]['code_revision']=='a'*40
    assert seen['model'][1]['torch_dtype']==torch.float32
    assert seen['model'][1]['device_map']=={'':'cpu'}
    assert seen['tokenizer'][1]['revision']=='b'*40

def test_export_is_linear_not_all_previous_npzs_after_each_sample(tmp_path,monkeypatch):
    from src.collection_store import CollectionStore
    count=[];original=CollectionStore.export_generations
    def export(store):count.append(1);return original(store)
    monkeypatch.setattr(CollectionStore,'export_generations',export)
    run_collection('llada',['--fixture','--questions',str(ROOT/'data/raw_qa/subsets/smoke20.jsonl'),'--output',str(tmp_path),'--limit','3','--gen-length','4','--steps','4','--block-size','4'])
    assert len(count)==1, 'Do not re-read all prior NPZs after every generated question'

def test_mutable_revisions_rejected_before_any_loading(monkeypatch):
    import transformers
    from src.collection_cli import load_components
    monkeypatch.setattr(transformers.AutoModel,'from_pretrained',lambda *a,**k:pytest.fail('must not download'))
    monkeypatch.setattr(transformers.AutoTokenizer,'from_pretrained',lambda *a,**k:pytest.fail('must not download'))
    with pytest.raises(ValueError,match='immutable'):
        load_components('llada',{'model_id':'x','checkpoint_revision':'main','tokenizer_revision':'a'*40},'float32','cpu')

@pytest.mark.parametrize('precision',['float16','nf4_fp16'])
def test_cli_rejects_dream_half_before_opening_a_run(tmp_path,precision,monkeypatch):
    monkeypatch.setattr('src.collection_cli.load_components',lambda *a,**k:pytest.fail('must reject before loading'))
    with pytest.raises(ValueError,match='FP16'):
        run_collection('dream',['--questions',str(ROOT/'data/raw_qa/subsets/smoke20.jsonl'),'--output',str(tmp_path/'run'),'--precision',precision,'--device','cpu'])
    assert not (tmp_path/'run').exists()
