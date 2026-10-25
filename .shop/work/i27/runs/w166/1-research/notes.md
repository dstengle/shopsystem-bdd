# w166 notes: work start commits the initiative (work-queue r25)

Scripts: /home/vscode/shopsystem-bdd/scripts. No coverage map: `tools tests-of` says "no map", so every test list below is `by search`. `tools refs` ran; it does not resolve `workqueue_start.start` (0 refs, the caller is a module attribute at scripts/work:84).

## 1. Why the accepted scenario is red today

Command: `python3 -m pytest -q -n 0 "tests/scenarios/test_work_queue.py::test_start_commits_the_initiative_it_writes_on_the_current_branch"` (run). Fails at `tests/scenarios/work_queue_git_steps.py:51` (`assert done.returncode == 0`): `work start q1` exits 1, stderr `work: spec/index.md, which names the context, is missing`.

Three gaps stand between it and green:
- Givens: the scenario writes no `spec/index.md` (features/work-queue.feature:47-54; the Given at work_queue_start_steps.py:15-18 writes only the request, the Given at work_queue_git_steps.py:40-45 only commits). `workqueue.context_path` (scripts/workqueue.py:38-42) refuses. r22's scenario avoids this with `Given an initiative i1`, which writes the index (tests/scenarios/test_work_queue.py:40-50).
- Code: `workqueue_start.start` (scripts/workqueue_start.py:22-43) writes `initiative.md` and never commits. It is the one writer in the queue not using `workqueue.committed` (scripts/workqueue.py:264-279), which `work add`, `note`, `answer`, `request` and `resolve` all use (workqueue.py:101, workqueue_note.py:20, workqueue_answer.py:50, workqueue_request.py:60).
- Steps: `new_commit_holds` (work_queue_git_steps.py:48-55) receives the literal text `the new initiative's initiative.md` and runs `git show main:<that text>`; `kept()` (line 58-60) maps only `q<n>`. Nothing maps the phrase to `.shop/work/<new>/initiative.md`. The step that sets `context["new"]` (work_queue_start_steps.py:38-45) is a Then this scenario does not have.
- Also `nothing under {where} differs` (work_queue_git_steps.py:68-71) receives the literal `the new initiative's directory under .shop/work/`; see probe h, it passes vacuously.

## 2. What the system answers today

Probe file: `.shop/scratch/w166-1-research/probe_start.py`, run `python3 -m pytest -q -n 0 -s .shop/scratch/w166-1-research/probe_start.py` (run, 9 passed). Repositories made under the scratch directory; `scripts/work` of this worktree.

- a. accepted q1, git repo on main, index present: `rc 0`, prints `i1`; `git log` head is the set-up commit, `git status --porcelain` shows `?? .shop/work/i1/initiative.md`. Not committed (the bug).
- b. accepted q1, no git repository: `rc 0`, prints `i1`, writes `i1/initiative.md`. No refusal (committed() would refuse this before writing).
- c. accepted q1, detached HEAD: `rc 0`, same as a; no commit.
- d. no request q1: `rc 1`, `work: there is no request q1 under .shop/work/requests`, nothing written.
- e. q1 `drafted`: `rc 1`, `q1 is drafted, not accepted; ...`, nothing written.
- f. `.shop/work/i1/` holds only `ledger.md` (committed): `rc 1`, Python traceback `FileExistsError: '.shop/work/i1'` from `directory.mkdir` (workqueue_start.py:38); nothing written.
- g. no `spec/index.md`: `rc 1`, `spec/index.md, which names the context, is missing`, nothing written. (The scenario's own Givens, as written.)
- h. after a start (uncommitted): `git status --porcelain -- "the new initiative's directory under .shop/work/"` gives `''` (rc 0), while `-- .shop/work/i1` gives `?? .shop/work/i1/initiative.md`. `git show main:"the new initiative's initiative.md"` gives rc 128. (Step-gap evidence.)
- i. two starts: `i1` then `i2`, both uncommitted; numbering counts uncommitted initiatives (`_highest`, workqueue_start.py:10-19).

Nearest cases not in the scenario: b, c, f (the directory collision: a traceback where the rest of the queue refuses), d, e, g.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py:84-88 (`Run` start check, `loose`) | refuses `work run <i>` while anything under `.shop/work/` is uncommitted; so an initiative `work start` wrote stops `work run` until someone commits it | r25 commits the initiative, so the check passes without a hand commit; the refusal stays for other loose files | by search: none (no test runs `work start` then `work run`); the supervision tests write their initiatives by file | read; grep `not committed` in tests |
| scripts/supervise_brief.py:14-18 (`base`) | the initiative's base is the commit that added its `initiative.md` (`git log --diff-filter=A`) | the commit is now `work start`'s own commit on the current branch, not a later hand commit | none found by search (the supervision Givens commit their own files, not via start) | read |
| scripts/workqueue_status.py:150-156 (`work status`, uncommitted/untracked lists) | lists an initiative `start` wrote as untracked (probe a) | after r25 it is not listed | by search: work_queue_status_steps.py (no start in it) | read; probe a |
| scripts/workqueue_start.py:22-43 (`start`) | writes, no commit | the function r25 changes | the r25 scenario only (red); the r22 scenario (see part 4) | read |
| docs and skills (grep `work start` outside `.shop/`) | none | none | none | search: only features, tests, spec, CLAUDE.md:25 |

## 4. Tests the requirement makes impossible to keep

Map absent, so `by search`: the tests that run `work start` are `test_work_queue.py::test_start_commits...` (the accepted one) and the r22 scenario, whose Thens (work_queue_start_steps.py:38-58) check fields, id and `.shop/work/i1/` only, not git. Read: r22 is not sound-checked by a run here: `python3 -m pytest -n 0 --collect-only tests/scenarios/test_work_queue.py` collects one of the file's 65 tests, and `-o addopts=""` gives the same; I did not find the cause in conftest.py, the root conftest.py or scripts/work_items.py. So r22's current status is unverified (open question). After the change: no test that I found asserts an uncommitted start. Verified sound by reading: the r22 Thens do not depend on git state.

## 5. A step the work-item skips

`committed()` (scripts/workqueue.py:264-279) does, and `start` does not:
- refuses a directory git cannot commit in, before writing (`git rev-parse --is-inside-work-tree`). Probe b: today a no-git directory gets `rc 0` and a written initiative.
- commits only the named file (`git add -- rels`, `commit -- rels`); a pre-existing staged change stays out of the commit. Read.
- on a failed commit puts the file back and `reset`s the index, so r7's "change nothing" holds. Read: `start` has no such path; a failed commit would leave `initiative.md` and still print the id. Probe not run (it needs an identity failure); marked read.
- after r25 `start` must hand its directory to `committed()`; `mkdir` (workqueue_start.py:38) runs before it, so a refused commit would leave the empty directory; read.

## 6. Defects

### D1. `work start` crashes on an existing initiative directory with no initiative.md (run, probe f)
`.shop/work/i1/ledger.md` committed; `work start q1` gives `rc 1` and `FileExistsError: '.shop/work/i1'` from workqueue_start.py:38. Nothing written. Reproduction: probe `test_f_directory_without_initiative_md`. Not caused by r25; `_highest` counts only `initiative.md` files.

### D2. `work start` writes outside a git repository (run, probe b)
`work start q1` in a directory with no git repository: `rc 0`, `i1/initiative.md` written. The other queue writers refuse first (committed(), workqueue.py:268). Reproduction: probe `test_b_not_a_git_repository`.

### D3. The r25 scenario's "nothing under ... differs" Then passes on any path (run, probe h)
`git status --porcelain -- "the new initiative's directory under .shop/work/"` is empty when the initiative is uncommitted (rc 0). Reproduction: probe `test_h_scenario_then_steps_on_uncommitted_start`. The check is vacuous, not failing.

## 7. The file set

Changes the scenario needs (plan decides the exact edit):
- scripts/workqueue_start.py (43 lines; room 257): `start` writes through `workqueue.committed(root, [rel], "work start: <name> proposed", write)` (scripts/workqueue.py:264), returns the id. Found by sections 1, 3, 5.
- tests/scenarios/work_queue_git_steps.py (71 lines; room 229): map `the new initiative's initiative.md` and `... directory under .shop/work/` to the new initiative (diff against `context["before"]`); fix D3. Found by probe h, section 1.
- tests/scenarios/work_queue_start_steps.py (69 lines; room 231): a Given or a step that gives the scenario its index (or the r25 feature's Givens get `an initiative i1`), and sets `context["new"]`. Found by probe g, section 1.
- features/work-queue.feature (398 lines; not a Python file, no size limit): the r25 scenario's Givens, if the plan chooses to add `Given an initiative i1 under .shop/work/` as r22 does.

Files on the change's path, edited or not (`wc -l`):
- scripts/work, 150 lines, room 150: `cmd_start` (line 83-85) prints the id; unchanged unless the commit adds a message.
- scripts/workqueue.py, 290 lines, room 10: `committed` (264-279) is reused, not changed; a change here would need a split first.
- scripts/supervise.py, 247 lines, room 53, and scripts/supervise_brief.py, 129, room 171: old-assumption rows only, unchanged.
- scripts/workqueue_status.py, 170 lines, room 130: old-assumption row only.
- tests/scenarios/test_work_queue.py, 288 lines, room 12: the scenario's When (`context["before"] = snapshot`, line ~188) and the `initiative()` helper (line 47-50); unchanged unless the plan adds a Given here.
- tests/scenarios/conftest.py, 176 lines, room 124: `INDEX` (line 49-50); unchanged.

`tools size --limit 300`: printed nothing (no tracked Python file over 300).
