# Gate, i32 round 1

## supervision (frontmatter `rests_on` gains `design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done`)
Added:
- [supervision#r118] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that asks for a change, `work run` shall transition the work-item to `ready`.
- [supervision#r119] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that accepts the work-item as it is, `work run` shall transition the work-item to `done`.

## review
Added:
- [review#r31] **When** a branch review ends, the branch reviewer shall give in its result's questions only the findings it triages fix now.

## Glossary
No entry added, changed or removed.

## Decisions
- spec/decisions/0069-an-answer-to-a-reviewer-returns-to-ready-or-done.md — summary: An answer to a reviewer's question on a work-item takes the work-item from `awaiting-answer` to `ready` when it asks for a change and to `done` when it accepts the work-item as it is, replacing decision 0063's row for a reviewer's question. `supersedes` decision 0063; source: q9, observation/2026-10-25-apply-ids-and-fix-work-items, decisions 0063 and 0064; by: the person's delegation of 2026-10-25 via q9.

## Questions
1. A delegated session answers a reviewer's question without saying whether it asks for a change or accepts the work-item. Readings: (a) no line (request gives none; work-queue r28 already refuses it); (b) add [supervision#r120] **If** a session that `work run` started under a delegation answers a reviewer's question on a work-item without saying whether the answer asks for a change or accepts the work-item as it is, **then** `work run` shall leave the question unanswered for the person. The writer gave no recommendation; (a) is the request's text as given.
2. Decision 0069 `supersedes` all of 0063 though only the reviewer's row is replaced. Readings: (a, recommended) keep `supersedes`, the Decision text limits it to that row; (b) drop `supersedes`, name 0063 in `source` only.
3. review#r31 "its result's questions". Readings: (a, recommended) keep the request's wording; (b) "shall give as questions in its result only…" with the field name under Implementation.

## Cut sentences
None.
