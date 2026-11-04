---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, session or script reading work-items or writing their transitions
group: service
language: codified-1
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/work-retry-reads-the-log, design-decision/query-commands-answer-in-their-output, design-decision/work-items-named-by-ids, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked, design-decision/work-list-and-work-show-replace-work-status]
retired: []
---

# Work queue

## Purpose
`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them, and
writes their transitions through their lifecycle, logging every transition; it starts an initiative from an
`accepted` request and makes it `done` when its work and the requests it raised are; it prints where an initiative
stands, for a session to start from, and appends notes to an initiative's ledger. It is the only writer of a
work-item's status; `work run` (supervision) takes them through it. It judges nothing.

## Terms
- **note** (kind): the one line `work note` appends to a ledger after the date it writes.
- **form** (attribute of note): Values: `one-line`, `multi-line`.
- **form** (attribute of answer): Values: `one-line`, `multi-line`.
- **out of step** (condition of work-item): a work-item whose last status in `log.jsonl` differs from the status in its file.
- **asking stage** (attribute of question): the kind of stage that asked the question. Values: `research`, `plan`, `implement`, `review`.
- **flag** (attribute of answer): the flag `work answer` is given with an answer to a reviewer's question. Values: `--change`, `--accept`, `unflagged`.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| ledger | of | initiative | one |
| work-item | kept in | initiative | one |

## Behaviour

### [g1] `work add` drafts a work-item
Restates: r1@0.29, r9@0.29.
- [r1] When the person runs `work add` on an initiative that is `started`, `work` shall write a work-item that is
  `drafted` and commit the work-item.

### [g2] `work add` refuses an initiative that is not open
Restates: r32@0.29.
- [r2] If the person runs `work add` on an initiative that is not open, then `work` shall exit with an error naming
  the status of the initiative and change nothing.

### [g3] `work start` begins an initiative for an accepted request
Restates: r22@0.29, r25@0.29.
- [r3] When the person runs `work start` on a request that is `accepted`, `work` shall write an initiative that fulfils
  the request and commit the initiative.

### [g4] `work start` refuses a request that is not accepted
Restates: r7@0.29.
- [r4] If the person runs `work start` on a request that is not `accepted`, then `work` shall exit with an error
  naming the request and change nothing.

### [g5] An initiative whose work is closed becomes done
Restates: r62@0.29.
- [r5] While an initiative is `started` and the initiative is complete, when the person runs `work withdraw` on a
  work-item that is `ready`, `work` shall set the status of the initiative to `done`.

### [g6] An initiative whose every work-item is withdrawn stays as it is
Restates: r31@0.29.
- [r6] While an initiative is `started` and the initiative is not complete, when the person runs `work withdraw` on
  a work-item that is `ready`, `work` shall not set the status of the initiative to `done`.

### [g7] An open capability-proposal keeps its initiative started
Restates: r47@0.29.
- [r7] While an initiative is `started` and a capability-proposal part of the initiative is not closed, when the
  person runs `work withdraw` on a work-item that is `ready`, `work` shall not set the status of the initiative to
  `done`.

### [g8] `work list` prints every node with its status
Restates: r60@0.29.
- [r8] When the person runs `work list`, `work` shall print every initiative and the status of the initiative and
  print every work-item and the status of the work-item.

### [g9] `work list --json` prints one JSON object
Restates: r61@0.29.
- [r9] Where `--json` is given, when the person runs `work list`, `work` shall exit successfully.

### [g10] `work show` on an initiative prints where it stands
Restates: r36@0.29.
- [r10] When the person runs `work show` on an initiative, `work` shall print the status of the initiative and every
  work-item kept in the initiative.

### [g11] `work show` on a work-item prints its status
Restates: r37@0.29.
- [r11] When the person runs `work show` on a work-item, `work` shall print the status of the work-item.

### [g12] `work show --json` prints one JSON object
Restates: r38@0.29.
- [r12] Where `--json` is given, when the person runs `work show` on an initiative, `work` shall exit
  successfully.

### [g13] `work note` appends a note to the ledger
Restates: r19@0.29, r20@0.29.
- [r13] When the person runs `work note` on an initiative, `work` shall write the ledger of the initiative and commit
  the ledger.

### [g14] `work note` refuses a note of more than one line
Restates: r21@0.29.
- [r14] While a note is `multi-line`, if the person runs `work note` on an initiative, then `work` shall exit with an
  error naming the note and change nothing.

### [g15] `work withdraw` withdraws a work-item that is not claimed or green
Restates: r10@0.29, r4@0.29, r5@0.29.
- [r15] When the person runs `work withdraw` on a work-item that is `ready`, `work` shall set its status to
  `withdrawn`, write a transition and commit the work-item.

### [g16] `work withdraw` refuses a green work-item
Restates: r10@0.29.
- [r16] If the person runs `work withdraw` on a work-item that is `green`, then `work` shall exit with an error
  naming the status of the work-item and change nothing.

### [g17] A transition the log does not agree with is refused
Restates: r6@0.29.
- [r17] If the person runs `work withdraw` on a work-item that is out of step, then `work` shall exit with an error
  naming the work-item and change nothing.

### [g18] `work retry` returns a failed work-item
Restates: r8@0.29.
- [r18] When the person runs `work retry` on a work-item that is `failed`, `work` shall set its status to `claimed`.

### [g19] `work answer` writes an answer
Restates: r13@0.29, r24@0.29, r30@0.29.
- [r19] When the person runs `work answer` on a capability-proposal that is `awaiting-answer`, `work` shall write an
  answer and commit the capability-proposal.

### [g20] `work answer` returns a work-item to the research stage that asked
Restates: r13@0.29, r14@0.29.
- [r20] While a work-item is `awaiting-answer` and the question on the work-item is `research`, when the person runs
  `work answer` on the work-item, `work` shall set its status to `drafted` and write an answer.

### [g21] `work answer` returns a work-item to the plan stage that asked
Restates: r14@0.29.
- [r21] While a work-item is `awaiting-answer` and the question on the work-item is `plan`, when the person runs
  `work answer` on the work-item, `work` shall set its status to `researched`.

### [g22] `work answer` returns a work-item to the implement stage that asked
Restates: r14@0.29.
- [r22] While a work-item is `awaiting-answer` and the question on the work-item is `implement`, when the person runs
  `work answer` on the work-item, `work` shall set its status to `ready`.

### [g23] An answer to a reviewer's question that asks for a change
Restates: r26@0.29.
- [r23] While a work-item is `awaiting-answer` and the question on the work-item is `review` and the answer is
  `--change`, when the person runs `work answer` on the work-item, `work` shall set its status to `ready`.

### [g24] An answer to a reviewer's question that accepts the work-item
Restates: r27@0.29.
- [r24] While a work-item is `awaiting-answer` and the question on the work-item is `review` and the answer is
  `--accept`, when the person runs `work answer` on the work-item, `work` shall set its status to `done`.

### [g25] An answer to a reviewer's question must say which
Restates: r28@0.29.
- [r25] While a question is `review` and an answer is `unflagged`, if the person runs `work answer` on a work-item
  that is `awaiting-answer`, then `work` shall exit with an error naming the flag of the answer and change nothing.

### [g26] `work answer` refuses an answer of more than one line
Restates: r15@0.29.
- [r26] While an answer is `multi-line`, if the person runs `work answer` on a work-item that is `awaiting-answer`,
  then `work` shall exit with an error naming the answer and change nothing.

## Implementation, may change
- `scripts/work` with its library `scripts/workqueue.py`, standard library only; the frontmatter subset
  `scripts/model` reads. A work-item's fields are design-decision/work-file-forms'.
- A work-item's frontmatter `id` is `work-item/<context path>/w<n>`; `<work-item>` in a command is its id `w<n>`
  (design-decision/work-items-named-by-ids). `work add` numbers a new work-item's id `w<n>` with `<n>` one above the
  highest `<n>` of any work-item under `.shop/work/`, in any initiative and any status, and prints it.
- `work add` takes `--part-of`, `--under` and `--accepts`, and writes the title as the work-item's `# ` heading.
- `work start` writes `.shop/work/<initiative>/initiative.md`, a `capability-change` initiative whose `fulfils` names
  the request and whose `source` is the request's, and prints its id.
- `log.jsonl` is one JSON object a line, with the time, the work-item, the status before and after, and who made the
  transition; a transition and the work-item's file are written together, the log line last.
- A transition the lifecycle does not allow from the work-item's status is refused (U3).
- `work answer` on a work-item that is not `awaiting-answer` is a change `work` cannot make, refused (U3). It writes
  the answer, with the date, under the node's `## Answers`; `<initiative>/<name>` names the node of that initiative.
  The work-item returns to the status its asking stage started from: `drafted` for a researcher, `researched` for a
  planner, `ready` for an implementer.
- `work retry` returns a work-item to the status before that `log.jsonl` gives in its transition into `failed`.
- `work retry` and `work withdraw` print `<work-item> <status>`, the status being the one the transition made.
- An initiative is complete (the glossary's condition) when it has a `green` work-item, every work-item is `green`
  or `withdrawn`, every capability-proposal is `formulated` or `withdrawn`, and every request kept in this context
  whose asker is this context and that names the initiative in its `part_of` or its `source` is `delivered`.
- The flag of a reviewer's answer is `--change` for an answer that asks for a change and `--accept` for one that
  accepts the work-item as it is; the answer stays one line of free text.
- A note or an answer is one line: it has none of Unicode's mandatory line breaks, U+000A (LF), U+000B (VT),
  U+000C (FF), U+000D (CR), U+0085 (NEL), U+2028 or U+2029.
- `work show <initiative>` also prints each capability-proposal with its status, each work-item's open questions,
  the initiative branch and whether the remote has every commit of it, the checkout's uncommitted and untracked
  files, the last ten lines of the ledger and its last line whose note begins `next:`. `work show <request>` prints
  the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its
  resolution.

## Not yet
- `next`, `claim`, `questions`, `log` and `plugin` (`work_expectations.py`), `--check`
  work-items, the guards between work-items, `show --status` (see skeleton-notes.md).
- `work list` printing an initiative as waiting on a request it raised into an upstream while that request is not
  `delivered` (0.29's r39): the grammar has no condition on a relation between two nodes yet.

## Dropped
- r12@0.29: the numbering of a work-item's id is `work add`'s implementation, kept under Implementation, may change.
- r39@0.29: the grammar cannot say a condition on a relation between an initiative and a request; kept under Not yet.
- r59@0.29: moved to requests.
