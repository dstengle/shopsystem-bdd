---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i45-spec-consistency
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i45
status: approved
argues: [spec-consistency]
date: 2026-10-28
adds: [spec-consistency#r28]
changes: []
removes: [spec-consistency#r5]
---

# spec-consistency

The drafts of this proposal are in .shop/work/i45/runs/i45/1-integrate/drafts/round-1/.

## Questions
- Decision on spec-consistency r5 and r28 (request q26, line 7: a changed line is retired and its replacement given a new id). r5 says: "**Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, ids kept, through one gate pass for the term." It says the opposite of line 7 (ids kept). Readings: A (recommended, drafted): retire r5 (it goes to `retired`) and add r28: "**Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, each changed line retired and its replacement given a new id, through one gate pass for the term." B: leave r5 as it is and add no r28; the spec then contradicts itself, since line 7's rule would hold for every line but the fix mode's. The answer with A also holds for the same decision on spec-integration r13 (retired) and r53 (added), which that proposal's gate asks.

## Answers
- 2026-10-28: Decision on r5 and r28: reading A, retire r5 and add r28 (answered by the person, 2026-10-28)
