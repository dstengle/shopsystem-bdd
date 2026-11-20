---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-57/review-1
kind: review
batch: batch-57
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/81
head: 240de64b57b52ac9828194661ee30675ef719270
range: 6f98f62d3d1d1beadc9ac6da7f0d38423435f925..240de64b57b52ac9828194661ee30675ef719270
result: clean
---

# batch-57 review 1

## Verdict

Both items are built and I found nothing to fix now. b437's relative clauses are now built once per kind and attached per kind. Each reader of the old fun names has been updated, the construct catalogue's Functions and GLUE were regenerated, and no old name is left in `scripts/`, `grammar/` or `docs/`. Its check holds every live line to the logical form it had before, and the fixture for that comparison was committed in f54aba04b, before the factoring in 9a8785372. b441's guards read the generated Context.gf of this repository and of both construct-catalogue contexts, and the tests show each guard catching a generator that multiplies. Every commit stays within its chore's files. Every run exits 0 at `Head:` and at the base, and no `.feature` file changed. Three observations follow.

## Findings

### f1 Minor observation: the change is over the size limit
- item: b437
- where: tests/scripts/fixtures/grammar4-factored/forms.json:1
The range changes 12 files, +2000 -68, against a limit of 1000 changed lines. b437's logical-form fixture is 1674 of those lines. It is generated data that its own check needs, so the code part of the change is well under the limit.

### f2 Minor observation: the parse-time budget may be tight when 32 workers run at once
- item: b441
- where: tests/scripts/test_grammar4_guards.py:204
`BUDGET = 10.0` seconds is about 6.7 times the 1.5 s the docstring measured for one process. The item asks for a budget "loose enough for 32 xdist workers (b436)". With 32 GF parses sharing the CPU, a slowdown past 6.7 times is plausible, and the test would then fail with no grammar change. Before the factoring the line set took 28.6 s, so a budget of about 20 s would still catch that regression and leave more headroom. This was not measured under load here.

### f3 Minor observation: the guards' tests pin counts of the construct catalogue's context
- item: b441
- where: tests/scripts/test_grammar4_guards.py:271
`test_the_guards_catch_a_fun_per_pair_of_values` asserts `"funs for 27 kinds, over 1080"`, and the senses test asserts `"79612 senses' funs for 27 kinds, over 400"`, which counts the catalogue's own 12. Adding a kind or an attribute sense to `grammar/corpus/constructs/` would break these tests even though no guard has failed. Asserting which guard fired, as `test_the_guards_catch_a_fun_per_gap_and_kind` does, would avoid this.
