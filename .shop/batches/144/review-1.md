---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-144/review-1
kind: review
batch: batch-144
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/167
head: 16b12cafa8dee60a5e3205a4948e0c48c098e67e
range: 6f1d1ab432633d558ec3ebb3cb94d826dc2ed967..16b12cafa8dee60a5e3205a4948e0c48c098e67e
result: clean
---

# batch-144 review 1

## Verdict

The batch builds b746's fourteen laying lines, r28 to r41. Each one has a generated scenario that drives `laying.lay` through the new laying_handlers_model handlers, and `laying.md` keeps `unbuilt: []`. The fourteen batches lines the item retires (r79, r80, r87, r92, r116, r117, r118, r120, r121, r126, r127, r133, r134, r142) are out of `batches.md`, its feature, the corpus and `cli.toml`'s annotations, and they are listed under `retired:`. Their handlers moved over with assertions at least as strong as before.

The batches scenarios still live (g91, g119) still have handlers. g119's "an element e1" is taken by world_fallbacks' `INTRODUCED`, and its "does not hold" Then by batches_handlers_added. No file goes over 300 lines, the module map gained rows for the two new modules and lost the rows of the deleted ones, and every run exited 0 as it did at the base. No `fix now` findings; three observations.

## Findings

### f1 Minor observation: the change is over the review limit
- item: b746
- where: -
`## Size` gives 21 files, +771 -1335, against a limit of 1000 changed lines. Nearly all of it is b746 moving the fourteen batches scenarios, corpus blocks and handlers to laying: 1335 lines deleted from batches' feature, corpus and handlers, and their counterparts added under laying. The item's note estimated about 650 changed lines, counting the move only once. This does not hold the merge.

### f2 Minor observation: g31 and g38 do not exercise the renumbering their batches originals were written for
- item: b746
- where: tests/scenarios/laying_handlers_model.py:252
r31 and r38 replace batches r126 and r127. Those were about an item's operation table and moved term surviving the pick's renumbering when its ids collide with its capability's. `laying.lay` does not renumber, so in g31 and g38 the item's colliding `g1` and `r1` go into the lay as they are.

The Thens only read the adapter contract (g31) or notes' and shared's layers (g38), not the capability file. So the scenarios pass whatever the lay does with the duplicate `r1`, and the colliding-ids precondition is decorative here. The lines as written are still met: the contract holds the table and the area holds the term.

I checked this by reading `colliding` and `_tabled`/`_moved` against `laying_handlers_model_then.kept`. Nothing reads `spec/capabilities/` after the lay. If the renumbering guarantee is still wanted, it belongs to a pick scenario of batches.

### f3 Minor observation: one Then handler checks the whole group whatever its step says
- item: b746
- where: tests/scenarios/laying_handlers_model_then.py:411
`then` dispatches on the scenario's group tag alone. In g32 to g35, for example, all four Thens ("holds the model line", "keeps the model line", "keeps the domain model", "does not hold the operation") run the same `_restated` assertions. Each Then therefore checks every claim of its scenario rather than its own.

Nothing passes that should fail today, since every check runs on each step. But a Then added to one of these groups later would pass on its group's checks without being read. A dispatch on `(template, kinds)` within each group would make each Then check its own claim.
