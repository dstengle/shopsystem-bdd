---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Measurement of an initiative's deliveries
narrator: a session measuring an initiative's deliveries
group: service
language: codified-1
rests_on: [design-decision/measure-an-initiative, design-decision/measure-refuses-unknown-shapes, design-decision/plugin-takes-the-dependencies-it-needs]
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17]
---

# Measurement of an initiative's deliveries

## Purpose
`scripts/measure` writes one measurement of an initiative's deliveries from what `work run` already records: the
initiative's `log.jsonl`, each stage's `session.json` and the sessions' transcripts. It reads measurements back as
tables and compares two of them. It writes no prompt, reply or tool content, and refuses a file of a shape it does
not know rather than guessing at it.

## Terms
- **logged stage** (noun): a stage the initiative log gives a start for, run in one session.
- **include** (verb, action): `measure` puts a figure or a name into the measurement it writes. Forms: includes, included. Frame: `measure` includes measurement.

## Behaviour

### [g18] `measure show` prints a measurement's figures as tables, a stage's round trips beside its turns
Restates: r44@0.29, r54@0.29.
- [r18] When the person runs `measure show m1.md`, `measure` shall print "stages", "totals" and "round trips".

```given
the measurement `m1` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
```

### [g19] `measure show` prints the stages of a measurement that gives no round trips without them
Restates: r56@0.29.
- [r19] When the person runs `measure show m2.md`, `measure` shall print "stages", and `measure` shall not print "round trips".

```given
the measurement `m2` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
```

### [g20] `measure show` prints each session's round trips, tool uses, dispatches and compactions
Restates: r61@0.29.
- [r20] When the person runs `measure show m3.md`, `measure` shall print "tool uses", "dispatched" and "compactions".

```given
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```

### [g21] `measure compare` prints two measurements' totals side by side with the ratio of the second to the first
Restates: r45@0.29.
- [r21] When the person runs `measure compare m1.md m3.md`, `measure` shall print "ratio".

```given
the measurement `m1` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```

### [g22] `measure compare` prints the totals over the sessions side by side with their ratio
Restates: r62@0.29.
- [r22] When the person runs `measure compare m3.md m3.md`, `measure` shall print "tool uses" and "compactions".

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
