# Research of w127 (requests: line outcome, turn, awaiting statuses)

Accepts requests#r7, r15, r16, r17, r18. Scenarios (features/requests.feature): r15 outcome; r16 refused out of turn;
r7 turn, Outline, 2 examples; r17 turn to asker, Outline with no Examples; r18 turn to upstream.
Tools: no map exists, `tools map` not made (it runs the suite): `tests-of` and `untested` answer "no map"; test
lists below are `by search` or from runs. `refs` not run: the request commands name nothing in the code yet.
Probe files: `.shop/scratch/w127-1-research/probe_*.py` (ignored by git).

## 1. Why each scenario is red today

No test module binds `features/requests.feature` (no `scenarios("requests.feature")` in tests/; no requests step
module). Binding reproduced with a scratch file (probe_bind.py) that calls pytest-bdd `scenarios()` on it:

Command: `python3 -m pytest -o addopts="" -p no:warnings -q .shop/scratch/w127-1-research/probe_bind.py` (run)
- r15 outcome: StepDefinitionNotFoundError, Given "a request q1 from the asker ctx-a whose turn is the upstream's,
  with two lines that have no line outcome" (line 68). The When `work outcome` has no command (section 2).
- r16 refused: undefined Given "...whose turn is the asker's, with one line whose line outcome is question" (line 76).
- r7 upstream to asker: undefined Given, same pattern (line 85).
- r7 asker to upstream: undefined Given, same pattern (line 85).
- r17 awaiting-asker: undefined Given "...with two lines, line 1 ... and line 2 with <line 2>" (line 97). The
  Outline has no Examples, so `<line 2>` is passed on literally (D2).
- r18 awaiting-upstream: undefined Given "...whose status is awaiting-asker and whose turn is the asker's..."
  (line 104).
- Result: 6 failed, 1 passed (my placeholder), 17 deselected by the work-item plugin.

Missing in code, by file and function:
- `scripts/work`: `main()` (lines 60-90) has no `request`, `outcome`, `turn` or `resolve` subcommand; the dispatch
  dict at lines 89-90 has none.
- No module keeps request files: nothing reads or writes `.shop/work/requests/q<n>.md`. Grep of `scripts/` for
  request commands and request statuses (`awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`): none in
  `work`, `workqueue*.py`.
- Missing in tests: no step module for requests (Givens that write a request file, Whens that run `work`, Thens
  that read `status` and `turn`).

## 2. What the system answers today

Probes (run): `python3 -m pytest -o addopts="" -p no:warnings -q -s .shop/scratch/w127-1-research/probe_requests_cli.py`

- The four request commands, as the scenarios' Whens run them (`work --root <repo> request|outcome|turn|resolve ...`):
  each exits 2 with `argument cmd: invalid choice: '<cmd>'`. Stdout empty. Nothing written. So each When gives an
  argparse error, not the refusal r16 asks for (exit 1 from `Refused`).
- Nearest case, a request file written by hand in the spec's form (`.shop/work/requests/q1.md`, frontmatter
  `kind: request`, `status: open`, `turn: upstream`, sections `## Lines`, `## Outcomes`):
  - `work show`: exit 0, prints nothing. `work show --json`: `{"work-items": []}`. `work status`: exit 0, nothing.
    The request is ignored by the queue (no work-item kind).
  - `work turn q1` with that file: exit 2, invalid choice.
- Nearest case for `model check --json` on the same file (with `spec/index.md`): exit 1, `problems`:
  `.shop/work/requests: no initiative.md`, `violations` empty. The requests folder is read as an initiative (D1).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:16-17 `PART_KINDS`; scripts/model_facts.py:25 kind list | the request kind is `cross-context-request`; there is no `request` kind | the spec's file form is `kind: request`, id `request/<context path>/q<n>` (requests.md, Implementation) | test_design_model_check.py `test_an_id_of_a_kind_kept_in_shopwork_with_another_contexts_path_is_v18` (not run) | read, by search |
| scripts/model_work.py:9-14 `STATUSES` | no request statuses; work-item, initiative and capability-proposal sets only | `open`, `accepted`, `refused`, `delivered`, `awaiting-asker`, `awaiting-upstream` are in no set; nothing checks them | none | by search |
| scripts/model.lp:286 `w_many_requests` | warns on more than five `status(Q,"open")` requests across one seam | r7, r17, r18 move an open request to `awaiting-*`, so it stops counting as open: the warning's meaning changes | none (by search: no test mentions `more than five` or `w_many_requests`) | by search |
| scripts/model.lp:54-58 `closed/1` | `delivered` and `refused` close a non-capability-proposal node | `accepted`, `awaiting-asker`, `awaiting-upstream` are not closed | none | by search |
| scripts/workqueue.py `items`; scripts/work `cmd_show` | prints work-items only; request files are skipped | a request must show its status and turn (r13, not in w127's accepts) | test_work_queue.py drives `show` (by search, not run) | read, probe |

The xfail tests owned by other work-items read these same statuses or the folder: test_design_model_check.py
`[.shop/work/requests/q1.md ...]` (w131) and test_supervision.py intake round `[open]`, `[awaiting-upstream]` (w135).
They are not w127's, but they consume what w127 writes (section 4).

## 4. Tests the requirements make impossible to keep

Searched, not mapped (no map). By search: grep of tests for `invalid choice|choose from|usage:`: no match, so no
test pins the subcommand list of `work`. grep of tests for `"open"`, `requests/`, `w_many_requests`, `more than
five`: only migration tests on `docs/superpowers/requests` (moved folder, unrelated) and the xfail
design-model-check rows. Ran (`--whole-suite`, run; `python3 -m pytest -o addopts="" -p no:warnings -q --whole-suite -rfxX <4 node ids>`):
the request tests of w130, w131 and w135 are XFAIL (their own work-items' expected failures); the
`.shop/work/requests/q1.md` row is XFAIL (w131); 13 model-reads rows XPASS. None of them fails or passes because of
w127's requirements today. Not checked: whether any existing test asserts the old text of `work`'s help; none found
by search. So: none that pins old behaviour that w127 changes.

## 5. A step the work-item skips

Existing way: every `work` write goes through `workqueue.committed` (scripts/workqueue.py:236-251): it refuses
before writing when git cannot commit, makes the write, stages and commits only its files on the current branch,
and restores the files if the commit fails. Callers: `add` (line 96), `retry` (196), `withdraw` (222),
`workqueue_note.py:20`, `workqueue_answer.py:47`, `migrate_session.py:40` (grep, read).

Probe (run): `python3 -m pytest -o addopts="" -p no:warnings -q -s --whole-suite .shop/scratch/w127-1-research/probe_commit_step.py`
- `work note i1 "a line"` in a git repo: exit 0; one new commit `work note: i1` holding only
  `.shop/work/i1/ledger.md`; status clean. The effect only this step gives: the commit.
- `work note` in a repo nested in the worktree: exit 1, `git add failed: ... ignored by .gitignore`; nothing kept.
  The probe sits under the worktree's ignored `.shop`, so this is the ignore rule, not "not a git repo".
- The work-item's new `turn` and `outcome` would skip `committed`: no commit, no refusal for a repo git cannot
  commit, no restore on failure. r12 (commit) is not in w127's accepts, so as accepted w127 leaves these writes
  uncommitted unless the plan adds `committed`. Two readings for the plan: (a) call `committed` now (beyond the
  accepted requirements); (b) leave it to the r12 work-item (writes uncommitted until then). read.

## 6. Defects

D1. `model check` reads the requests folder as an initiative.
Repro (run): `probe_requests_cli.py::test_model_check_on_request_file_by_hand`: a hand-written
`.shop/work/requests/q1.md` in the spec's form; `model check --json` exits 1 with
`"problems": [".shop/work/requests: no initiative.md"]`. The `test_design_model_check.py` row
`[.shop/work/requests/q1.md ...]` is XFAIL, expected by w131.

D2. `features/requests.feature` r17 is a Scenario Outline with no Examples table.
Repro (run): probe_bind.py, the r17 test's error quotes `line 2 with <line 2>` as the step text. No values are given
for `<line 2>`. Readings for the plan: (a) add an Examples table (e.g. a line with no line outcome, and one with
question); (b) make it a plain Scenario with one named line. The feature file is spec-side, not this work-item's.

## 7. The file set

Production:
- `scripts/work`: add `request`, `outcome`, `turn`, `resolve` subparsers and dispatch (main, lines 60-90). Read.
- new module (a new concern: CLAUDE.md says a new concern gets a new module and a row), e.g.
  `scripts/workqueue_request.py`: request file form, turn, outcome, the statuses. Read (requests.md, Implementation).
- `scripts/workqueue.py`: reuse `committed` and `Refused` only if the plan commits (section 5). Read.
- `CLAUDE.md`: module map row for the new module. Read.
- `scripts/model_work.py`, `scripts/model.lp`: not required for the six scenarios; touched only if the plan adds
  request statuses to the model (section 3). By search.

Tests (new, under the scenarios' pattern):
- `tests/scenarios/test_requests.py`: `scenarios("requests.feature")` binding. Read (probe_bind shows none exists).
- `tests/scenarios/requests_*_steps.py`: Givens writing `.shop/work/requests/q1.md`, Whens running `work`, Thens. Read.
- `tests/scenarios/conftest.py` (176 lines) may gain a helper; not required. Read.

Size: `python3 <Scripts>/tools size --limit 300` printed no tracked Python file over 300 lines. Line counts (wc) and room:
- scripts/work: 97 lines, room 203.
- scripts/workqueue.py: 262 lines, room 38.
- scripts/model_work.py: 213 lines, room 87.
- scripts/model_facts.py: 275 lines, room 25.
- scripts/model.lp: 304 lines (not a Python file; not in the size tool).
- tests/scenarios/conftest.py: 176 lines, room 124.
- tests/scenarios/test_work_queue.py: 286 lines, room 14 (not changed).
