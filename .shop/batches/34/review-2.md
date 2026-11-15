---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-34/review-2
kind: review
batch: batch-34
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/54
head: e5caa15aeea18c665f98f67a6850c4d3c079cb72
range: 37ea867598a7cacca05bffd12f8e41e291c22c26..e5caa15aeea18c665f98f67a6850c4d3c079cb72
result: clean
---

# batch-34 review 2

## Verdict

All three earlier findings are fixed, and the fix commits change nothing that is wrong. One observation about the `features generate --check` run.

## Findings

### f9 Minor observation: `features generate --check` runs the base checkout's scripts against the batch tree
- item: -
- where: -
The `## Runs` entry for `python3 /home/vscode/shopsystem-bdd/scripts/features generate --check` says `Exit code: 1 (base: 0)` and lists every feature file under `differs:`. The fixes in this range touch only `scripts/spec_solve.py`, `tests/scenarios/feature_file_tools_collections.py` and `tests/scripts/test_corpus_spec.py`, and none of these is read by `features generate`. The command path is the base checkout's `scripts/`, not the Tree's. So the run compares main's generator, which does not have b268's or b273's changes, against features that the batch's generator wrote. That would make every feature differ. It is the problem idea b279 already names, and it says nothing about the fix. I have not seen this run from the Tree's own scripts, because I have no shell. The person should run `python3 .shop/worktrees/batch-34/scripts/features generate --check` in the Tree before merging.

## Earlier findings
- f1: fixed
- f2: fixed
- f3: fixed
