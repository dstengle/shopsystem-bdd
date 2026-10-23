# Plan of w102: measure reads what i22 left (empty session.json, Unicode line breaks, Z times)

Capability `batch-measurement`; accepts r47, r57, r58, r59. No Retires section, no Rulings. Planned from
`runs/w102/1-research/notes.md`, with `scripts/measure_read.py`, `scripts/measure_build.py` and
`scripts/supervise_worker.py` (`run_dir`, `worker`) read for decision 1.

## 1. What goes green

- **r47**: "a <file kind> of a shape measure does not know is refused, naming it" (session.json and transcript
  rows). Green today (notes §1, run), and must stay green: the r57 and r58 changes must not stop the refusal of
  `["not","a","session"]` or `this is not a transcript`. The `@r47 @deprecated` outline is also green today and stays
  that way. This work-item does not retire it.
- **r58**: "a transcript line with <line break> inside a JSON string is read as one line" (U+2028, U+2029, U+0085).
  Red because the step "the text of one of those messages holds <line break> inside its JSON string" is missing. In
  the code behind it, `measure_read.json_rows` splits on `splitlines()`, so the fragment is refused as "not a JSON
  object" (probe 1, D1). The helper `store_session` also writes with `json.dumps`'s default `ensure_ascii`, which
  escapes the break, so the scenario would pass for the wrong reason unless the helper writes the raw character
  (notes §2.14).
- **r59**: "a time ending in Z in <file> is read as a time in UTC" (log.jsonl and transcript rows). Red only on steps:
  "the session's local time zone is UTC+05:00", "the directory sessions holds the transcript s-9, starting at … and
  ending at …", "the measurement gives the session s-9", and `gives_totals` raising KeyError on a table that has only
  a time column. The code already reads Z as UTC on Python 3.11 (probe 3).
- **r57**: "a stage whose session.json is empty is given without its session's figures, named as such". Red because
  the steps "that stage was run as the agent researcher", "that stage's session.json is empty", "the measurement
  gives no turns, output tokens, new input tokens, cache-read tokens or cost for the stage" and "the measurement names
  the stage as a stage whose session.json is empty" are missing. In the code, `read_session_json` refuses the empty
  file and the whole run is refused (probes 5–7, D2).

## 2. Where the change lands

- `scripts/measure_read.py`
  - `json_rows` splits lines on `\n` only (decision 4).
  - `read_session_json` gives a named "empty" result for a zero-byte file. Anything else that is not the known shape
    is still refused (decisions 2, 3).
  - `read_session_jsons` returns two things: the non-empty files by session id, as today, and the empty files by
    their place, i.e. work-item and run directory (decision 1).
- `scripts/measure_build.py`
  - `stages_of` matches an empty session.json to its stage (decision 1). It gives that stage the empty marker and no
    turns, tokens or cost, and keeps its round trips (decision 5).
  - `figures_of`: the `sessions` total waits on question C.
- `tests/scenarios/batch_measurement_given_steps.py`: new Givens for:
  - "that stage was run as the agent {agent}" with no session named (the World makes up the session id);
  - "that stage's session.json is empty";
  - "the session's local time zone is UTC+05:00";
  - the single-transcript s-9 line with start and end;
  - "the text of one of those messages holds {line break} inside its JSON string".
- `tests/scenarios/batch_measurement_then_steps.py`:
  - Thens for "no turns, … or cost for the stage", "names the stage as a stage whose session.json is empty" and
    "the measurement gives the session {name}";
  - `gives_totals` checks only the columns its table gives.
- `tests/scenarios/batch_measurement_transcripts.py`: `store_session` can take a message text and writes the raw
  character (no ASCII escaping) when given one. Its default output is unchanged for r53 and r55.
- `tests/scenarios/batch_measurement_world.py`:
  - `session()` can write an empty session.json in the stage's run directory;
  - `run` puts the local time zone a Given asked for into effect and puts it back afterwards.

This is the researcher's file set unchanged. `scripts/measure` (its CONTRACT text) and `measure_show.py` are on the
path, but no decision requires editing them. Every file stays under 300 lines (largest today: given_steps at 213).

## 3. Decisions

1. **Which stage an empty session.json belongs to.** An empty file has no session id, so it is matched by its place.
   `runs/<work-item>/<k>-<stage>/session.json` belongs to the n-th start of that work-item's stage in `log.jsonl`,
   where n is the directory's rank among that work-item's `<k>-<stage>` directories, in increasing k.
   - Why: `work run` picks the next k and writes the start row under the same lock, one run at a time per work-item
     (supervise_worker `worker` / `run_dir`). So the order of the run directories is the order of the starts.
   - Non-empty files keep matching by `session_id`, as today.
   - This answers the notes' question A. Under it the narrator sees the stage that actually ran in that directory,
     which is what r57 asks.
   - Rests on: batch-measurement#r57, and the Implementation note that a stage's figures are read from its stage
     directory's `session.json`.
2. **"Empty" means zero bytes.** A session.json that holds only whitespace is not empty and stays refused, naming the
   file. This answers question D.
   - Rests on: r47 ("not empty … not of a shape measure knows" is refused) and design-decision
     measure-refuses-unknown-shapes (refuse rather than guess).
3. **What the stage carries.** A stage whose session.json is empty is given with work-item, stage, agent, session
   (from `log.jsonl`) and how long it took, plus a marker naming its session.json as empty. It has no turns, output
   tokens, new input tokens, cache-read tokens or cost keys. The implementer names the marker.
   - Rests on: r57, r40.
4. **One line reader for both files.** `json_rows` splits on `\n` only, for transcripts and for `log.jsonl` alike.
   - So a log row holding a raw U+2028 inside a JSON string is read, not refused (D3).
   - Blank lines are still skipped. A line that is not a JSON object is still refused, naming the file and line.
   - Why: r58 states how a JSON line is read, and log.jsonl and transcripts share that reader today. Under
     measure-refuses-unknown-shapes, a refusal is for unknown shapes, and a valid JSON object on one line is a known
     shape.
   - Rests on: r58, measure-refuses-unknown-shapes.
5. **Round trips stay for an empty session.json.** The round trips are still read from the session's transcript in
   the store, under the session id `log.jsonl` gives, and still count in the round-trip total. This answers question
   B.
   - Why: r53 gives round trips "for each stage it gives". r55 is the one case that drops them, and it is about the
     transcript, not the session.json. The "session's figures" r57 withholds are the ones r40 lists (turns, tokens,
     cost), and the r57 scenario asserts exactly those absent.
   - Rests on: r53, r55, r57, r40.
6. **Z times: no production change.** `moment` already reads Z as UTC (probe 3). The measurement's file date stays
   the local day; r39's "the day it is run" is untouched by r59, so D6 is not this work-item's to change.
   - Rests on: r59, r39.
7. **r47 kept.** The refusal of non-empty unknown session.json files and transcripts is unchanged. Only the zero-byte
   session.json (decision 2) leaves that path.
   - Rests on: r47.

## 4. Tests the decisions break

None among the test functions. Checked in the notes (§4, by search, since there is no coverage map): only
`tests/scenarios/test_batch_measurement.py` and the batch_measurement step modules touch measure. The r47 rows use
non-empty files that decisions 2 and 7 still refuse, and the r53/r55 rows use `store_session`'s default output,
which stays as it is. Two shared step pieces change, but no test is removed:

- the step `gives_totals` (batch_measurement_then_steps.py) is rewritten to check only the columns its table gives.
  The r42 table, which has every column, still checks every total;
- the helper `store_session` (batch_measurement_transcripts.py) gains a raw-text option for r58.

Decision 4 changes how `log.jsonl` is read only for a raw Unicode break. No existing scenario writes one (r40, r41,
r42, r51 and r59 logs are ASCII, per the notes).

## 5. Open cases (for the implementer to name, not to choose)

- More `<k>-<stage>` directories than starts of that stage, or the reverse (a run directory left without a start
  row): what decision 1's match does with the extra one.
- An empty session.json under a run directory whose stage has no start in `log.jsonl` at all.
- The review stage, which `supervise_review` logs without a work-item: where its session.json lives, and whether
  decision 1 reaches it.
- Whether `measure show` prints the empty marker beside the stage. r44 says show prints the figures; no scenario
  covers it.
- A zero-byte store transcript gives `round_trips: 0`, while no transcript gives none (nearest 12). Unchanged here.
- Two stages naming one session both take its figures (D4), and `--sessions` naming a missing directory is silent
  (D5). Both are out of these requirements and unchanged.
- `merged_commits` still uses `splitlines()` on git output. r58 does not cover it.
- How the scenarios' local time zone is put into effect in-process, and restored afterwards.
- The `sessions` total for a stage whose session.json is empty: see the question in the result.
