## Coverage

| id | line | scenario |
|---|---|---|
| r122 | "**When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes." | Scenario Outline: when the whole suite is run <run>, a failing scenario whose requirement a capability-proposal that is <status> adds or changes is counted as <counted> |

Every other line is already formulated in features/supervision.feature and was left as it is. The outline goes directly after the @r43 outline. Its Examples cover both whole-suite runs from the ruling: the one in the implementer's worktree before the implementer starts (r24) and the one before w1's merge (r43). The rows cover every capability-proposal status, adds and changes, and a proposal that does not name the scenario's requirement. The Given and Then steps follow the r24 and r43 wording and the existing "i1's capability-proposal p1 is <status>, its adds/changes naming ..." steps.

## Questions

None. The ruling settled which runs the line covers.

## Cases no line mentions

- A `merged` capability-proposal is "neither `formulated` nor `withdrawn`", so the line as written counts its requirements' failing scenarios as expected. The outline pins this (a row for `merged`). If that was not intended, the line needs `merged` added to its exclusions.
- Capability-proposals of other initiatives: the line says "a capability-proposal" with no initiative named. The outline uses only i1's own proposal.
- A scenario counted as expected to fail that passes: the line does not say what happens.
- A requirement that a capability-proposal names and that a work-item also accepts (where r122 and r43 overlap): the line does not say whether this changes anything.

## Drafts

- /tmp/work-run-i34-m7mb7b1k/supervision-4-formulate/.shop/scratch/4-formulate/drafts/round-1/supervision.feature
