---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, session or script reading work-items or writing their transitions
group: service
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs]
retired: []
---

# Work queue

## Purpose
`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them, and
moves them through their lifecycle, logging every move. It is the only writer of a work-item's status; `work run`
(supervision) moves them through it. It judges nothing. A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what running it shows.

## Behaviour
- [r1] **When** `work add <initiative> <name>` is run with `--part-of`, `--under` and `--accepts`, `work` shall write `.shop/work/<initiative>/<name>.md` as a `drafted` work-item with the fields given.
- [r2] **If** the work-item's file already exists, then `work add` shall leave the file as it was.
- [r3] **When** `work show` is run, `work` shall print each work-item of every initiative under `.shop/work/` with its status.
- [r4] **When** `work` moves a work-item, `work` shall write the new status into the work-item's file.
- [r5] **When** `work` moves a work-item, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the time, the work-item, the status before and after, and who moved it.
- [r6] **If** a work-item's status in its file is not the last status `log.jsonl` gives it, then `work` shall refuse to move it, naming the file and both statuses.
- [r7] **If** `work` cannot do what it was asked, then `work` shall exit non-zero, say why, and change nothing.

## Implementation, may change
- `scripts/work` with its library `scripts/workqueue.py`, standard library only; the frontmatter subset
  `scripts/model` reads. A work-item's fields are design-decision/work-file-forms'.
- `log.jsonl` is one JSON object a line; a move and its file are written together, the log line last.
- A move the lifecycle does not allow from the work-item's status is refused under r7.

## Not yet
- `next`, `claim`, `questions`, `withdraw`, `log` and `plugin` (`work_expectations.py`), `--check`
  work-items, the guards between work-items, `show --status` (see skeleton-notes.md).
- `work rule`, which records the person's ruling in an `awaiting-ruling` work-item and moves it on (i8 run 1).
