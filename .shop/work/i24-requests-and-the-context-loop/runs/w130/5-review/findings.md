# Review of w130 (work-queue#r22, work-queue#r23)

**Verdict: DONE_WITH_CONCERNS.** r22 and r23 are implemented and their five scenarios pass. No change under
`features/`, no test removed or weakened, and the one allowance holds. But one finding is triaged fix now: `work retry`
does not run the done check, even though a retry can bring a work-item back to `green` (after a push failure that
followed `work run`'s green move). When it does, r23 is contradicted, and the person's Answer (reading B) names retry as
one of the commands that set done.

## Commits reviewed

- Branch `work/w130` no longer exists, so I took the commits between `5ce9f24 work: w130 ready -> claimed` and
  `d350d36 work: w130 claimed -> done` on HEAD, less the `work:` commits.
- That leaves `7b769e8 work start and an initiative done (work-queue r22, r23)`, plus `1303b55 model check: request rules …`.
  1303b55 is another work-item's commit (it falls inside w132's claimed -> done span) and touches none of w130's files.
- The implementer's result lists `a1b01eb`. That commit exists, and its patch is byte-identical to 7b769e8's: the sha1
  of `git show --format=` is the same for both. So it is the same change, rebased on merge. Not a finding.
- Files: CLAUDE.md, scripts/work, scripts/workqueue.py, scripts/workqueue_done.py (new), scripts/workqueue_request.py,
  scripts/workqueue_start.py (new), tests/scenarios/test_work_queue.py, tests/scenarios/work_queue_start_steps.py
  (new), tests/scenarios/work_queue_status_steps.py.

## Removed and weakened tests

None.

- I read the diff for deleted test functions, dropped parametrize or Examples rows, removed or loosened `assert`s, and
  added skip/xfail marks. There are none.
- `features/` is untouched (not in the diff).
- The only edit to an existing test file is the Given `with_state` in work_queue_status_steps.py (see Allowances).
  test_work_queue.py gains one import line.

## Allowances

- `tests/scenarios/work_queue_status_steps.py` `with_state`, a `setup` row: **holds**.
  - The diff changes only how the Given writes work-items. It splits "… and whose work-item w2 is ready" into a second
    work-item.
  - It adds, removes and changes no `assert`, no expected value and no case.
  - Givens without that tail write exactly what they wrote before.

## Cannot verify

- That the requests scenarios which run `work resolve` still pass, and that the whole suite stood at 752 passed /
  5 failed before the change. I took these from the report and did not run the whole suite (`work run` ran it).
- The `work resolve` done path: no scenario drives it, and from the commits I could only read it, not run it. On
  reading: the refusal of a request that is not accepted (in `edit`) still runs first, `_path` still refuses a missing
  request, and initiative.md joins the commit only when `becomes` is true.

## Findings

### 1. Important, fix now: `work retry` back to `green` does not set the initiative done (scripts/workqueue.py:195-208)

- **What is wrong.** `retry` commits `rels_of(...)` and moves the work-item, but runs no done check. `withdraw` and
  `resolve` do.
- **The path that reaches it.** This is not just in theory:
  1. `Supervisor.move` (scripts/supervise.py:100-106) moves the work-item to `green`, then `commit` pushes
     (supervise.py:97-98).
  2. If that push fails, `push` raises a Fault (supervise_faults.py:72-76).
  3. `step` catches the Fault (supervise.py:140-143) and calls `fail`, which moves the work-item "from whatever status
     it has" (supervise_faults.py:78-85). So log.jsonl gets a `green -> failed` line.
  4. `work retry` then returns the work-item to `green` (r8).
- **Why it matters.** If that work-item was the initiative's last open one, retry's change makes r23's condition true,
  but initiative.md stays `started`. Nothing later sets it, because the condition then already holds. That is a wrong
  answer against r23.
- **The plan and the report.** The person's Answer (reading B) lists `work retry` among the commands that set done, and
  so does plan decision D7. The report's reason for leaving retry out ("their moves … cannot make the condition true")
  is wrong for this path.
- **Fix.** Give `retry` the same hook as `withdraw`: `workqueue_done.becomes(root, path.parent, {name: before})`, add
  initiative.md to the commit, and call `mark` inside the write. `answer` needs no hook: its targets are
  drafted/researched/ready/done, never green.
- **How I verified it.** By reading the code path above. I wrote no reproduction, because building a repository with a
  failing push needs commands this review may not run.

### 2. Minor, observation: ruff I001 on two lines the commit wrote

- **Where.** `tools check --base 5ce9f24` gives:
  - `scripts/workqueue.py:232:5 I001`: the function-level `import workqueue_done` with its trailing comment.
  - `tests/scenarios/test_work_queue.py:7:1 I001`: the new `from .work_queue_start_steps import *` placed after
    `withdraw`, out of order.
- **Why it matters.** Lint fails on lines w130 introduced.
- **Fix.** Run `ruff --fix` on those two files (move the start import to its sorted place).
- The check's other results are not w130's:
  - ruff FURB167 at tests/scenarios/design_model_check_requests.py:132 comes from 1303b55.
  - vulture `notes` at work_queue_status_steps.py:77 was already there before (line 74 at the base).

### 3. Minor, observation: work_queue_status_steps.py is outside the work-item's `fileset`

- The commit edits `tests/scenarios/work_queue_status_steps.py`, which the work-item's `fileset:` does not list
  (design-decision/the-file-set-is-the-claim).
- The report states it openly, and the edit is setup only.
- Fix: none needed now. The planner's file set should name it next time.

### 4. Minor, observation: `work start` crashes instead of refusing when the next `i<n>` directory exists without initiative.md (scripts/workqueue_start.py:13,37)

- **What is wrong.** `_highest` counts only directories that have an initiative.md. If `.shop/work/i<n+1>/` exists
  without one, `directory.mkdir(parents=True)` raises FileExistsError. scripts/work catches only `Refused`, so the user
  gets a traceback where r7 wants an error that says why.
- **Reproduction.** By reading only. No client makes such a directory today.
- **Fix.** Count every `i<n>` directory name in `_highest`, or refuse when the directory exists.

## Commands run

- `git log --format='%H %s' --grep="^work: w130 "`, `git log --format='%h %s' 5ce9f24..d350d36`: found the claim and
  done commits and listed the commits between them.
- `git show --stat 7b769e8`, `git show --stat a1b01eb`, and `git show --format= <c> | sha1sum` for both: identical patch.
- `git show 7b769e8 --format=`: read the diff once.
- `git show 7b769e8^:scripts/workqueue_request.py`. Risk: resolve's refactor drops `_change`'s refusals. Verified that
  `_path` and the accepted check are kept.
- `grep` and `sed` on scripts/workqueue.py, supervise.py, supervise_faults.py and supervise_merge.py. Risk: a retry can
  return a work-item to green. Verified: fail() moves a work-item from green after a failed push (finding 1).
- `grep` on spec/capabilities/requests.md. Risk: a `part_of` request's origins go missing. Verified: origins are
  `source`; a job-thread is not an origin.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 5ce9f243…`: ruff 3 errors (2 are w130's), vulture 1
  (already there), import-linter: no contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output, so no file is over the limit.
- `python3 -m pytest -q --work-item w130 -n 0 -p no:cacheprovider tests/scenarios/test_work_queue.py`: 5 passed.
- `git status --short`: clean.
