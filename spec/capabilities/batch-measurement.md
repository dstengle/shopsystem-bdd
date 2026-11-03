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
- **initiative log** (kind): the `log.jsonl` of an initiative: its transitions and each stage's start and end.
- **session file** (kind): a stage's `session.json`, what `claude -p --output-format json` printed for its session.
- **transcript** (kind): a session's JSONL transcript: Claude Code's own rows or the slim export's.
- **fulfilled request** (kind): a request the measured initiative fulfils, named by its id.
- **origin** (attribute of fulfilled request): whether the queue holds the request with an asker, and whether that
  asker is this bounded context. Values: `internal`, `external`, `unheld`, `askerless`.
- **logged stage** (kind): a stage the initiative log gives a start for, run in one session.
- **ending** (attribute of logged stage): whether the initiative log gives the stage an end. Values: `ended`, `unended`.
- **content** (attribute of session file): Values: `filled`, `empty`.
- **presence** (attribute of transcript): whether `measure` finds the session's transcript. Values: `found`, `lost`.
- **include** (event): `measure` puts a figure or a name into the measurement it writes. Forms: includes, included.

## Behaviour

### [g1] `measure initiative` writes one measurement named by the day and the initiative
Restates: r39@0.29.
- [r1] When the person runs `measure initiative i7-cart`, `measure` shall print `.shop/records/measurements/2026-10-22-i7-cart.md`.
- [r2] When the person runs `measure initiative i7-cart`, `measure` shall exit successfully.

```given
an initiative log `i7-cart`
```

### [g2] `measure initiative` refuses an initiative with no `log.jsonl`
Restates: r46@0.29, r50@0.29.
- [r3] If the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming `log.jsonl` and change nothing.

### [g3] `measure initiative` refuses an initiative fulfilling a request the queue does not hold
Restates: r65@0.29.
- [r4] If the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the fulfilled request and change nothing.

```given
an initiative log `i7-cart`
a fulfilled request q1 that is `unheld`
```

### [g4] `measure initiative` refuses an initiative fulfilling a request with no asker
Restates: r66@0.29.
- [r5] If the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the fulfilled request and change nothing.

```given
an initiative log `i7-cart`
a fulfilled request q1 that is `askerless`
```

### [g5] `measure initiative` refuses an initiative fulfilling more than one request
Restates: r67@0.29.
- [r6] If the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming "more than one request" and change nothing.

```given
an initiative log `i7-cart`
a fulfilled request q1 that is `external`
a fulfilled request q2 that is `external`
```

### [g6] `measure initiative` refuses a `session.json` of a shape it does not know, naming it
Restates: r47@0.29.
- [r7] If the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the session file and change nothing.

```given
an initiative log `i7-cart`
the session file `s-1` holds "not a session"
```

### [g7] `measure initiative --sessions` refuses a transcript of a shape it does not know, naming it
Restates: r47@0.29.
- [r8] If the person runs `measure initiative i7-cart --sessions sessions`, then `measure` shall exit with an error naming the transcript and change nothing.

```given
an initiative log `i7-cart`
the transcript `sessions/s-9.jsonl` holds "this is not a transcript"
```

### [g8] a line break inside a transcript's JSON string does not split its line
Restates: r58@0.29.
- [r9] While a transcript is `found`, when the person runs `measure initiative i7-cart`, `measure` shall include "round_trips".
- [r10] While a transcript is `found`, when the person runs `measure initiative i7-cart`, `measure` shall exit successfully.

```given
an initiative log `i7-cart`
a transcript `u2028` that is `found`
```

### [g9] a time ending in `Z` is read as a time in UTC
Restates: r59@0.29.
- [r11] When the person runs `measure initiative i7-cart`, `measure` shall include "1 hour 45 minutes".

```given
an initiative log `zulu`
```

### [g10] `measure initiative` does not write over a measurement without `--replace`
Restates: r48@0.29.
- [r12] If the person runs `measure initiative i7-cart`, then `measure` shall exit with an error naming the measurement and change nothing.

```given
an initiative log `i7-cart`
the measurement `2026-10-22-i7-cart` holds "an earlier measurement"
```

### [g11] `measure initiative --replace` writes over the measurement
Restates: r52@0.29.
- [r13] Where `--replace` is given, when the person runs `measure initiative i7-cart`, `measure` shall print `.shop/records/measurements/2026-10-22-i7-cart.md`.
- [r14] Where `--replace` is given, when the person runs `measure initiative i7-cart`, `measure` shall include "12 minutes".

```given
an initiative log `i7-cart`
the measurement `2026-10-22-i7-cart` holds "an earlier measurement"
```

### [g12] each stage with a start and an end is given with how long it took and its session's figures
Restates: r40@0.29.
- [r15] While a logged stage is `ended`, when the person runs `measure initiative i7-cart`, `measure` shall include "12 minutes".
- [r16] While a logged stage is `ended`, when the person runs `measure initiative i7-cart`, `measure` shall include "output_tokens".
- [r17] While a logged stage is `ended`, when the person runs `measure initiative i7-cart`, `measure` shall include "cache_read_tokens".
- [r18] While a logged stage is `ended`, when the person runs `measure initiative i7-cart`, `measure` shall include "cost".

```given
a logged stage `cart-1` that is `ended`
```

### [g13] a stage with a start and no end is given without how long it took
Restates: r51@0.29.
- [r19] While a logged stage is `unended`, when the person runs `measure initiative i7-cart`, `measure` shall include "turns".
- [r20] While a logged stage is `unended`, when the person runs `measure initiative i7-cart`, `measure` shall not include "took".

```given
a logged stage `cart-1` that is `unended`
```

### [g14] a stage whose `session.json` is empty is given without its session's figures, named as such
Restates: r57@0.29.
- [r21] While a session file is `empty`, when the person runs `measure initiative i7-cart`, `measure` shall include "session_json".
- [r22] While a session file is `empty`, when the person runs `measure initiative i7-cart`, `measure` shall not include "turns".

```given
an initiative log `i7-cart`
a session file `s-1` that is `empty`
```

### [g15] each stage is given with its session's round trips
Restates: r53@0.29.
- [r23] While a transcript is `found`, when the person runs `measure initiative i7-cart`, `measure` shall include "round_trips".

```given
an initiative log `i7-cart`
a transcript `s-1` that is `found`
```

### [g16] a stage whose session has no transcript is given without its round trips
Restates: r55@0.29.
- [r24] While a transcript is `lost`, when the person runs `measure initiative i7-cart`, `measure` shall not include "round_trips".

```given
an initiative log `i7-cart`
a transcript `s-1` that is `lost`
```

### [g17] each work-item is given with its transitions, its counts of `awaiting-answer` and `failed`, and its commits
Restates: r41@0.29.
- [r25] When the person runs `measure initiative i7-cart`, `measure` shall include "transitions".
- [r26] When the person runs `measure initiative i7-cart`, `measure` shall include "awaiting_answer".
- [r27] When the person runs `measure initiative i7-cart`, `measure` shall include "commits".

```given
an initiative log `transitions`
```

### [g18] the totals are over the stages' sessions and span the first transition to the last
Restates: r42@0.29.
- [r28] When the person runs `measure initiative i7-cart`, `measure` shall include "totals".
- [r29] When the person runs `measure initiative i7-cart`, `measure` shall include "time_seconds".

```given
an initiative log `transitions`
```

### [g19] the request an initiative fulfils is given as internal or external
Restates: r63@0.29.
- [r30] When the person runs `measure initiative i7-cart`, `measure` shall include "internal".

```given
an initiative log `i7-cart`
a fulfilled request q1 that is `internal`
```

### [g20] an initiative that fulfils no request is measured without an origin
Restates: r64@0.29.
- [r31] When the person runs `measure initiative i7-cart`, `measure` shall not include "origin".

```given
an initiative log `i7-cart`
```

### [g21] `--sessions` gives the sessions active inside the window, and the sessions they dispatched
Restates: r43@0.29.
- [r32] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall include "s-9".
- [r33] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall include "s-11".
- [r34] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall not include "s-7".

```given
an initiative log `window`
a transcript `sessions`
```

### [g22] each session `--sessions` gives is given with its round trips, tool uses, dispatches and compactions
Restates: r60@0.29.
- [r35] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall include "tool_uses".
- [r36] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall include "compactions".

```given
an initiative log `window`
a transcript `sessions`
```

### [g23] the measurement holds no prompt, reply or tool content
Restates: r49@0.29.
- [r37] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall not include "a secret reply".
- [r38] When the person runs `measure initiative i7-cart --sessions sessions`, `measure` shall not include "a secret prompt".

```given
an initiative log `secret`
```

### [g24] `measure show` prints a measurement's figures as tables, a stage's round trips beside its turns
Restates: r44@0.29, r54@0.29.
- [r39] When the person runs `measure show m1.md`, `measure` shall print "stages", "totals" and "round trips".

```given
a measurement `m1`
```

### [g25] `measure show` prints the stages of a measurement that gives no round trips without them
Restates: r56@0.29.
- [r40] When the person runs `measure show m2.md`, `measure` shall not print "round trips".

```given
a measurement `m2`
```

### [g26] `measure show` prints each session's round trips, tool uses, dispatches and compactions
Restates: r61@0.29.
- [r41] When the person runs `measure show m3.md`, `measure` shall print "tool uses", "dispatched" and "compactions".

```given
a measurement `m3`
```

### [g27] `measure compare` prints two measurements' totals side by side with the ratio of the second to the first
Restates: r45@0.29.
- [r42] When the person runs `measure compare m1.md m3.md`, `measure` shall print "ratio".

```given
a measurement `m1`
a measurement `m3`
```

### [g28] `measure compare` prints the totals over the sessions side by side with their ratio
Restates: r62@0.29.
- [r43] When the person runs `measure compare m3.md m3.md`, `measure` shall print "tool uses" and "compactions".

```given
a measurement `m3`
```

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

## Dropped
