## frontmatter
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Measurement of an initiative's deliveries
narrator: a session measuring an initiative's deliveries
group: service
rests_on: [design-decision/measure-an-initiative, design-decision/measure-refuses-unknown-shapes, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/commands-and-agents-answer-in-json]
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36, r37, r38, r50]
---

## Behaviour

### Output and exits
- [r68] `measure` shall give its output as one JSON object on stdout.
- [r69] The JSON object that `measure` gives shall hold the field `ok`.
- [r70] **When** `measure` does what it was asked, `measure` shall give `ok` true in its JSON object.
- [r71] **When** `measure` ends without crashing on an error it does not handle, `measure` shall exit successfully.
- [r72] **If** `measure` crashes on an error it does not handle, **then** `measure` shall exit with an error.

### The initiative
- [r39] **When** `measure initiative <initiative>` is run, `measure` shall write one measurement for the initiative at `.shop/records/measurements/<date>-<initiative>.md`, the date being the day it is run.
- [r46] **If** the initiative has no `log.jsonl`, **then** `measure initiative` shall refuse, writing nothing, because the initiative has no `log.jsonl`.
- [r65] **If** the initiative fulfils a request that the queue does not hold, **then** `measure initiative` shall refuse, writing no measurement, because the queue does not hold that request.
- [r66] **If** the request the initiative fulfils has no asker, **then** `measure initiative` shall refuse, writing no measurement, because the request has no asker.
- [r67] **If** the initiative fulfils more than one request, **then** `measure initiative` shall refuse, writing no measurement, because the initiative fulfils more than one request.
- [r47] **If** a `session.json` that is not empty, or a transcript, is not of a shape `measure` knows, **then** `measure` shall refuse, writing nothing, naming that file.
- [r58] **When** a line of a transcript holds U+2028 or another Unicode line break inside a JSON string, `measure` shall read it as one line.
- [r59] **When** a time in `log.jsonl` or in a transcript ends in `Z`, `measure` shall read it as a time in UTC.
- [r48] **If** the measurement exists and `--replace` is not given, **then** `measure initiative` shall refuse, writing nothing, because the measurement exists.
- [r52] **Where** `--replace` is given, `measure initiative` shall write the measurement over the one that exists.
- [r73] **If** `measure` refuses, **then** `measure` shall give `ok` false in its JSON object, with the reason it refuses.

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
- [r74] **When** `measure show` or `measure compare` is run, `measure` shall give the text of its tables inside a field of its JSON object.
