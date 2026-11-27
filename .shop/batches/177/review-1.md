---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-177/review-1
kind: review
batch: batch-177
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/199
head: 04686d6ee59928ff9fd6ab4bbff97a09599a2b64
range: 7b7a996ba421ed9d867f4fffa6f6e38dfe7c805d..04686d6ee59928ff9fd6ab4bbff97a09599a2b64
result: clean
---

# batch-177 review 1

## Verdict

The batch builds all eleven lines of b873, and I found nothing to fix now. applying#r37 to r47 are written into the capability, the corpus and the generated feature. laying#r6 and r9 to r18 are retired, and applying#r1 is retired in favour of r37. The scenarios now run through `spec_apply.apply`, whose `prepare` (scripts/spec_apply.py:67-101) already writes what the lines name: the features, the corpus, the decision successors, the reached features, the Composition, the annotations and the catalogues. The handlers moved without losing an assertion: g37's scenario check now also requires the feature to be among the apply's changed paths, which is stricter than before. `features generate --check`, `bindings --unbound`, `tools check`, `size` and `spec decisions --check` all exit 0 at the head and at the base. There are three observations.

## Findings

### f1 Minor observation: the change is over the review size limit
- item: b873
- where: -
`## Size` gives 11 files, +462 -564, which is 1026 changed lines against a limit of 1000. All of it is b873, the batch's only item. Most of it is the eleven laying lines with their corpus blocks and scenarios being deleted and restated in applying (grammar/corpus/spec/laying.md -204, features/laying.feature -157, grammar/corpus/spec/applying.md +193, features/applying.feature +137). The item's own note put it at about 500 lines. A move of this kind deletes and adds the same lines, so it counts twice.

### f2 Minor observation: laying.prepare is left in the port with no laying line describing it
- item: b873
- where: spec/vocabulary/laying.md:14
With laying#r6 and r9 to r18 retired, no laying line covers the `prepare` operation any more. That operation is the vocabulary entry `prepare` → `laying.prepare` and `laying.prepare` in scripts/laying.py:43. Yet batches#r188 (spec/capabilities/batches.md:212) still has the batches service prepare the workspace, and scripts/batch_start.py:65 and scripts/batch_amend.py:129 still call it. Decision 0116 says each port line names the core lines that rely on it, and for this operation there is now no such line. I checked whether a later item closes the gap: b874's notes retire or replace batches#r188 and r189. So this is a temporary state across b861's split, not something b873 should fix. The next item should also take out the `laying.prepare` operation and verb, not only batches#r188.

### f3 Minor observation: the brief's runs include no scenario test run
- item: -
- where: tests/scenarios/applying_handlers_prepare.py:95
`## Runs` gives no pytest run of features/applying.feature or features/laying.feature, so nothing here shows that g37 to g47 pass against `spec_apply.apply`. I checked two risks by reading the code:
- `applied` (tests/scenarios/applying_handlers.py:77-90) calls `R().codify` before each world function, and each world function calls it again. That is harmless, because `codify` returns at once when the scenario context is already marked `codified` (tests/scenarios/readiness_world.py:111).
- The g39 and g46/g47 worlds now return their `## Requirements` block for `applied` to write, where before they wrote it themselves with `B.write_item`. The effect on the item is the same.

`applied` also calls `backlog_lines.renumber` before the apply, which the old laying prepare path did not. The handlers read the ids from the item (`_line`), except g37, which uses `ID = "r5"` the same way applying's old g1 handler did. Whether these scenarios pass is still only shown by a run the brief does not give.
