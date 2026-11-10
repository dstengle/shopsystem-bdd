---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-28/review-1
kind: review
batch: batch-28
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/40
head: e4fffd5ee3e75b3e864b5821e3c35f9c4d738e17
range: da43811b33d17830af42b5a6e1b451da91955202..e4fffd5ee3e75b3e864b5821e3c35f9c4d738e17
result: fix-now
---

# batch-28 review 1

## Verdict

The batch builds all nine requirement lines. The scenarios exist for r136–r144, and every check passes at `Head:` as it did at the base. Three changes have observable behaviour that no line of the batch asks for and no Implementation section gives, so they go back for a fix:
- "the newest K" and "the oldest K" in grammar 4;
- `model logic` reading times exactly;
- `model logic` using a necessity as a premise.

The change is also over the size limit.

## Findings

### f1 Important fix now: "the newest K" and "the oldest K" are parsed, and no line asks for it
- item: b147
- where: scripts/spec_rgl_time.py:34
Every context's grammar now gets `K_Sup : Sup -> K_CN -> K_NP0`, backed by `Newest` and `Oldest` in `grammar/Time.gf`. `spec_lf_np` reads it into an `order(newest, x)` atom, and `spec_lf_facts.restrict` drops that atom without a word. So `model parse` now accepts "`work` shall print the newest stage", and `model logic` reads the line as if it said "a stage". None of b147's lines names newest or oldest. "timed" (r138) covers "after", "before", "since" and "within the last", and no Implementation section mentions an order. The words are only in the item's notes, and notes are not lines. The check also reads the line as something it does not say. Fix: take the `Sup` construct and the `order` atom out of this batch. Or, if the person wants them, put them on an item with a line that says what `model parse` and `model logic` do with them.

### f2 Important fix now: `model logic` now reads a comparison of moments and a history, and no line asks for it
- item: b147
- where: grammar/check.lp:191
b147's lines (r138–r141) cover only `model parse`. The batch also makes `model logic` handle time:
- `cmp/5` facts, and their `lo`/`hi`/`later` bounds, rule pairs out;
- a history becomes the state relation `hist(E)`, through `spec_lf_time.edge` and `spec_lf_facts`.

That changes which L1s `model logic` prints for timed lines. `tests/scripts/test_spec_lf_time.py::test_bounds_that_leave_no_moment_between_them_never_clash` and `test_bounds_that_leave_a_moment_between_them_clash` show the effect. No line of the batch asks for this reading, and the capability's Implementation section does not give it. Fix: either add a `model logic` line for timed capabilities on an item and build it there, or leave the time atoms with no check reading, so that `model logic` refuses them by name as it refuses other constructs it has no translation for.

### f3 Important fix now: a necessity becomes a premise of every pair in `model logic`, and no line asks for it
- item: b148
- where: grammar/check.lp:208
r143 asks only that `model parse` exit successfully on an invariant line. The batch goes further:
- `spec_lf_modal.necessity` emits `nec/5` and `necsub/2`;
- three new `out(A,B)` rules in `check.lp` use them to rule out pairs whose merged state the necessity forbids.

So an "always" or "never" line in a capability now hides L1s that `model logic` printed before. `tests/scripts/test_spec_modality.py::test_a_necessity_puts_out_a_pair_whose_state_it_rules_out` shows this: the L1 for `(pre + "print the stage.", pre + "not print the stage.")` disappears once "A session never follows a stage." is added. The behaviour appears only in b148's notes. Fix: either add a `model logic` line for a necessity on an item and build it there, or keep the necessity's facts out of the solve (no `out` rules on `nec`) in this batch.

### f4 Minor observation: "one K" alone is read as exactly one, and no line names it
- item: b146
- where: grammar/BaseEng.gf:211
`DetOne` makes "print one stage" a count `exactly 1`. That changes how a line saying "one K" reads in `model parse --form` and in `model logic`. "counted" (r136) lists "at least", "at most", "exactly", "more than" and "fewer than"; it does not list "one" alone. The item's notes and language.md's R7 ask for it, so this is recorded rather than held.

### f5 Minor observation: a count of zero is not compared with a plain obligation
- item: b146
- where: grammar/check.lp:326
A count is keyed only as `ev(cnt,E)` and only meets other counts. "`work` shall print fewer than one stage" therefore emits no `resp`, and it never clashes with "`work` shall print a stage" on the same trigger, though no number meets both. No line names this case. To reproduce: put the two lines in a codified-2 capability and run `model logic`; it prints no L1.

### f6 Minor observation: the module map's codified2_world row does not mention the time world
- item: -
- where: CLAUDE.md
The row for `tests/scenarios/codified2_world.py` still describes only the fixture `tests/scripts/fixtures/codified-2/` with `imports: [cli]`. The module now also writes `TIME_FIXTURE` (`codified-2-time`, `imports: [cli, time]`) for the conditions in `TIMED`, and gained `context(..., fixture=)`. The row should say so.

### f7 Minor observation: the change is over the size limit
- item: -
- where: -
31 files, +1163 −60, against a limit of 1000 changed lines. Most of it is b147: Time.gf and TimeEng.gf, spec_rgl_time.py, spec_lf_time.py, its test, the time corpus, the fixture, the time pack and the time section of language.md, about 550 lines. Next comes b148: spec_lf_modal.py, test_spec_modality.py, the modality rules in check.lp, and Base and BaseEng.
