# Label protocol v2 (conservative preliminary labels)

The matcher is a screening rule, not complete response-level factual verification. `correct` is an exact/alias/numeric/yes-no short-answer match proposal. Unmatched outputs are `needs_review`, never automatically factual-error positives. Human-reviewed `incorrect` is the only positive class. All rules and human overrides must retain source, reviewer status and original output.

Blank text: refusal_empty. Non-text: format_failure. Explicit refusal: refusal_empty. Question echo: format_failure. Nonmatching output at the length budget: incomplete_truncated. Matching output that is truncated, has additional lines, or includes refusal language: needs_review. Other unmatched text: needs_review. Audit even matching short answers for additional false claims; a first-line match does not establish response factuality.

Number matching preserves sign, decimal point and thousands separators; no unit/percentage stripping. Non-numeric normalization uses NFKC, lowercase, punctuation replaced by spaces, articles removed and whitespace collapsed. This differs from official SQuAD punctuation deletion, and must not be described as identical to the published metric.

Primary evaluation excludes refusals, truncations, format failures and needs_review. Report exclusion counts and coverage by model/dataset. Never treat needs_review as a verified negative. Review a stratified batch of positive/negative proposals and all disputed boundary cases; preserve automatic proposal plus adjudicated label separately. No real generated answers have yet been labelled.
# 自动标签只作为提案；真实审核后的行应设置 human_reviewed=true，
# 并把 label_source 改为 human:<reviewer/run>，保留原自动提案供审计。
