# Review of w173 (supervision#r98)

**Verdict: DONE.** No finding is Critical and none is to be fixed now. There are two Minor observations about hardening.

## Commits reviewed

- The branch `work/w173` no longer exists. The commits are the ones between `906706f0 work: w173 ready -> claimed` and `9e50678a work: w173 claimed -> done`, minus `work run`'s own commits and the other initiatives' commits that are interleaved there (i27, i28, i30 and the formulation rounds). That leaves one commit: `b6c4feb1 supervision r98: an implementer returned to ready by a reviewer's answer is given the reviewer's findings`. It changes `scripts/supervise_brief.py` (+19) and `tests/scenarios/supervision_answers_steps.py` (+36).
- The implementer's result lists `1860fabe`. `git diff 1860fabe b6c4feb1 -- scripts tests` is empty, and the author, date and message are the same. So it is the same commit, placed again on the line when it was merged. Its content matches the result.
- Both files are in the work-item's `fileset`. Nothing under `features/` was changed. The `@r98` scenario came from 46fef129, before the claim.

## Removed and weakened tests

None. The diff only adds lines: two Givens, one Then and a `REVIEW` constant. I searched the diff for `-def `, `-    assert`, removed `parametrize` cases, and added `skip` or `xfail`. I found none. The `briefs_hold_answers` step (r57) has not changed.

## Allowances

The report says "none", and I found no test change that would need an allowance.

## Cannot verify

- **The end-to-end route.** In this checkout, `work answer` on a reviewer's question still returns the item to `done`: `ASKED_FROM = {"claimed": "ready"}` in `scripts/workqueue_answer.py:9`. The work-queue r26 route to `ready` through `--change` was w174's work, and w174 was withdrawn. So the only way to reach `findings_lines`' condition today is the scenario's own setup, which writes the state directly (plan decision 3). The commits cannot show whether r98's brief line comes out once r26 is implemented. That depends on the move r26 logs being `awaiting-answer -> ready` with `done -> awaiting-answer` before it, which is what `findings_lines` reads.
- **The report's figures.** It reports 143 passed on the `--work-item w173` run and 856 passed / 1 failed for the suite at the start. I did not rerun these, because `work run` runs the suite. I ran the `@r98` scenario alone, and it passed.

## Findings

### 1. Minor, observation: one log line that is not JSON makes the brief writer crash (`scripts/supervise_brief.py:93-94`)
- **What is wrong:** `findings_lines` parses `log.jsonl` itself, calling `json.loads` on each line with no guard. `workqueue.logged` (`scripts/workqueue.py:282`) skips lines that are not JSON, and `agrees`/`last_logged` accept such a log. So a work-item the queue accepts can still make `work run` stop with a `JSONDecodeError` traceback while it writes the implement brief.
- **The plan:** decision 2 said "Read the log through the existing log-reading helpers", and this code does not follow it.
- **Why it matters little today:** `work` appends each line whole (`append` cuts a failed write back), so no client writes such a line today. That makes this hardening.
- **Reproduction:** `.shop/scratch/w173-6-review/test_probe_findings.py::test_malformed_log_line` writes a log with a `not json` line between the `done -> awaiting-answer` and `awaiting-answer -> ready` moves. Running `python3 -m pytest -q -n 0 -s -p no:cacheprovider .shop/scratch/w173-6-review/test_probe_findings.py` gave `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` at `scripts/supervise_brief.py:94`.
- **Fix:** read the moves with `workqueue.logged(self.dir / "log.jsonl", self.root)`.

### 2. Minor, observation: the brief can name a findings file that does not exist (`scripts/supervise_brief.py:99-103`)
- **What is wrong:** when the last `<k>-review` directory has no `findings.md`, the line still names `<k>-review/findings.md`. The plan left this as open case 1, and the report names it.
- **Why it matters:** the implementer is pointed at a file that is missing. No reviewer under r98 leaves its stage without `findings.md` today, so this is hardening.
- **Reproduction:** `test_no_findings_file` in the same probe printed `["Reviewer's findings: .../runs/w1/3-review/findings.md"]` for a `3-review` directory with no `findings.md` in it.
- **Fix, if wanted:** write the line only when the file exists. That is a reading the capability's Implementation line ("the findings file of the work-item's last review stage directory") does not settle.

### Behaviour and lines

- The new line `Reviewer's findings: <path>` is written only in implement briefs, and only on the r98 route: the last move into `ready` is from `awaiting-answer`, and the move before it is `done -> awaiting-answer`. This is what supervision#r98 and its Implementation line ask for. No other route's brief changes.
- The answer is still written by `answer_lines` (r57).
- I found no code whose behaviour no line asks for.
- Risk I checked: whether the implementer, planner or researcher question routes could trigger the line. They cannot, because they move `claimed`, `researched` or `drafted` into `awaiting-answer`, not `done`.

### tools check (base 906706f0)
- **ruff:** one error, `scripts/supervise_brief.py:84:13 ISC004`. It is in `research_questions`, and none of the reviewed commits touch those lines (`git log -L80,86` over the range is empty), so it was there before.
- **vulture:** `tests/scenarios/requests_write_steps.py:76 unused variable 'named'`. The commits do not touch that file, so it was there before.
- **import-linter:** the project states no import contracts.

### tools size --limit 300
It printed nothing, so no tracked Python file is over the limit.

## Commands run
- `git log --format=%H -1 --grep="^work: w173 ready -> claimed$" work/w173`: the branch is gone.
- `git log --oneline --grep=w173`, `git log --oneline --ancestry-path 906706f0..9e50678a`
- `git show --stat 1860fabe`, `git diff 1860fabe b6c4feb1 --stat -- scripts tests`, `git show b6c4feb1`
- `grep` in `scripts/supervise_brief.py`, `scripts/workqueue.py`, `scripts/workqueue_answer.py`, `features/supervision.feature` and `spec/capabilities/work-queue.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 906706f0`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `git log -L80,86:scripts/supervise_brief.py 906706f0..9e50678a`
- `python3 -m pytest -q -n 0 tests/scenarios/test_supervision.py -m r98`: 1 passed.
- `python3 -m pytest -q -n 0 -s -p no:cacheprovider .shop/scratch/w173-6-review/test_probe_findings.py`
- `git status --short`: clean.
