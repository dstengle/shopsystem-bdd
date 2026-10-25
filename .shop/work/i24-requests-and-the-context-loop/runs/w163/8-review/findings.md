# Review of w163 (accepts supervision#r79, supervision#r84)

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now. The fix works: an integrate round that ends DONE now commits its stage directory, so the next `work run` is not refused. But it lands as a second commit. The scenario's text and the person's answer ask for one commit holding the stage directory and the change to `started`. The new step definition is written loosely, so it passes on the two commits anyway.

## Commits reviewed

The ready -> claimed commit is 103aee03. The branch `work/w163` is gone, so the commits are those between 103aee03 and `work: w163 claimed -> done` (e8a6d4e2), less `work:` commits:

- aa842020 `work run: commit an integrate round's stage directory once it ends DONE (r84)`: scripts/supervise_rounds.py +3, tests/scenarios/supervision_rounds_steps.py +16.

The implementer's result lists `acb76107`. That commit exists and has the same message, author date and stat (+3/+16 in the same two files). It is the same commit before work run's rebase or merge. The difference is noted (F3).

The @r84 scenario at features/supervision.feature:1063-1073 was added in c552fa6c by the formulator, before the claim. That matches the person's answer. The commits make no change under `features/` (`git diff --stat 103aee03 HEAD -- features` is empty).

## Removed and weakened tests

None. I searched `git diff 103aee03 HEAD -- tests` for any removed line: 0. The only test change is two new step definitions. No test function, parametrize case, assert, skip or xfail was removed or changed.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: no existing test was changed.

## Cannot verify

- The report's suite figures ("849 passed, 1 failed at 27f26a0d"; `--work-item w163`: 147 passed, 1 skipped). I did not run the suite, as the brief directs. I ran only the two r84 scenarios (below).
- The report's claim that committing `started` after the round, as one commit, makes the worker guard (supervise_worker.py:185-195) fault the round. This is the stated reason for using two commits. I did not reproduce it.
- That the push after the new commit reaches the remote (`self.commit` pushes by default). No scenario here checks the push.

## Findings

### F1: Important, fix now. The stage directory and the change to `started` land in two commits; the step passes anyway

Where:
- The code: scripts/supervise_rounds.py:85-87, with `start_initiative` at :89-94.
- The step: tests/scenarios/supervision_rounds_steps.py:97-105.

What is wrong:
- The scenario (features/supervision.feature:1070) says "the initiative branch has a commit of the integrate round's stage directory with i1's change to started". The person's answer in the brief says: "one commit holding the stage directory, its log.jsonl lines and the initiative's change".
- The implementation does something else. `start_initiative` commits `started` before the session starts. The new branch then makes a second commit after the round, `work: i1 started -> started`, holding the stage directory.
- The step definition checks only for some commit that touches the stage directory, at which `initiative.md` reads `status: started`. Every commit after `start_initiative` meets that. So the step cannot tell one commit from two, and it passes on more than the scenario says.

Why it matters:
- The scenario reports green on a shape the person explicitly asked against.
- A later regression is also invisible: the stage directory committed by any unrelated later commit would pass the step too.

Fix:
- The implementer raised this as an open question, so it needs a ruling first. Either:
  - **(a) Keep two commits.** Reword the scenario's Then through a formulation round (the stage directory is committed after the commit of `started`). Then tighten the step to say exactly that, for example: the stage directory's first commit is the commit right after the commit that changes `initiative.md` to `started`.
  - **(b) Make it one commit.** Exempt `initiative.md`'s change to `started` from the worker guard. Then make the step assert that the same commit's diff changes `initiative.md` from `proposed` to `started` and adds the `-integrate/` stage directory.

### F2: Minor, observation. The new commit's message reads as a transition

Where: scripts/supervise_rounds.py:87, which calls `self.commit(name, after, after)`; the message is written at scripts/supervise.py:103.

What is wrong:
- The message `work: i1 started -> started` claims a transition that did not happen.
- `measure_build.py:81` reads `work: <name> .*-> .*` as one of `<name>`'s moves, and this message matches that pattern.
- The other commits with no transition use messages of their own: `work: %s %s round %s faulted` (supervise_rounds.py:102) and `work: %s intake round ...` (supervise_intake.py:109).

Why it matters: little today, since measure takes moves per work-item. But a reader of the log, or a later measure of an initiative, would see a transition that did not happen.

Reproduction: reading the code only. The regex at measure_build.py:81 matches `work: i1 started -> started` (`.*-> .*`). I ran no Python probe, which the brief does not allow.

Fix: give this commit a message of its own, like `keep_round`'s, e.g. `work: i1 integrate round <label> done`. That needs `commit` to take a message, or a small helper.

### F3: Minor, drop. The implementer's result does not match the branch

Where: .shop/work/i24-requests-and-the-context-loop/runs/w163/7-implement/result.json.

What is wrong:
- `commits` lists `acb76107`, but the branch holds `aa842020`. Their content is identical.
- `questions` is empty, though the report has three open questions. The first of them is F1.

### Risk checked, not a finding

- **Risk:** the new `self.commit` runs `git commit` without first checking `git status`, unlike `keep_round`. If nothing were staged, it would raise GitFailed outside the round's try block.
- **What I verified:** an integrate round's stage directory (`runs/<init>/<k>-integrate/`) is written in the main checkout by work run (brief, result, session) and was never committed before (the finding of branch review 3). The DONE path always has something to stage, so this is not reached.

## Checks

- `tools check --base 103aee03`: ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts".
- `tools size --limit 300`: nothing printed. The touched files have 105 lines (supervise_rounds.py) and 258 lines (supervision_rounds_steps.py).
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "leaves_nothing_uncommitted or initiative_is_started"`: 2 passed.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w163 ready -> claimed$"` gave 103aee03; the same for `claimed -> done` gave e8a6d4e2.
- `git log --oneline 103aee03..HEAD`, `git show --stat aa842020`, `git show aa842020`, `git show --stat acb76107`, `git show --stat e8a6d4e2`
- `git diff --stat 103aee03 HEAD -- features tests`; `git diff 103aee03 HEAD -- tests | grep -c '^-[^-]'` gave 0
- `grep -n -B2 -A10 "leaves nothing uncommitted" features/supervision.feature`; `grep -n "r84\|r46\b\|r7\b" spec/capabilities/supervision.md`
- `sed -n 55,110p scripts/supervise_rounds.py`; `grep -n "def commit|def move|def keep_round" -A14 scripts/supervise.py`; `sed -n 75,92p scripts/measure_build.py`; `sed -n 60,80p scripts/supervise_worker.py`
- `grep -rn '"work: ...' scripts/...` (readers of `work:` commit messages)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 103aee03...`; `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`; `wc -l` of the two touched files
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "leaves_nothing_uncommitted or initiative_is_started"`
