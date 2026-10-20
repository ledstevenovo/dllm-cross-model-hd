"""Single-writer, content-checked trajectory commits and crash recovery."""
import hashlib
import json
import os
from pathlib import Path
import socket
from datetime import datetime, timezone
from .trace_schema import save_trace, load_trace
from .io_utils import sync_directory


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    partial = path.with_suffix(path.suffix+'.partial')
    with partial.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    partial.replace(path)
    sync_directory(path.parent)


class CollectionStore:
    def __init__(self, root, identity, *, resume=False):
        self.root = Path(root)
        self.identity, self.resume = identity, resume
        self.fingerprint = fingerprint(identity)
        self.manifest = None

    def __enter__(self):
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = self.root/'.collection.lock'
        # A killed process leaves an explicit stale lock. Never guess it is dead.
        fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            os.write(fd, json.dumps({'pid': os.getpid(), 'host': socket.gethostname()}).encode())
        finally:
            os.close(fd)
        try:
            path = self.root/'manifest.json'
            if path.exists():
                if not self.resume:
                    raise FileExistsError('run exists; use --resume or a new output directory')
                self.manifest = json.loads(path.read_text(encoding='utf-8'))
                if self.manifest['fingerprint'] != self.fingerprint:
                    raise ValueError('run config/input/environment/code fingerprint changed')
            else:
                self.manifest = {'collection_schema': 'collection-v1', 'fingerprint': self.fingerprint,
                                 'identity': self.identity, 'samples': {}, 'errors': [],
                                 'created_utc': datetime.now(timezone.utc).isoformat()}
            self.manifest['status'] = 'running'
            self._persist()
            return self
        except BaseException:
            self.lock.unlink()
            raise

    def __exit__(self, kind, value, traceback):
        try:
            if kind is not None:
                self.manifest['status'] = 'interrupted'
                self._persist()
        finally:
            self.lock.unlink()

    def _persist(self):
        atomic_json(self.root/'manifest.json', self.manifest)

    def _path(self, sample_id):
        # Untrusted question IDs never become paths (slashes/.. cannot escape root).
        return self.root/'traces'/(hashlib.sha256(sample_id.encode()).hexdigest()+'.npz')

    def existing(self, sample_id):
        entry = self.manifest['samples'].get(sample_id)
        path = self._path(sample_id)
        if entry is not None:
            if entry['path'] != path.relative_to(self.root).as_posix():
                raise ValueError('manifest path mismatch')
            if not path.exists() or file_hash(path) != entry['sha256']:
                raise ValueError('committed trace missing or hash mismatch: '+sample_id)
        elif not path.exists():
            return None
        meta, arrays = load_trace(path)
        if meta.get('collection_fingerprint') != self.fingerprint or meta['sample_id'] != sample_id:
            raise ValueError('orphan/config/sample mismatch: '+sample_id)
        if entry is None:
            # NPZ replace succeeded but manifest replace was interrupted. Adopt
            # only a fully validated trace with the same immutable run signature.
            self._index(path, meta)
        return meta, arrays

    def _index(self, path, meta):
        self.manifest['samples'][meta['sample_id']] = {
            'path': path.relative_to(self.root).as_posix(), 'sha256': file_hash(path),
            'question_id': meta['question_id']}
        self._persist()

    def commit(self, meta, arrays):
        if self.existing(meta['sample_id']) is not None:
            raise FileExistsError('sample already committed')
        meta = {**meta, 'collection_fingerprint': self.fingerprint}
        path = self._path(meta['sample_id'])
        save_trace(path, meta, arrays)
        self._index(path, meta)

    def record_failure(self, sample_id, error):
        self.manifest['errors'].append({'sample_id': sample_id, 'error_type': type(error).__name__,
                                        'message': str(error), 'utc': datetime.now(timezone.utc).isoformat()})
        self.manifest['status'] = 'interrupted'
        self._persist()

    def export_generations(self):
        path = self.root/'generations.jsonl'
        partial = path.with_suffix('.jsonl.partial')
        with partial.open('w', encoding='utf-8', newline='\n') as f:
            for sample_id in sorted(self.manifest['samples']):
                meta, _ = self.existing(sample_id)
                row = {k: meta[k] for k in ('sample_id','question_id','model_id','generated_text',
                                            'termination','effective_length','seed','precision')}
                row['synthetic'] = meta.get('synthetic', False)
                row['hit_max_length'] = meta['termination'] == 'length_budget'
                row['collection_fingerprint'] = self.fingerprint
                f.write(json.dumps(row, ensure_ascii=False)+'\n')
            f.flush()
            os.fsync(f.fileno())
        partial.replace(path)
        sync_directory(path.parent)
        return path

    def finish(self):
        self.export_generations()
        self.manifest['status'] = 'completed'
        self._persist()
