"""Inspect the raw parquet sources: schema, row counts, key uniqueness, samples.

Run:  source scripts/env.sh && python scripts/inspect_raw.py
"""

from __future__ import annotations

import os

import pandas as pd
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw_download")

FILES = {
    "triviaqa_validation": "triviaqa/rc.nocontext_validation.parquet",
    "triviaqa_test": "triviaqa/rc.nocontext_test.parquet",
    "hotpotqa_validation": "hotpotqa/distractor_validation.parquet",
}


def main() -> None:
    for key, rel in FILES.items():
        path = os.path.join(RAW, rel.replace("/", os.sep))
        print("=" * 78)
        print(f"{key}  ->  {rel}")
        pf = pq.ParquetFile(path)
        print(f"rows={pf.metadata.num_rows}  row_groups={pf.metadata.num_row_groups}")
        print("--- arrow schema ---")
        print(pf.schema_arrow)
        df = pd.read_parquet(path)
        print("--- dtypes ---")
        print(df.dtypes.to_string())
        print("--- first row (repr, truncated) ---")
        row = df.iloc[0].to_dict()
        for k, v in row.items():
            s = repr(v)
            print(f"  {k}: {s[:400]}{'...' if len(s) > 400 else ''}")
        # key uniqueness
        for cand in ("question_id", "id"):
            if cand in df.columns:
                print(f"--- {cand}: n={len(df)} unique={df[cand].nunique()} dup={len(df) - df[cand].nunique()}")
        print()


if __name__ == "__main__":
    main()
