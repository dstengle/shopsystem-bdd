---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Measurement of an initiative's deliveries
narrator: a session measuring an initiative's deliveries
group: service
language: codified-2
rests_on: [design-decision/measure-an-initiative, design-decision/measure-refuses-unknown-shapes, design-decision/plugin-takes-the-dependencies-it-needs]
unbuilt: []
retired: [g18, g19, g20, g21, g22, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22]
---

# Measurement of an initiative's deliveries

## Purpose
`scripts/measure` writes one measurement of an initiative's deliveries from what `work run` already records: the
initiative's `log.jsonl`, each stage's `session.json` and the sessions' transcripts. It reads measurements back as
tables and compares two of them. It writes no prompt, reply or tool content, and refuses a file of a shape it does
not know rather than guessing at it.

## Terms
- **logged stage** (noun): a stage the initiative log gives a start for, run in one session.
- **stage row** (noun): the figures a measurement gives for one logged stage: its work-item, stage, agent, session and turns. Kind of: text.
- **total row** (noun): the sums of the figures of a measurement. Kind of: text.
- **round trip** (noun): one request of a session to its model and the reply. Kind of: thing.
- **session row** (noun): the figures a measurement gives for one session: its tokens, round trips, tool uses, dispatches and compactions. Kind of: text.
- **tool use** (noun): one call of a tool by a session. Kind of: thing.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| stage row | of | measurement |  |
| total row | of | measurement | one |
| round trip | of | stage row |  |
| session row | of | measurement |  |
| round trip | of | session row |  |
| tool use | of | session row |  |
| dispatch | of | session row |  |
| compaction | of | session row |  |
| tool use | in | measurement |  |
| compaction | in | measurement |  |

## Behaviour

### [g23] `measure show` prints a measurement's stage rows, its total row and the number of round trips of a stage row
Restates: r44@0.29, r54@0.29.
- [r23] When the person runs `measure show` on a measurement that has a stage row that has a round trip, `measure` shall print the number of round trips of the stage row, every stage row of the measurement and the total row of the measurement.

```given
the measurement `m1` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
```

### [g24] `measure show` prints the stage rows of a measurement whose stage row has no round trip without a round trip
Restates: r56@0.29.
- [r24] When the person runs `measure show` on a measurement that has a stage row that has no round trip, `measure` shall print every stage row of the measurement and not print a round trip.

```given
the measurement `m2` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
```

### [g25] `measure show` prints each session row's tool uses, dispatches and compactions
Restates: r61@0.29.
- [r25] When the person runs `measure show` on a measurement that has a session row, `measure` shall print the number of tool uses of the session row, every dispatch of the session row and the number of compactions of the session row.

```given
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```

### [g26] `measure compare` prints the total rows of two measurements side by side with their ratio
Restates: r45@0.29.
- [r26] When the person runs `measure compare` on two measurements, `measure` shall print two total rows and a ratio.

```given
the measurement `m1` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```

### [g27] `measure compare` prints the totals over the session rows of a measurement
Restates: r62@0.29.
- [r27] When the person runs `measure compare` on a measurement that has a session row, `measure` shall print the number of tool uses in the measurement and the number of compactions in the measurement.

```given
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```

## Implementation, may change
- A measurement is a record whose frontmatter id is of kind `measurement`; its figures are one JSON block in its
  body, which `show` and `compare` read back. `measure initiative`, which wrote an initiative's, was retired in
  plugin 2.0.0 with r1-r17 (the-old-workflow-retired); the records it wrote are still shown and compared.

## Not yet
- Figures beyond what `work run` already records: the skeleton grows from the measurements of 0.21.0's, 0.22.0's
  and 0.23.0's deliveries; a line is added when one of those measurements needs a figure the measurement does not
  give.

## Dropped
- r39@0.29: retired with batch-measurement#r1 in 2.0.0 (the-old-workflow-retired).
- r40@0.29: retired with batch-measurement#r1 in 2.0.0 (the-old-workflow-retired).
- r41@0.29: retired with batch-measurement#r9 in 2.0.0 (the-old-workflow-retired).
- r42@0.29: retired with batch-measurement#r9 in 2.0.0 (the-old-workflow-retired).
- r43@0.29: retired with batch-measurement#r17 in 2.0.0 (the-old-workflow-retired).
- r46@0.29: retired with batch-measurement#r2 in 2.0.0 (the-old-workflow-retired).
- r47@0.29: retired with batch-measurement#r6, #r7 in 2.0.0 (the-old-workflow-retired).
- r48@0.29: retired with batch-measurement#r10 in 2.0.0 (the-old-workflow-retired).
- r49@0.29: retired with batch-measurement#r17 in 2.0.0 (the-old-workflow-retired).
- r50@0.29: retired with batch-measurement#r2 in 2.0.0 (the-old-workflow-retired).
- r51@0.29: retired with batch-measurement#r12 in 2.0.0 (the-old-workflow-retired).
- r52@0.29: retired with batch-measurement#r11 in 2.0.0 (the-old-workflow-retired).
- r53@0.29: retired with batch-measurement#r8 in 2.0.0 (the-old-workflow-retired).
- r55@0.29: retired with batch-measurement#r14 in 2.0.0 (the-old-workflow-retired).
- r57@0.29: retired with batch-measurement#r13 in 2.0.0 (the-old-workflow-retired).
- r58@0.29: retired with batch-measurement#r8 in 2.0.0 (the-old-workflow-retired).
- r59@0.29: retired with batch-measurement#r9 in 2.0.0 (the-old-workflow-retired).
- r60@0.29: retired with batch-measurement#r17 in 2.0.0 (the-old-workflow-retired).
- r63@0.29: retired with batch-measurement#r15 in 2.0.0 (the-old-workflow-retired).
- r64@0.29: retired with batch-measurement#r16 in 2.0.0 (the-old-workflow-retired).
- r65@0.29: retired with batch-measurement#r3 in 2.0.0 (the-old-workflow-retired).
- r66@0.29: retired with batch-measurement#r4 in 2.0.0 (the-old-workflow-retired).
- r67@0.29: retired with batch-measurement#r5 in 2.0.0 (the-old-workflow-retired).
