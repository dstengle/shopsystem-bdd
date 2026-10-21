---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
title: Supervision
narrator: the person who started `work run`
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors]
retired: []
---

# Supervision

## Purpose
`work run <initiative>` delivers an initiative's work-items: for each stage it starts a fresh `claude -p` worker,
reads the worker's result and writes the status itself. It is a script and takes no judgment; what nobody may
decide goes to the person as a question. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows
from what using it shows.

## Behaviour
- [r1] **When** `work run <initiative>` is started, `work run` shall pull the initiative's work-items through research, plan, implementation and review, one worker at a time, until no work-item can make a transition.
- [r2] **When** a work-item's status is `drafted`, `researched`, `ready` or `done`, `work run` shall start a new `claude -p` session of that stage's agent (`code-scout`, `bdd-planner`, `bdd-implementer`, `bdd-task-reviewer`), given one brief that names the work-item, the files to read and where its result goes.
- [r3] **When** a worker's result gives the outcome `DONE`, `work run` shall make the work-item's transition to its next status.
- [r4] **When** an implementer's outcome is `DONE`, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios and the whole suite pass on it.
- [r5] **If** a worker gives any outcome but `DONE`, writes no result, or its work fails the work-item's scenarios or the suite, then `work run` shall make the work-item's transition to `awaiting-ruling`, with the worker's questions or the failure as its question.
- [r6] **If** a worker changes a file under `.shop/work/` outside its stage directory, then `work run` shall put the file back as it was.
- [r7] **When** `work run` makes a work-item's transition, `work run` shall commit the work-item's file, its stage directories and `log.jsonl` on the initiative branch, and nothing else.
- [r8] **When** a worker starts or ends, `work run` shall append a line to `log.jsonl` with the time, the work-item, the stage, the agent and the session id.
- [r9] **When** no work-item can make a transition and every work-item is `green` or `withdrawn`, `work run` shall exit successfully, printing each work-item's status.
- [r32] **When** no work-item can make a transition and a work-item is `awaiting-ruling`, `work run` shall exit with an error, printing each work-item's status and each open question.
- [r10] **If** `work run` cannot do what it was asked, then `work run` shall exit with an error, say why, and change nothing.
- [r11] **When** `work run` starts a worker, `work run` shall give the worker this plugin's own directory as its plugin.
- [r12] **When** `work run` starts a worker whose agent lists skills, `work run` shall allow the worker to load each of those skills.
- [r13] `work run` shall give no worker a bare Write or Edit tool.
- [r14] `work run` shall allow a worker's Bash only `python3 -m pytest`, the plugin's scripts its stage runs, by path, and the git commands its stage needs.
- [r15] **When** `work run` removes a worker's worktree, `work run` shall first copy each file the worker's result names into its stage directory.
- [r16] **When** a researcher's result gives the outcome `DONE` with questions, `work run` shall put those questions into the planner's brief.
- [r17] **When** `work run` writes a worker's brief, `work run` shall tell the worker that it starts in its worktree and never changes directory.
- [r18] **When** `work run` merges a work-item branch, `work run` shall delete that branch.
- [r19] **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 25 turns.
- [r20] **While** two ready work-items have claims that would not share a file, `work run` shall have both implemented at the same time, two at most, merging one at a time.
- [r21] **If** `work run` is started by a worker of another `work run`, then `work run` shall refuse, saying so.
- [r22] `work run` shall give every pytest command it starts, and every worker's, the plugin's option `--work-item <name>`, which selects the scenarios the work-item accepts.
- [r23] **Where** the repository is inside the plugin's own directory, `work run` shall make each worker's worktree in a temporary directory outside it.
- [r24] **When** `work run` starts an implementer, `work run` shall first run the whole suite in the implementer's worktree and say in the brief how it ended.
- [r25] **When** `work run` writes a worker's brief, `work run` shall name in it the plugin's scripts directory, the initiative branch's base, the worker's worktree and its work-item branch.
- [r26] **When** `work run` makes a work-item's transition to `awaiting-ruling`, `work run` shall keep the work-item branch.
- [r27] **When** every work-item of the initiative is `green` or `withdrawn`, `work run` shall start a `claude -p` session of `bdd-branch-reviewer` over the initiative branch from its base, given one brief.
- [r28] **If** the main checkout's `.shop/work/` differs from its last commit when a worker ends, then `work run` shall put it back and make the work-item's transition to `awaiting-ruling`, naming each file.
- [r29] **Where** `.shop/delivery.toml` gives `[tests]`, `work run` shall run those commands in place of its own commands for the work-item's scenarios and the suite.
- [r30] **Where** `.shop/delivery.toml` gives a stage's `[allowed_tools]`, `work run` shall give that stage's worker that list in place of its own, less any bare Write or Edit.
- [r31] **When** a planner's result gives the outcome `DONE` with a `fileset`, `work run` shall write that file set into the work-item as `fileset:` as it makes the work-item's transition to `planned`.

## Implementation, may change
- The work-item's scenarios and the suite alike run in parallel with pytest-xdist (`-n auto`) (design-decision/plugin-takes-the-dependencies-it-needs).
- A worker is `claude -p "Read the brief file <brief path> and do what it says." --agent shopsystem-bdd:<agent>
  --session-id <uuid> --output-format json --permission-mode acceptEdits`; the executable is `$SHOPSYSTEM_WORK_CLAUDE`, else `claude` (the plugin's tests
  set a stub).
- `work run` writes the brief in the worker's worktree, as `.shop/scratch/<k>-<stage>/brief.md`, and the worker writes
  its result and its other files beside it. When the worker ends, `work run` copies that directory into the stage
  directory `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`, which then holds `brief.md`, `result.json`,
  `session.json` and the worker's notes, plan, report or findings. The implementer works in
  `.shop/worktrees/<work-item>/`, on its work-item branch from the initiative branch's head, rebased before its
  scenarios and the suite run.
- A result's `questions` given as one string is read as one question.
- The transitions from `planned` to `ready` and from `ready` to `claimed` have no guard beyond the lifecycle's.
- Commit message `work: <work-item> <before> -> <after>`. Exit code 0 every work-item `green` or `withdrawn`, 3 awaiting a ruling, 1 otherwise.
- The commands for the work-item's scenarios and the suite: `python3 -m pytest -q -p work_items --work-item <name>` (the plugin's `scripts/work_items.py` on `PYTHONPATH`) and `python3 -m pytest -q`, `-n auto` where pytest-xdist is there; `.shop/delivery.toml`'s `[tests]` replaces them.

## Not yet
- Retries, continuations after `PARTIAL`, refused claims, the guards between
  work-items, fix work-items and re-reviews, time and spending limits and budgets, the lock,
  interruption, `work step`, and the full log of each session's cost (see skeleton-notes.md).
- `work run` honouring a work-item's `blocked_by` (i8, delivery 1).
- A researcher's findings kept when it stops, for the next delivery (i8, delivery 1).
- A fix work-item that sends new scenario rows to the blind feature-formulator, so that a fix keeps
  formulation's blindness (i8, delivery 3).
