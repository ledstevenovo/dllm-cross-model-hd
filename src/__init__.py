"""dllm-cross-model-hd: source package.

Modules
-------
``textnorm``   Text normalisation shared by deduplication and answer matching.
``prompts``    The single frozen no-context prompt template (one per experiment).
``schema``     Unified QA-record schema and validation.
``splitting``  Deterministic hash splits, collision clusters and subset carving.
``labeling``   Answer matching and the five-way output label protocol.

Only data-preparation concerns live here.  Model inference, trajectory
collection and detector training are added by later stages and must not import
from this package's internals.
"""

from __future__ import annotations

__all__ = ["labeling", "prompts", "schema", "splitting", "textnorm"]

__version__ = "0.1.0"
