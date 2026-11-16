---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-40/review-1
kind: review
batch: batch-40
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/62
head: 2444b124f00bda89dba1a505d240c9f15c095f7b
range: 84124871f4fefdbb020f5f65dfa158be2b2ba294..2444b124f00bda89dba1a505d240c9f15c095f7b
result: clean
---

# batch-40 review 1

## Verdict

The batch builds all three items' lines: b179's `work decision --supersedes` (r31, r32), b271's `work line --no-line --retires` (r47, r48) and b300's order after "every K" of any act (r317, r130). No test was removed or weakened, and every changed `.feature` file is what `features generate` writes (`--check` exits 0). No file is over the size limit and the change is within its line limit. The new modules and behaviours have module-map rows. Nothing has to be fixed before the merge; there are four observations.

## Findings

### f1 Minor observation: a park left a stray change in spec/capabilities/conversation.md
- item: -
- where: spec/capabilities/conversation.md:27
Commit efe9cc4de took parked b20's lines back out. It also deleted the blank line between `## Relations` and its table, so the file is not byte-for-byte as the base had it. That blank line is the only net change the range makes to conversation.md, and no item of this batch asks for it. I read efe9cc4de.patch and change.diff to confirm this. The text is harmless, but it points to a flaw in the park tooling: `batch_parked.take_out` (or the unlay it uses) does not give back exactly the bytes it removed. A test of that is worth adding. Repair: put the blank line back on the batch branch, or leave it to a later item.

### f2 Minor observation: `model decisions --check` still fails on 0086-0088
- item: b179
- where: spec/decisions/0086-u4-is-checked-after-every-scenario.md:1
The run exits 1 at Head and also exited 1 at base. It fails on 0086, 0087 and 0088 (`tests/scenarios/vocab.py: exit 5`), so the failure is not this batch's. b179's notes plan three runs of `work decision --supersedes` on main after the merge, because `work` refuses to commit on a task branch. That plan depends on the new option and on the U4 test this batch adds (`test_the_u4_check_after_a_scenario`). b179 is not finished until those runs happen and `model decisions --check` exits 0 on main. This is recorded so it is not forgotten.

### f3 Minor observation: no test of an item whose only piece is a retired id
- item: b271
- where: scripts/readiness_bar.py:104
`well_formed` now lets an item that has no requirement line through, as long as it retires one (`not mine and not any(b.retired for b in blocks)`). No test checks this:
- The r47 scenario gives the item `R.PASSING` before running `--no-line` (readiness_handlers_line.py:99), so the item still has a line.
- tests/scripts/test_readiness_bar.py is not changed.

As a result, an item made only with `work line --no-line --retires` is never run through `work ready`, `work batch start`'s lay, or `work batch done`'s "its ids are built". Reproduction: `work idea`, then `work line b<n> --no-line --retires readiness#r4`, `work shape`, `work ready`. Nothing tested shows that the bar passes, or that the laid spec drops r4 and its scenario. Fix: add a readiness_bar test of such an item.

### f4 Minor observation: the ambiguity check b300's shaping asked for has no test
- item: b300
- where: scripts/spec_rgl_np.py:162
b300's notes asked the implementer to check that "every worktree, ordered by version" does not now read two ways beside `r<n>_in_By_<T>`. The old docstring of `orders` gave that risk as the reason `<T>_<K>_Every` was limited to `thing`. `<T>_<K>_Every` is now a `K_NP0` for every kind, while `r<n>_in_By_<T>` takes the same `K2_NP0`. When K and its members both carry the attribute T, these two functions are two candidate readings of one string.

The corpus and construct runs pass, so no live line reads two ways today. But no test or corpus line has a K that holds members sharing its attribute, so the check was not recorded. Fix: add a corpus or `test_spec_lf_read` case with such a K. It should show one meaning, or a refusal that names the words that read two ways.
