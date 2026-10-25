# Review of w147: DONE_WITH_CONCERNS

Verdict: r77 and r78 are green, the three scenarios pass on HEAD, and no test was removed or weakened. Two Important findings are triaged fix now. (1) The answer pass runs only once, at the start of `run()`. Questions that appear during the same run, such as a gate round's questions (r69/r85) or a worker's (r5), are therefore printed for the person with exit 3 and never given to a session, which r77 contradicts. (2) An answer session that faults raises Refused without committing its stage directory, log lines or any answers already written. The next `work run` then refuses on r46, and a work-item never goes `failed` (r45).

## Commits reviewed

The branch `work/w147` is gone. On HEAD, the commits between `0798166 work: w147 ready -> claimed` and `be50925 work: w147 claimed -> done` are, less other work-items' `work:` commits:

- `3f97115` work run: questions under a request's delegation go to sessions of their own, the answer naming the delegation (r77, r78). It touches 8 files, +259/-3: CLAUDE.md, agents/delegation-answerer.md, scripts/supervise.py, scripts/supervise_answers.py, scripts/supervise_brief.py, scripts/supervise_worker.py, tests/scenarios/supervision_delegation_steps.py and tests/scenarios/test_supervision.py.

The implementer's result lists `8565af5`. That commit exists with the same message and stat. `git diff 8565af5 3f97115` differs only under `.shop/work/` (other work-items' run files), so 3f97115 is 8565af5 rebased with identical code. The difference is in the hash only (Minor, drop). The files match the work-item's fileset and the report's budget. Nothing is outside the file set.

## Removed and weakened tests

None. I searched the test diff for deleted test functions or steps, dropped parametrize cases, removed or loosened asserts, and added skip/xfail. The only changes to tests are a new module, `tests/scenarios/supervision_delegation_steps.py`, and one added star import in `test_supervision.py:27`. Nothing under `features/` changed.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test changed.

## Cannot verify

- That a real `claude -p` session of `delegation-answerer` can write its result file with `--allowedTools Read,Glob,Grep` under `acceptEdits`. This is the same arrangement as the researcher and reviewer stages (READER, no Write), so it is consistent, but the stub does not exercise it.
- That the agent text keeps a real session to "the delegation and the named files and nothing else". The session runs in a full worktree, so the limit rests on its instructions alone (plan D3). The brief's content is verified by the scenario.
- The report's counts ("--work-item w147: 145 passed, 1 skipped", the suite record). I did not rerun them; `work run` ran the suite before the merge.

## Findings

### F1. Important, fix now (w147): questions raised during the run are never given to a session
`scripts/supervise.py:193` and `scripts/supervise_answers.py:59-80`. `answers()` runs once, before `rounds()`, `draft()` and `pull()`. It does not run again.

- A drafted capability-proposal's gate round in the same run moves it to `awaiting-answer` with questions (r69, r85).
- A worker can move a work-item to `awaiting-answer` (r5, r36).

In both cases `run()` ends with r32's exit 3, printing those questions for the person. r77 gives "each question of the initiative" to a session where the request gives a delegation. Under a delegation such as "Do not stop to ask me questions", the first `work run` of a drafted proposal always stops and asks; only a second `work run` answers. This is the main path of the context loop, not an edge. It contradicts r77 and the Purpose ("what nobody may decide goes to the person"). Plan D6 required the repeat ("runs again after each `pull` that leaves an open question not yet given in this run, followed by `rounds`, `draft` and `pull`"). The report says that part was not done.

Fix: after `rounds()` and after each `pull`, run `answers()` again for the questions not yet given in this run, then `rounds`/`draft`/`pull`, until no new question is open (D6). Add a scenario, through a line if one is needed, with a drafted proposal under a delegation whose gate questions are answered in the same run.

### F2. Important, fix now (w147): a faulted answer session leaves uncommitted state and never fails the work-item
`scripts/supervise_answers.py:85-96`. When the session faults, `ask()` raises Refused straight away. Faults here mean a cut-short session, no or bad result file, a checkout change, a push-verification failure or a worktree change. By then `Workers.worker` has already copied the stage directory into `.shop/work/<i>/runs/<node>/<k>-answer/` and appended the start/end lines to `log.jsonl` (`supervise_worker.py:177-184`). Answers written by `self.section` to the same node before the fault are uncommitted too. Nothing commits them: compare `Rounds.round`, which calls `keep_round` before its Refused (`supervise_rounds.py:56-62`).

The next `work run` then stops in `check()` (`supervise.py:81-86`, r46) until the person commits by hand. On a work-item, r45, r42 and r28 say the work-item is transitioned to `failed`, recording the fault. Instead `work run` exits with a refusal, and the item stays `awaiting-answer` with no fault recorded. The risk I named: a session fault leaves uncommitted `.shop/work/` changes. I verified the order in `worker()` (copy and log before any Fault is raised) and the absence of any commit on the `ask()` path.

Fix: on a fault, a work-item goes `failed` through `self.fail(name, fault_of(fault))`, as `step()` does. For a proposal, commit the stage directory and log (and any answers written) as `keep_round` does before raising, so the next run is not refused.

### F3. Minor, observation (w147): a quoted delegation that is not valid JSON crashes `work run`
`scripts/supervise_answers.py:44-45`. `json.loads(value)` runs outside the `try`, which catches only Refused and OSError. A request whose frontmatter is `delegation: "use C:\tmp"` raises a JSONDecodeError (a ValueError), and the traceback ends `work run` where a refusal or "no delegation" belongs. Reproduction, by reading: `json.loads('"use C:\\tmp"')` raises `JSONDecodeError: Invalid \escape`. No `work` command writes `delegation:` yet (plan D1), so only a hand-written request reaches this. Hardening.

### F4. Minor, observation (w147): a delegation holding a double quote or line break breaks the `by` line
`scripts/supervise_answers.py:72-73`. The delegation goes into `by: work run, under the delegation "%s"` raw. A `"` inside it makes the quoted delegation ambiguous to a reader. A line break turns it into a further continuation line. `held()` keeps that line in the bullet, so the n-th-answer rule holds, but the `by` names only the delegation's first line. This is an open case of plan §5, and no line or scenario names it.

### F5. Minor, drop (w147): the implementer's result names the pre-rebase hash
`3-implement/result.json` lists `8565af5`. The merged commit is `3f97115`, with identical code. This is a record-keeping difference only.

### Not findings (checked)
- Moving a fully answered work-item from `awaiting-answer` to `workqueue_answer.asked_from`'s status (`supervise_answers.py:76-78`) is behaviour beyond r77/r78's text. It serves r77, since an answered question lets the item go on (r37 would otherwise hold it for ever). It rests on design-decision/a-ruling-returns-to-the-asking-stage, which the capability rests on. It is not "code no line asks for".
- TOOLS["answer"] (Read, Glob, Grep) gives no Bash, Write or Edit: r13 and r14 hold. The agent has no Agent tool and names its model.
- CLAUDE.md has its module-map row. `size --limit 300` prints nothing (supervise_answers.py has 120 lines, the steps 108).

## Commands run

- `git log --format='%H %s' --grep="^work: w147 " HEAD`
- `git log --format='%h %s' --stat 0798166..be50925`
- `git show --stat 8565af5`; `git diff 8565af5 3f97115 --stat`; `git show 3f97115`
- `grep` of spec/capabilities/supervision.md and features/supervision.feature for r77, r78 and delegation
- Reads of supervise.py (check, commit, move, section, held, run), supervise_worker.py (tools, worker), supervise_rounds.py (rounds, round), supervise_brief.py (answer_lines)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 0798166…`: ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts"
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output (no file over the limit)
- `python3 -m pytest -q -n 0 -p no:cacheprovider -k "under_a_delegation or naming_that_delegation" tests/scenarios/test_supervision.py`: 3 passed
- `git status --porcelain`: clean
