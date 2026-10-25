# Review of w168 (answer-by-initiative: work-queue, accepts work-queue#r30)

**Verdict: DONE.** No Critical finding and none triaged fix now. The change does what r30 asks, the bare form is unchanged, and every `work answer` scenario passes.

## Commits reviewed

The branch `work/w168` is gone, so I took the commits on the checked-out branch between `39fad50d work: w168 ready -> claimed` and `37a7c7fc work: w168 claimed -> done`:

- `fa6929fb` work answer: name a work-item or proposal by `<initiative>/<name>` (work-queue r30). Files: `scripts/workqueue_answer.py` (+8/-2), `README.md` (+1/-1).

This matches the implementer's `result.json` (`commits: [fa6929fb ...]`). Both files are inside the work-item's fileset.

## Removed and weakened tests

None. `git diff --stat 39fad50d 37a7c7fc -- features tests` is empty: the commit touches no test, step, parametrize case, skip/xfail or feature file. The plan's "Tests the decisions break" says none, and that holds.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commit changes no test, so that holds.

## Cannot verify

- The report's "Suite at start: 858 passed, 3 failed". The implementer did not run that itself, and I did not run the whole suite (`work run` runs it before merging).
- The report's red run (2 failed before the change). I took it from the plan's diagnosis: `find` refuses `/` (scripts/workqueue.py:224). I did not re-run the parent revision.

## Findings

No Critical or Important findings. I checked these risks:

1. **Path traversal through the prefixed form.**
   - The risk: `../x/w1`, `i1/`, `/w1` or `i1/w1/extra` reaching a path outside `.shop/work/<initiative>/`.
   - What I verified: `name.split("/", 1)` puts any second `/` into the name part. `workqueue.entry` (scripts/workqueue.py:58-61) refuses `""`, `.`, `..`, `/` and `\`. A missing file is refused by `agrees` (scripts/workqueue.py:189-190). So every one of those forms is refused, as plan decision 2 says.
2. **The bare name passed on after the split.**
   - The risk: the prefixed `i2/w2` reaching `agrees`, `asked_from`, `move` or the commit message, where the log would record a work-item named `i2/w2`.
   - What I verified: line 30 rebinds `name` to the bare part before every later use (scripts/workqueue_answer.py:37-58).
3. **Code no line asks for.** None found. The only new observable behaviour is answering the named initiative's file (r30). The refusals are r7's existing ones. The printed line is unchanged (plan decision 3).
4. **The bare form regressed.** No. All 19 `work answer` scenarios pass with `--whole-suite -k answer`: r13, r14, r15, r24, the r9 rows and the 2 r30 rows.

Minor:

- **M1 (Minor, drop)**, README.md:141. The edited line now runs past the README's ~120-column wrap; the lines around it are wrapped. It is cosmetic, and re-wrapping is polish this review does not ask for.
- **M2 (Minor, observation)**, scripts/workqueue_answer.py:31-37. An unknown initiative (`nosuch/w1`) is refused with `agrees`' text: `.shop/work/nosuch/w1.md does not exist; there is no work-item w1 to move`. That is correct and changes nothing (r7). It names the missing file rather than the missing initiative, and the plan left that open (§5). Reproduction (from the code, not run): `work answer nosuch/w1 x` reaches `agrees` with `path.is_file()` false and raises that Refused. No client sends this today.

The plan's other open cases:

- A glob in the prefixed form: no finding. The prefixed path is built literally and never globbed, so `i1/w*` is a missing file and refused.
- A done or archived initiative: no line names it, so it is not a finding.

## Tool checks

- `tools check --base 39fad50d`
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `tools size --limit 300`: prints nothing, so no tracked Python file is over the limit. `scripts/workqueue_answer.py` is 60 lines.

## Commands run

- `git log --format='%H %s' -25`
- `git show --stat fa6929fb`
- `git show fa6929fb -- . ':!.shop'`
- `git diff --stat 39fad50d 37a7c7fc -- features tests`
- `python3 -m pytest -q tests/scenarios/test_work_queue.py -k answer`: 2 passed (the plugin deselects the other scenarios)
- `python3 -m pytest -q --work-item w168`: 144 passed, 1 skipped
- `python3 -m pytest -q tests/scenarios/test_work_queue.py --work-item w168 --whole-suite -k answer`: 19 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 39fad50ddc89883b0c981803f007d685360f3add`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- Read with grep: `scripts/workqueue.py` (`entry`, `agrees`, `find`, `read`, the imports), `pytest.ini`, `scripts/work_items.py` docstring
