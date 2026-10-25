# plan of w179: a result field too long to be a file name is taken as no file (supervision#r15)

## 1. What goes green

supervision#r15: "When `work run` removes a worker's worktree, `work run` shall first copy each file the worker's result names into its stage directory."

- "a file the worker's result names is copied into the stage directory before its worktree is removed" (features/supervision.feature:352). Passes today (notes §1): `Workers.keep_named` already copies before `Supervisor.step` removes the worktree. Must stay green.
- "a field of a worker's result giving a sentence longer than a file name may be is taken as no file" (features/supervision.feature:360). Red today for two reasons, in order (notes §1, §2):
  1. its Given "the implementer's result also gives a field whose value is a sentence of over 255 characters, with spaces, naming no file" has no step definition (StepDefinitionNotFoundError);
  2. once it has one, `Workers.keep_named` asks the file system whether the sentence is a file and gets `OSError [Errno 36] File name too long` (probes P1, P4, P10); the exception ends the worker, so "w1 is green" fails even though report.md was already copied.

Retires: none (the work-item has no `## Retires`; no scenario of r15 is deprecated).

## 2. Where the change lands

- `scripts/supervise_worker.py` (247 lines): `Workers.keep_named` takes a field value the file system refuses as a path as no file: it skips that value and goes on with the other fields, so a refused value neither copies anything nor raises. No other function changes; the call in `Workers.worker` stays where it is, before the worktree's removal.
- `tests/scenarios/supervision_given.py` (259 lines): one new given for the step above, beside the report given (199-202), adding to the implementer's planned result (the stub's `fields` for `bdd-implementer`) one field whose value is a sentence of over 255 characters with spaces. The stub (`tests/scripts/stub_claude.py`) already writes `fields`; it does not change.

Unchanged and not in the set: `tests/scenarios/test_supervision.py` (already binds the feature and imports the givens), `scripts/supervise.py`, `scripts/supervise_pool.py` and the other callers of `worker()` (notes §3: they get the fix through `worker()`). Both edited files stay well under 300 lines.

## 3. Decisions

- **D1. How a value is judged "no file": by the file system's refusal, not by a length count.** `keep_named` treats a value as no file when resolving it or checking it as a file raises `OSError` or `ValueError`, besides the cases it already skips (empty values, `status`, `summary`, paths outside the worktree, paths that are not files). Not a guard by character count: the notes show the limit is per byte and per file system (a 203-byte accented name fails with errno 95, P11; a 255-char ASCII name passes, P3), so a count would both miss refusals and depend on the file system. Rests on supervision#r15 (only what the result *names* is copied; text that the system cannot take as a name names nothing) and design-decision/worker-results-are-files (a result's stage fields are what `work run` reads; its prose fields are not paths to fail on).
- **D2. The refusal is per value, not per result.** A refused value is skipped and the remaining fields are still tried, so files named after or before the sentence are still copied (P10 shows report.md is copied before the sentence in the stub's order; the scenario's Then needs it either way). Rests on supervision#r15 ("each file the worker's result names").
- **D3. No new outcome for the narrator.** A refused value writes nothing to the log, the stage directory or the work-item; the work-item's transition proceeds from the outcome as for any other result (supervision#r3). The scenario's "w1 is green" is all the narrator sees; no requirement asks for a warning, so none is added.

## 4. Tests the decisions break

None. Verified from the notes (§4, searched `keep_named`, `named-`, `report.md`, `"names"`, `names=` across tests/): no test asserts the OSError, a raise from `keep_named`, or the `named-` rename; `test_supervision.py:report_copied`, the report given and the stub's `names`/`fields` path stay sound under D1–D3, since real files inside the worktree are still copied as today.

## 5. Open cases

For the implementer to name (in the report), not to choose:

- a `questions` field given as one long string rather than a list (P6): covered by D1 as well, since `keep_named` runs before `questions` is read; no scenario pins it.
- a field holding a NUL byte (P8, `ValueError`): covered by D1; no scenario pins it.
- a name refused with errno 95 rather than 36 (P11): covered by D1; no scenario pins it.
- a field whose value is a list or other non-string: today skipped as non-string; no scenario pins it.
