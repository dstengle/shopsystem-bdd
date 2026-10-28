# Gate, i47 integrate round 3 (request q33, supervision)

## supervision

Added:
- [r188] **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. (after r122; source: q33 line 1)
- [r189] **When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output. (after r132; source: q33 line 2)
- [r190] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r188 count as expected. (in r4's place; source: answer Q1, 2026-10-28, "r4 changes (retired, new id)")

Removed (id retired):
- [r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 counts as expected. (replaced by r190)

Implementation, may change, added (source: answer Q2, 2026-10-28):
- r188: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail.

## glossary

No entry added, changed or removed.

## decisions

None.

## Questions

1. supervision r61 says "the work-item branches that r4 merges"; r4 is now retired.
   - Reading A (recommended): retire r61 and add [r191] **When** implementers working at the same time end, `work run` shall merge the work-item branches that r190 merges into the initiative branch one at a time, in the order the implementers ended.
   - Reading B: r61 stays, pointing to a retired id.
2. supervision, Implementation: the `--whole-suite` line says it "marks as xfail each scenario r43 counts as expected".
   - Reading A (recommended): change it to "each scenario r43, r122 and r188 count as expected".
   - Reading B: leave it; the r188 line covers r188.
3. requests line 3 is drafted by the requests proposal, not here. The Implementation note in red-green.md, "supervision r4", names a retired id.
   - Reading A: leave it (an Implementation note, outside this proposal). Reading B (recommended): name r190 in a later change to red-green.

## Cut sentences

- q33 line 3 (requests capability).
