---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-31/review-1
kind: review
batch: batch-31
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/45
head: 7d9b4be97749e404d26ec87c8b9c0301040b4227
range: c7fccc747b0cc1e8e2ac9348080ea9806dbd00cf..7d9b4be97749e404d26ec87c8b9c0301040b4227
result: clean
---

# batch-31 review 1

## Verdict

The batch builds every requirement line of its four items: b220 (readiness#r17-r19), b221 (design-model-check#r164, r165; feature-file-tools#r29, r30), b222 (design-model-check#r166, r167; feature-file-tools#r31) and b216 (design-model-check#r168-r170; feature-file-tools#r32). The two test edits do not weaken anything. In `test_spec_steps4.py`, the line that stands for a group no step words was "print every stage" and is now "print at least two stages", because "every" now gets Thens; the same group is still checked as skipped. The module map has rows for the new modules (`backlog_universal.py`, `spec_lf_set.py`, `readiness_handlers_universal.py`). The size is 962 changed lines, under the limit. Every run that exits other than 0 at `Head:` did so at the base too (`model decisions --check`, 1 at both). Nothing needs fixing before the merge. There are two observations.

## Findings

### f1 Minor observation: the second copy of an `every` box's acts uses the wrong number to look up entailment
- item: b221
- where: scripts/spec_steps4.py:242
`Reader.each` marks the second copy's acts `"again"`. `read` then does `number += act is True`, so `number` stays at the last act of the first copy. Then it tests `act and number in gone`, and `"again"` is truthy. With an `every` scope of two or more acts, the second copy's acts are all looked up under the last act's number. The `each` docstring says they are "numbered as the first's", but they are not. An entailed first act is written out again in the second copy. If the last act is entailed, every act of the second copy becomes a comment naming that act's premise.
Reproduction (read, not run): take a line like "`work` shall print the worktree of every session and exit successfully" in a context where a universal condition entails only the print. The second session's print is written as a Then, not as `# entailed:`. No line of the batch names entailment inside an `every` box, so this does not hold the merge. Fix: give each copy's acts their own numbers (1..k), as the first copy has.

### f2 Minor observation: "the K of X" never binds to an earlier "a K of X"
- item: b221
- where: scripts/spec_lf_np.py:138
`det` now reads every `DetThe` over a `K | of | S` modifier through `of`, which calls `st.image((row, x.ref), K)`. An earlier "a stage of the worktree" is read by `restricting` as a `rel` atom and is never put in `st.images`. So in "When a session ends a stage of a worktree, `work` shall print the stage of the worktree.", the stage printed is a new referent, not the trigger's stage. Before this change, R2 bound it to the trigger's stage.
- **What it affects:** `model logic` may still unify the two through `fun/1` when the row is `one`. But `features generate` would bring in a second stage s3 with "the worktree w1 has the stage s3" and print s3, not s2.
- **Why it is only an observation:** `grammar/language.md` now says "never an earlier K", which is the batch's stated reading, and no line of the batch names this case. The risk is the wrong anaphora in existing codified-2 lines.
- **What I checked:** `spec_lf_core.State.image` and `spec_lf_np.restricting` (the `Mod` branch only emits the `rel` atom).
- **Fix to consider later:** have `restricting` record the image of a `one` row in `st.images`, so a later "the K of X" binds to it.
