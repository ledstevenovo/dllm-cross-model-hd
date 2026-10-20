"""CLI for pinned real-model collection, with explicit CPU-only fixture mode.

No torch import on --help. Real runs never construct a fixture automatically.
"""
import argparse
from dataclasses import asdict
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import time

from .collection_store import CollectionStore, file_hash, fingerprint

ROOT = Path(__file__).resolve().parents[1]


def validate_model_config(config):
    for key in ('checkpoint_revision', 'tokenizer_revision'):
        if not isinstance(config.get(key), str) or not re.fullmatch(r'[0-9a-f]{40}', config[key]):
            raise ValueError(key+' must be an immutable full lowercase commit SHA, not main/tag/short revision')
    if not isinstance(config.get('model_id'), str) or not config['model_id'].strip():
        raise ValueError('model_id must be specified')


def validate_precision(family, precision):
    if family == 'dream' and precision in ('float16', 'nf4_fp16'):
        raise ValueError('Dream FP16/NF4-FP16 native entropy ranking can produce NaN; use BF16 or FP32')


def completion_boundary(config, tokenizer, family, tokens):
    eos = config.eos_token_id
    eos_ids = [eos] if isinstance(eos, int) else list(eos or [])
    if isinstance(tokenizer.eos_token_id, int):
        eos_ids.append(tokenizer.eos_token_id)
    turn_marker = '<|eot_id|>' if family == 'llada' else '<|im_end|>'
    turn_id = tokenizer.get_vocab().get(turn_marker)
    stops = set(eos_ids) | ({turn_id} if turn_id is not None else set())
    positions = [i for i, token in enumerate(tokens) if token in stops]
    length = positions[0] if positions else len(tokens)
    termination = ('eos' if tokens[length] in eos_ids else 'eot') if positions else 'length_budget'
    return {'effective_length': length, 'termination': termination,
            'eos_token_ids': sorted(set(eos_ids)), 'stop_token_ids': sorted(stops), 'stop_positions': positions}


def verify_dream_source(model, source_lock=ROOT/'configs/collection_sources.json'):
    """Fail closed if the native sampler no longer guarantees hook-after-shift."""
    locked = json.loads(Path(source_lock).read_text(encoding='utf-8'))['dream_generation_utils']
    module = inspect.getmodule(inspect.unwrap(model.diffusion_generate))
    if module is None or file_hash(module.__file__) != locked['sha256']:
        raise ValueError('Dream native generation source differs from the audited revision; re-audit hook/shift before collecting')


def load_components(family, model_config, precision, device):
    validate_model_config(model_config)
    validate_precision(family, precision)
    import torch
    from transformers import AutoModel, AutoTokenizer
    dtype = {'bf16': torch.bfloat16, 'float16': torch.float16, 'float32': torch.float32,
             'nf4_fp16': torch.float16}[precision]
    if device == 'cuda':
        if not torch.cuda.is_available():
            raise RuntimeError('CUDA unavailable in this inference environment')
        if precision == 'bf16' and (torch.cuda.get_device_capability(0)[0] < 8 or not torch.cuda.is_bf16_supported()):
            raise RuntimeError('native BF16 unavailable; do not silently replace formal precision')
    kwargs = {'revision': model_config['checkpoint_revision'],
              'code_revision': model_config['checkpoint_revision'],
              'trust_remote_code': True, 'torch_dtype': dtype}
    if precision == 'nf4_fp16':
        if device != 'cuda':
            raise ValueError('NF4 collector requires CUDA')
        from transformers import BitsAndBytesConfig
        kwargs.update(quantization_config=BitsAndBytesConfig(load_in_4bit=True,
                      bnb_4bit_quant_type='nf4', bnb_4bit_use_double_quant=True,
                      bnb_4bit_compute_dtype=torch.float16), device_map={'': 0})
    else:
        kwargs['device_map'] = {'': 0 if device == 'cuda' else 'cpu'}
    tokenizer = AutoTokenizer.from_pretrained(model_config['model_id'],
                   revision=model_config['tokenizer_revision'], trust_remote_code=True)
    model = AutoModel.from_pretrained(model_config['model_id'], **kwargs).eval()
    if precision == 'nf4_fp16':
        import bitsandbytes as bnb
        if not any(isinstance(m, bnb.nn.Linear4bit) for m in model.modules()):
            raise ValueError('NF4 requested but no Linear4bit modules were loaded')
    if family == 'dream':
        verify_dream_source(model)
    return model, tokenizer


def _environment(torch, device):
    versions = {'python': sys.version.split()[0], 'torch': torch.__version__}
    for name in ('numpy','transformers','accelerate','bitsandbytes'):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            pass
    versions['cuda_runtime'] = torch.version.cuda
    versions['device'] = device
    if device == 'cuda':
        versions.update(gpu=torch.cuda.get_device_name(0), capability=list(torch.cuda.get_device_capability(0)))
    return versions


def run_collection(family, argv=None):
    parser = argparse.ArgumentParser(description='Collect '+family+' diffusion trajectories (real CUDA by default).')
    parser.add_argument('--questions', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--model-config', default=str(ROOT/'configs/models'/(family+'.json')))
    parser.add_argument('--gen-length', type=int, default=64)
    parser.add_argument('--steps', type=int, default=64)
    parser.add_argument('--block-size', type=int, default=64)
    parser.add_argument('--seed', type=int, default=20261020)
    parser.add_argument('--precision', choices=['bf16','float16','float32','nf4_fp16'])
    parser.add_argument('--device', choices=['cpu','cuda'])
    parser.add_argument('--limit', type=int)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--fixture', action='store_true', help='explicit synthetic CPU models; no weight downloads')
    parser.add_argument('--verify-observer', action='store_true', help='repeat each generation without observation and require equal token IDs')
    args = parser.parse_args(argv)

    import numpy as np
    import torch
    from .collectors import DecodeConfig, collect, count_forward_calls

    device = args.device or ('cpu' if args.fixture else 'cuda')
    precision = args.precision or ('float32' if args.fixture else 'bf16')
    validate_precision(family, precision)
    if args.fixture and (device != 'cpu' or precision != 'float32'):
        raise ValueError('fixture runs must remain explicit CPU float32 synthetic data')
    if args.fixture:
        torch.set_num_threads(1)  # Small CPU fixture reductions; never a real-run override.
    if args.limit is not None and args.limit < 1:
        raise ValueError('limit must be positive')
    cfg = DecodeConfig(args.gen_length, args.steps, args.block_size)
    cfg.validate(family)
    records = [json.loads(line) for line in Path(args.questions).read_text(encoding='utf-8').splitlines() if line.strip()]
    if args.limit is not None:
        records = records[:args.limit]
    if not records or len({r['question_id'] for r in records}) != len(records):
        raise ValueError('question input must contain unique, nonempty question IDs')
    for row in records:
        for field in ('question_id','dataset','split','prompt'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError('missing question field: '+field)
        if row['split'] not in ('train','validation','test','smoke'):
            raise ValueError('invalid question split')
    model_config = json.loads(Path(args.model_config).read_text(encoding='utf-8'))
    validate_model_config(model_config)
    source_files = ['src/collectors.py','src/collection_cli.py','src/collection_store.py',
                    'src/trace_schema.py','src/io_utils.py','configs/collection_sources.json']
    identity = {'collector_version': 'collector-v1', 'family': family, 'model_config': model_config,
                'decoding': asdict(cfg), 'seed': args.seed, 'precision': precision,
                'device': device, 'synthetic': args.fixture, 'question_fingerprint': fingerprint(records),
                'question_count': len(records), 'environment': _environment(torch, device),
                'verify_observer': args.verify_observer,
                'code_hashes': {name: file_hash(ROOT/name) for name in source_files}}
    if args.fixture:
        for path in sorted((ROOT/'tests/fixtures').glob('*.py')):
            identity['code_hashes'][path.relative_to(ROOT).as_posix()] = file_hash(path)
    git = subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True)
    commit = git.stdout.strip() if git.returncode == 0 else 'unavailable-see-code-hashes'

    def reset_seed():
        random.seed(args.seed)
        np.random.seed(args.seed % (2**32))
        torch.manual_seed(args.seed)
        if device == 'cuda':
            torch.cuda.manual_seed_all(args.seed)

    with CollectionStore(args.output, identity, resume=args.resume) as store:
        pending = []
        for row in records:
            sample_id = row['question_id']+'__seed'+str(args.seed)
            if store.existing(sample_id) is None:
                pending.append((sample_id, row))
        if not pending:
            store.finish()
            print('All samples already validated; no model loaded.', flush=True)
            return 0
        try:
            started = time.perf_counter()
            if args.fixture:
                from tests.fixtures.collector_models import PositionModel, DreamPositionModel, Tokenizer
                model = (PositionModel() if family == 'llada' else DreamPositionModel())
                tokenizer = Tokenizer()
                if family == 'dream':
                    verify_dream_source(model)
            else:
                model, tokenizer = load_components(family, model_config, precision, device)
            store.manifest['load_seconds'] = time.perf_counter()-started
            store.manifest['execution_commit'] = commit
            dtype_counts, device_counts = {}, {}
            for parameter in model.parameters():
                dtype_counts[str(parameter.dtype)] = dtype_counts.get(str(parameter.dtype), 0)+parameter.numel()
                device_counts[str(parameter.device)] = device_counts.get(str(parameter.device), 0)+parameter.numel()
            store.manifest['model_runtime'] = {'parameter_dtypes_numel': dtype_counts,
                                               'parameter_devices_numel': device_counts}
            if not args.fixture and precision == 'bf16' and not dtype_counts.get('torch.bfloat16'):
                raise ValueError('BF16 requested but no BF16 model parameters were loaded')
            store._persist()
            mask_id = model.config.mask_token_id
            for sample_id, row in pending:
                messages = [{'role': 'user', 'content': row['prompt']}]
                rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                                     return_tensors='pt').to(device)
                reset_seed()
                if device == 'cuda':
                    torch.cuda.synchronize()
                    torch.cuda.reset_peak_memory_stats()
                started = time.perf_counter()
                with count_forward_calls(model) as forwards:
                    final, arrays = collect(model, ids, cfg, family, mask_id)
                if forwards['count'] != arrays['entropy'].shape[0]:
                    raise ValueError('observed model forward count does not match trace steps')
                if device == 'cuda':
                    torch.cuda.synchronize()
                seconds = time.perf_counter()-started
                peaks = {'allocated': torch.cuda.max_memory_allocated(),
                         'reserved': torch.cuda.max_memory_reserved()} if device == 'cuda' else None
                if args.verify_observer:
                    reset_seed()
                    baseline, _ = collect(model, ids, cfg, family, mask_id, observe=False)
                    if not torch.equal(final, baseline):
                        raise ValueError('observer changed final tokens or generation is nondeterministic')
                    del baseline
                tokens = arrays['final_tokens'].tolist()
                boundary = completion_boundary(model.config, tokenizer, family, tokens)
                length = boundary['effective_length']
                text = tokenizer.decode(tokens[:length], skip_special_tokens=True)
                meta = {'sample_id': sample_id, 'question_id': row['question_id'],
                        'dataset': row['dataset'], 'split': row['split'], 'prompt': row['prompt'],
                        'model_id': model_config['model_id'],
                        'checkpoint_revision': model_config['checkpoint_revision'],
                        'tokenizer_revision': model_config['tokenizer_revision'], 'code_commit': commit,
                        'environment': identity['environment'], 'seed': args.seed,
                        'gen_length': cfg.gen_length, 'steps': int(arrays['entropy'].shape[0]),
                        'requested_steps': cfg.steps, 'block_size': cfg.block_size, 'temperature': 0.,
                        'sampling_method': family+('_low_confidence_greedy' if family == 'llada' else '_entropy_greedy'),
                        'precision': precision, 'generated_text': text, 'effective_length': length,
                        **boundary,
                        'vocab_size': model.config.vocab_size, 'synthetic': args.fixture,
                        'rendered_chat_prompt': rendered, 'prompt_token_ids': ids[0].tolist(),
                        'actual_forward_count': forwards['count'],
                        'observer_verified': args.verify_observer, 'elapsed_seconds': seconds,
                        'peak_memory_bytes': peaks, 'logit_alignment': 'identity' if family == 'llada' else 'native_hook_after_shift',
                        'entropy_distribution': 'FP32 predictive logits before sampling transforms'}
                store.commit(meta, arrays)
                print(f'[{family}] {len(store.manifest["samples"])}/{len(records)} {sample_id} {seconds:.3f}s', flush=True)
                del final, arrays
            store.finish()
        except BaseException as error:
            store.record_failure(locals().get('sample_id', '<model-load>'), error)
            store.export_generations()
            raise
    return 0
