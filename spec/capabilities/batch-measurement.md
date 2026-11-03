---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Measurement of an initiative's deliveries
narrator: a session measuring an initiative's deliveries
group: service
language: codified-1
rests_on: [design-decision/measure-an-initiative, design-decision/measure-refuses-unknown-shapes, design-decision/plugin-takes-the-dependencies-it-needs]
retired: []
---

# Measurement of an initiative's deliveries

## Purpose
`scripts/measure` writes one measurement of an initiative's deliveries from what `work run` already records: the
initiative's `log.jsonl`, each stage's `session.json` and the sessions' transcripts. It reads measurements back as
tables and compares two of them. It writes no prompt, reply or tool content, and refuses a file of a shape it does
not know rather than guessing at it.

## Terms
- **initiative log** (kind): the `log.jsonl` of an initiative.
- **unwritten** (condition of initiative log): `work run` has written no `log.jsonl` for the initiative.
- **requestless** (condition of initiative log): the log's initiative fulfils no request.
- **overfulfilling** (condition of initiative log): the log's initiative fulfils more than one request.
- **session file** (kind): a stage's `session.json`, what `claude -p --output-format json` printed for its session.
- **content** (attribute of session file): whether the session file holds a session, nothing, or a shape `measure`
  does not know. Values: `filled`, `empty`, `garbled`.
- **transcript** (kind): a session's JSONL transcript, in Claude Code's own rows or the slim export's.
- **availability** (attribute of transcript): whether `measure` finds the transcript and knows its shape.
  Values: `found`, `lost`, `unreadable`.
- **fulfilled request** (kind): a request the measured initiative fulfils, named by its id.
- **standing** (attribute of fulfilled request): whether the queue holds the request with an asker, and whether that
  asker is this bounded context. Values: `internal`, `external`, `unheld`, `askerless`.
- **logged stage** (kind): a stage the initiative log gives a start for, run in one session.
- **ending** (attribute of logged stage): whether the initiative log gives the stage an end. Values: `ended`, `unended`.
- **present** (condition of measurement): a measurement of the initiative on the day is already written.
- **include** (event): `measure` puts a figure or a name into the measurement it writes. Forms: includes, included.

## Behaviour

### [g1] `measure initiative` writes one measurement named by the day and the initiative, each ended stage with how long it took and its session's figures
Restates: r39@0.29, r40@0.29.
- [r1] While a logged stage is `ended`, when the person runs `measure initiative i7-cart`, `measure` shall print `.shop/records/measurements/2026-10-22-i7-cart.md`, include "12 minutes", include "output_tokens", include "cache_read_tokens", include "cost" and exit successfully.

### [g2] `measure initiative` refuses an initiative with no `log.jsonl`
Restates: r46@0.29, r50@0.29.
- [r2] While an initiative log is unwritten, if the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming `log.jsonl` and change nothing.

### [g3] `measure initiative` refuses an initiative fulfilling a request the queue does not hold
Restates: r65@0.29.
- [r3] While a fulfilled request is `unheld`, if the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the fulfilled request and change nothing.

### [g4] `measure initiative` refuses an initiative fulfilling a request with no asker
Restates: r66@0.29.
- [r4] While a fulfilled request is `askerless`, if the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the fulfilled request and change nothing.

### [g5] `measure initiative` refuses an initiative fulfilling more than one request
Restates: r67@0.29.
- [r5] While an initiative log is overfulfilling, if the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming "more than one request" and change nothing.

### [g6] `measure initiative` refuses a `session.json` of a shape it does not know, naming it
Restates: r47@0.29.
- [r6] While a session file is `garbled`, if the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the session file and change nothing.

### [g7] `measure initiative --sessions` refuses a transcript of a shape it does not know, naming it
Restates: r47@0.29.
- [r7] While a transcript is `unreadable`, if the person runs `measure initiative i7-cart --sessions sessions`, then `measure` shall exit with an error naming the transcript and change nothing.

### [g8] each stage is given with its session's round trips, a line break inside a transcript's JSON string not splitting its line
Restates: r53@0.29, r58@0.29.
- [r8] While a transcript is `found`, when the person runs `measure initiative i7-cart`, `measure` shall include "round_trips" and exit successfully.

### [g9] each work-item is given with its transitions, its counts of `awaiting-answer` and `failed`, and its commits, and the totals span the first transition to the last, a time ending in `Z` read as a time in UTC
Restates: r41@0.29, r42@0.29, r59@0.29.
- [r9] When the person runs `measure initiative i7-cart`, `measure` shall include "transitions", include "awaiting_answer", include "commits", include "totals", include "time_seconds" and include "1 hour 45 minutes".

```given
the initiative log `i7-cart` holds:
  {"time": "2026-10-22T07:55:00Z", "work-item": "cart-1", "before": "drafted", "after": "researched"}
  {"time": "2026-10-22T08:30:00Z", "work-item": "cart-1", "before": "researched", "after": "awaiting-answer"}
  {"time": "2026-10-22T11:40:00+02:00", "work-item": "cart-1", "before": "awaiting-answer", "after": "researched"}
```

### [g10] `measure initiative` does not write over a measurement without `--replace`
Restates: r48@0.29.
- [r10] While a measurement is present, if the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the measurement and change nothing.

### [g11] `measure initiative --replace` writes over the measurement
Restates: r52@0.29.
- [r11] While a measurement is present, when the person runs `measure initiative i7-cart --replace`, `measure` shall print `.shop/records/measurements/2026-10-22-i7-cart.md` and include "12 minutes".

### [g12] a stage with a start and no end is given without how long it took
Restates: r51@0.29.
- [r12] While a logged stage is `unended`, when the person runs `measure initiative i7-cart`, `measure` shall include "turns", and `measure` shall not include "took".

### [g13] a stage whose `session.json` is empty is given without its session's figures, named as such
Restates: r57@0.29.
- [r13] While a session file is `empty`, when the person runs `measure initiative i7-cart`, `measure` shall include "session_json", and `measure` shall not include "turns".

### [g14] a stage whose session has no transcript is given without its round trips
Restates: r55@0.29.
- [r14] While a transcript is `lost`, when the person runs `measure initiative i7-cart`, `measure` shall not include "round_trips".

### [g15] the request an initiative fulfils is given as internal or external
Restates: r63@0.29.
- [r15] While a fulfilled request is `internal`, when the person runs `measure initiative i7-cart`, `measure` shall include "internal".

### [g16] an initiative that fulfils no request is measured without an origin
Restates: r64@0.29.
- [r16] While an initiative log is requestless, when the person runs `measure initiative i7-cart`, `measure` shall not include "origin".

### [g17] `--sessions` gives the sessions active inside the window and the sessions they dispatched, each with its round trips, tool uses, dispatches and compactions, and no prompt, reply or tool content
Restates: r43@0.29, r49@0.29, r60@0.29.
- [r17] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall include "s-9", include "s-11", include "tool_uses" and include "compactions", and `measure` shall not include "s-7", include "a secret reply" or include "a secret prompt".

```given
the initiative log `i7-cart` holds:
  {"time": "2026-10-22T09:55:00+00:00", "work-item": "cart-1", "before": "drafted", "after": "researched"}
  {"time": "2026-10-22T10:00:00+00:00", "event": "start", "work-item": "cart-1", "stage": "research", "session": "s-1"}
  {"time": "2026-10-22T10:12:00+00:00", "event": "end", "work-item": "cart-1", "stage": "research", "session": "s-1"}
  {"time": "2026-10-22T11:40:00+00:00", "work-item": "cart-1", "before": "researched", "after": "planned"}
```

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
  body, which `show` and `compare` read back.
- A stage's start and end, and a work-item's transitions, are read from the initiative's `log.jsonl`; a stage's
  session's turns, tokens and cost from its stage directory's `session.json`.
- A stage's turns are its `session.json`'s `num_turns`, which is not the unit `--max-turns` limits
  (measurement/2026-10-22-research-at-the-limit); its round trips (r8) are that unit.
- r8: a stage's session's transcript is read from the path its `session.json` records (supervision r62).
- The initiative's window runs from the first transition `log.jsonl` gives to the last.
- Tokens are output, new input (input and cache writes) and cache read.
- `--sessions` reads Claude Code's raw transcripts or the slim export of dstengle/shopsystem-records; the sessions
  it finds are those that did the spec work around the delivery: the coordinator, its rounds and its direct
  dispatches.
- r12: a stage with a start and no end is given with everything r1 gives, its session's figures included where its
  `session.json` is there, except how long it took.
- r9: the commits merged for a work-item are the commits of its work-item branch that its merge brought into the
  initiative branch.
- r9: the totals are over the stages' sessions only, with or without `--sessions`, and a stage with a start and no
  end counts in them.
- r17: each session it dispatched is each session dispatched by a session found inside the window, wherever its
  dispatches fall in time.

## Not yet
- Figures beyond what `work run` already records: the skeleton grows from the measurements of 0.21.0's, 0.22.0's
  and 0.23.0's deliveries; a line is added when one of those measurements needs a figure the measurement does not
  give.

## Dropped
