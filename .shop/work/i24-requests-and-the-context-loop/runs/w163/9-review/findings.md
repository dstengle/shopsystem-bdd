# Review 9 of w163 (accepts supervision#r79, supervision#r84)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now.

Review 8's one fix-now finding was that the work lands as two commits: first the commit of `started`, then the commit of the stage directory. The person has ruled on it (third answer in the brief, 2026-10-25): "two commits on the initiative branch, started and then the stage directory, meet the scenario's point". The step definition checks that shape, so the finding is closed. What is left is two Minor items.

## Commits reviewed

The ready -> claimed commit is 103aee03. `work/w163` does not exist in this checkout, so the commits are those from 103aee03 to `work: w163 claimed -> done` (e8a6d4e2), less the `work:` commits:

- aa842020 `work run: commit an integrate round's stage directory once it ends DONE (r84)`. It changes scripts/supervise_rounds.py (+3) and tests/scenarios/supervision_rounds_steps.py (+16).

The implementer's result lists `acb76107`. That commit has the same message, author date and stat as aa842020, so it is the same change before work run brought it onto the branch (F2). Nothing changed under `features/`: `git diff --stat 103aee03 HEAD -- features tests scripts` lists only the two files above. The @r84 scenario at features/supervision.feature:1063-1073 came in earlier, in c552fa6c, written by the formulator as the person's answer says.

## Removed and weakened tests

None. I looked for removed lines in `git diff 103aee03 HEAD -- tests scripts`, which adds 19 lines and removes none. No test function, parametrize case, assert, skip or xfail was removed or changed. The only test change is two new step definitions.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds, because no existing test changed.

## Cannot verify

- The report's suite figures (849 passed, 1 failed at 27f26a0d; `--work-item w163` 147 passed, 1 skipped). The whole suite was not run, as the brief directs.
- The report's claim that one commit would trip the worker guard (supervise_worker.py:185-195). It is moot now that the person accepts two commits.
- That the push after the new commit reaches the remote. No scenario here checks it.

## Findings

### F1: Minor, observation. The new commit's message reads as a transition that did not happen
- **Where:** scripts/supervise_rounds.py:87 calls `self.commit(name, after, after)`, and supervise.py:103 writes the message from it: `work: i1 started -> started`.
- **Why it matters:** measure_build.py:81 reads `work: <name> .*-> .*` as a move, so the log shows a transition that did not happen. Other commits that make no transition get messages of their own, such as `work: %s %s round %s faulted` (supervise_rounds.py:102).
- **Reproduction:** from the code only. The commit message pattern matches the regex at measure_build.py:81.
- **Fix:** give the commit its own message, e.g. `work: i1 integrate round <label> done`.

### F2: Minor, drop. The implementer's result names a different commit
- **Where:** 7-implement/result.json.
- **What is wrong:** `commits` lists acb76107, but the branch holds aa842020. Their content is identical.

### Risk checked, not a finding
- **Risk:** the new `self.commit` runs without first checking `git status`, unlike `keep_round`, so if nothing were staged it would raise GitFailed outside the round's try block.
- **What I verified:** an integrate round that ends DONE always leaves its stage directory written and uncommitted (brief, result, session; the finding of branch review 3). So the commit always has something to stage.

### Note, outside the commits reviewed
The research probe repositories under runs/w163/2-research/probe_repos (224 files, including bare git repos) are tracked on the initiative branch. That is work run's commit of the research stage directory, not the implementer's, so it is not graded here. The work-item had asked for probes under .shop/scratch/.

## Checks
- `tools check --base 103aee03…`: ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts".
- `tools size --limit 300`: printed nothing. The touched files are 105 lines (supervise_rounds.py) and 258 lines (supervision_rounds_steps.py).
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "leaves_nothing_uncommitted or initiative_is_started or integrate"`: 5 passed (the four accepted scenarios and the @r84 one).

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w163 ready -> claimed$"` gave 103aee03; the same for `claimed -> done` gave e8a6d4e2.
- `git log --oneline 103aee03..HEAD`; `git show aa842020`; `git show --stat acb76107`
- `git diff --stat 103aee03 HEAD -- features tests scripts`
- `sed`-free reads: `scripts/supervise_rounds.py` lines 55-105, `grep -n "def commit" -A16 scripts/supervise.py`, `grep -n -B3 -A12 "leaves nothing uncommitted" features/supervision.feature`, and a grep of r7, r46 and r84 in spec/capabilities/supervision.md
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 103aee03…`; `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`; `wc -l` of the two touched files
- the focused pytest run above; `git ls-files …/2-research/probe_repos | wc -l` gave 224
