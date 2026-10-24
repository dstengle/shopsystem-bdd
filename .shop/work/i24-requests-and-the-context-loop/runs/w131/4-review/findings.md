# Review of w131: model reads requests, their file form, and an initiative of kind job

**Verdict: DONE.** No Critical finding and nothing triaged fix now. There are two Minor findings, both in w131's commit.

## Commits reviewed

- The branch `work/w131` is gone. The commits are those between `1f97efc work: w131 ready -> claimed` and
  `c537678 work: w131 claimed -> done` on HEAD, less `work run`'s own `work:` commits:
  - `d23a6a4` model reads requests under .shop/work/requests; job and job-path initiatives are file problems
  - `4e5c8de` (work show / work status, requests r13, r14) also lies in that range. It is w129's commit, merged by
    the pool between w131's claim and its done (`418ae04 work: w129 claimed -> done`), not w131's.
- The implementer's result lists `05d6b56`. `d23a6a4` is the same change replayed onto HEAD:
  `git show --stat` gives the same 9 files and the same +94/-27 for both, and `git diff 05d6b56 d23a6a4` shows only
  w129's files. So they match. This is not a finding.

## Removed and weakened tests

Searched the diff for removed `def test_`, scenarios, parametrize or Examples rows, changed `assert` lines, and
added skip or xfail markers.

- `test_design_model_check.py::test_model_reads_the_repositorys_files_under_its_root_deprecated` (13 cases, bound by
  `scenarios("design-model-check.feature")`). It pinned which files model reads under `--root`, before the requests
  row was added. The scenario was removed from `features/design-model-check.feature:126-149`. The work-item's
  Retires section names it, and the plan lists it under "Tests the decisions break". It holds.
  (The plan and report say "14 cases"; the deprecated outline had 13 rows. Not material.)
- Nothing else was removed or weakened. The only other test changes are additions: a row in the `_files_read` table
  (`design_model_check_reading.py:107`), the new Givens module, and its import.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commit agrees: no existing test's assert,
expected value or case changed.

## Cannot verify

- The report's "Suite at start: 757 passed, 5 failed" and "160 passed, 1 skipped" under `--work-item w131`. I did
  not run the whole suite. I ran the three accepted scenarios by name: 18 passed (14 r19 rows, 1 r112, 3 r118).

## Findings

### 1. Minor: import block un-sorted (ruff I001), `tests/scenarios/test_design_model_check.py:16`
- Work-item: w131. Triage: **drop** (cheap, but cosmetic).
- `from .design_model_check_requests import *` was inserted before `design_model_check_reading`. `tools check`
  reports `I001 Import block is un-sorted` there. The block was sorted at the base.
- Why it matters: `tools check` is no longer clean on this file.
- Fix: put the import after `design_model_check_reading` (`ruff --fix`).

### 2. Minor: the Givens ignore the file name in their path, `tests/scenarios/design_model_check_requests.py:16-25`
- Work-item: w131. Triage: **drop**.
- `request_with_no_asker` always writes id `.../q1`, and `request_work_request_wrote` always writes `.../q2`,
  whatever `{path}` names. A future scenario that uses another file name with these Givens would get a file problem
  for a name that does not match the id, not for the reason its title gives.
- Fix: take the id's name from `Path(path).stem`.

### Risks checked, no finding
- **The form check (D2) against what `work request` writes on HEAD.** `scripts/workqueue_request.py:74-77` writes
  `id request/<path>/q<n>`, `kind: request`, `asker`, `part_of` or `source`, `status: open`, `turn: upstream`, a
  `# title` line (not a `##` section), and `## Lines`, `## Outcomes` and `## Resolution`. Every one of these passes
  `request_form`. `model check` does not flag a file that `work request` writes.
- **Code no line asks for.** Each check in `request_form` follows the file form in requests' Implementation
  (spec/capabilities/requests.md:44-47), which r112 names as its authority. The job/job-path file problem is r118.
  Skipping `requests/` as an initiative folder is r19. The status list follows requests r1, r8, r9, r11, r17 and r18.
  The help text and the CLAUDE.md row describe these. Nothing else is added.
- **features/.** The only change removes the deprecated scenario that Retires names.
- **Size.** `tools size --limit 300` printed nothing.

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w131 ready -> claimed$"` (and the same for `claimed -> done`), then `git log --oneline -8`
- `git show --stat 05d6b56`, `git show --stat d23a6a4`, `git show --stat 4e5c8de`, `git diff 05d6b56 d23a6a4 --stat`, `git diff 05d6b56^!`
- `grep` on features/design-model-check.feature, spec/capabilities/design-model-check.md, spec/capabilities/requests.md, scripts/workqueue_request.py, scripts/model_work.py, scripts/model_facts.py and tests/scenarios/test_design_model_check.py
- `python3 -m pytest -q -n 0 tests/scenarios/test_design_model_check.py -k "files_under_its_root or not_of_the_form or job_or_jobpath or job_or_job"`: 18 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 1f97efc…`: ruff found one error (the I001 above); vulture clean; import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output
