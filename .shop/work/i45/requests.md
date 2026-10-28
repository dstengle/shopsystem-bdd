---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i45-requests
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i45
status: awaiting-answer
argues: [requests]
adds: [requests#r46]
changes: []
removes: []
date: 2026-10-28
---

# requests

The drafts of this proposal are in .shop/work/i45/runs/i45/1-integrate/drafts/round-1/.

## Questions
- Q1 (requests r46): What does `work request` check for "an implementation detail or a term the glossary does not define"? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended, drafted): a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in a Behaviour line under `spec/capabilities/` (r46 as above). B (stricter): any word that is not a glossary term: "**If** a line given to `work request` names an implementation detail or uses a word that is not a glossary term, **then** `work request` shall refuse the line, naming the word and why it is refused." (nearly every line refused unless ordinary words are exempt). C: implementation details only: "**If** a line given to `work request` names an implementation detail, **then** `work request` shall refuse the line, naming the word and why it is refused." Recommended: A.
- Q7 (requests r46): Which glossary does `work request` use, since it runs in the asker's repository with no checkout of the upstream's? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended): the upstream's glossary and `spec/capabilities/`: "...a word that is neither a term of the upstream's glossary nor a word of a Behaviour line under the upstream's `spec/capabilities/`..." (replaces r46's wording). B: the glossary and `spec/capabilities/` of the repository it runs in (r46 as drafted). Recommended: A.
- Q12 (requests r46): Does "refuse the line" refuse the whole request? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended): yes, as r2: "..., **then** `work request` shall refuse, naming the word and why it is refused, and change nothing." (replaces r46's ending). B: only the line; the other lines are written: r46 as drafted, plus "**When** `work request` refuses a line, `work` shall write the request with its other lines." Recommended: A.

## Answers
- 2026-10-28: Q1, r46's check: reading A, a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in a Behaviour line (answered by the person, 2026-10-28)
- 2026-10-28: Q7, r46's glossary: reading A, the upstream's glossary and spec/capabilities/ (answered by the person, 2026-10-28)
- 2026-10-28: Q12, r46 refusing a line: reading A, it refuses the whole request and changes nothing, as r2 (answered by the person, 2026-10-28)
