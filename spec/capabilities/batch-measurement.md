---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Measurement of an initiative's deliveries
narrator: a session measuring an initiative's deliveries
group: service
rests_on: [design-decision/measure-an-initiative, design-decision/measure-refuses-unknown-shapes, design-decision/plugin-takes-the-dependencies-it-needs]
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36, r37, r38]
---

# Measurement of an initiative's deliveries

## Purpose
`scripts/measure` writes one measurement of an initiative's deliveries from what `work run` already records: its
work-items, the stages `work run` ran for them, the sessions of those stages and the commits that landed them. It
also prints a measurement, or two measurements' totals side by side. It is not a judgement of the delivery, writes
no prompt, reply or tool content, and refuses rather than guesses when its inputs are not of a shape it knows.

## Behaviour

### The initiative
- [r39] **When** `measure initiative <initiative>` is run, `measure` shall write one measurement for the initiative at `.shop/records/measurements/<date>-<initiative>.md`, the date being the day it is run.
- [r46] **If** the initiative has no `log.jsonl`, **then** `measure initiative` shall refuse, writing nothing, because the initiative has no `log.jsonl`.
- [r47] **If** a `session.json` that is not empty, or a transcript, is not of a shape `measure` knows, **then** `measure` shall refuse, writing nothing, naming that file.
- [r58] **When** a line of a transcript holds U+2028 or another Unicode line break inside a JSON string, `measure` shall read it as one line.
- [r59] **When** a time in `log.jsonl` or in a transcript ends in `Z`, `measure` shall read it as a time in UTC.
- [r48] **If** the measurement exists and `--replace` is not given, **then** `measure initiative` shall refuse, writing nothing, because the measurement exists.
- [r52] **Where** `--replace` is given, `measure initiative` shall write the measurement over the one that exists.
- [r50] **If** `measure` refuses, **then** `measure` shall exit with an error.

### What the measurement holds
- [r40] `measure initiative` shall give, for each stage `log.jsonl` gives a start and an end for, the work-item, the stage, the agent, the session id, how long the stage took, and the session's turns, output tokens, new input tokens, cache-read tokens and cost.
- [r51] `measure initiative` shall give each stage `log.jsonl` gives a start and no end for, without how long it took.
- [r57] **If** a stage's `session.json` is empty, **then** `measure initiative` shall give the stage without its session's figures, named as a stage whose `session.json` is empty.
- [r53] `measure initiative` shall give, for each stage it gives, its session's round trips, the number of assistant messages with distinct request ids in the session's transcript.
- [r55] **If** a stage's session has no transcript `measure` can find, **then** `measure initiative` shall give the stage without its round trips.
- [r41] `measure initiative` shall give, for each work-item, its transitions, how many times it went to `awaiting-answer` and to `failed`, and the commits merged into the initiative branch for it.
- [r42] `measure initiative` shall give the totals over the initiative: stages, sessions, turns, round trips, tokens of each kind, cost, and the time from the first transition to the last.
- [r63] `measure initiative` shall give whether the request the initiative fulfils is internal, its asker being this bounded context, or external.
- [r64] **If** the initiative fulfils no request, **then** `measure initiative` shall give the measurement without whether the request is internal or external.
- [r43] **Where** `--sessions <dir>` names a directory of transcripts, `measure initiative` shall also give each session found there that is active inside the initiative's window, starting inside it or starting before it with a message inside it, and each session it dispatched, with its tokens of each kind.
- [r60] **Where** `--sessions <dir>` is given, `measure initiative` shall give, for each session it gives, its round trips, its tool uses by tool name, the sessions it dispatched, and the number of compactions its transcript holds.
- [r49] `measure` shall write no prompt, reply or tool content into the measurement.

### Reading measurements
- [r44] **When** `measure show <record>` is run, `measure` shall print the measurement's figures as tables.
- [r54] **When** `measure show <record>` is run, `measure` shall print each stage's round trips beside its turns.
- [r56] **When** `measure show <record>` is run on a measurement that gives no round trips, `measure` shall print its stages without them.
- [r61] **When** `measure show <record>` is run on a measurement that gives sessions, `measure` shall print, beside each session's tokens, its round trips, its tool uses by tool name, the sessions it dispatched, and the number of compactions its transcript holds.
- [r45] **When** `measure compare <a> <b>` is run, `measure` shall print the two measurements' totals side by side with the ratio of the second to the first.
- [r62] **When** `measure compare <a> <b>` is run on measurements that give sessions, `measure` shall print, side by side, each measurement's total over its sessions of round trips, of tool uses of all tools together, and of compactions, each total with one ratio of the second measurement's to the first's.

## Implementation, may change
- A measurement is a record whose frontmatter id is of kind `measurement`; its figures are one JSON block in its
  body, which `show` and `compare` read back.
- A stage's start and end, and a work-item's transitions, are read from the initiative's `log.jsonl`; a stage's
  session's turns, tokens and cost from its stage directory's `session.json`.
- A stage's turns are its `session.json`'s `num_turns`, which is not the unit `--max-turns` limits
  (measurement/2026-10-22-research-at-the-limit); its round trips (r53) are that unit.
- r53: a stage's session's transcript is read from the path its `session.json` records (supervision r62).
- The initiative's window runs from the first transition `log.jsonl` gives to the last.
- Tokens are output, new input (input and cache writes) and cache read.
- `--sessions` reads Claude Code's raw transcripts or the slim export of dstengle/shopsystem-records; the sessions
  it finds are those that did the spec work around the delivery: the coordinator, its rounds and its direct
  dispatches.
- r51: a stage with a start and no end is given with everything r40 gives, its session's figures included where its
  `session.json` is there, except how long it took.
- r41: the commits merged for a work-item are the commits of its work-item branch that its merge brought into the
  initiative branch.
- r42: the totals are over the stages' sessions only, with or without `--sessions`, and a stage with a start and no
  end counts in them.
- r43: each session it dispatched is each session dispatched by a session found inside the window, wherever its
  dispatches fall in time.

## Not yet
- Figures beyond what `work run` already records: the skeleton grows from the measurements of 0.21.0's, 0.22.0's
  and 0.23.0's deliveries; a line is added when one of those measurements needs a figure the measurement does not
  give.
