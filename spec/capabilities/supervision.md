---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
title: Supervision
narrator: the person who started `work run`
group: service
language: codified-2
rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36, r37, r38, r39, r40, r41, r42, r43, r44, r45, r46, r47, r48, r49, r50, r51, r52, r53, r54, r55, r56, r57, r58, r59, r60, r61, r62, r63, r64, r65, r66, r67, r68, r69, r70, r71, r72, r73, r74, r75, r76, r77, r78, r79, r80, r81, r82, r83, r84]
---

# Supervision

## Purpose
**Retired in plugin 0.31.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

`work run` takes a bounded context's initiatives through their transitions: `work run <initiative>` that
initiative, `work run` with no initiative every initiative that is neither `done` nor `abandoned`. It starts the
`intake` round of a request this context is the upstream of, starts with `work start` the initiative of such a
request once it is `accepted`, and starts the `integrate` round of an initiative, checks and keeps that round's drafts
and writes the capability-proposals its change list names, starts a capability-proposal's `gate` and `apply` rounds,
runs its `formulate` round as a script, drafts and delivers its work-items, for each stage starting a fresh
`claude -p` worker, reading the worker's result and writing the status itself, starts the initiative's measurement
and analysis and commits them, and sets the initiative `done`, committing it, when what it delivers is closed
(design-decision/the-context-runs-without-a-coordinator). It is a script and takes no judgment; what nobody may
decide goes to the person as a question.

## Terms
- **change list** (noun): the list an `integrate` or `apply` round's result gives of what it adds, changes and removes.
- **outputless** (adjective of result): A result is outputless when the result gives no question and the result gives no output.
- **draft** (verb, action): `work run` writes a node with `work add` or from a change list. Forms: drafts, drafted. Frame: `work run` drafts node.
- **take** (verb, action): `work run` takes an initiative through the transitions its nodes can make. Forms: takes, took, taken. Frame: `work run` takes initiative.
- **log** (verb, action): `work run` appends a line to `.shop/work/<initiative>/log.jsonl`. Forms: logs, logged. Frame: `work run` logs ledger.
- **remove** (verb, action): a session or a tool removes a file, a directory or a text it wrote, or takes a text out of a git branch with a commit. Forms: removes, removed. Frame: agent removes text. Frame: agent removes text from git branch.
- **output** (noun): what a stage's result gives as its stage's work. Redefines: cli.
- **draft** (noun): a file an `integrate` round writes under its drafts path, kept on the initiative branch. Plural: drafts.
- **naming** (adjective of result): a result that names a report its session wrote in its worktree.
- **kept** (adjective of work-item branch): a work-item branch `work run` kept when its work-item became `awaiting-answer`.
- **codified** (adjective of change list): a change list whose every capability has `language: codified-1` in its file.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| result | gives | question |  |
| result | gives | output |  |
| result | gives | change list |  |

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r42@0.29: restated U6 (a stage that ends with no result is discarded: its work-item becomes `failed`).
- r22@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r55@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r56@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r64@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r65@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r29@0.29: `.shop/delivery.toml`'s `[tests]`, moved to Implementation; every scenario's repository runs its tests through it.
- r43@0.29: what the suite counts as expected to fail, and the question with both runs of a failing scenario, moved to Implementation; tested by `tests/scripts/test_work_items.py` and `tests/scripts/test_supervise*.py`.
- r122@0.29: what the suite counts as expected to fail, and the question with both runs of a failing scenario, moved to Implementation; tested by `tests/scripts/test_work_items.py` and `tests/scripts/test_supervise*.py`.
- r220@0.29: what the suite counts as expected to fail, and the question with both runs of a failing scenario, moved to Implementation; tested by `tests/scripts/test_work_items.py` and `tests/scripts/test_supervise*.py`.
- r73@0.29: deprecated scenarios are gone (design §14: the generator owns the feature files); a work-item retiring scenarios comes from the proposal's `removes`.
- r123@0.29: deprecated scenarios are gone (design §14: the generator owns the feature files); a work-item retiring scenarios comes from the proposal's `removes`.
- r124@0.29: deprecated scenarios are gone (design §14: the generator owns the feature files); a work-item retiring scenarios comes from the proposal's `removes`.
- r116@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
- r186@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
- r152@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
- r153@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
- r1@0.29: retired with supervision#r1 in 2.0.0 (the-old-workflow-retired).
- r2@0.29: retired with supervision#r2, #r3, #r4, #r5 in 2.0.0 (the-old-workflow-retired).
- r4@0.29: retired with supervision#r14, #r15 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with supervision#r21 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with supervision#r24 in 2.0.0 (the-old-workflow-retired).
- r8@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with supervision#r37 in 2.0.0 (the-old-workflow-retired).
- r11@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r12@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r13@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r14@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r15@0.29: retired with supervision#r14 in 2.0.0 (the-old-workflow-retired).
- r17@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r18@0.29: retired with supervision#r16 in 2.0.0 (the-old-workflow-retired).
- r19@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r20@0.29: retired with supervision#r82, #r83 in 2.0.0 (the-old-workflow-retired).
- r21@0.29: retired with supervision#r36 in 2.0.0 (the-old-workflow-retired).
- r23@0.29: retired with supervision#r24 in 2.0.0 (the-old-workflow-retired).
- r24@0.29: retired with supervision#r14 in 2.0.0 (the-old-workflow-retired).
- r25@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r26@0.29: retired with supervision#r17 in 2.0.0 (the-old-workflow-retired).
- r27@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r30@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r31@0.29: retired with supervision#r25 in 2.0.0 (the-old-workflow-retired).
- r33@0.29: retired with supervision#r24 in 2.0.0 (the-old-workflow-retired).
- r34@0.29: retired with supervision#r21 in 2.0.0 (the-old-workflow-retired).
- r35@0.29: retired with supervision#r33 in 2.0.0 (the-old-workflow-retired).
- r36@0.29: retired with supervision#r10 in 2.0.0 (the-old-workflow-retired).
- r37@0.29: retired with supervision#r27, #r28 in 2.0.0 (the-old-workflow-retired).
- r38@0.29: retired with supervision#r24 in 2.0.0 (the-old-workflow-retired).
- r39@0.29: retired with supervision#r33 in 2.0.0 (the-old-workflow-retired).
- r40@0.29: retired with supervision#r13 in 2.0.0 (the-old-workflow-retired).
- r41@0.29: retired with supervision#r19 in 2.0.0 (the-old-workflow-retired).
- r44@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r45@0.29: retired with supervision#r13 in 2.0.0 (the-old-workflow-retired).
- r46@0.29: retired with supervision#r35 in 2.0.0 (the-old-workflow-retired).
- r47@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r48@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r49@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r50@0.29: retired with supervision#r40 in 2.0.0 (the-old-workflow-retired).
- r51@0.29: retired with supervision#r34 in 2.0.0 (the-old-workflow-retired).
- r52@0.29: retired with supervision#r28 in 2.0.0 (the-old-workflow-retired).
- r53@0.29: retired with supervision#r34 in 2.0.0 (the-old-workflow-retired).
- r54@0.29: retired with supervision#r32 in 2.0.0 (the-old-workflow-retired).
- r57@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r58@0.29: retired with supervision#r18 in 2.0.0 (the-old-workflow-retired).
- r59@0.29: retired with supervision#r82 in 2.0.0 (the-old-workflow-retired).
- r60@0.29: retired with supervision#r82 in 2.0.0 (the-old-workflow-retired).
- r61@0.29: retired with supervision#r83 in 2.0.0 (the-old-workflow-retired).
- r62@0.29: retired with supervision#r6 in 2.0.0 (the-old-workflow-retired).
- r63@0.29: retired with supervision#r38 in 2.0.0 (the-old-workflow-retired).
- r66@0.29: retired with supervision#r30, #r81 in 2.0.0 (the-old-workflow-retired).
- r67@0.29: retired with supervision#r51 in 2.0.0 (the-old-workflow-retired).
- r68@0.29: retired with supervision#r65 in 2.0.0 (the-old-workflow-retired).
- r69@0.29: retired with supervision#r67 in 2.0.0 (the-old-workflow-retired).
- r70@0.29: retired with supervision#r70 in 2.0.0 (the-old-workflow-retired).
- r72@0.29: retired with supervision#r79 in 2.0.0 (the-old-workflow-retired).
- r74@0.29: retired with supervision#r42 in 2.0.0 (the-old-workflow-retired).
- r75@0.29: retired with supervision#r43 in 2.0.0 (the-old-workflow-retired).
- r76@0.29: retired with supervision#r43 in 2.0.0 (the-old-workflow-retired).
- r78@0.29: retired with supervision#r46 in 2.0.0 (the-old-workflow-retired).
- r79@0.29: retired with supervision#r54 in 2.0.0 (the-old-workflow-retired).
- r81@0.29: retired with supervision#r31 in 2.0.0 (the-old-workflow-retired).
- r82@0.29: retired with supervision#r30 in 2.0.0 (the-old-workflow-retired).
- r83@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- r84@0.29: retired with supervision#r54 in 2.0.0 (the-old-workflow-retired).
- r85@0.29: retired with supervision#r67 in 2.0.0 (the-old-workflow-retired).
- r86@0.29: retired with supervision#r78 in 2.0.0 (the-old-workflow-retired).
- r87@0.29: retired with supervision#r78 in 2.0.0 (the-old-workflow-retired).
- r88@0.29: retired with supervision#r78 in 2.0.0 (the-old-workflow-retired).
- r89@0.29: retired with supervision#r50 in 2.0.0 (the-old-workflow-retired).
- r90@0.29: retired with supervision#r50 in 2.0.0 (the-old-workflow-retired).
- r91@0.29: retired with supervision#r57 in 2.0.0 (the-old-workflow-retired).
- r94@0.29: retired with supervision#r41 in 2.0.0 (the-old-workflow-retired).
- r95@0.29: retired with supervision#r80 in 2.0.0 (the-old-workflow-retired).
- r96@0.29: retired with supervision#r56 in 2.0.0 (the-old-workflow-retired).
- r97@0.29: retired with supervision#r41 in 2.0.0 (the-old-workflow-retired).
- r98@0.29: retired with supervision#r18 in 2.0.0 (the-old-workflow-retired).
- r100@0.29: retired with supervision#r52 in 2.0.0 (the-old-workflow-retired).
- r101@0.29: retired with supervision#r29 in 2.0.0 (the-old-workflow-retired).
- r102@0.29: retired with supervision#r54 in 2.0.0 (the-old-workflow-retired).
- r103@0.29: retired with supervision#r53 in 2.0.0 (the-old-workflow-retired).
- r106@0.29: retired with supervision#r43 in 2.0.0 (the-old-workflow-retired).
- r107@0.29: retired with supervision#r61 in 2.0.0 (the-old-workflow-retired).
- r108@0.29: retired with supervision#r65, #r70 in 2.0.0 (the-old-workflow-retired).
- r109@0.29: retired with supervision#r44 in 2.0.0 (the-old-workflow-retired).
- r110@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r111@0.29: retired with supervision#r1, #r44 in 2.0.0 (the-old-workflow-retired).
- r115@0.29: retired with supervision#r78 in 2.0.0 (the-old-workflow-retired).
- r117@0.29: retired with supervision#r68 in 2.0.0 (the-old-workflow-retired).
- r118@0.29: retired with supervision#r48 in 2.0.0 (the-old-workflow-retired).
- r119@0.29: retired with supervision#r49 in 2.0.0 (the-old-workflow-retired).
- r120@0.29: retired with supervision#r48, #r49 in 2.0.0 (the-old-workflow-retired).
- r121@0.29: retired with supervision#r43 in 2.0.0 (the-old-workflow-retired).
- r128@0.29: retired with supervision#r13 in 2.0.0 (the-old-workflow-retired).
- r129@0.29: retired with supervision#r10, #r11 in 2.0.0 (the-old-workflow-retired).
- r130@0.29: retired with supervision#r7 in 2.0.0 (the-old-workflow-retired).
- r131@0.29: retired with supervision#r12 in 2.0.0 (the-old-workflow-retired).
- r132@0.29: retired with supervision#r7, #r12 in 2.0.0 (the-old-workflow-retired).
- r133@0.29: retired with supervision#r9 in 2.0.0 (the-old-workflow-retired).
- r134@0.29: retired with supervision#r52 in 2.0.0 (the-old-workflow-retired).
- r135@0.29: retired with supervision#r59 in 2.0.0 (the-old-workflow-retired).
- r136@0.29: retired with supervision#r60 in 2.0.0 (the-old-workflow-retired).
- r141@0.29: retired with supervision#r54 in 2.0.0 (the-old-workflow-retired).
- r142@0.29: retired with supervision#r63 in 2.0.0 (the-old-workflow-retired).
- r143@0.29: retired with supervision#r63 in 2.0.0 (the-old-workflow-retired).
- r144@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- r145@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- r146@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- r147@0.29: retired with supervision#r73 in 2.0.0 (the-old-workflow-retired).
- r148@0.29: retired with supervision#r63 in 2.0.0 (the-old-workflow-retired).
- r150@0.29: retired with supervision#r73 in 2.0.0 (the-old-workflow-retired).
- r151@0.29: retired with supervision#r73 in 2.0.0 (the-old-workflow-retired).
- r154@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r155@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r156@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r157@0.29: retired with supervision#r39 in 2.0.0 (the-old-workflow-retired).
- r159@0.29: retired with supervision#r57 in 2.0.0 (the-old-workflow-retired).
- r161@0.29: retired with supervision#r45 in 2.0.0 (the-old-workflow-retired).
- r164@0.29: retired with supervision#r66 in 2.0.0 (the-old-workflow-retired).
- r165@0.29: retired with supervision#r71 in 2.0.0 (the-old-workflow-retired).
- r166@0.29: retired with supervision#r75 in 2.0.0 (the-old-workflow-retired).
- r167@0.29: retired with supervision#r75 in 2.0.0 (the-old-workflow-retired).
- r168@0.29: retired with supervision#r65 in 2.0.0 (the-old-workflow-retired).
- r169@0.29: retired with supervision#r69 in 2.0.0 (the-old-workflow-retired).
- r170@0.29: retired with supervision#r66, #r71 in 2.0.0 (the-old-workflow-retired).
- r171@0.29: retired with supervision#r58 in 2.0.0 (the-old-workflow-retired).
- r172@0.29: retired with supervision#r72 in 2.0.0 (the-old-workflow-retired).
- r173@0.29: retired with supervision#r69 in 2.0.0 (the-old-workflow-retired).
- r180@0.29: retired with supervision#r55 in 2.0.0 (the-old-workflow-retired).
- r184@0.29: retired with supervision#r27 in 2.0.0 (the-old-workflow-retired).
- r185@0.29: retired with supervision#r8 in 2.0.0 (the-old-workflow-retired).
- r187@0.29: retired with supervision#r63 in 2.0.0 (the-old-workflow-retired).
- r188@0.29: retired with supervision#r63 in 2.0.0 (the-old-workflow-retired).
- r189@0.29: retired with supervision#r64 in 2.0.0 (the-old-workflow-retired).
- r209@0.29: retired with supervision#r47 in 2.0.0 (the-old-workflow-retired).
- r210@0.29: retired with supervision#r46 in 2.0.0 (the-old-workflow-retired).
- r211@0.29: retired with supervision#r46 in 2.0.0 (the-old-workflow-retired).
- r212@0.29: retired with supervision#r26 in 2.0.0 (the-old-workflow-retired).
- r213@0.29: retired with supervision#r44 in 2.0.0 (the-old-workflow-retired).
- r214@0.29: retired with supervision#r23 in 2.0.0 (the-old-workflow-retired).
- r215@0.29: retired with supervision#r23 in 2.0.0 (the-old-workflow-retired).
- r216@0.29: retired with supervision#r23 in 2.0.0 (the-old-workflow-retired).
- r218@0.29: retired with supervision#r22 in 2.0.0 (the-old-workflow-retired).
- r219@0.29: retired with supervision#r20 in 2.0.0 (the-old-workflow-retired).
- r221@0.29: retired with supervision#r74 in 2.0.0 (the-old-workflow-retired).
- r222@0.29: retired with supervision#r20 in 2.0.0 (the-old-workflow-retired).
- formulation#r1@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- formulation#r2@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- formulation#r6@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- formulation#r7@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- formulation#r11@0.29: retired with supervision#r76 in 2.0.0 (the-old-workflow-retired).
- formulation#r22@0.29: retired with supervision#r77 in 2.0.0 (the-old-workflow-retired).
- spec-integration#r44@0.29: retired with supervision#r59 in 2.0.0 (the-old-workflow-retired).
- spec-integration#r45@0.29: retired with supervision#r63 in 2.0.0 (the-old-workflow-retired).
- spec-integration#r46@0.29: retired with supervision#r73 in 2.0.0 (the-old-workflow-retired).
- spec-integration#r54@0.29: retired with supervision#r58 in 2.0.0 (the-old-workflow-retired).
- spec-integration#r55@0.29: retired with supervision#r72 in 2.0.0 (the-old-workflow-retired).
