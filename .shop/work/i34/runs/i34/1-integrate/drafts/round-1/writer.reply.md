/tmp/work-run-i34-_okpayqm/i34-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | supervision | r122 | **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes. | q11 line 1: "**When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes." |

No glossary terms added, changed or removed. No decision files.

## Questions

1. supervision, r4: r4 merges only if the whole suite passes "but for the failing scenarios r43 counts as expected", so it does not name the scenarios r122 counts. Should r4 name them too? Yes (recommended; without it r122 does not change whether a merge happens): "[r4] **When** an implementer's outcome is `DONE`, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r122 count as expected." No: r4 stays as it is.
2. supervision, r122 scope (two readings of "checks a work-item against the whole suite"): (a) only the whole-suite run before a merge (r4, r43): r122 as drafted, and Implementation gets "r122: the check is the whole-suite run before a merge (r43)"; (b) every whole-suite run for a work-item, including the run before an implementer starts (r24): r122 as drafted, and Implementation gets "r122: the checks are the whole-suite runs of r24 and r43". Recommended: (b), the reading that matches the line's wording.
3. supervision, r122: if a scenario that r122 counts as expected to fail passes, does the suite still pass? Yes (recommended): "[r123] **When** a scenario that r122 counts as expected to fail passes, `work run` shall count the whole suite as passing on that scenario." No: "[r123] **If** a scenario that r122 counts as expected to fail passes, **then** `work run` shall count the whole suite as failing, naming the scenario."
4. supervision, Implementation: the `--whole-suite` note says it "marks as xfail each scenario r43 counts as expected". I left it unchanged because r122 does not need it. Should it also name r122? Yes: "... marks as xfail each scenario r43 or r122 counts as expected ...". No: it stays as it is.

## Cut sentences

None. q11's title, "Scenarios of a proposal still at its gate do not fail other work-items", restates line 1 and is not a sentence to integrate.
