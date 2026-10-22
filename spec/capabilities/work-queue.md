---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, session or script reading work-items or writing their transitions
group: service
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/work-retry-reads-the-log, design-decision/query-commands-answer-in-their-output, design-decision/work-items-named-by-ids]
retired: [r2]
---

# Work queue

## Purpose
`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them, and
writes their transitions through their lifecycle, logging every transition. It is the only writer of a work-item's status; `work run`
(supervision) takes them through it. It judges nothing. A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Behaviour
- [r1] **When** `work add <initiative> <title>` is run with `--part-of`, `--under` and `--accepts`, `work` shall write `.shop/work/<initiative>/w<n>.md` as a `drafted` work-item with the id `w<n>`, the fields given and the title as its `# ` heading, and print the id.
- [r12] `work add` shall number a new work-item's id `w<n>` with `<n>` one above the highest `<n>` of any work-item under `.shop/work/`, in any initiative and any status.
- [r3] **When** `work show` is run, `work` shall print each work-item of every initiative under `.shop/work/` with its status.
- [r11] **Where** `--json` is given, `work show` shall print its result, each work-item with its initiative and status, as one JSON object.
- [r4] **When** `work` makes a work-item's transition, `work` shall write the new status into the work-item's file.
- [r5] **When** `work` makes a work-item's transition, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the time, the work-item, the status before and after, and who made the transition.
- [r6] **If** a work-item's status in its file is not the last status `log.jsonl` gives it, then `work` shall refuse the transition, naming the file and both statuses.
- [r7] **If** `work` cannot do what it was asked, then `work` shall exit with an error, say why, and change nothing.
- [r8] **When** `work retry <work-item>` is run on a `failed` work-item, `work` shall transition it to the status before that `log.jsonl` gives in the work-item's transition into `failed`.
- [r10] **When** `work withdraw <work-item>` is run on a work-item that is neither `claimed` nor `green`, `work` shall transition it to `withdrawn`.
- [r9] **When** `work add`, `work retry` or `work withdraw` changes a work-item, `work` shall commit on the current branch the work-item's file and the `log.jsonl` line the change made, if it made one.

## Implementation, may change
- `scripts/work` with its library `scripts/workqueue.py`, standard library only; the frontmatter subset
  `scripts/model` reads. A work-item's fields are design-decision/work-file-forms'.
- A work-item's frontmatter `id` is `work-item/<context path>/w<n>`; `<work-item>` in a command is its id `w<n>`
  (design-decision/work-items-named-by-ids).
- `log.jsonl` is one JSON object a line; a transition and the work-item's file are written together, the log line last.
- A transition the lifecycle does not allow from the work-item's status is refused under r7.
- `work retry` and `work withdraw` print `<work-item> <status>`, the status being the one the transition made.

## Not yet
- `next`, `claim`, `questions`, `log` and `plugin` (`work_expectations.py`), `--check`
  work-items, the guards between work-items, `show --status` (see skeleton-notes.md).
- `work rule`, which writes the person's ruling in an `awaiting-ruling` work-item and makes its transition on (i8, delivery 1).
