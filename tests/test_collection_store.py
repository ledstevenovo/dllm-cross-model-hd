import json
import pytest
from src.collection_store import CollectionStore
from tests.test_trace import fixture


def test_resume_and_generation_rebuild(tmp_path):
    m,a=fixture()
    with CollectionStore(tmp_path,{'seed':1}) as store:
        store.commit(m,a);store.finish()
    with CollectionStore(tmp_path,{'seed':1},resume=True) as store:
        assert store.existing(m['sample_id'])[0]['question_id']==m['question_id']
        p=store.export_generations()
        assert len(p.read_text().splitlines())==1
    with pytest.raises(ValueError,match='config'):CollectionStore(tmp_path,{'seed':2},resume=True).__enter__()


def test_hash_mismatch_fails_closed(tmp_path):
    m,a=fixture()
    with CollectionStore(tmp_path,{'seed':1}) as store:store.commit(m,a)
    manifest=json.loads((tmp_path/'manifest.json').read_text())
    p=tmp_path/manifest['samples'][m['sample_id']]['path'];p.write_bytes(b'corrupt')
    with CollectionStore(tmp_path,{'seed':1},resume=True) as store:
        with pytest.raises(ValueError,match='hash'):store.existing(m['sample_id'])


def test_orphan_from_interrupted_manifest_commit_is_adopted(tmp_path,monkeypatch):
    m,a=fixture()
    with CollectionStore(tmp_path,{'seed':1}) as store:
        original=store._persist
        monkeypatch.setattr(store,'_persist',lambda:(_ for _ in ()).throw(OSError('interrupted')))
        with pytest.raises(OSError):store.commit(m,a)
        monkeypatch.setattr(store,'_persist',original)
    with CollectionStore(tmp_path,{'seed':1},resume=True) as store:
        assert store.existing(m['sample_id']) is not None
        assert len(store.manifest['samples'])==1


def test_single_writer_lock_and_failed_sample_can_resume(tmp_path):
    m,a=fixture()
    with CollectionStore(tmp_path,{'seed':1}) as store:
        with pytest.raises(FileExistsError):CollectionStore(tmp_path,{'seed':1},resume=True).__enter__()
        store.record_failure(m['sample_id'],RuntimeError('OOM fixture'))
    with CollectionStore(tmp_path,{'seed':1},resume=True) as store:
        assert store.existing(m['sample_id']) is None
        store.commit(m,a);store.finish()
        assert store.manifest['status']=='completed'

def test_npz_sync_and_directory_sync_precede_manifest_ack(tmp_path,monkeypatch):
    import src.trace_schema as trace
    import src.collection_store as storage
    m,a=fixture();events=[]
    with CollectionStore(tmp_path,{'seed':1}) as store:
        original_fsync=storage.os.fsync
        def fsync(fd):events.append('file_sync');return original_fsync(fd)
        monkeypatch.setattr(storage.os,'fsync',fsync)
        monkeypatch.setattr(trace,'sync_directory',lambda p:events.append('npz_directory_sync'),raising=False)
        monkeypatch.setattr(storage,'sync_directory',lambda p:events.append('manifest_directory_sync'),raising=False)
        store.commit(m,a)
        assert events==['file_sync','npz_directory_sync','file_sync','manifest_directory_sync']


def test_npz_sync_failure_does_not_commit_manifest(tmp_path,monkeypatch):
    import src.trace_schema as trace
    m,a=fixture()
    with CollectionStore(tmp_path,{'seed':1}) as store:
        with monkeypatch.context() as patch:
            patch.setattr(trace,'sync_directory',lambda p:(_ for _ in ()).throw(OSError('sync failed')),raising=False)
            with pytest.raises(OSError,match='sync failed'):store.commit(m,a)
        assert not store.manifest['samples']

def test_posix_directory_sync_orders_open_fsync_close(tmp_path,monkeypatch):
    from types import SimpleNamespace
    import src.io_utils as io
    events=[]
    fake=SimpleNamespace(name='posix',O_RDONLY=0,O_DIRECTORY=65536,
        open=lambda path,flags:events.append(('open',str(path),flags)) or 123,
        fsync=lambda fd:events.append(('fsync',fd)),
        close=lambda fd:events.append(('close',fd)))
    monkeypatch.setattr(io,'os',fake)
    io.sync_directory(tmp_path)
    assert events==[('open',str(tmp_path),65536),('fsync',123),('close',123)]
