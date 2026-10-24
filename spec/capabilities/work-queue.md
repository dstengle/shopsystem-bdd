---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, session or script reading work-items or writing their transitions
group: service
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/work-retry-reads-the-log, design-decision/query-commands-answer-in-their-output, design-decision/work-items-named-by-ids, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked]
retired: [r2]
---

# Work queue

## Purpose
`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them, and
writes their transitions through their lifecycle, logging every transition; it prints where an initiative stands,
for a session to start from, and appends notes to an initiative's ledger. It is the only writer of a work-item's
status; `work run` (supervision) takes them through it. It judges nothing. A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Behaviour
- [r1] **When** `work add <initiative> <title>` is run with `--part-of`, `--under` and `--accepts`, `work` shall write `.shop/work/<initiative>/w<n>.md` as a `drafted` work-item with the id `w<n>`, the fields given and the title as its `# ` heading, and print the id.
- [r12] `work add` shall number a new work-item's id `w<n>` with `<n>` one above the highest `<n>` of any work-item under `.shop/work/`, in any initiative and any status.
- [r3] **When** `work show` is run, `work` shall print each work-item of every initiative under `.shop/work/` with its status.
- [r11] **Where** `--json` is given, `work show` shall print its result, each work-item with its initiative and status, as one JSON object.
- [r16] **When** `work status <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`.
- [r17] **When** `work status` is run with no initiative, `work` shall print what r16 gives for each initiative that is neither `done` nor `abandoned`.
- [r18] **Where** `--json` is given, `work status` shall print its result as one JSON object.
- [r19] **When** `work note <initiative> <line>` is run, `work` shall append the line, with the date, to the initiative's ledger `.shop/work/<initiative>/ledger.md`.
- [r20] **When** `work note` appends a line to an initiative's ledger, `work` shall commit the ledger on the current branch.
- [r21] **If** the line given to `work note` has in it one of Unicode's mandatory line breaks, U+000A (LF), U+000B (VT), U+000C (FF), U+000D (CR), U+0085 (NEL), U+2028 or U+2029, then `work` shall exit with an error, saying that a note is one line, and change nothing.
- [r4] **When** `work` makes a work-item's transition, `work` shall write the new status into the work-item's file.
- [r5] **When** `work` makes a work-item's transition, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the time, the work-item, the status before and after, and who made the transition.
- [r6] **If** a work-item's status in its file is not the last status `log.jsonl` gives it, then `work` shall refuse the transition, naming the file and both statuses.
- [r7] **If** `work` cannot do what it was asked, then `work` shall exit with an error, say why, and change nothing.
- [r8] **When** `work retry <work-item>` is run on a `failed` work-item, `work` shall transition it to the status before that `log.jsonl` gives in the work-item's transition into `failed`.
- [r10] **When** `work withdraw <work-item>` is run on a work-item that is neither `claimed` nor `green`, `work` shall transition it to `withdrawn`.
- [r13] **When** `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item, `work` shall write the answer, with the date, under the work-item's `## Answers`.
- [r14] **When** `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item, `work` shall transition it to the status the stage that asked its question started from: `drafted` for a researcher's question, `researched` for a planner's, `ready` for an implementer's and `done` for a reviewer's.
- [r15] **If** the answer given to `work answer` has in it one of Unicode's mandatory line breaks, U+000A (LF), U+000B (VT), U+000C (FF), U+000D (CR), U+0085 (NEL), U+2028 or U+2029, then `work` shall exit with an error, saying that an answer is one line, and change nothing.
- [r9] **When** `work add`, `work retry`, `work withdraw` or `work answer` changes a work-item, `work` shall commit on the current branch the work-item's file and the `log.jsonl` line the change made, if it made one.

## Implementation, may change
- `scripts/work` with its library `scripts/workqueue.py`, standard library only; the frontmatter subset
  `scripts/model` reads. A work-item's fields are design-decision/work-file-forms'.
- A work-item's frontmatter `id` is `work-item/<context path>/w<n>`; `<work-item>` in a command is its id `w<n>`
  (design-decision/work-items-named-by-ids).
- `log.jsonl` is one JSON object a line; a transition and the work-item's file are written together, the log line last.
- A transition the lifecycle does not allow from the work-item's status is refused under r7.
- `work answer` on a work-item that is not `awaiting-answer` is a change `work` cannot make, refused under r7.
- `work retry` and `work withdraw` print `<work-item> <status>`, the status being the one the transition made.

## Not yet
- `next`, `claim`, `questions`, `log` and `plugin` (`work_expectations.py`), `--check`
  work-items, the guards between work-items, `show --status` (see skeleton-notes.md).
