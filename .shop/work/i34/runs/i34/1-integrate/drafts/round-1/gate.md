# Gate, i34 round 1

## supervision

Added:
- [r122] **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes.

Changed: none. Removed: none. Glossary: none. Decisions: none.

## Questions

1. r4 (supervision): r4 merges only if the whole suite passes "but for the failing scenarios r43 counts as expected", so it does not name r122's scenarios. Should r4 name them? Yes (recommended): "[r4] **When** an implementer's outcome is `DONE`, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r122 count as expected." (was: "... r43 counts as expected."). No: r4 stays.
2. r122 scope: (a) only the whole-suite run before a merge (r4, r43); Implementation gets "r122: the check is the whole-suite run before a merge (r43)". (b) every whole-suite run for a work-item, including the run before an implementer starts (r24); Implementation gets "r122: the checks are the whole-suite runs of r24 and r43". Recommended: (b).
3. If a scenario r122 counts as expected to fail passes: Yes, the suite still passes (recommended): "[r123] **When** a scenario that r122 counts as expected to fail passes, `work run` shall count the whole suite as passing on that scenario." No: "[r123] **If** a scenario that r122 counts as expected to fail passes, **then** `work run` shall count the whole suite as failing, naming the scenario."
4. Implementation note on `--whole-suite` ("marks as xfail each scenario r43 counts as expected"): also name r122? Yes: "... each scenario r43 or r122 counts as expected ...". No: unchanged.

Cut sentences: 1 (the request's title restates line 1).
