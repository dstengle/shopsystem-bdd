# Plan of w151: the integrate round of a proposed initiative, and its transition to started

Planned from `runs/w151/1-research/notes.md`; sections cited as N§n, probes as P1-P5, defects as D1-D4.

## 1. What goes green

- **supervision#r79**: `a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils`. Red at its first Given, line 851 (`StepDefinitionNotFoundError`): no step writes a proposed initiative fulfilling a request with `## Outcomes`; the Then at line 854 has no step either (`rounds(repo, kind)` matches only `# <kind> of p1`). Behind the steps, no code starts an integrate round: `Rounds.due` and `AFTER` know capability-proposals only (P1: exit 0, no session, i1 still proposed).
- **supervision#r84**: `when work run starts the integrate round of a proposed initiative, the initiative is started`. Red at its first Given, line 999; the Then at line 1002 has no step. Behind them, nothing writes `started` on an initiative: `workqueue.move` refuses it (P4), and `Run.commit` would not commit `initiative.md` (P5, D3).
- Retires: none (the work-item has no `## Retires`).

## 2. Where the change lands

- `scripts/supervise_rounds.py`: `due` offers the initiative itself first, a `proposed` one getting the round `integrate`; `round` makes the integrate round's transition when it starts the round, not once it ends (D2 below).
- `scripts/supervise.py`: `Run.commit` commits the initiative's `initiative.md` when the name is the initiative's (D3); no other change to `run()` (D5).
- `scripts/supervise_brief.py`: the brief of an integrate round reads the initiative's `initiative.md`, not `<name>.md` (D4), and gives the kind `integrate`, the request and its accepted lines.
- `scripts/supervise_worker.py`: `integrate` joins `ROUNDS` and the round tools, so its session gets the rounds' scripts and no `--work-item`.
- `scripts/workqueue_request.py`: a reader of a request's accepted lines, number and text, over `_entries` and the request's `## Lines`.
- `scripts/workqueue_done.py`: `mark` takes the status it writes (done as today when none is given), so the integrate path writes `started` through it.
- `tests/scenarios/supervision_rounds_steps.py`: the shared Given of both scenarios, and both Thens; `rounds` takes the node's name as well as the kind.

Removed from the researcher's set, by the decisions below: `scripts/workqueue.py` (D1: `move` is not widened; it has 14 lines of room), `scripts/supervise_review.py` (D5: no change to branch review), `scripts/supervise_faults.py` (D3 lands in `Run.commit`), `tests/scenarios/test_supervision.py` (the Givens go into `supervision_rounds_steps.py`, already imported, so no new module and no import line). Every file stays under 300 lines; `supervise_worker.py` (243) and `supervise.py` (236) have the least room.

## 3. Decisions

- **D1. The initiative's transition is not a `workqueue.move`.** `move` stays the work-item and proposal lifecycle's writer. The integrate path rewrites `status:` of `initiative.md` with `workqueue_done.mark`, given the status, appends to `log.jsonl` through `Run.log` the same fields `move` writes (`work-item` naming the initiative, `before: proposed`, `after: started`, `by` as `work run`'s), and commits with `Run.commit` as `work: i1 proposed -> started`, then pushes. Rests on supervision#r84 (the transition), r7 and r38 (the commit and push), r8 (the log). The CLAUDE.md size rule (workqueue.py has 14 lines of room) is why `move` is not widened.
- **D2. When the transition is made: as the round starts, before its session.** r84 says "When `work run` starts the round … shall transition". So `round`, for `integrate`, makes D1's transition before it makes the round's worktree and starts the worker. The transition's log line then comes before the round's `start` line, and the round's worktree already holds the started initiative. After the round ends there is no second transition: the round's branch merges as the other rounds' do. Rests on supervision#r84 and r79.
- **D3. `Run.commit` commits `initiative.md` for the initiative.** When the name it is given is the initiative's own, the file it commits is `initiative.md`, alongside `runs/<name>` and `log.jsonl` (P5 shows today's path leaves it uncommitted, and r46 would then refuse the next run). Rests on supervision#r7 and r46.
- **D4. The integrate brief.** It is the brief of an `initiative-round` session (Implementation: r79's integrate round is an `initiative-round` session of spec-integration). Its heading is `# integrate of <initiative>`, the form the other rounds' briefs use. It names the request the initiative `fulfils` (the short form `q1` and the full form `request/<ctx>/q1` both resolve, as `Answers.delegation` resolves them, N§2). It gives each line whose line outcome is `accepted`, with its number and text, and no other line of the request. It reads the initiative from `initiative.md` and has no `Work-item branch:` line, as rounds do. Rests on supervision#r79 and r17, r25, r44 (what every brief says).
- **D5. Branch review and analysis after an integrate round are left as they are.** On an initiative with no work-items, today's `run()` reads "every work-item green or withdrawn" as true, so a round's commit is followed by a branch review and `measure initiative` in the same run. P2 shows this already happens after a gate round (D1 of the notes). This work does not change that reading. Changing it would change what the narrator observes, and r79 and r84 do not ask for it: their scenarios pass either way (P2 exits 0). Rests on supervision#r27 and r75 as the code reads them today.
- **D6. Where the round sits in the run.** The integrate round is the first round `due` offers. `rounds()` then goes on, in the same run, to whatever proposals the round leaves, as r66 asks ("every transition its nodes can make"). Rests on supervision#r66 and r79.

## 4. Tests the decisions break

None. What was verified, from N§4 and the file set:
- Every `supervision` Background writes i1 as `status: started`, so D6's integrate offer is never due in an existing scenario. No existing test runs `work run` on a `proposed` initiative (by search: `work_queue_start_steps.py`, `migration_session_steps.py`, and `supervision_given.py:171`, an i2 that never runs).
- D3 changes `Run.commit` only when the name is the initiative's, which no existing caller passes. D4 changes the brief only for an integrate round. `mark` keeps `done` as its default, so `work withdraw` and `work resolve` are unchanged.
- `rounds(repo, kind)` in `supervision_rounds_steps.py` gets a name parameter. Its gate, apply and formulate callers pass `p1` and keep asserting what they assert now.
- Not verified by the notes: the gate scenarios (r68, r69, r85). They are untouched by D1-D6, because `due` offers them only on a started i1, as today. The implementer runs them.

## 5. Open cases

- The integrate round faults after D2's transition: is i1 then left `started` and committed, so no later run offers it the round again? And what replaces `round`'s refusal text, which says the node "keeps its status"?
- A request with no `## Outcomes`, or no accepted line (`_entries` gives none, N§2): is the round still started with no lines, or not started?
- An initiative that is `proposed` with no `fulfils:`, or whose request file is missing.
- The log line of D1 names an initiative under the key `work-item`. Do `agrees`, `last_logged` or `measure`'s reading of `log.jsonl` read such a line (`items()` ignores initiatives)?
- The r84 Then's measure of "when the round was started": which log lines it orders (the transition line against the integrate round's `start` line) and whether it also checks the committed `initiative.md`.
- D2 of the notes (a refused `measure initiative` printed with exit 0) and D5 above: existing behaviour, reached on this path, outside r79 and r84.
