---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i39-design-model-check
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i39
status: awaiting-answer
argues: [design-model-check]
date: 2026-10-27
adds: [design-model-check#r120, design-model-check#r121]
changes: []
removes: [design-model-check#r115, design-model-check#r117]
---

# design-model-check

The drafts of this proposal are in .shop/work/i39/runs/i39/1-integrate/drafts/round-1/.

## Questions
- design-model-check r120, r121 against table rows r115 (v17) and r117 (v18). Lines: [r120] **When** `model check` reads a request whose `part_of` names a job-thread kept in another repository, `model check` shall print no `v17` for the request. [r121] **When** `model check` reads a request raised for a request of another context, `model check` shall print neither `v17` nor `v18` for the request. Readings: (a) as drafted, standalone lines that override the rows for these requests (recommended, since the lines are what q14 accepted); (b) the rows change instead: "| [r115] | v17 | a request neither is part of a job-thread, cites an origin nor is raised for a request |" and "| [r117] | v18 | ... judged from the id alone, other than the request a request is raised for |", with lines 8 and 9 citing them.
- design-model-check r121 (v18): 'an id in this context's files has another context's path on a kind kept in .shop/work/, judged from the id alone, other than the request a request is raised for'. Reading 1: only a request's own naming of the request it is raised for is excused; another file (e.g. the source of an initiative fulfilling it) naming that id gets v18. Reading 2: an id that is the request some request is raised for is excused wherever this context's files name it, the initiative's source included. Also unmentioned: how a request comes to be raised for a request (work request takes only --source or --thread).

## Answers
- 2026-10-27: r120, r121: no requirement edits or overrides another. Rows r115 (v17) and r117 (v18) are retired and replaced by new rows with new ids covering q14 lines 8 and 9; r120 and r121 are dropped. Also folded in: a retired requirement is a node labelled retired, not returned by queries about the current spec; closed records (a delivered request, a done work-item, a merged, formulated or withdrawn proposal, ledgers, decisions, measurements) may name one; the current spec (scenario tags, live lines and rows) and open work naming one is an error; v3 becomes a resolution naming a requirement that never existed.
- 2026-10-27: Also: every query hides retired requirements by default and includes them only when asked.
