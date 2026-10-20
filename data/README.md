# Data layout

raw_download: pinned original parquet, ignored; recover with scripts/download_raw.py.
raw_qa/{dataset}/{train,validation,test}.jsonl: frozen research questions.
raw_qa/subsets: smoke20 (engineering), small200 (test-only), pilot200 (120/30/50 collection list).
manifests: source/build/pilot provenance; latest manifest is authoritative, older versions are historical.
trajectories, generations, labels, features: future real-model outputs. Keep all bulk/model-specific outputs out of Git. Synthetic examples belong only in results/synthetic_demo.

See docs/DATASET.md and docs/LABEL_PROTOCOL.md before collecting or labelling.
