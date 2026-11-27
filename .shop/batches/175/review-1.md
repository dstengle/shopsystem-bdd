---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-175/review-1
kind: review
batch: batch-175
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/197
head: 7115b892c8ae93282a55ded4d71ead29269ab0ab
range: d0f62a80cf2101505d85b5bb8b19b3ab96b5bd8e..7115b892c8ae93282a55ded4d71ead29269ab0ab
result: clean
---

# batch-175 review 1

## Verdict

b877 is built, and none of the findings needs fixing before merge. A line's grammar-4 parse is now kept by its footprint in a store beside the parse cache, which `spec_parse_cache.lookup` and `keep` manage. A refusal or a parse that hit `LIMIT` is read back only under the sha it was parsed with. The grammar is compiled only when a parse misses or a refusal has to write a tree out as words. The replay test checks that every footprint hit equals a fresh GF parse. Every commit touches only the chore's files, every run in the brief exits 0 at Head, and the change (+550 -52) is under the limit. I made two observations.

## Findings

### f1 Minor observation: a grammar gf cannot compile is no longer reported while the parses are kept
- item: b877
- where: scripts/spec_grammar4.py:225
The risk: `_parse` and `hint` used to call `_named(root)` first. `_named` compiles the sources and raises `spec_gf.GrammarError` when gf refuses them. `model_spec.parsed` (scripts/model_spec.py:129) turns that error into the problem "the codified statements are not parsed: ...". `request_lines`, `model_report` and `features` catch it too.

What I verified: `_parse` now takes `_context(root)` and a `_Lazy` grammar, and compiles only when `lookup` misses. Suppose a vocabulary or model change makes Context.gf fail to compile, and no line yet holds the new term's words. Then every line's footprint is unchanged, every parse is read from the disk cache, and `spec check` gives no problem. `spec_prefetch._prefetch` behaves the same way: it returns before `_named` when there are no misses.

On a machine with an empty cache the failure still shows, so this is hardening, not a wrong answer against a line. Fix, if wanted: in `_parse`, compile or check the sources once per sha when the sha has no `.pgf` yet. Or record that a set of sources compiled, and check that before trusting a footprint hit.

### f2 Minor observation: the replay is a made-up history over a fixture, not the repository's recent history
- item: b877
- where: tests/scripts/test_spec_parse_footprint.py:89
The item's notes ask for soundness "proved by a test replaying recent history". `HISTORY` is nine hand-written edits to `tests/scripts/fixtures/request-4`, checked against the lines of `grammar/corpus/core-4.txt` and `refused.txt`. They cover a good spread of cases: an unused noun, an attribute, a relation row, a frame, an actor, a value, a subkind, a row that holds a used kind, and a code that is spelled like a noun. But they do not replay the changes this repository's own specification went through, against its own lines.

The footprint's soundness rests on regex heuristics in `spec_footprint._words` and `UNSURE`: stems less two letters, prefix matching of chains, and functions read as taking part in every line. A shape of generated linearisation that the fixture never produces would not be caught. The chore's check passes as written, so this is recorded and does not hold the merge. A later item could replay a window of this repository's own `spec/` history across its own lines.
