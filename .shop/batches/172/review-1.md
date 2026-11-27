---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-172/review-1
kind: review
batch: batch-172
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/194
head: ee82f9c53ec7e98d1f1012324e48718dc3b37114
range: ec38f4d268f96b1be5bf889a8f5c10152bb5fa40..ee82f9c53ec7e98d1f1012324e48718dc3b37114
result: clean
---

# batch-172 review 1

## Verdict

The batch builds all five lines of b871 (checking#r164-r168). It retires laying#r3, r4, r19 and r20 as the item says, and the scenario handlers it takes out are only those of the retired lines. All runs exit 0. Nothing has to be fixed before the merge. There are six observations: the change is over the size limit, the grammar guard's budget was raised, r168's refusal reply is only produced by a function the batch's real path never calls, and three hardening edges.

## Findings

### f1 Minor observation: the change is over the review size limit
- item: b871
- where: -
`## Size` gives 27 files, +834 -449, which is 1283 changed lines against a limit of 1000. All of it is b871's. Most of it is moving `laying_inprocess`'s lay, prepare and check into the new `scripts/spec_apply.py` and `scripts/spec_apply_check.py`, plus the two new scenario handler modules. The item's estimate was about 700 lines.

### f2 Minor observation: the grammar guard's fun budget per kind was raised from 40 to 41
- item: b871
- where: tests/scripts/test_grammar4_guards.py:51
This loosens an assertion: `FUNS_PER_KIND = 40` became `41`. I checked the stated reason. The commit gives 11394 funs for 284 kinds, which is 40.1 a kind, and the vocabulary grew by one verb with a two-slot frame (`apply`) plus two relation rows. That is linear growth, not a generator that multiplies, and this guard exists to catch the second kind. So it is recorded here and not sent back. Each raise like this leaves less room before the guard misses a real blow-up. A later item could measure funs per verb rather than per kind.

### f3 Minor observation: r168's refused reply exists only in `spec_apply.apply`, which no production path calls
- item: b871
- where: scripts/spec_apply.py:60
r168 names the batches service as the actor. The batches service reaches the specification through `laying_inprocess.lay` and `prepared`, which call `spec_apply.lay` and `spec_apply.prepare`, never `spec_apply.apply`. On that path an unresponsive generator raises `Refused("<command>: features generate failed: ...")`. It does not return the `refused` Response that names `feature generator:<program>`, and it does not run `_put_back`. The module map says `apply` is "read by laying_inprocess, the readiness bar and spec_preview", but those three read `lay` only. The scenario (`checking_handlers_apply.py`) calls `spec_apply.apply` directly. So the reply the line describes is tested only on a function the batch never uses.

This is not a wrong answer: the batch's path still refuses and names the generator in its message, and batch_start removes the worktree on failure. The refusal message there also no longer names the capability, as `_generated`'s still does. A cheap fix is to have `laying_inprocess` lay and prepare through `apply` and turn its refused reply into the laying refusal.

### f4 Minor observation: `_put_back` leaves a file that was already changed before the apply
- item: b871
- where: scripts/spec_apply.py:890
`_put_back` restores only paths in `_dirty(after) - _dirty(before)`. A file that was already changed or untracked before the apply, and that the apply then changes again (a capability file, `spec/index.md`), keeps the apply's writes after a refusal. Parsing `entry[3:]` of `--porcelain -z` also misreads renames, whose source comes as a separate NUL field. Today the only caller of `apply` is the scenario, which starts from a clean tree, so no client hits this.

### f5 Minor observation: `spec check --item` hides an item's own violation when its ids collide with the capability's
- item: b871
- where: scripts/spec_apply_check.py:1079
`brought` drops every finding whose `(code, args)` the root also has. `spec_preview.laid` lays the item with its ids as written; unlike the readiness bar and the pick, it does not renumber them (b648). If an item's `notebook#r5` collides with a live `notebook#r5` that the root already violates, the item's own violation of the same rule matches and is dropped. In that case r167's filter also swallows a finding that r164 needs reported. To reproduce: an item whose line takes a live, already-violating id of its capability, run with `spec check --item`. The fix is to renumber the item in `laid`, as `backlog_moves` does for the bar.

### f6 Minor observation: laying.check no longer has any port line
- item: b871
- where: spec/capabilities/laying.md:9
With laying#r3, r4, r19 and r20 retired, the operation `laying.check`, which batches#r180 and r189 still rely on through the batches service, has no port line left in laying. Its replacements, checking#r164-r166, are triggered by the person validating with an item, not by the batches service's request to the laying port. Decision 0116 says a port holds only what core lines use, and each port line names the core lines that rely on it. The batches service's reliance on a failed check that names the rule is now stated only in batches' own lines. The item asks for this, so it is recorded only. A later item could either move `check` off the port or restate one port line for it.
