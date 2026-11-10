---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-26/review-1
kind: review
batch: batch-26
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/38
head: 9e6446052e216db968c6c9c1e5b0c95aec1c160e
range: 5ac37c9abb1294b47d90c47a9c1e34c5eb332f42..9e6446052e216db968c6c9c1e5b0c95aec1c160e
result: clean
---

# batch-26 review 1

## Verdict

The batch builds all ten lines: r92-r94 (b136), r95-r96 (b138), r97-r99 (b139) and r100 (b137). Each has a generated scenario. Every run that exits other than 0 exited the same way at the base. Nothing needs fixing before the merge. There are four observations: the "the" binding, the change's size, the r58/r59/r63/r65 scenarios moving to the codified-2 world, and one dead method.

## Findings

### f1 Minor observation: R2 binds "the K" to a referent inside a `no` or `every` box
- item: b139
- where: scripts/spec_lf_read.py:36
`the()` takes the latest referent in `st.refs` whose origin is a part's. But `spec_lf_np.det` also makes the referent of "no K" and "every K" with its part's origin (`st.ref(kind)`, line 1308 of change.diff), so that referent is a candidate too. A "the K" after one of them binds to a referent that only exists inside a `not` or `every` box. It is neither refused under r97 nor bound to the row image R2 gives next. Reproduction, read off the code (the risk was this binding; I checked `det`, `State.ref` and `the`): `model parse --form` on `While a session has no worktree, when the person runs `work start`, `work` shall print the worktree.` gives `print(e2, subject: x5, object: x2)`, where x2 is the worktree under `not [x2: worktree]`. `When a session ends a stage, `work` shall print every file and exit with an error naming the file.` does the same with the `every` box. grammar/language.md's R2 says "the" binds to "something the line gave", and a `no` phrase gives nothing. No scenario uses this construct today. A fix would leave out referents whose NP quant is `no`, `every` or `only` once their box is closed.

### f2 Minor observation: the change is over the size limit
- item: -
- where: -
`## Size` gives 27 files, +1919 -48, against a limit of 1000 changed lines. Most of it is b138 (spec_lf.py, spec_lf_core.py, spec_lf_clause.py, spec_lf_np.py, spec_meaning.py and test_spec_lf.py, about 750 lines) and b139 (grammar/language.md at 319 lines, spec_lf_read.py and test_spec_lf_read.py, about 530 lines).

### f3 Minor observation: the r58/r59/r63/r65 scenarios no longer run in a codified-1 context
- item: b137
- where: tests/scenarios/design_model_check_handlers_conditions.py:112
`objectless`, `recipientless`, `mistyped` and `agentless` were taken out of `FRAMED` and now run in the codified-2 world (`codified2_world.LINES`). b137's notes ask for exactly that, so this is not a weakened test. But no scenario now exercises grammar 3's frame refusals, which every codified-1 context still gets from `model parse`. I checked what still covers them:
- grammar/corpus/core.txt:63-67 (objectless, recipientless, the passive);
- tests/scripts/test_spec_typed_verbs.py:43 (mistyped).

Nothing is lost today. It is recorded so that I19's switch does not lose that coverage.

### f4 Minor observation: `State.bound` is dead code
- item: b138
- where: scripts/spec_lf_core.py:98
Nothing calls `State.bound`: `spec_lf_read.the` replaced it, and its own docstring says so. The module-map row for `spec_lf` in CLAUDE.md still describes "the" as "bound to the latest referent of its kind, else marked definite", which is this unused method. Remove the method and reword the row to point to spec_lf_read's R2.
