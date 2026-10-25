# Review of w147 (second review, after the person's answer): DONE

Verdict: the commit reviewed is the same as in the first review (`4-review`), and it has not changed since. r77 and r78 are green: all three scenarios pass on HEAD. No test was removed or weakened, and nothing under `features/` changed.

The first review raised two Important fix-now findings: F1, the answer pass runs once a run, and F2, a faulted answer session leaves uncommitted state. The person ruled on both on 2026-10-25 ("Accept the work-item as it stands"):
- F2 gets a supervision line first (integrate round 8), then its own fix work-item.
- F1 is accepted for now as an observation. Commit `0993412` recorded it as `2026-10-25-answer-pass-once-a-run`.

Both are carried below, triaged as that ruling says. Neither is put to the person again. No new finding is fix now or Critical.

## Commits reviewed

The branch `work/w147` is gone. On HEAD, between `0798166 work: w147 ready -> claimed` and `be50925 work: w147 claimed -> done`, the only commit that is not a `work:` commit is:

- `3f97115` work run: questions under a request's delegation go to sessions of their own, the answer naming the delegation (r77, r78). It changes 8 files, +259/-3: CLAUDE.md, agents/delegation-answerer.md, scripts/supervise.py, scripts/supervise_answers.py, scripts/supervise_brief.py, scripts/supervise_worker.py, tests/scenarios/supervision_delegation_steps.py and tests/scenarios/test_supervision.py.

The implementer's result lists `8565af5`. `git diff 8565af5 3f97115 -- scripts agents tests features CLAUDE.md` is empty, so the code is identical and only the hash differs (F5).

After `be50925`, two commits touched these files: `bbca36c` and `c79de72`, both in `supervise.py`. They belong to other work-items and are not reviewed here.

## Removed and weakened tests

None. I searched the diff for:
- deleted test functions or steps;
- dropped parametrize cases;
- removed or loosened asserts;
- added skip or xfail.

The only test changes are a new module (`supervision_delegation_steps.py`) and one added star import (`test_supervision.py:27`).

## Allowances

The report gives "none", and the commits agree: no existing test changed.

## Cannot verify

- **The result file.** Whether a real `delegation-answerer` session can write its result file. `TOOLS["answer"]` is Read, Glob, Grep and has no Write. This is the same arrangement as the researcher and reviewer stages, but the stub does not exercise it.
- **The agent keeping to its brief.** Whether a real session reads only the delegation and the named files. It runs in a full worktree, so this rests on its instructions alone.
- **The report's suite counts.** I did not rerun the suite; `work run` ran it before the merge.

## Findings

### F1. Important, observation (w147, ruled 2026-10-25): the answer pass runs once a run
`scripts/supervise.py:193`, `scripts/supervise_answers.py:59-80`. `answers()` runs only before `rounds()`. A question raised later in the same run, by a gate round (r69/r85) or by a worker (r5), goes to the person with exit 3. This is plan D6's repeat, which was not done. The person accepted it for now, and it is recorded as observation `2026-10-25-answer-pass-once-a-run` (commit `0993412`).

### F2. Important, deferred to its own fix work-item (w147, ruled 2026-10-25): a faulted answer session leaves uncommitted state
`scripts/supervise_answers.py:85-96`. `ask()` raises Refused after `Workers.worker` has already copied the stage directory and written its `log.jsonl` lines. Nothing commits them, so the next `work run` is refused (r46), and the work-item does not go `failed` (r45). By the person's ruling, this gets a supervision line in integrate round 8, then its own fix work-item.

### F3. Minor, observation (w147): a quoted delegation that is not valid JSON crashes `work run`
`scripts/supervise_answers.py:44-45`. `json.loads` runs outside the `try`, so a hand-written `delegation: "use C:\tmp"` raises JSONDecodeError. No `work` command writes `delegation:` yet. This is the same as the first review's F3.

### F4. Minor, observation (w147): a delegation holding `"` or a line break breaks the `by` line
`scripts/supervise_answers.py:72-73`. The delegation is put into the `by` line unescaped. This is open case §5 of the plan.

### F5. Minor, drop (w147): the implementer's result names the pre-rebase hash
The result lists `8565af5`; the commit on HEAD is `3f97115`, with identical code.

### Not findings (checked)
- **The move after the last answer.** Moving a fully answered work-item to `asked_from`'s status serves r77. It rests on design-decision/a-ruling-returns-to-the-asking-stage.
- **Tools and agent.** The answer stage has no Bash, Edit or Agent tool, so r13 and r14 hold. The agent names its model. CLAUDE.md has the new module's row.
- **Lint.** `tools check` reports two ruff I001 errors, in `scripts/supervise_analysis.py:4` and `tests/scenarios/test_work_queue.py:7`. w147's commit touches neither file; they come from other commits after the base.

## Check results

- **ruff:** 2 errors (I001), both in files w147 did not touch: `scripts/supervise_analysis.py`, `tests/scenarios/test_work_queue.py`.
- **vulture:** clean.
- **import-linter:** "the project states no import contracts".
- **size --limit 300:** no output, so no file is over the limit.

## Commands run

- `git log --format='%H %s' --grep="^work: w147 " --all`
- `git log --format='%h %s' 0798166..be50925`
- `git log --format='%h %s' be50925..HEAD -- <w147's files>`
- `git diff 8565af5 3f97115 --stat -- scripts agents tests features CLAUDE.md`: empty
- `git show 3f97115`
- `git show --stat 0993412`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 0798166369ec037dde8651cb0f00633883f0e066`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q -n 0 -p no:cacheprovider -k "under_a_delegation or naming_that_delegation" tests/scenarios/test_supervision.py`: 3 passed
- `git status --porcelain`: clean
