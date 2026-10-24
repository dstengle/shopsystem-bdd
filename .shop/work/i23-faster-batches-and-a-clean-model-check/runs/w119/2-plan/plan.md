# Plan of w119: blocked_by read across initiatives (supervision#r63)

## 1. What goes green

supervision#r63, two scenarios in features/supervision.feature:
- "no worker is started for a work-item whose blocked_by names a work-item that is not green" (line 665). It passes today (notes §1, run) and has to stay green.
- "a worker is started for a work-item whose blocked_by names a green work-item of another initiative" (line 673). Red today in two ways:
  - Steps: its first Given, "i1's work-item w1 is drafted, its blocked_by naming w2", has no definition. The existing `blocked_item` step only matches the form with a second work-item in i1. The notes found by reading that "an initiative i2 under .shop/work/ whose work-item w2 is green" (defined only in test_work_queue.py, which test_supervision.py does not import) and "a worker was started for w1" are not defined either.
  - Code: `Pool.choose` builds its status map from `Run.items`, which holds this initiative's work-items only. The blocker w2 in i2 is never found, so `Pool.blocked` holds w1 back. Probe A1 confirms it: `w1 drafted`, exit 1, no worker started.

The work-item retires no deprecated scenario.

## 2. Where the change lands

- scripts/supervise_pool.py: `Pool.choose` looks up blockers in a status map of every initiative under `.shop/work/`, laid out as decision D1 says. The work-items `choose` loops over to pick what moves stay this initiative's. `Pool.blocked` itself does not change.
- tests/scenarios/supervision_parallel_steps.py: three new steps, the scenario's three undefined ones. One Given writes i1's w1 as drafted with blocked_by naming one work-item and writes no second work-item in i1. One Given writes another initiative with one work-item at a given status, committed the way the other initiative Givens of the supervision steps commit theirs. One Then checks that some worker was started for the named work-item: the positive of the existing "no worker was started for" step.

This is the researcher's file set, unchanged. Read but not edited: scripts/supervise.py (`Run.items` stays this initiative's, because `check` and `run` read it; notes §3), scripts/workqueue.py (its `items` already reads every initiative; D2 needs no `agrees` call, so it is not edited). Size: both edited files have room (141 and 125 lines).

## 3. Decisions

- D1. **The status map that `Pool.choose` checks blockers against is built from every initiative's work-items, with the work-item's own initiative taking precedence for a name more than one initiative holds.** The cross-initiative reading is what r63's scenario at line 673 pins (supervision#r63). Work-item names are unique across initiatives from 0.24.0 on (work-queue#r12 numbers ids above any initiative's highest, and migration-tools#r26 gives every legacy work-item a `w<n>` id). Where a legacy name is still held by several initiatives, migration-tools#r26 already reads that name as the naming work-item's own initiative's, and this decision uses the same reading. This settles the researcher's question 1 with reading (a). Reading (b), refusing as ambiguous, is not taken.
- D2. **A blocker's status is the one its file gives. It is read without `workqueue.agrees`.** r63 asks whether the named work-item "is not `green`" (supervision#r63). Where status is defined, a work-item's status is the one its file gives: work-queue#r3's `work show` prints the file status, and so does `workqueue.items`. The check against log.jsonl is a guard on transitions (work-queue#r6, "shall refuse the transition"), and `work run i1` makes no transition of a blocker. A file with no status (probe B2) is not `green`, so its work-item stays blocked. This settles the researcher's question 2 with reading (b).
- D3. **The new steps live in supervision_parallel_steps.py.** The scenario's other `@r63` steps live there, and test_supervision.py's star imports pick them up (notes §7).

## 4. Tests the decisions break

None. The notes searched every test that names blocked_by (§4) and found none that asserts a blocker in another initiative holds its work-item back. The i2 scenarios in test_supervision.py write only an `initiative.md`, which `workqueue.items` skips. Every other `work run` scenario has one initiative, so for them the map of all initiatives is the same as today's map. D1's precedence rule changes nothing where names are unique. S1 still holds, because its w2 is in i1 and is awaiting-answer.

## 5. Open cases (for the implementer to name, not to choose)

- Which checkout's copy of another initiative is read: `.shop/work/` as the run reads it. If i2's `green` is committed only on i2's own branch and not where i1's run reads, the scenarios do not cover that case.
- A blocker named by id form (`work-item/w2`, probe A5) still blocks. Neither scenario covers it.
- A blocker that is absent everywhere (probe A4, notes defect D1) blocks with nothing printed to say why. r63 does not ask for a reason.
- A blocker in another initiative whose file and log.jsonl disagree (probe B1) counts by its file under D2. `work run i2` would refuse that same file.
