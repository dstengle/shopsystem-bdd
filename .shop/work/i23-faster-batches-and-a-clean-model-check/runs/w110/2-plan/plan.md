# Plan of w110: measure reads what i22 left

Work-item w110 accepts batch-measurement#r47, #r57, #r58, #r59. Planned from the research notes
(`runs/w110/1-research/notes.md`), the capability, design-decisions 0018 and 0060, the feature and the work-item's
ruling.

## 1. What goes green

- **batch-measurement#r47**, "a <file kind> of a shape measure does not know is refused, naming it" (session.json,
  transcript). Green today (run): their input is non-empty and is already refused, naming the file. It must stay
  green after r57 changes the session.json reading.
- **batch-measurement#r57**, "a stage whose session.json is empty is given without its session's figures, named as
  such". Red: undefined steps ("that stage was run as the agent researcher", "that stage's session.json is empty",
  the two Thens about no figures and the name). Behind the steps, `measure_read.read_session_json` refuses an empty
  file (probe: rc 1, nothing written), and `measure_build.stages_of` has no mark saying why a stage has no figures.
- **batch-measurement#r58**, "a transcript line with <line break> inside a JSON string is read as one line"
  (U+2028, U+2029, U+0085). Red: undefined Given about the line break and Then "measure exits successfully".
  Behind them, `measure_read.json_rows` uses `str.splitlines`, which splits on those characters; the half line is
  refused as "not a JSON object" (probe D1).
- **batch-measurement#r59**, "a time ending in Z in <file> is read as a time in UTC" (log.jsonl, a transcript). Red
  at steps only: undefined Givens (local time zone, the single transcript s-9 with start and end), undefined Thens
  ("measure exits successfully", "the measurement gives the session s-9"); step defects in
  `transitions_between` (ISO time fed through `stamp`) and `gives_totals` (KeyError on a table with only `time`).
  The code already reads Z as UTC (probe, both examples).
- **Retired**: "a <file kind> of a shape measure does not know is refused, naming it (deprecated)" (@r47 @deprecated,
  both examples), per the work-item's Retires (delivery#r17). Its Scenario Outline is removed from the feature.

## 2. Where the change lands

- `scripts/measure_read.py`: `json_rows` splits a file on the newline character only, still skipping blank lines
  (r58); `read_session_json` / `read_session_jsons` give an empty session.json as "empty" for its stage directory
  instead of refusing, and still refuse every non-empty unknown shape (r47, r57).
- `scripts/measure_build.py`: `stages_of` gives a stage whose session.json is empty without figures and with a mark
  naming it as such (r57); totals unchanged (ruling).
- `scripts/measure`: the CONTRACT text says an empty session.json gives its stage without figures, named, and that a
  non-empty file of an unknown shape is refused.
- `tests/scenarios/batch_measurement_given_steps.py`: "that stage was run as the agent {agent}", "that stage's
  session.json is empty"; `transitions_between` takes full ISO times as given.
- `tests/scenarios/batch_measurement_then_steps.py`: "the measurement gives no turns, output tokens, new input
  tokens, cache-read tokens or cost for the stage", "the measurement names the stage as a stage whose session.json
  is empty"; `gives_totals` checks only the columns its table gives.
- `tests/scenarios/batch_measurement_reading_steps.py` (new, added by decision 7): the r58/r59 steps: the line
  break in one message's text, the session's local time zone, the directory sessions holding the single transcript
  s-9 with its start and end, "measure exits successfully", "the measurement gives the session s-9".
- `tests/scenarios/test_batch_measurement.py`: imports the new steps module (added by decision 7).
- `tests/scenarios/batch_measurement_world.py`: the World can hold a stage's session.json as an empty file and
  the time zone setting for the in-process run.
- `tests/scenarios/batch_measurement_transcripts.py`: a helper putting a given character into one store row's text
  (or the s-9 slim transcript with explicit start and end), if the steps need it there.
- `features/batch-measurement.feature`: the deprecated @r47 Scenario Outline (lines 22-35) removed.

Read, not edited: `scripts/measure_show.py` (decision 5), `scripts/measure_write.py`,
`tests/scenarios/batch_measurement_show_steps.py`.

## 3. Decisions

1. **"Empty" is a session.json of zero bytes.** A file holding only whitespace is not empty and stays refused as
   an unknown shape, naming it. Rests on batch-measurement#r47 ("a session.json that is not empty") read
   literally, and design-decision/measure-refuses-unknown-shapes (refuse rather than guess).
2. **An empty session.json is tied to its stage by its stage directory** (work-item and stage under `runs/`), not by
   session id, which an empty file does not have. The stage is given with what log.jsonl gives it (work-item,
   stage, agent, took) and no turns, tokens or cost; with no recorded transcript path it has no round trips, as
   r55 gives. Rests on batch-measurement#r57, #r40, #r55.
3. **The name is a field on the stage's entry in the measurement's figures block**, saying its session.json is
   empty; a stage whose session.json is absent gets no such field (the notes' D3 is not this work). Rests on
   batch-measurement#r57 and the Implementation note that the figures are one JSON block `show` reads back.
4. **Totals: `sessions` counts only the sessions whose session.json gave figures**, so an empty-session.json stage
   counts in `stages` and not in `sessions`; a stage with a start, no end and no session.json the same. Ruling in
   the work-item (reading B, 2026-10-23), batch-measurement#r42.
5. **`measure show` is not changed.** No accepted requirement asks it to print the new mark; r44/r54/r56 name what
   it prints, and the stage already prints without turns where it has none. Rests on batch-measurement#r44, #r56.
6. **A transcript or log.jsonl line is split on the newline character only**; blank lines are still skipped and a
   trailing carriage return is left to JSON reading as whitespace. Rests on batch-measurement#r58. The `moment`
   reading of times is unchanged: Z is already UTC (probe), lowercase z stays refused. Rests on #r59.
7. **The r58/r59 steps go in a new module `batch_measurement_reading_steps.py`**, imported by
   `test_batch_measurement.py`: `batch_measurement_given_steps.py` has 213 lines and the r57 steps, the
   `transitions_between` change and the r58/r59 steps together risk the 300-line limit (CLAUDE.md, one step module
   a concern).
8. **The time zone step sets the local time zone for the in-process run and restores it after the scenario**
   (environment through the scenario's monkeypatch, re-read by the time module), since the When runs `measure`
   in-process. Rests on batch-measurement#r59.

## 4. Tests the decisions break

- `features/batch-measurement.feature`, the "(deprecated)" @r47 outline, both examples in
  `tests/scenarios/test_batch_measurement.py`: removed, retired by the work-item (delivery#r17); its live
  replacement (the "not empty" outline) keeps the refusal covered.
- `tests/scenarios/batch_measurement_then_steps.py:gives_totals`: broken by the r59 scenario's table, which gives
  only `time`; rewritten to compare only the columns the table names, so the r42 tables that give stages and
  sessions still assert them.
- `tests/scenarios/batch_measurement_given_steps.py:transitions_between`: rewritten so a full ISO time in the step
  is written to log.jsonl as given, a clock time still going through `stamp`; the r41/r42 scenarios using clock
  times assert what they did.
- Nothing else: the notes found by search no test in `tests/scripts/` that drives `measure_read`, `measure_build`,
  `measure_show` or `measure_write`, no test of the empty-session.json refusal and none of `splitlines` behaviour;
  the non-deprecated r47 pair writes non-empty files, so decision 1 keeps it green.

## 5. Open cases

- A session.json holding only whitespace or a newline: refused under decision 1; no scenario says so.
- An empty transcript under `--sessions` is read as no session while an empty session.json now gives a named
  stage (notes D2); not in the accepted scenarios.
- A stage whose session.json is absent is given with no figures and no name (notes D3); not in the scenarios.
- An empty session.json in a stage directory that log.jsonl gives no start for; the scenarios are silent.
- A U+2028 inside a log.jsonl string (r58 names transcripts only; decision 6's split applies to both readers).
