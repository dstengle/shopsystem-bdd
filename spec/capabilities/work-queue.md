---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, session or script reading work-items or writing their transitions
group: service
language: codified-1
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/work-retry-reads-the-log, design-decision/query-commands-answer-in-their-output, design-decision/work-items-named-by-ids, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked, design-decision/work-list-and-work-show-replace-work-status]
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26]
---

# Work queue

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them, and
writes their transitions through their lifecycle, logging every transition; it starts an initiative from an
`accepted` request and makes it `done` when its work and the requests it raised are; it prints where an initiative
stands, for a session to start from, and appends notes to an initiative's ledger. It is the only writer of a
work-item's status; `work run` (supervision) takes them through it. It judges nothing.

## Terms
- **note** (noun): the one line `work note` appends to a ledger after the date it writes.
- **form** (attribute of note): Values: `one-line`, `multi-line`.
- **form** (attribute of answer): Values: `one-line`, `multi-line`.
- **out of step** (adjective of work-item): a work-item whose last status in `log.jsonl` differs from the status in its file.
- **asking stage** (attribute of question): the kind of stage that asked the question. Values: `research`, `plan`, `implement`, `review`.
- **flag** (attribute of answer): the flag `work answer` is given with an answer to a reviewer's question. Values: `--change`, `--accept`, `unflagged`.

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r12@0.29: the numbering of a work-item's id is `work add`'s implementation, kept under Implementation, may change.
- r39@0.29: the grammar cannot say a condition on a relation between an initiative and a request; kept under Not yet.
- r59@0.29: moved to requests.
- r1@0.29: retired with work-queue#r1 in 2.0.0 (the-old-workflow-retired).
- r4@0.29: retired with work-queue#r15 in 2.0.0 (the-old-workflow-retired).
- r5@0.29: retired with work-queue#r15 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with work-queue#r17 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with work-queue#r4 in 2.0.0 (the-old-workflow-retired).
- r8@0.29: retired with work-queue#r18 in 2.0.0 (the-old-workflow-retired).
- r9@0.29: retired with work-queue#r1 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with work-queue#r15, #r16 in 2.0.0 (the-old-workflow-retired).
- r13@0.29: retired with work-queue#r19, #r20 in 2.0.0 (the-old-workflow-retired).
- r14@0.29: retired with work-queue#r20, #r21, #r22 in 2.0.0 (the-old-workflow-retired).
- r15@0.29: retired with work-queue#r26 in 2.0.0 (the-old-workflow-retired).
- r19@0.29: retired with work-queue#r13 in 2.0.0 (the-old-workflow-retired).
- r20@0.29: retired with work-queue#r13 in 2.0.0 (the-old-workflow-retired).
- r21@0.29: retired with work-queue#r14 in 2.0.0 (the-old-workflow-retired).
- r22@0.29: retired with work-queue#r3 in 2.0.0 (the-old-workflow-retired).
- r24@0.29: retired with work-queue#r19 in 2.0.0 (the-old-workflow-retired).
- r25@0.29: retired with work-queue#r3 in 2.0.0 (the-old-workflow-retired).
- r26@0.29: retired with work-queue#r23 in 2.0.0 (the-old-workflow-retired).
- r27@0.29: retired with work-queue#r24 in 2.0.0 (the-old-workflow-retired).
- r28@0.29: retired with work-queue#r25 in 2.0.0 (the-old-workflow-retired).
- r30@0.29: retired with work-queue#r19 in 2.0.0 (the-old-workflow-retired).
- r31@0.29: retired with work-queue#r6 in 2.0.0 (the-old-workflow-retired).
- r32@0.29: retired with work-queue#r2 in 2.0.0 (the-old-workflow-retired).
- r36@0.29: retired with work-queue#r10 in 2.0.0 (the-old-workflow-retired).
- r37@0.29: retired with work-queue#r11 in 2.0.0 (the-old-workflow-retired).
- r38@0.29: retired with work-queue#r12 in 2.0.0 (the-old-workflow-retired).
- r47@0.29: retired with work-queue#r7 in 2.0.0 (the-old-workflow-retired).
- r60@0.29: retired with work-queue#r8 in 2.0.0 (the-old-workflow-retired).
- r61@0.29: retired with work-queue#r9 in 2.0.0 (the-old-workflow-retired).
- r62@0.29: retired with work-queue#r5 in 2.0.0 (the-old-workflow-retired).
