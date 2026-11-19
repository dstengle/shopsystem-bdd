---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/measurement
title: Measurement
narrator: the person
group: service
area: measurement
specifies: service measurement
language: codified-2
retired: []
unbuilt: []
---

# Measurement

## Purpose
What a batch cost and what it found: measured once merged, compared with another, and defects reported against its
items.

## Behaviour

### [g1] A merged batch measured keeps its time, tokens and cost
- [r1] While a batch is `merged`, when the person measures the batch, the measurement service shall keep a measurement
  of the batch and return the wall time of the batch, the session time of the batch, the tokens of the batch and the
  cost of every role of the batch.

### [g2] A batch measured keeps its review findings by grade
- [r2] When the person measures a batch that has a proposed change, the measurement service shall keep a measurement of
  the batch and return the number of review findings on the proposed change whose grade is `Critical`, the number of
  review findings on the proposed change whose grade is `Important` and the number of review findings on the proposed
  change whose grade is `Minor`.

### [g3] A defect reported in a delivered item is kept for its batch
- [r3] While an item in a batch is `delivered`, when the person reports a defect in the item, the measurement service
  shall keep a defect for the batch that the item has.

### [g4] Two batches compared give their measurements and a ratio
- [r4] When the person compares two batches, the measurement service shall return two measurements and a ratio.

### [g5] A measurement viewed gives the round trips of a stage row
Restates: batch-measurement#r44@0.29, batch-measurement#r54@0.29.
- [r5] When the person views a measurement that has a stage row that has a round trip, the measurement service shall
  return the number of round trips of the stage row, every stage row of the measurement and the total row of the
  measurement.
```given
the measurement `m1` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
```

### [g6] A measurement viewed gives no round trip of a stage row that has none
Restates: batch-measurement#r56@0.29.
- [r6] When the person views a measurement that has a stage row that has no round trip, the measurement service shall
  return every stage row of the measurement and not return a round trip.
```given
the measurement `m2` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
```

### [g7] A measurement viewed gives the tool uses, dispatches and compactions of a session row
Restates: batch-measurement#r61@0.29.
- [r7] When the person views a measurement that has a session row, the measurement service shall return the number of
  tool uses of the session row, every dispatch of the session row and the number of compactions of the session row.
```given
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```

### [g8] Two measurements compared give their total rows and a ratio
Restates: batch-measurement#r45@0.29.
- [r8] When the person compares two measurements, the measurement service shall return two total rows and a ratio.
```given
the measurement `m1` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```

### [g9] A measurement compared gives its tool uses and compactions
Restates: batch-measurement#r62@0.29.
- [r9] When the person compares a measurement that has a session row, the measurement service shall return the number of
  tool uses in the measurement and the number of compactions in the measurement.
```given
the measurement `m3` holds:
  {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
```
