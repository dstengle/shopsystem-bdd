# research of w179: supervision r15, a result field too long to be a file name

Tools: `tools` at the brief's Scripts path. No coverage map (`tools tests-of` says "no map"), so every test list below is `by search`. `tools refs` ran for keep_named (1 production reference, 0 tests).

## 1. Why each scenario is red today

**S1** "a file the worker's result names is copied into the stage directory before its worktree is removed" (features/supervision.feature:352).
Command: `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_file_the_workers_result_names_is_copied_into_the_stage_directory_before_its_worktree_is_removed"`
Result: **passes today (1 passed)**. Not red. The copy already exists: `scripts/supervise_worker.py:Workers.keep_named` (226-238), called from `Workers.worker` (207) before the worktree is removed in `scripts/supervise.py:Supervisor.step` finally (164-165). Must stay green.

**S2** "a field of a worker's result giving a sentence longer than a file name may be is taken as no file" (features/supervision.feature:360).
Command: `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_field_of_a_workers_result_giving_a_sentence_longer_than_a_file_name_may_be_is_taken_as_no_file"`
Result: `StepDefinitionNotFoundError: Step definition is not found: Given "the implementer's result also gives a field whose value is a sentence of over 255 characters, with spaces, naming no file"` (feature line 364). Missing: that @given in `tests/scenarios/supervision_given.py` (next to the report.md given at 199-202). Its body can set `plan["bdd-implementer"]["fields"]` (the stub already writes `fields`, `tests/scripts/stub_claude.py:252-253`).
Behind it, once the step exists: the code raises, so "w1 is green" would fail. Cause: `supervise_worker.py:Workers.keep_named` line 234 `path.is_file()` raises `OSError: [Errno 36] File name too long` for a sentence of 255+ chars (probe P1, P2). Stays a raise through `Workers.worker`; see section 6.

## 2. What the system answers today

Probes run by calling `Workers.keep_named` directly (unbound, self=None: it uses no instance state), on a tree holding `report.md` and a `here` dir. Real entry point is `work run i1`; not run (the S2 Given is undefined, and the scenario world is the test's own), so the end-to-end path is `read`.

Command for each: `python3 -m pytest -q -s -n 0 .shop/scratch/w179-1-research/<probe file>` (the `-n 0` is needed: the pytest.ini runs xdist and swallows prints).

| case | result | run |
|---|---|---|
| P1 `report` named + 300-char sentence field (spaces) | `OSError [Errno 36] File name too long` from `is_file()`, kept nothing | `probe_keep_named.py` case 2 |
| P2 `report` named + 256-char no-space field | same OSError | case 3 |
| P3 `report` named + 255-char no-space field | ok, kept `report.md` (boundary: 255 ok) | case 4 |
| P4 sentence field alone | same OSError | case 5 |
| P5 field of `a/a/…` 400 chars (slashes) | ok, kept nothing (nonexistent path, ENOENT ignored) | case 6 |
| P6 `questions` given as one 260-char string | same OSError (keep_named runs before `questions` is read, worker 207 vs 208) | `probe_keep_named_more.py` case 7 |
| P7 `questions` given as one 60-char string | ok | case 8 |
| P8 field `"a\x00b"` (NUL) | `ValueError: embedded null byte`, uncaught | case 9 |
| P9 `summary` field of 256 chars | ok (summary skipped by design, line 231) | case 10 |
| P10 `report` named then sentence field, in the stub's order | OSError; `report.md` already copied to kept before the raise: `['report.md']` | `probe_keep_named_order.py` case 11 |
| P11 accented name, 203 bytes (100 chars + .md) in a field | `is_file()` raises `OSError [Errno 95] Operation not supported` | `probe_keep_named_order.py` case 13 |
| P12 same name's `resolve()` | ok (resolve catches; `is_file` does not) | `probe_name_limit.py` |
| P13 `is_file()` on 257-byte accented name | `[Errno 36] File name too long`; 50 chars (103 bytes) ok | `probe_name_limit.py` |

Nearest cases not given: an empty or blank field value is skipped (`keep_named` line 231), `read`. A field naming a file outside the tree is skipped (line 234 `is_relative_to`), `read`.

Note P10 ordering: the stub writes named fields before extra fields (`stub_claude.py:252-253`), so in S2 the report is copied first, then the sentence raises. So S2 as drafted would show `report.md` in the stage directory but no `w1 is green`.

## 3. Old assumptions

The requirement makes a field's text no path when it is not a file name. The old assumption: every string field except `status` and `summary` is a path to try.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_worker.py:Workers.keep_named (226-238) | resolves and `is_file()`s every string field except status/summary; raises on names the OS refuses | a sentence field must be taken as no file: no raise, no copy | test_supervision.py:test_a_file_the_workers… (1 passed; by search) | refs; read |
| scripts/supervise_worker.py:Workers.worker (207, the call; 208-213 questions) | passes the whole result to keep_named before reading `questions`, so a long `questions` string also reaches it | a `questions` string is one question, not a path; must not raise | none for a long string (by search); the short-question researcher scenario runs it | read; probe P6 |
| scripts/supervise.py:Supervisor.step (162, 164-165) | the worker call, then removes the worktree in finally | unchanged; the copy must still come before the removal | many supervision scenarios (by search) | read |
| scripts/supervise_rounds.py:76, supervise_intake.py:84, supervise_answers.py:97, supervise_merge.py:99 | call `worker()` and take its result; get the same raise | the same guard covers them through worker(); no change in each | by search: their stage scenarios | refs |
| scripts/supervise_pool.py:96 and 113 (`except Exception`) | carries any exception to the run's thread | unchanged; the raise is what the defect looks like here (section 6) | none for OSError (by search) | read |

## 4. Tests the requirements make impossible to keep

Searched (no map): `keep_named`, `named-`, `report.md`, `"names"`, `names=` across tests/.

- `tests/scenarios/test_supervision.py:report_copied` (251-254): asserts report.md copied. Passes today, will pass with a guard that keeps the copy for real files. Sound.
- `tests/scenarios/supervision_given.py:199-202` (the report given): sets `names`. Sound.
- `tests/scripts/stub_claude.py:251-253`: writes `names` as absolute paths and merges `fields`. Sound; the stub needs no change.
- No test asserts the OSError, the `named-` rename or a raise. Nothing a guard could break.

Verdict: none. Checked: the 1 `report` scenario and the stub's fields path, both sound.

## 5. A step the work-item skips

The existing way to decide "this field names a file" is one step: `(tree / value).resolve()` then `path.is_file()` (supervise_worker.py 233-234). The sentence field skips nothing; the step itself fails. A guard that rejects a value before `resolve()` (by length or NUL) skips the step for that value. Effects only that step produces, `read`: the `shutil.copy2` into the stage directory and the `named-` rename. Nothing else. Probes P3/P13 show the boundary is per byte, not per character: a 203-byte name fails (P11), a 255-char ASCII one passes (P3). A guard by character count would let a 200-char accented name through to the raise. Note the errno: `is_file` raises for EOPNOTSUPP (errno 95) too, not only ENAMETOOLONG (P11). A guard on length alone misses it; the robust guard is to catch OSError and ValueError around the check (`read`; the plan decides).

## 6. Defects

**D1. A result field whose value the OS refuses as a file name ends the worker with an exception.**
Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w179-1-research/probe_keep_named.py` (cases 2, 5), `probe_keep_named_more.py` (case 7), `probe_keep_named_order.py` (case 11, 13).
Came back: `OSError: [Errno 36] File name too long` (or errno 95) from `supervise_worker.py:234`. Read: `Workers.worker` does not catch it; `supervise.py` removes the worktree in finally (164-165); `supervise_pool.py:96` carries it to the run's thread, which re-raises once threads end. The work-item keeps its status (no transition). The stage directory keeps what was copied before the raise (P10).

**D2. A result field containing a NUL byte raises ValueError.** Reproduction: `probe_keep_named_more.py` case 9. Came back: `ValueError: embedded null byte`; same path as D1 (read).

## 7. The file set

- `scripts/supervise_worker.py` (247 lines; room 53): `keep_named` takes a field whose value cannot be a file name (too long, NUL, or an OSError on the check) as no file; `questions` text too. Found by: read 226-238; probes P1-P13.
- `tests/scenarios/supervision_given.py` (259 lines; room 41): new `@given` for "the implementer's result also gives a field whose value is a sentence of over 255 characters, with spaces, naming no file" setting `plan["bdd-implementer"]["fields"]`. Found by: the StepDefinitionNotFoundError (by search of tests/ for the sentence: none).
- `tests/scenarios/test_supervision.py` (259 lines; room 41): no change expected; it binds the feature and imports `supervision_given` already (line 30). Found by: read.

Modules on the change's path, not edited (line counts by `wc -l`; room under 300 per CLAUDE.md, `tools size` lists none over 300):
- `scripts/supervise.py` 260 (room 40)
- `scripts/supervise_pool.py` 143 (room 157)
- `scripts/supervise_rounds.py` 134 (room 166), `scripts/supervise_intake.py` 123 (room 177), `scripts/supervise_answers.py` 128 (room 172), `scripts/supervise_merge.py` 135 (room 165)
- `tests/scripts/stub_claude.py` 270 (room 30)

Search for the set: `tools refs keep_named` (1 production ref, 0 test); grep `report.md|names|named-` over tests/ and scripts/.

Untracked files: `git status --porcelain` shows nothing; the scratch dir `.shop/scratch/w179-1-research/` is git-ignored (`.shop/` ignored), not listed. Probe files there: `probe_keep_named.py`, `probe_keep_named_more.py`, `probe_keep_named_order.py`, `probe_name_limit.py`.
