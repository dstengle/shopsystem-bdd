---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-145/review-1
kind: review
batch: batch-145
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/168
head: 330f518dcfba58fdd92b6cad2adacabdf5804322
range: e66ea86c1d8a8369563c0878830b6fab769b63b0..330f518dcfba58fdd92b6cad2adacabdf5804322
result: clean
---

# batch-145 review 1

## Verdict

The batch builds b747's five lines. `batch_amend.relay` already lifted and laid through `laying`, so b747's whole change is spec, corpus, contract annotations and scenario handlers. The scenario handlers for the retired park and amend lines were moved into laying's lift scenarios. No finding needs fixing now; there are two observations.

## Findings

### f1 Minor observation: g42's world contradicts its own Given that the item holds no capability of `registry`
- item: b747
- where: tests/scenarios/laying_handlers_lift.py:1227
laying#r42 is stated for an item that "holds no capability that the `registry` area holds". In g42's world, i1 holds the `registry-recording` capability of `registry`. `given` records nothing for "the item i1 holds no capability in the `registry` area", the world lays i1 with that capability, and the scenario then lifts the same item. So the scenario passes in a state the line does not describe.

Its Then also asserts more than the line asks. The line says only "keep the `registry` area", and the handler asserts that `registry` imports nothing:

```
assert _imports(step, "registry") == [], _imports(step, "registry")
```

The retired batches#r156 handler did match its Given. It took the line out of the item on main before `work batch amend`, so at the amend the item held no `registry` capability. That match was lost in the move.

A faithful world for r42 as written would lift an item with no `registry` capability while `registry` imports `tracking`, and would check only that `registry` is kept. That test passes trivially, which shows the line does not state what r156 meant ("takes out the imports … its lines no longer need"). A later item should reword r42 so the line states that the import is taken out, and say which item, as laid or as it now reads, holds no capability. It does not hold this merge.

### f2 Minor observation: the change is over the review size limit
- item: b747
- where: -
`## Size` gives 13 files, +466 -656, which is 1122 changed lines against a limit of 1000. All of it is b747's, the only item. Most of it is removals: `batches_handlers_added.py`, `batches_handlers_imports.py` and `batches_handlers_restate.py` deleted, and six retired groups taken out of `batches.md`, the feature and the corpus. They are moved into the new `laying_handlers_lift.py` and laying's four groups.
