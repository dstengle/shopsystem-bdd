---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-answer-to-a-reviewer-returns-to-ready-or-done
summary: "An answer to a reviewer's question on a work-item takes the work-item from `awaiting-answer` to `ready` when it asks for a change and to `done` when it accepts the work-item as it is, replacing decision 0063's row for a reviewer's question."
date: 2026-10-25
status: accepted
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-ruling-returns-to-the-asking-stage]
source: [request/missingmass.io/shopsystem/shopsystem-bdd/q9, observation/2026-10-25-apply-ids-and-fix-work-items, design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-ruling-returns-to-the-asking-stage, design-decision/missingmass.io/shopsystem/shopsystem-bdd/answers-not-rulings]
by: "the person's delegation of 2026-10-25 (\"Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release\"), answering every question with its recommended reading, via request q9"
---

# 0069. An answer to a reviewer returns to ready or done

## Decision

This replaces one row of decision 0063, "awaiting-ruling → done | the person, `work rule` | the question was a
reviewer's" (read with decision 0064's names); the rest of 0063 stands.

| from → to | made by | guard |
|---|---|---|
| awaiting-answer → ready | the person, `work answer` with the flag that the answer asks for a change; `work run`, for an answer a session gave under a delegation | the question was a reviewer's and the answer asks for a change |
| awaiting-answer → done | the person, `work answer` with the flag that the answer accepts the work-item as it is; `work run`, for an answer a session gave under a delegation | the question was a reviewer's and the answer accepts the work-item as it is |
