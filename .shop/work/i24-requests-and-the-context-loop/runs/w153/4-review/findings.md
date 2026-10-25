# Review of w153

**Verdict: DONE.** Nothing is triaged fix now and nothing is Critical. r75 and r76 are done as the plan says. There are two Minor observations.

## Commits reviewed

The branch `work/w153` is gone. Commits between `177cf13 work: w153 ready -> claimed` and `2852013 work: w153 claimed -> done`, with `work run`'s `work:` commits left out (`c2ef824 work: w152 done -> green`):

- `7999ff2` "work run measures and analyses only after a DONE branch review with nothing to fix; keeps no analysis from a cut-short session (r75, r76)". It touches `scripts/supervise_analysis.py` (+20/-5) and `tests/scenarios/supervision_analysis_steps.py` (+26).

The implementer's result lists `f511b7f`, which has the same subject. `git diff f511b7f 7999ff2 -- scripts tests` is empty, so 7999ff2 is f511b7f rebased onto the branch when it was merged. It is the same change. That is no finding.

The diff stays inside the fileset and the budget. Nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff of `tests/` for removed lines (`-` lines), removed `def test_`/step functions, changed asserts and parametrize lists, and added `skip`/`xfail`. The diff adds two Givens and two Thens and removes nothing. The plan's "Tests the decisions break" says none, and that matches.

## Allowances

The report's `## Tests changed under an allowance` says "none". There are no rows to check.

## Cannot verify

- The report's red-before-green run (2 failed before the code, 146 passed after with `--work-item w153`). Only one commit holds both the steps and the code, so the red state can't be seen in the history. The four r75/r76 scenarios pass now (below).
- The report's suite figures (818 passed, 2 failed at start). I did not run the whole suite; `work run` ran it before merging.

## Findings

### 1. Minor, observation: ruff I001 at scripts/supervise_analysis.py:10 (w153)

- **What:** `tools check --base 177cf13` fails ruff with `scripts/supervise_analysis.py:4:1: I001 Import block is un-sorted or un-formatted`.
- **Cause:** the commit changed the import to `from supervise_worker import SCRIPTS, cut_short     # supervise_worker first: ...`, with five spaces before the inline comment. The import block at the base was clean.
- **Why it matters:** `tools check` exits 1 on the work-item's own files.
- **Fix:** put two spaces before the `#`, or move the comment to its own line (`ruff --fix` does this).
- **Reproduction:** `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 177cf13b5fe0896d94ef4062c5ced76c33102e8d` printed `== ruff == ... I001 ... Found 1 error.`, then `== vulture == clean` and `== import-linter == the project states no import contracts`. Exit code 1.

### 2. Minor, observation: an analysis session that ends in success with a PARTIAL or NEEDS_CONTEXT result still has its analysis.md kept as the record (scripts/supervise_analysis.py:61-70, w153)

- **What:** `analyse` refuses only a session that `cut_short` names or one with no readable result. It does not read the result's `status`. A batch-analyst whose result says PARTIAL or NEEDS_CONTEXT, but which wrote `analysis.md`, has that file copied into `.shop/records/`.
- **Why it matters:** this sits close to the reason for r76's turn-limit scenario ("an analysis cut short is not kept"). A self-declared PARTIAL analysis is an unfinished one. But no line or scenario names it, and the plan (§5) and the report (Open questions) leave it open on purpose. So this is hardening, not a wrong answer against a line.
- **Fix, if wanted:** a line first, through integrating-a-proposal, then keep the record only on status DONE, as `lists_nothing` now does for the branch review.
- **Reproduction:** the probe `.shop/scratch/w153-4-review/test_probe_partial.py` calls the real `Analyses.analyse` with a fake `measure` and a fake session. I ran it with `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w153-4-review/test_probe_partial.py`:
  - `PARTIAL success -> ['2026-10-25-i1-analysis.md']`
  - `NEEDS_CONTEXT success -> ['2026-10-25-i1-analysis.md']`
  - `DONE error_max_turns exit1 -> []`, with stderr "the analysis session of i1 was cut short, so there is no analysis record: session ended at its turn limit (error_max_turns, None turns, exit code 1)"

### Checked and sound (no finding)

- **Risk: `session()` doesn't return what `cut_short` needs.** `supervise_worker.py:211-218` returns `subprocess.run(..., capture_output=True, text=True)`, so `.stdout` and `.returncode` are there.
- **Risk: an import cycle from the new import.** `supervise_faults.py:8` imports `supervise_worker` as a module, at call time. `supervise_worker.py:13` imports `cut_short` from `supervise_faults`. So importing `cut_short` through `supervise_worker` is sound, as the comment says.
- **Risk: the D1 status check changes r74's path.** The call site in `supervise.py` is unchanged. r74 is tested before `lists_nothing`.
- **Code no line asks for:** the "no readable result file" refusal and its stderr message are the plan's D2. That rests on r76, r45 and decision 0038 ("a missing or malformed result is a failed stage"). They are the mechanism of a line, not new behaviour.
- **Size:** `tools size --limit 300` printed nothing. `supervise_analysis.py` is at 74 lines and `supervision_analysis_steps.py` at 77.
- **Step bindings:** the new Givens and Thens match `features/supervision.feature:936, 938, 953, 956` word for word.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w153 ready -> claimed$"` (and the same for `claimed -> done`), `git log --oneline -8`
- `git show --stat 7999ff2`, `git show 7999ff2 -- scripts tests features spec`, `git diff f511b7f 7999ff2 -- scripts tests | wc -l` (0), `git diff 177cf13 2852013 --stat`
- `grep` in `features/supervision.feature`, `spec/capabilities/supervision.md`, `scripts/supervise_faults.py` and `scripts/supervise_worker.py`; `git show 177cf13:scripts/supervise_analysis.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 177cf13b5fe0896d94ef4062c5ced76c33102e8d`:
  - ruff: 1 error (I001)
  - vulture: clean
  - import-linter: no contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: nothing printed
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "r75 or r76 or kept_branch_review or analyzing_a_batch or measure_initiative"`: 4 passed
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w153-4-review/test_probe_partial.py`: output above
- `git status --porcelain`: clean
