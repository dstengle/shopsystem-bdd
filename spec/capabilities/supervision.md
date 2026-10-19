---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
title: Supervision
narrator: the person who started work run
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents]
formulated_as: features/supervision.feature
retired: []
---

# Supervision

## Purpose
`work run <initiative>` delivers an initiative's work-items: it pulls each through its stages, starting a fresh
`claude -p` worker for each stage, reads each worker's result file, checks the guards, writes the status, merges
the implementers' work, runs the reviews, and logs every worker and every move for measurement. It is a script and
takes no judgment: what a worker decides comes back in its result, and what nobody may decide goes to the person as
a question. It never changes an initiative's or a capability-proposal's status.

## Behaviour
- [r1] **When** `work run <initiative>` is started, it pulls the initiative's work-items through their stages until none can move: a `drafted` one to a `code-scout` worker, a `researched` one to a `bdd-planner`, a `ready` one to a `bdd-implementer`, a `done` one with a named risk to a `bdd-task-reviewer`, and the initiative's branch to a `bdd-branch-reviewer` once every work-item is `done`, `green` or `withdrawn`.
- [r2] Each worker is a new `claude -p` session of its stage's agent, given one brief file that names the work-item, the stage, the files to read, the run directory to write in and the result file; no worker is resumed.
- [r3] `work run` takes a worker's outcome only from its result file. **If** the worker ends without one, or with one not in its stage's form, the stage has failed.
- [r4] **If** a stage fails, `work run` starts a new worker for it once more. **If** that one fails too, the work-item goes to `awaiting-ruling` with the failure as its question.
- [r5] **If** a worker changes a file under `.shop/work/` outside its run directory, `work run` puts the file back as it was, fails the stage and logs the file.
- [r6] **When** a researcher's result is `DONE` with a file set, `work run` writes the file set and the notes' path into the work-item and moves it to `researched`. **If** the file set is empty, the stage has failed.
- [r7] **When** a planner's result is `DONE`, `work run` writes the plan's path, the final file set and the capabilities the work depends on into the work-item and moves it to `planned`. **When** it is `QUESTION`, the work-item goes to `planned` and then `awaiting-ruling`, with each question and its readings.
- [r8] `work run` moves a `planned` work-item to `ready` as soon as the queue's guard allows it, and claims a `ready` one as it starts its implementer, when an implementer's place is free.
- [r9] Each implementer works in its own git worktree under `.shop/worktrees/<work-item>/`, on a branch made from the initiative branch's head, and no more implementers work at once than `delivery.toml` allows, 2 when it says nothing.
- [r10] **When** an implementer's result is `DONE` or `DONE_WITH_CONCERNS`, `work run` rebases its branch onto the initiative branch, runs the work-item's accepted scenarios, or its check, and the whole suite in its worktree, and only when they pass and nothing fails that passed in the last suite record merges the branch fast-forward and moves the work-item to `done`.
- [r11] **If** the work-item's commits change a file outside its file set, `work run` does not merge them, and the work-item goes to `awaiting-ruling` naming the files.
- [r12] **If** the rebase conflicts or the scenarios or the suite fail in the worktree, `work run` leaves the initiative branch as it was, and the work-item goes to `awaiting-ruling` with the conflict or the failing tests.
- [r13] **When** an implementer's result is `PARTIAL`, `work run` starts a new implementer on the same worktree and report as a continuation, at most three times in a row; at a fourth `PARTIAL` the work-item goes to `awaiting-ruling`.
- [r14] **When** an implementer's result is `BLOCKED`, `HAND-BACK` or `NEEDS_CONTEXT`, the work-item goes to `awaiting-ruling` with the result's questions and evidence, its claim released and its worktree and branch kept.
- [r15] **When** an implementer stops because `work claim` refused a path, `work run` moves its work-item back to `ready`, where it waits until the work-item whose claim has the path is no longer `claimed`, and the next implementer continues on the same branch.
- [r16] **While** a work-item is `awaiting-ruling`, `work run` goes on with every work-item that is not blocked by it.
- [r17] **When** no work-item can move and no worker is running, `work run` exits, printing the number of work-items in each status, and each open question with its readings and the `work rule` command that answers it.
- [r18] `work run` exits 0 when every work-item is `green` or `withdrawn`, 3 when one is `awaiting-ruling`, 4 when a budget stopped it, and 1 when it stopped for any other reason.
- [r19] Each worker runs within the time and the spending `delivery.toml` gives its role. **If** it reaches either, `work run` ends it and the stage has failed.
- [r20] **When** the spending of the workers `work run` has started reaches the run's budget in `delivery.toml`, it starts no further worker, waits for the running ones, and exits saying what was spent.
- [r21] **When** a work-item whose risk is `contract`, `concurrency` or `data` is `done`, `work run` starts a task review of its commits. **When** the review finds nothing to fix now, the work-item goes to `green` once its accepted scenarios pass at the initiative branch's head.
- [r22] **When** a review triages findings as fix now, `work run` adds for each work-item they name a fix work-item at `planned`, with `fixes:` naming that work-item, `findings:` naming the review-finding, the files the findings name as its file set, and the requirements that work-item accepts; the work-item fixed goes to `green` only once every fix work-item for it is `green`.
- [r23] **When** a review ends, `work run` writes its findings as a review-finding record under `.shop/records/review-findings/`, about the reviewed work-item's capability, or about the bounded context for a branch review.
- [r24] **When** a review triages a finding as an observation, `work run` appends it to `.shop/records/observations.md`, about the work-item's capability, with its reproduction and the review-finding it came from.
- [r25] **When** every work-item of the initiative is `done`, `green` or `withdrawn`, none is `awaiting-ruling`, and the initiative branch has commits since its last branch review, `work run` starts a branch review from the initiative's base. **When** it finds nothing to fix now, each `done` work-item whose scenarios pass goes to `green`.
- [r26] **When** a fix work-item is `done`, `work run` starts a scoped re-review of its commits. A finding that is data left invalid, the system's own fault on input, or a write that lands where a refusal belongs gets a further fix work-item; any other finding is an observation, and the fix work-item goes to `green`.
- [r27] **When** `work run` starts or ends a worker, it appends a line to `log.jsonl` with the time, the work-item, the stage, the attempt, the agent, the model and the session id, and at the end the result's status, the exit, and the duration, cost and token counts the session reported.
- [r28] **When** `work run` has run the whole suite, it appends a suite record to `log.jsonl` (passed, failed, expected, the commit, the seconds), and each implementer's brief gives the last one.
- [r29] **When** `work run` moves a work-item, it commits the work-item's file, its run directory and `log.jsonl` on the initiative branch, and nothing else, with the message `work: <work-item> <before> -> <after>`.
- [r30] **If** another `work run` is running in the repository, `work run` refuses, naming its process id.
- [r31] **If** `work run` is started on the repository's default branch, or with changes in the working tree outside `.shop/`, it refuses before starting any worker and says which.
- [r32] **When** `work run` is interrupted, it ends its running workers and logs each as interrupted; the next `work run` continues each `claimed` work-item from its worktree and report as a continuation.
- [r33] **When** every work-item of the initiative is `green` or `withdrawn` and the last branch review found nothing to fix now, `work run` says the initiative's work-items are done, and changes no initiative's or capability-proposal's status.
- [r34] **When** `work step <work-item>` is run, `work` runs that work-item's next stage alone, under the rules of `work run`, and exits when it ends.
- [r35] **When** `work run` starts a worker, it prints one line naming the work-item, the stage and the agent, and one line when the worker ends with its result's status; it prints nothing a worker wrote.

## Implementation, may change
- A worker is `claude -p "<the brief's path and the result file>" --agent shopsystem-bdd:<agent> --session-id <uuid>
  --output-format json --max-budget-usd <n> --permission-mode <delivery.toml, default acceptEdits>`, with `--model`
  only where `delivery.toml` overrides the agent definition's. The executable is `$SHOPSYSTEM_WORK_CLAUDE`, else
  `claude`; the plugin's tests set it to a stub that follows a script.
- Run directory `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`: `brief.md`, `result.json`, `session.json`
  (claude's JSON output), and the worker's `notes.md`, `plan.md`, `report.md` or `findings.md`.
- `.shop/delivery.toml`: `[tests] scenarios` (default `python3 -m pytest -q --work-item {item}`) and `suite`
  (default `python3 -m pytest -q`); `[workers] implementers = 2`, `researchers = 3`; `[limits]` minutes and dollars
  per role (scout 10/1, planner 20/3, implementer 45/8, task reviewer 20/3, branch reviewer 45/8) and `run_dollars`
  (default 60); `[worktree] setup`; `[models]` overrides.
- The initiative's base is the merge-base of the initiative branch with the default branch when `work run` first
  starts; it is the first line of `log.jsonl`. `.shop/worktrees/` and `.shop/scratch/` are git-ignored.
- One process, a lock file `.shop/work/.lock` with its pid; workers run as child processes polled for exit.

## Not yet
- Re-planning after a ruling (the planner run again on the ruled work-item) — trigger: a ruled work-item's implementer stops on what the ruling changed.
- Workers in a sandbox the supervisor starts (a container per worker) — trigger: a consuming repository asks to run `work run` with bypassed permissions.
