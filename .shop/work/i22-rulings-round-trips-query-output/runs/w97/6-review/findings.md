# Review of w97: work-item ids, the review's open findings

**Verdict: DONE.** No Critical finding, none triaged fix now. The commit does what the plan's decisions 1–6 say, and it follows the person's answer of 2026-10-23 (reading A).

## Commits reviewed

- Claim commit: `8659d64` (`work: w97 ready -> claimed`). The branch `work/w97` is gone, so the commits are those between it and `f858c04 work: w97 claimed -> done` on HEAD.
- `625728c work-item ids: check the held id and its stem, count ids in work add, refuse a plain note`. This is the only non-`work:` commit, and it is the one commit the implementer's `result.json` lists. They match.
- It changes 4 files, the work-item's fileset exactly: `scripts/model_work.py`, `scripts/workqueue.py`, `tests/scenarios/design_model_check_problems.py` and the new `tests/scripts/test_work_item_ids.py`. Nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff for:
- deleted `def test_`;
- parametrize edits;
- removed or loosened `assert` lines;
- `skip` and `xfail`;
- changed expected values.

The one test-code change is the step "it prints a file problem naming …" (`design_model_check_problems.py:164-167`):
- **Before:** it dropped r110's problems for every fixture.
- **Now:** it drops them only when the named path is not a `w<n>.md`.

So the step counts more problems than before and passes on fewer cases. It is a tightening, not a weakening. The plan names it under "Tests the decisions break" (decision 5).

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: no test's asserts were changed under an allowance, and the step's rewrite is a planned decision (decision 5).

## Cannot verify

- **That every scenario using the rewritten step passes.** The plan asked the implementer to rerun them. The report claims test_design_model_check and test_work_queue are green. My focused run of those two modules passed, but `pytest.ini`'s `-m "not fixture"` deselects most of their scenarios. I did not run the whole suite; `work run` ran it before merging.
- **The 2 failures in `tests/scripts/test_tools.py` that the report calls environmental** (a nested pytest given `--work-item w97`, "no such work-item"). Nothing in the commit touches `tools_map` or `test_tools`, so it cannot be their cause. I cannot confirm from the commits that the failures are environmental.

## Risks checked

1. **Held key is the raw frontmatter id, not a qualified id.** `read_part` passes the id as written (`p`), so `w3` and `work-item/<ctx>/w3` would be different keys.
   - Verified: `check_id` (`model_facts.py:73-77`) already reports any work-item id not of the form `work-item/<context path>/<name>`. An unqualified id is a problem in its own right, so no duplicate goes unreported.
2. **`work add` refusing over an existing file that is a work-item.**
   - Verified: `highest` counts every work-item's stem (`workqueue.py:62-71`). So the path for `w<highest+1>.md` can only be a file that is not a work-item, and the new wording ("… is a file that is not a work-item") is always true. It names the path and writes nothing (r7), as the person's reading A says. The new test asserts that HEAD and the note are unchanged.
3. **N7.** `entry`'s message for `what="initiative"` is the same text as before ("the initiative X is not a name"). Only the unreachable branch went.

## Findings

### F1. Minor: the id/stem problem goes further than r110's table text (observation)

- **Where:** `scripts/model_work.py:84-85`.
- **What is wrong:** the check now reports a work-item `w3.md` whose id is `…/w9`. r110's table says only "a work-item's file name is not `w<n>.md`, or two work-items have one id", which does not literally cover this case.
- **Why it is accepted:** the capability rests on design-decision/work-items-named-by-ids (0061), which binds the file `w<n>.md` and the id `work-item/<ctx>/w<n>` to the same `w<n>`. The work-item's finding F6 asks for exactly this check. So it is code a binding decision gives, not code no line asks for.
- **Fix:** none needed in the code. When r110 is next touched, its wording could say "is not `w<n>.md`, the `w<n>` of its id".
- **Reproduction:** `tests/scripts/test_work_item_ids.py::test_a_work_item_whose_id_is_not_its_file_stem_is_a_file_problem` passes.
- **Triage:** observation (wording of a line, no wrong answer).

### F2. Minor: ruff style on the new lines (drop)

- **Where:**
  - `workqueue.py:59, 91` (UP031, percent format);
  - `tests/scripts/test_work_item_ids.py:11` (RUF100, unused `noqa: E402`), `:18` (UP031), `:44` (PLW1510, `subprocess.run` without `check`).
- **Why it does not matter much:** the files around them use the same percent-format style throughout, and `tools check` reports about 100 such hits in the files the base range touched.
- **Fix:** none needed now.
- **Triage:** drop.

## Tool results

- **ruff:** 100 hits over the files touched since the base. The ones on w97's lines are listed in F2; the rest are pre-existing or in other work-items' files.
- **vulture:** clean.
- **import-linter:** the project states no import contracts.
- **size (`--limit 300`):** printed nothing; no file is over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w97 ready -> claimed$"` gave `8659d64`.
- `git log --oneline -12` and `git log --ancestry-path 8659d64..f858c04`
- `git show --stat 625728c` and `git show 625728c`
- `grep` of the r110, r12 and r7 lines, and of `check_id`; `sed` of `model_work.py` around `read_part`
- `cat spec/decisions/0061-work-items-named-by-ids.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 8659d64…`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q -n 0 tests/scripts/test_work_item_ids.py tests/scenarios/test_design_model_check.py`: 8 passed (173 deselected by `-m "not fixture"`)
- `python3 -m pytest -q tests/scenarios/test_design_model_check.py tests/scenarios/test_work_queue.py -m ""`: 5 passed
