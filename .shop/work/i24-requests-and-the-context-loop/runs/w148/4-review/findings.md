# Review of w148: `work request` refuses a --lines file that does not exist

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. The change is the two-line check the plan asked for, plus a small steps module. It does what work-queue#r7 asks: it says why and changes nothing. The focused scenario passes. One Minor observation: the wording when `--lines` is a directory.

## Commits reviewed

The branch `work/w148` no longer exists, so I took the commits on HEAD between `e0cf128` (`work: w148 ready -> claimed`) and `e1eadd1` (`work: w148 claimed -> done`), leaving out `work run`'s own `work:` commits:

- `fd180a0` "work request refuses a --lines file that does not exist, naming it". It changes scripts/workqueue_request.py (+2), tests/scenarios/test_work_queue.py (+1) and tests/scenarios/work_queue_request_steps.py (new, 15 lines).

This is the one commit the implementer's result.json lists. All three files are in the work-item's `fileset`. Nothing under `features/` changed, and the work-item has no Retires section.

## Removed and weakened tests

None. I read the full diff `git diff e0cf128 fd180a0` (18 insertions, 0 deletions), looking for:
- deleted test functions;
- dropped parametrize cases;
- removed or loosened `assert`s;
- added skip or xfail;
- rewritten steps.

There are none. The only test change is new steps: `upstream_without_a_request`, which delegates to `requests_write_steps.upstream_keeps_none`, and `no_lines_file`, which asserts that `lines.md` is absent. The plan's "Tests the decisions break" says none.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commits agree: no existing test changed.

## Cannot verify

- The report's figures: the red run (1 failed, FileNotFoundError traceback), the green run (155 passed, 1 skipped) and the suite record at the start (810 passed). I did not run the whole suite. `work run` ran it before the merge.
- The report says `tools size` printed nothing. I confirmed this myself (below).

## Findings

### 1. Minor — observation: a directory given as `--lines` is refused as "does not exist"

- **Work-item:** w148.
- **Where:** scripts/workqueue_request.py:68-69. `if not Path(lines_file).is_file(): raise Refused("the file %s does not exist" % lines_file)`.
- **What is wrong:** `is_file()` is also False for a directory, so `work request ... --lines <dir>` says "the file <dir> does not exist". The path does exist. r7's "say why" is then given a reason that is not true. The plan's decision 2 chose `is_file()` on purpose, and both the plan (open case 1) and the report name this wording as open. No scenario or client gives a directory today.
- **Reproduction:** from the code. With `--source o1` given, the origin check at line 66 passes. A directory fails `is_file()`, so the refusal at line 69 is raised before any read or write. I could not run the probe: `python3 scripts/work request "Show the queue" --from ctx-a --lines tests --source o1` was refused by the command allowlist.
- **Fix:** when the path exists, word the refusal by what it is, e.g. `the file %s is not a regular file`, or "is a directory". This would come with an r7 scenario if wanted.

### 2. Pre-existing, not of this work-item: ruff I001 in tests/scenarios/test_work_queue.py:7

`tools check` reports the import block as unsorted. The cause is `work_queue_withdraw_steps` placed before `work_queue_start_steps`, which was already so at `e0cf128` (`git show e0cf128:tests/scenarios/test_work_queue.py`). The new import went in at its sorted place. Triage: drop for w148.

### Risks I checked

- **Step clash.** Importing `upstream_keeps_none` from requests_write_steps could bring that module's other steps into test_work_queue.py, such as `it exits with an error`. Only the one function is imported, by name. Its pytest-bdd fixture stays in requests_write_steps, and the new module re-binds the step text itself. The focused scenario passes, and test_requests.py still star-imports requests_write_steps unchanged.
- **Order and writes.** The check sits after the origin check and before the read, the git check and any write (line 68, before `workqueue.read` at line 70). This matches the plan's decision 1 and r7's "change nothing", and the scenario's `nothing under the repository has changed` passes.
- **Code no line asks for.** The new refusal serves r7, so it is not such code.

## Commands run

- `git log --format='%H %s' --grep="^work: w148 " HEAD`: found the claim commit `e0cf128` and the done commit `e1eadd1`. `work/w148` is an unknown revision.
- `git log --stat e0cf128..e1eadd1` and `git diff e0cf128 fd180a0`.
- `grep` of the step, the feature scenario (features/work-queue.feature:190) and r7 in spec/capabilities/work-queue.md.
- `python3 -m pytest -q tests/scenarios/test_work_queue.py -k "lines_file_that_does_not_exist"`: 1 passed.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base e0cf128`:
  - **ruff:** 1 error, I001 at tests/scenarios/test_work_queue.py:7 (pre-existing, finding 2).
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing, so no file is over the limit.
- `git status --short`: clean.
