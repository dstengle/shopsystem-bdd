# Review of w133 (second review, after the person's answer): measure gives whether the initiative's request is internal or external

**Verdict: DONE.** r63 and r64 are met and nothing under `features/` changed. No test was removed or weakened. Stage 5
found one Important fix-now finding: refusals that no Behaviour line asks for. The answer of 2026-10-25 accepted it as
it stands and recorded it as an observation for a later line (`4363b41`, `.shop/records/observations.md`). So it
stands here as ruled, not as fix now. What is left is Minor: one ruff I001 error in a touched file, one formatting
slip, and the plan's open cases.

## Commits reviewed

The branch `work/w133` is gone. I took the commits between `3e80c5c work: w133 ready -> claimed` and
`a219346 work: w133 claimed -> done` on HEAD and left out `work run`'s own commits (w137, w127, w130):

- `e713679` measure gives whether the initiative's request is internal or external (r63, r64): 8 files, +90 -9.

The implementer's result lists `b419ef0` with the same subject, and its `--stat` matches `e713679` file for file. It is
the same change landed after `work run`'s commits, so the two lists do not differ in substance. No later commit
touches the work-item's file set (`git log a219346..HEAD -- <fileset>` is empty). Every file is inside the file set.

## Removed and weakened tests

None. I searched the diff for:
- removed `def test_` lines;
- removed or changed `@given`/`@when`/`@then` steps;
- removed or loosened `assert` lines;
- changed parametrize or Examples rows;
- added `skip` or `xfail`.

The test files only gain lines: the field `World.request`, `flush` writing `initiative.md` and the request file, the
new `batch_measurement_request_steps.py`, and one star import. `git diff 3e80c5c a219346 --stat -- features/` is
empty.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test changed.

## Cannot verify

- That the suite is green (the report gives 145 passed on `--work-item w133`). I did not run it; `work run` runs it
  before it merges.
- That `tools refs` confirmed the rename of `_path`/`_field`. A grep for `workqueue_request.(_path|_field|path_of|field)`
  finds no caller outside `workqueue_request.py` other than the new `measure_read.request_of`, and vulture is clean.

## Findings

### 1. Important, ruled (w133): refusals no Behaviour line asks for
`scripts/measure_read.py:55-66`. `measure initiative` refuses in three cases:
- the request is missing;
- the request has no `asker`;
- `fulfils` holds more than one id.

No batch-measurement line asks for these refusals. The person's answer (2026-10-25, through the coordinator) accepted
the work-item as it stands, with the case recorded as an observation for a later line (`4363b41`). This review does not
reopen the finding. Triage: **observation (ruled)**.

### 2. Minor, observation (w133): ruff I001 in `scripts/measure_build.py`
`scripts/measure_build.py:7-14`: `request_of` is imported between `read_log` and `read_session_jsons`.
- To reproduce: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 3e80c5c…` printed
  `scripts/measure_build.py:3:1: I001 [*] Import block is un-sorted or un-formatted` and exited 1.
- The other I001 it prints, `scripts/workqueue.py:235`, is not from w133: `workqueue.py` was last changed by
  `e0ba985`, which is another work-item's commit.
- Fix: put `request_of` after `read_transcripts`, or run `ruff --fix` on the file.

### 3. Minor, drop (w133): formatting
`scripts/workqueue_request.py:123` reads `after =edit(...)`, with no space after `=`. It came in with the rename.
Fix: `after = edit(...)`.

### 4. Minor, observation (w133): the plan's open cases, named and not chosen
Plan section 5 left these cases open:
- A `fulfils` value of another kind (`observation/q3`) passes the character test, and is read as the request `q3` by
  its last segment.
- A request that is not `accepted` is measured anyway.

No client writes `fulfils` today. The fixture writes `request/q3` only (`tests/scenarios/batch_measurement_world.py`).
`model check` (v16d) holds both cases.

## Risks I verified outside the diff

- **Shadowing.** `field(text, field)` has a parameter with the function's own name, and `_with_field` has a parameter
  `field`. Neither calls the module-level `field` from inside, so nothing is shadowed in use
  (`grep -n field scripts/workqueue_request.py`).
- **Missing or unreadable context id.** `workqueue.context_path` (`scripts/workqueue.py:36-45`) raises
  `workqueue.Refused` when `spec/index.md` is missing or gives no id. `request_of` catches that and raises it again as
  measure's `Refused`, so the result is a refusal, not a traceback. The `or` short-circuits on the asker `internal`.
- **The external example.** The fixture's asker `bounded-context/ex.com/prod/other` is compared with
  `"bounded-context/" + context_path(root)`, which is `bounded-context/ex.com/prod/ctx`. They differ, so the origin is
  `external`, as the Examples row expects.
- **`measure show`.** It prints the request table only when the figure is there. r44 ("the measurement's figures as
  tables") covers this, so it is not code no line asks for.

## Tool results

- `tools check --base 3e80c5c1fa7a0710baa1f180e29b7acda6b1d1a1`:
  - ruff: 2 errors. `scripts/measure_build.py:3` is finding 2. `scripts/workqueue.py:235` is not w133's.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. No tracked Python file is over the limit.

## Commands run

- `cat` of the brief, the work-item, the capability, the plan, the report, `result.json` and stage 5's findings
- `git branch -a`, `git log --oneline -12`, `git log --format='%H %s' --grep="^work: w133 " --all`
- `git log --format='%h %s' 3e80c5c..a219346`, `git log a219346..HEAD` (all, and limited to the file set)
- `git show --stat e713679`, `git diff --stat b419ef0^ b419ef0`, `git show e713679`
- `git diff 3e80c5c a219346 --stat -- features/`, `git show --stat 4363b41`, `git log 3e80c5c..HEAD -- scripts/workqueue.py`
- `grep` on `scripts/workqueue.py`, `scripts/workqueue_request.py`, `features/batch-measurement.feature`, and the
  repository for `workqueue_request` callers
- `cat spec/decisions/0060-measure-an-initiative.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 3e80c5c1fa7a0710baa1f180e29b7acda6b1d1a1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
