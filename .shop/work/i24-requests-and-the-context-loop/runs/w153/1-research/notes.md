# w153 research: analysis after a kept branch review (r75, r76)

Method: no coverage map (`tools tests-of`, `untested`: "no map"); `tools refs` finds no methods. Counts by search. Scenarios run by node id, serial and xdist. Probes in `.shop/scratch/w153-1-research/` (`probe_analysis.py`, `probe_measure.py`, output `probe_out.txt`). Probes call the real methods in-process; they are not a `work run`.

## 1. Why each scenario is red today

- r75, "a kept branch review that ended PARTIAL ... no `measure initiative` is run": `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_kept_branch_review_that_ended_partial_..."`. Run: `StepDefinitionNotFoundError`, Given "every worker gives DONE, and the branch reviewer's result gives PARTIAL, with no question and no finding". Missing: step in `tests/scenarios/supervision_analysis_steps.py` (needs a stub plan `bdd-branch-reviewer: {"status": "PARTIAL"}`). Its Then is not reached, so not run. The code it pins is wrong: `scripts/supervise_analysis.py:lists_nothing` (l.19-25) reads only `questions`, so PARTIAL with none counts as "nothing to fix now"; called at `scripts/supervise.py:202`.
- r76, "a session of analyzing-a-batch ... ends at its turn limit leaves no analysis record": run: `StepDefinitionNotFoundError`, Given "... the analyzing-a-batch session writes an analysis file of i1 and ends at its turn limit". Missing: step in `supervision_analysis_steps.py` (plan `batch-analyst: {"notes": {"analysis.md": ...}, "subtype": "error_max_turns"}`). Code: `scripts/supervise_analysis.py:analyse` (l.52-55) discards the session's return value and never reads its result or cut-short state; it copies `analysis.md` into `.shop/records/` on any ending.
- r75 "measure initiative is run" (run, PASSES today), r76 "a session ... writes its analysis record" (run, PASSES today).

## 2. What the system answers today

P1 `probe_analysis.py::test_lists_nothing`, `lists_nothing(kept)` on a `result.json` (run):
- DONE, no question -> True
- PARTIAL, no question -> True (scenario's case; wrong)
- NEEDS_CONTEXT, no question -> True
- DONE, one question -> False
- PARTIAL, one question -> False
- no result.json -> False

P2 `probe_analysis.py::test_analyse_turn_limit`, `analyse()` on a fake repo, `measure` replaced by a fake that writes a measurement, session replaced by a fake that writes `analysis.md` and prints `error_max_turns`, exit 1 (run, in-process):
- briefs started: 1; records after: `['2026-10-25-i1-analysis.md']`; stderr empty.
- Scenario expects no record. The "wrote no analysis record" message is not printed, since a file exists.

P3 `probe_measure.py::test_measure_twice`, real `scripts/measure initiative i1` in a scratch git repo with `spec/index.md` and a one-line `log.jsonl` (run):
- run 1: rc 0, stdout `.shop/records/measurements/2026-10-25-i1.md`
- run 2 (same day): rc 1, `measure: the measurement ... exists; --replace writes over it`. `analyse()` then prints a refusal and starts no analysis.
- `git status --porcelain`: `?? .shop/`. The measurement is left uncommitted.
- Without `spec/index.md`, `measure` refuses (rc 1, "spec/index.md ... is missing"). Nearest case, run.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_analysis.py:lists_nothing | True when result.json reads and `questions` is empty; ignores `status` | r75: "lists nothing to fix now" must also exclude PARTIAL (and NEEDS_CONTEXT, reading in 4) | test_supervision.py r75 positive (DONE, passes); none for PARTIAL (red) | grep `lists_nothing`; run |
| supervise_analysis.py:analyse | runs measure, starts the session, copies analysis.md whatever the session's end | r76: no record from a session cut short (subtype error_*, is_error, exit 1, no JSON) | test_supervision.py r76 positive (passes); turn-limit scenario red | grep `analyse`; P2 |
| supervise.py:202 (caller of lists_nothing and analyse) | `elif kept is not None and self.lists_nothing(kept): self.analyse()` | unchanged call; any change to the test's result must keep the r74 branch first | r74 scenario in test_supervision.py (not run by me) | grep |
| supervise_draft.py:fix_work_item | reads `questions` as the fix-now findings (r74) | r75's change must not alter it: a PARTIAL review with a question still goes to fix_work_item first (`questions` non-empty) | r74 scenario (by search; not run) | read |
| supervise_analysis.py:analyse, measure write | writes `.shop/records/...` in the main checkout, no commit or push | not in r75/r76 text | r76 positive (passes) | read; P3 |

## 4. Tests the requirements make impossible to keep

By search (no map): tests with a branch reviewer's status other than DONE: none. Searched `tests/scenarios` for `bdd-branch-reviewer`, `branch reviewer`, `branch-reviewer`: plans in `supervision_review_steps.py` (l.24, DONE with notes), `supervision_proposal_steps.py` (l.47, DONE with questions), `supervision_faults_steps.py` (l.170, DONE with touch), `supervision_analysis_steps.py` (l.19, DONE, questions []). None is PARTIAL, none cut short. So none can no longer pass.
- Verified sound: the two passing accepted scenarios (r75 positive, r76 positive) run DONE with no questions; they keep passing under a status check.
- Existing green scenarios with a DONE branch review (default stub) already reach `analyse()` and start a `batch-analyst` session (the stub writes nothing; "wrote no analysis record" on stderr). Unchanged by the work; not run by me.
- Assertions on `git status --porcelain` in supervision tests cover `.shop/work` only (`test_supervision.py:145`, `supervision_faults_steps.py:104`, `supervision_review_steps.py:69`), so an uncommitted `.shop/records` file breaks none of them (by search).

## 5. A step the work-item skips

The branch review path (`supervise_review.py:branch_review`, via `worker`) does what `analyse` skips:
- push verification before the session (`git_push("--dry-run")`, r35/r51): `analyse` does none. read.
- the session's end: `worker` raises a Fault on a cut-short session (`cut_short`, r45), on a missing result (r42), and on changes under `.shop/work` (r28/r6). `analyse` does none: P2 shows the cut-short record kept. run (P2).
- log.jsonl: `branch_review` logs `push verified`, start and end (r49). `analyse` logs nothing. read (no `self.log` in supervise_analysis.py).
- commit: `branch_review` commits its directory and log.jsonl and pushes (r47, r48, r38). `analyse` leaves the record and measurement uncommitted (P3 `?? .shop/`); no push. run for the untracked file; read for the copy.
- a refused `measure` (second run the same day) is printed to stderr, not a fault (P3 run 2). read.

## 6. Defects

D1. A PARTIAL branch review with no question counts as "nothing to fix now".
- `python3 -m pytest -q -s .shop/scratch/w153-1-research/probe_analysis.py`: `lists_nothing` on `{"status": "PARTIAL", "questions": []}` -> True (probe_out.txt).
D2. An analysis session cut short at its turn limit leaves an analysis record.
- Same probe, `test_analyse_turn_limit`: session `error_max_turns`, exit 1, wrote `analysis.md`; `records after: ['2026-10-25-i1-analysis.md']`.
D3. A later measurement of an initiative on the same day is refused, so its analysis never starts.
- `probe_measure.py`: second `measure initiative i1` rc 1, "exists; --replace writes over it"; `analyse()` prints it to stderr and returns. Whether it should be refused is for the plan to decide.
D4. The measurement and the analysis record are left uncommitted in the main checkout.
- `probe_measure.py`: `?? .shop/` after run 1.

## 7. The file set

Changes needed for the scenarios and for those that pass to keep passing:
- scripts/supervise_analysis.py (59 lines): `lists_nothing` also needs `status == DONE` (or PARTIAL excluded; see the two readings below); `analyse` reads the session's result and cut-short state (`cut_short` from supervise_faults.py) and copies no record for a cut-short session. Found by grep and P1/P2.
- tests/scenarios/supervision_analysis_steps.py (51 lines): the two undefined Givens (PARTIAL branch review; analyst at turn limit with an analysis file), with plans `{"status": "PARTIAL"}` and `{"subtype": "error_max_turns", ...}`. Found by the run's StepDefinitionNotFoundError.

Read, no change expected:
- scripts/supervise.py (236 lines): call site l.202; unchanged if `lists_nothing(kept)` keeps its signature.
- scripts/supervise_faults.py (160 lines): `cut_short` and `session_end` reused; import only.
- scripts/supervise_draft.py (81 lines): fix_work_item unchanged.
- scripts/supervise_worker.py (242 lines): `session()` unchanged.
- scripts/measure (97), measure_write.py (41), measure_read.py (206), measure_build.py (143), measure_show.py (112): `measure initiative` unchanged (D3 is their behaviour; no change asked).
- tests/scripts/stub_claude.py (258 lines): plan keys already cover PARTIAL (`status`) and turn-limit (`subtype`, `num_turns`); no change needed.
- tests/scenarios/test_supervision.py (250 lines): node ids exist; steps bind by text; no change expected (not read in full).

Size: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing (no file over 300; exit code not shown). Room under 300: supervise.py 64, supervise_analysis.py 241, supervise_faults.py 140, supervise_worker.py 58, supervise_draft.py 219, measure_read.py 94, test_supervision.py 50, supervision_analysis_steps.py 249, stub_claude.py 42.

Two readings of "lists nothing to fix now" for the plan to choose between (not decided here):
(a) only status DONE with no question counts as nothing to fix now (excludes NEEDS_CONTEXT too);
(b) only PARTIAL is excluded, as the scenario pins.
