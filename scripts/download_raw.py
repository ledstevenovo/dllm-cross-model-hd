"""Download revision-pinned public parquet, verifying committed size and SHA256."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    specs = json.loads((ROOT/'configs/datasets/sources.lock.json').read_text())['files']
    records = {}
    for spec in specs:
        path = ROOT/spec['path']
        path.parent.mkdir(parents=True, exist_ok=True)
        if args.force or not path.exists() or sha256(path) != spec['sha256']:
            partial = path.with_suffix('.partial')
            print('[get]', spec['url'], flush=True)
            request = urllib.request.Request(spec['url'], headers={'User-Agent': 'dllm-hd/0.1'})
            with urllib.request.urlopen(request, timeout=60) as response, partial.open('wb') as out:
                for block in iter(lambda: response.read(1 << 20), b''):
                    out.write(block)
            if partial.stat().st_size != spec['bytes'] or sha256(partial) != spec['sha256']:
                raise ValueError('Upstream file differs from source lock: '+spec['key'])
            partial.replace(path)
        records[spec['key']] = {k: v for k, v in spec.items() if k != 'key'}
        print('[verified]', spec['key'], flush=True)
    (ROOT/'data/raw_download/raw_index.json').write_text(json.dumps({'files': records}, indent=2, sort_keys=True)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
