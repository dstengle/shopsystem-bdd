/tmp/work-run-i47-ee1m2t30/supervision-3-integrate/.shop/scratch/3-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | supervision | r188 | **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. (placed after r122) | q33 line 1: "**While** no work-item accepts a requirement that a scenario names, the whole-suite run of a work-item's branch shall count a failure of that scenario as expected." |
| added | supervision | r189 | **When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output. (placed after r132) | q33 line 2: "**When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output." |
| removed | supervision | r4 | **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 counts as expected. (r4 added to `retired`) | answer: "2026-10-28: Q1, r177 against r4: reading A, r4 changes (retired, new id) so a failure r177 counts as expected does not block the merge" |
| added | supervision | r190 | **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r188 count as expected. (in r4's place; replaces r4, retired, new id) | answer: "2026-10-28: Q1, r177 against r4: reading A, r4 changes (retired, new id) so a failure r177 counts as expected does not block the merge" (r177 read as r188) |

Implementation, may change (supervision), added after the r122 line:
- "r188: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail." Source: answer Q2: "r177 covers the whole-suite runs of r24 and r43" (r177 read as r188).

No glossary term added, changed or removed. No decision file.

## Questions

1. supervision r61: it says "the work-item branches that r4 merges", and r4 is now retired. Yes, refer to the replacement: [r61] stays, its text changed to "...the work-item branches that r190 merges..." (by the retire rule a changed line gets a new id: retire r61 and add [r191] with that text). No: leave r61 as it is, pointing to a retired id. I recommend yes. I did not draft it because the brief says to change nothing else.
2. supervision, Implementation: the `--whole-suite` line still says it "marks as xfail each scenario r43 counts as expected". With the new r188 line, should it read "each scenario r43, r122 and r188 count as expected"? If yes, change that line. If no, keep it as it is. The new r188 Implementation line already covers r188.

## Cut sentences

- q33 line 3: it is for the requests capability, not supervision. The brief says it is not mine.
