---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
title: Supervision
narrator: the person who started work run
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents]
retired: []
---

# Supervision

## Purpose
`work run <initiative>` delivers an initiative's work-items: for each stage it starts a fresh `claude -p` worker,
reads the worker's result file and writes the status itself. It is a script and takes no judgment; what nobody may
decide goes to the person as a question. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows
from what running it shows.

## Behaviour
- [r1] **When** `work run <initiative>` is started, `work run` shall pull the initiative's work-items through research, plan, implementation and review, one worker at a time, until none can move.
- [r2] **When** a work-item is `drafted`, `researched`, `ready` or `done`, `work run` shall start a new `claude -p` session of that stage's agent (`code-scout`, `bdd-planner`, `bdd-implementer`, `bdd-task-reviewer`), given one brief file that names the work-item, the files to read and the result file.
- [r3] **When** a worker's result file gives `DONE`, `work run` shall move the work-item to its next status.
- [r4] **When** an implementer's result is `DONE`, `work run` shall merge its branch into the initiative branch only if the work-item's scenarios and the whole suite pass on it.
- [r5] **If** a worker gives any result but `DONE`, gives no result file, or its work fails the tests, then `work run` shall move the work-item to `awaiting-ruling`, with the worker's questions or the failure as its question.
- [r6] **If** a worker changes a file under `.shop/work/` outside its run directory, then `work run` shall put the file back as it was.
- [r7] **When** `work run` moves a work-item, `work run` shall commit the work-item's file, its run directory and `log.jsonl` on the initiative branch, and nothing else.
- [r8] **When** a worker starts or ends, `work run` shall append a line to `log.jsonl` with the time, the work-item, the stage, the agent and the session id.
- [r9] **When** no work-item can move, `work run` shall exit, printing each work-item's status and each open question.
- [r10] **If** `work run` cannot do what it was asked, then `work run` shall exit non-zero, say why, and change nothing.
- [r11] **When** `work run` starts a worker, `work run` shall give the worker this plugin's own directory as its plugin.
- [r12] **When** `work run` starts a worker whose agent lists skills, `work run` shall allow the worker to load each of those skills.
- [r13] `work run` shall give no worker a bare Write or Edit tool.
- [r14] `work run` shall allow a worker's Bash only `python3 -m pytest`, the plugin's scripts by path, and the git commands its stage needs.
- [r15] **When** `work run` removes a worker's worktree, `work run` shall first copy each file the worker's result names into the run directory.
- [r16] **When** a researcher's result gives `DONE` with questions, `work run` shall put those questions into the planner's brief.
- [r17] **When** `work run` writes a worker's brief, `work run` shall tell the worker that it starts in its worktree and never changes directory.
- [r18] **When** `work run` merges a work-item's branch, `work run` shall delete that branch.
- [r19] **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 25 turns.
- [r20] **While** two ready work-items have file sets that do not overlap, `work run` shall run them at the same time, two at most, merging one at a time.

## Implementation, may change
- Tests run in parallel with pytest-xdist (`-n auto`), for the work-item's tests and the suite alike (design-decision/plugin-takes-the-dependencies-it-needs).
- A worker is `claude -p "<brief path>" --agent shopsystem-bdd:<agent> --session-id <uuid> --output-format json
  --permission-mode acceptEdits`; the executable is `$SHOPSYSTEM_WORK_CLAUDE`, else `claude` (the plugin's tests
  set a stub).
- Run directory `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`: `brief.md`, `result.json`, `session.json`
  and the worker's notes, plan, report or findings. The implementer works in `.shop/worktrees/<work-item>/`, a
  branch from the initiative branch's head, rebased before the tests.
- `planned` moves to `ready` and `ready` to `claimed` with no guard beyond the lifecycle's.
- Commit message `work: <work-item> <before> -> <after>`. Exit 0 every work-item green, 3 a question, 1 otherwise.
- The tests: `python3 -m pytest -q --work-item <name>` and `python3 -m pytest -q`, from `.shop/delivery.toml`.

## Not yet
- Retries, continuations after `PARTIAL`, refused claims, the guards between
  work-items, fix work-items and re-reviews, the branch review, time and spending limits and budgets, the lock,
  interruption, `work step`, and the full log of each session's cost (see skeleton-notes.md).
