# review of w178

**Verdict: DONE.** No Critical finding and none triaged fix now. Two Minor findings: an import-order lint the commit introduced, and the report's inaccurate `tools check` line.

## Commits reviewed

- Claim commit: `da0bfcde work: w178 ready -> claimed`. The branch `work/w178` is gone, so the commits are those between it and `d959d612 work: w178 claimed -> done` on the checkout, less `work run`'s `work:` commits.
- The work-item's one commit on the checkout is `641f95a9` ("work run: requests this context asked, waiting in its turn, end a run in an error; ..."). The implementer's result lists `dfc78964`, which is the same commit on the old branch. `git diff 641f95a9 dfc78964` differs only in `.shop/work/` files of other initiatives (i25, i27, i31). Under `scripts/`, `tests/` and `features/` the two are identical, so this is a cherry-pick or rebase, not a different change. The commits between the claim and 641f95a9 (w176, i31, i27 commits) belong to other work-items.
- Files: features/supervision.feature (-35), scripts/supervise.py, supervise_all.py, supervise_intake.py, workqueue_request.py, tests/scenarios/supervision_intake_steps.py, supervision_request_steps.py (new), test_supervision.py. All eight are in the work-item's fileset.

## Removed and weakened tests

Searched the diff for deleted step functions, assertion changes, parametrize/Examples rows, and skip/xfail.

- Retired scenarios. The r9 deprecated scenario, the r67 deprecated outline ([open], [awaiting-upstream]) and the r82 deprecated scenario were removed from features/supervision.feature. All three are under the work-item's Retires, and the plan lists them (part 4). They are bound by `scenarios()`, so their tests go with them.
- Steps only the retired outline used, removed or rewritten:
  - `intake_writes`, the all-lines Given, was removed.
  - `lines_have_outcomes` ("each of q1's lines has a line outcome …", which asserted outcomes `1. accepted 2. refused`) became `line_one_has_outcome` with new step text for the new r67 outline (asserts `1. accepted` and turn asker).
  - `intake_started` got new text and now asserts more: the brief's "line outcome or a question on it" and "/work turn q1".
  The plan lists these (part 2, part 4). A grep finds no remaining feature or test that uses the old step texts.
- No other test was removed or weakened. No skip or xfail was added.

## Allowances

The report gives "none". Nothing in the diff needs one.

## Cannot verify

- The report's green figures (148 passed with `--work-item w178`; 271 passed in the touched modules) were not rerun. I ran only the six focused scenarios, which pass.
- The report says "Deviation: I wrote the production code before running the red again with my steps". The order cannot be verified from one commit.

## Findings

1. **Minor, observation.** tests/scenarios/test_supervision.py:36. `from .supervision_request_steps import *` sits after `supervision_review_steps`, but "request" sorts before "review". ruff reports I001 on the import block (line 14). The base `da0bfcde` had no such hit. It matters because `tools check` fails on code this commit added. Fix: move the import one line up (or `ruff --fix`). Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base da0bfcde…` → `tests/scenarios/test_supervision.py:14:1: I001`.
2. **Minor, observation.** .shop/work/i26/runs/w178/4-implement/report.md:28 says "`tools check`: nothing to check". With the claim commit as base, `tools check` exits 1 with 4 ruff hits and 1 vulture hit. Only the I001 above is this commit's. The others were already on the base: `supervision_intake_steps.py:84` FURB167 `re.M` is in base line 65, `supervise_intake.py:51` unused `extra` is in the base, and `gq.py` is i31's scratch. It matters because the report's claim is inaccurate and hid finding 1. Fix: run the check with the claim commit as base.

### Risks verified (no finding)

- **Exit-code paths.** Risk: the request check runs twice or overrides a 1. Verified: `asked` runs once, in `Run.run` (supervise.py:198) and at the end of `run_all`. `Run.run` is not called from `run_all`, which calls `pull_through`. `asked` turns only exit 0 into 3, so an exit of 1 or 3 stays as it was (plan D3).
- **Reading B (D1).** `asked_here` keeps only `status == "awaiting-asker"` with `asker` set to `internal` or `bounded-context/<path>`. This follows the Answer and Implementation r101. Open questions are question entries with no answer of the same number.
- **Question writes before the merge (D8).** Risk: `ask` on the main checkout and the round's outcome/turn edits on its branch conflict when merged. In a request `work request` writes, `## Questions` and `## Outcomes` are separated by unchanged lines (`## Answers` and blanks), so the hunks do not touch. In the scenario fixture, `ask` appends `## Questions` after `## Resolution`. The r100 scenario passes. If a write fails, the code aborts the merge, resets to the pre-question head and raises Fault, so the request stays as it was. `Refused`, `ValueError` and `GitFailed` are all imported.
- **The question command.** Implementation r100 names `work`'s question command. The code calls its library function `workqueue_request.ask`, which is the same function (plan D5) and is refused in the asker's turn.
- **Code no line asks for.** Each observable change serves a line: r101 (the print and the exit), r100 (the question write), r67 (the brief's wording). The printed form `<name> awaiting-asker` followed by `  line <n>: <question>` is r101's "printing the request with its open questions".
- **Size.** Every touched file is at most 260 lines. `tools size --limit 300` prints nothing.

## Commands run

- `git log --format='%H %s' -12`, `git log --grep=w178`, `git log da0bfcde..d959d612`, `git diff 641f95a9 dfc78964 --stat`
- `git show 641f95a9 -- scripts tests`, `git show 641f95a9 -- features`
- `git show da0bfcde:tests/scenarios/test_supervision.py`, `…:scripts/supervise_intake.py`, `…:tests/scenarios/supervision_intake_steps.py` (to find which lint hits were already on the base)
- `python3 -m pytest -q -n 0 tests/scenarios/test_supervision.py -k "r100 or r101 or r67 or r82 or r9 or intake or request"` → 6 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base da0bfcde…` → ruff 4 (1 new), vulture 1 (on the base), import-linter: no contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → no output
- `wc -l` on the touched files; Grep for the removed step texts in features/ and tests/ → none
