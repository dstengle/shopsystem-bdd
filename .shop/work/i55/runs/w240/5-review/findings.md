# Review of w240 (work-queue r62)

**Verdict: DONE.** No finding is Critical, and none is triaged fix now. The commits do what the plan says. The only test changed is the one the plan lists under "Tests the decisions break". The only change under `features/` retires the two scenarios the work-item lists under Retires.

## Commits reviewed

- 8b68f27817f44c0d6d56ce1f97b1501a99065c85: work-queue r62: done needs every capability-proposal formulated or withdrawn (the step Givens, `CLOSED_PROPOSAL`, the unit test)
- aff8ddf1ed7deea1fbc43190ff2f7a92a56d37a1: retire the deprecated r23 done scenarios (features/work-queue.feature, 31 lines removed)

The implementer's last result (4-implement) lists 86ffc4d3 and 9799e060. These have the same subjects and stats as the merged commits. Running `git diff 9799e060 aff8ddf1` over the three code files gives nothing. So the merged commits are `work run`'s rebase of the implementer's commits, with the same content. The 3-implement result's ae1de590 and 521b2a43 came from an earlier session that this one superseded.

Suite: taken from the brief's record: 1088 passed, 0 failed at aff8ddf1. The 14 expected failures belong to w212, w238 and w239. The earlier failure was the index.lock flake; the person's answer covers it.

## Removed and weakened tests

Searched the diff for removed `def test_` functions, dropped parametrize cases, removed or loosened `assert`s, and added skip or xfail marks.

- `tests/scripts/test_workqueue_done.py::test_an_open_proposal_keeps_the_initiative_from_done`, case `("merged", True)` → `("merged", False)`.
  - Before: a proposal at `merged` lets the initiative reach done.
  - After: it holds the initiative open (r47).
  - The plan lists it in §4 (D1), so it is not a finding. The case is kept, the assertion is not loosened, and the 6 cases pass.
- Two deprecated scenarios were removed from features/work-queue.feature: the r23 Outline (4 examples) and the r23 retry scenario. Both are listed under the work-item's Retires. Their binding is the file-wide `scenarios("work-queue.feature")` in tests/scenarios/test_work_queue.py:33, so there is no per-scenario binding to remove. What they pinned is now pinned by the r62 Outline (features/work-queue.feature:60-79), which covers withdraw ×5 and retry ×1 with proposal Givens.
- Nothing else.

## Allowances

The report's `## Tests changed under an allowance` gives "none". That matches the commits: the one changed test is listed in the plan.

## Cannot verify

- That the r62 Outline's six examples were red before the change and are green after it. I did not run them; the brief's suite record and the implementer's report (187 passed for `--work-item w240`) say they pass.
- That no proposal still at `merged` belongs to an open initiative, which the plan claims under D1. The claim is about the main checkout's `.shop/work/`, and I did not survey it.

## Findings

1. **Minor, drop.** tests/scenarios/work_queue_status_steps.py:45: the `with_state` regex went from `whose work-items? (?P<items>.+)$` to `whose work-items?(?P<items>.+)$`, dropping the space.
   - Neither the plan nor the report mentions it.
   - The effect is harmless: `items` now starts with a space, and the `re.findall` that follows ignores it.
   - The pattern also accepts text glued to "work-item" with no space. My grep of features/ found no such step text, so no Given changes meaning.
   - Fix (optional): restore the space, or say in the report why it was dropped.

The capability's Purpose and r62/r47 lines are respected: `CLOSED_PROPOSAL = ("formulated", "withdrawn")` matches r62's wording and r47's "neither formulated nor withdrawn". No code was added beyond what r62 asks for: the three Givens are test steps, and the docstrings name r62 and r47.

Seen in passing, outside these commits and not a finding against w240: scripts/supervise.py:266 still counts `merged` as finished when it picks `work run`'s exit code, and scripts/model_work.py:17 counts `merged` as settled for retired ids. The second is a different rule (r5/r23). The first is about the exit code, not the done condition, and D1 calls `merged` a legacy status. It may deserve a look in a later initiative.

## Checks

- `tools check --base 3c1de94d`:
  - ruff: all checks passed.
  - vulture: one hit, `tests/scenarios/work_queue_status_steps.py:100: unused variable 'notes'`. It was already there: the same `ledger_of_twelve(repo, notes)` is at line 77 at the base. The commits only moved it.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. The touched files are 183, 78 and 28 lines.

## Commands run

- `cat` of the brief, the work-item, plan.md, and both implement reports and results
- `git show --stat` of both commits; `git log` from c53a7c25 to aff8ddf1; `git log -1` of 86ffc4d3 and 9799e060
- `git diff 8b68f278~1 aff8ddf1`; `git diff 86ffc4d3~1 9799e060 --stat`; `git diff 9799e060 aff8ddf1 --` over the three code files (empty)
- `sed` of work_queue_status_steps.py and supervise.py:255-275; `grep` of the r62 Outline and of r62/r47 in spec/capabilities/work-queue.md
- `grep -rn merged scripts/`; `grep -rnoE` over features/ for glued "whose work-item" text (none); `grep` of the bindings in test_work_queue.py
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 3c1de94d6842dc669e25ea2f79b29bbc8964a2b1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `git show 3c1de94d:tests/scenarios/work_queue_status_steps.py | grep -n notes`
- `python3 -m pytest -q tests/scripts/test_workqueue_done.py` (6 passed)
