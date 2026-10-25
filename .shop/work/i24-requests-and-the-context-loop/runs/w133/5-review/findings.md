# Review of w133: measure gives whether the initiative's request is internal or external

**Verdict: DONE_WITH_CONCERNS.** r63 and r64 are met and no test was removed or weakened. One finding is Important and
fix now: `measure initiative` now refuses when the link to the request can't be read, and no Behaviour line asks for
that refusal. One Minor finding is a ruff import-order error.

## Commits reviewed

The branch `work/w133` is gone. The commits between `3e80c5c work: w133 ready -> claimed` and
`a219346 work: w133 claimed -> done` on HEAD, less `work run`'s own `work:` commits, are:

- `e713679` measure gives whether the initiative's request is internal or external (r63, r64): 8 files, +90 -9.

The implementer's result lists `b419ef0` with the same subject. `b419ef0` is still in the object store and its
`--stat` matches `e713679` file for file and line for line. `e713679` is that commit landed on top of `work run`'s
`work:` commits (w130, w127, w137), so this is not a difference in content. Every file is inside the work-item's
fileset, and nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff for removed `def test_`, removed or changed `@given`/`@then`/`@when`, removed `assert`
lines, changed parametrize or Examples rows, and added `skip` or `xfail`. The test files only gain lines:
- `batch_measurement_world.py`: the field `World.request`, and `flush` writing `initiative.md` and the request.
- `batch_measurement_request_steps.py`: a new file.
- `test_batch_measurement.py`: one star import.

The new step "the measurement gives the stage of {item}'s {stage}" overlaps no existing step text. The existing
steps are "the measurement gives the stage" and "... with {turns:d} turns".

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commits agree: no existing test changed.

## Cannot verify

- That the suite is green (145 passed on `--work-item w133`): I did not run it. `work run` ran it before the merge.
- That `tools refs` and the search confirmed that renaming `_path`/`_field` broke no caller. The diff renames every
  caller inside `workqueue_request.py`, vulture reports clean, and no other module used the private names.

## Findings

### 1. Important, fix now (w133): a refusal no Behaviour line asks for
`scripts/measure_read.py:55-66` (`request_of`). `measure initiative` now refuses, exiting with an error and writing
nothing, in three cases:
- `fulfils` holds a value that isn't one id (the character-class test on line 57);
- the linked request is missing (work's `workqueue.Refused` is re-raised as measure's `Refused`, line 64);
- the request has no `asker` (line 62).

No line of batch-measurement asks for any of these:
- r63 and r64 cover only a readable link and the absence of a link.
- r46, r47 and r48 name other inputs.
- r50 says only that a refusal exits with an error.
- Decision 0018 (measure-refuses-unknown-shapes) is about transcripts.

The plan rests the refusals on the Purpose ("refuses rather than guesses") and decision 5. The refusals do keep the
Purpose: without them, a request with no asker would come out as `external`, which is a guess. But behaviour reaches
code only through a line.

**Fix:** write the line first through integrating-a-proposal. For example: "[rNN] **If** the request the initiative
fulfils is missing, has no asker, or `fulfils` holds more than one id, **then** `measure initiative` shall refuse,
writing nothing, naming the file." Then give it a scenario. Removing the code instead would turn the missing-request
case into a traceback and the no-asker case into a guessed `external`, so the line is the right fix.

### 2. Minor, observation (w133): ruff import-order error
`scripts/measure_build.py:7-14`. The new name `request_of` sits between `read_log` and `read_session_jsons`, so
`tools check` fails with ruff I001. To reproduce: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 3e80c5c`
printed `scripts/measure_build.py:3:1: I001 [*] Import block is un-sorted or un-formatted` and exited 1. **Fix:** put
`request_of` after `read_transcripts`, or run `ruff --fix`.

### 3. Minor, drop (w133): formatting
`scripts/workqueue_request.py:123` reads `after =edit(...)`, with no space after `=`. It came in with the rename.
Ruff, as configured, doesn't flag it. **Fix:** `after = edit(...)`.

### 4. Minor, observation (w133): open cases left unchosen, as the plan asked
These are the plan's section 5 cases, named in the report:
- A `fulfils` value of another kind passes the character test and is read as a request by its last segment. For
  example, `observation/q3` reads `requests/q3.md`.
- A request that isn't `accepted` is measured all the same.

No client writes either today: `grep -rn fulfils .shop/work --include=initiative.md` found no initiative with the
field. `model check` (v16d) holds both cases.

## Risks I verified outside the diff

- **Missing `spec/index.md`.** Does reading the context id break `tests/scripts/test_measure_runs.py`, which has no
  `spec/index.md`? `workqueue.context_path` refuses when the file is missing (`scripts/workqueue.py:36-45`). It is
  reached only when `asker != "internal"`, because the `or` short-circuits, and only when a request is linked. So it
  is not reached in those tests, and if reached elsewhere its refusal becomes measure's `Refused`.
- **Refusal output.** Is a measure `Refused` turned into an error exit? Yes: `scripts/measure:90` catches it.
- **Step overlap.** Covered under Removed and weakened tests above.

## Tool results

- `tools check --base 3e80c5c`:
  - ruff: 1 error (finding 2).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. No tracked Python file is over 300 lines.

## Commands run

- `git log --format='%H %s' --grep="^work: w133 "`, `git log --oneline -15`
- `git log --format='%H %P %s' 3e80c5c..a219346`
- `git show --stat e713679`, `git show b419ef0 --format= --stat`, `git show e713679 --format=`
- `grep` on `spec/capabilities/batch-measurement.md`, `features/batch-measurement.feature`, `tests/scenarios`,
  `scripts/workqueue.py`, `scripts/measure`, `.shop/work/**/initiative.md`
- `cat spec/decisions/0018-measure-refuses-unknown-shapes.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 3e80c5c1fa7a0710baa1f180e29b7acda6b1d1a1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
