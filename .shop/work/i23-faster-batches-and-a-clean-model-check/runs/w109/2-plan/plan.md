# Plan of w109: work run runs independent work-items side by side

From the research notes (`runs/w109/1-research/notes.md`); scenarios in `features/supervision.feature`.

## 1. What goes green

- **supervision#r1**: "`work run` pulls each work-item through research, plan, implementation and review until no work-item can make a transition" (19). Passes today; must stay green once research of w1 and w2 overlaps (each item's own four workers stay in order).
- **supervision#r59**: "when more than one work-item is drafted or researched, their research and plan stages are started at the same time" (28). Red: the Given "every worker gives DONE, the researcher of w1 and the planner of w2 each ending once both have started" and the Then "worked at the same time" for two agents are unbound; the stub's `meet` counts starts of one agent only; `Run.run` pulls `movable[0]` only, so research and plan never overlap.
- **supervision#r60**: outline "`work run` runs at most <limit> workers at the same time when .shop/delivery.toml <gives>", rows limit 2 and limit 4 (36). Red: the items regex takes no comma list ("w1, w2, w3, w4 and w5"); the workers-number Givens, the "each researcher ending once <limit> workers have started" Given and the Then are unbound; nothing reads a workers number (probe: a `workers = 2` key is ignored, one worker at a time).
- **supervision#r62**: "each stage's session.json records the path of the transcript of that stage's session" (210). Red: the Then is unbound; `Workers.worker` writes claude's stdout only (probe: keys `is_error, num_turns, result, session_id, subtype, total_cost_usd, type`).
- **supervision#r20**:
  - "two ready work-items whose claims would share no file are implemented at the same time, each in its own worktree" (405). Red: the Then "each of them worked in a worktree of its own" is unbound (the code already gives each implementer its own worktree).
  - outline "two ready work-items whose claims would share a file are implemented one after the other: <how>", three rows (414). Pass today; stay green (the disjointness check per member must hold in the new scheduler).
  - "of three ready work-items whose claims would share no file, no more are implemented at the same time than .shop/delivery.toml's number of workers" (438). Red: the Given ".shop/delivery.toml gives 2 as its number of workers" is unbound; `Run.pair` caps at a pair, not at a number.
- **supervision#r61**: "implementers working at the same time that end with DONE have their branches merged one at a time, in the order they ended" (447). Red: the Given "…, w2's implementer ending before w1's" is unbound (the stub has no end-order control) and the Then on commit order is unbound; merges today take `self.lock` in whatever order threads reach it.
- **supervision#r63**: "no worker is started for a work-item whose blocked_by names a work-item that is not green" (694). Red: the Given with `blocked_by` is unbound (`item_text` writes no `blocked_by`); probe D2: w1 blocked by an awaiting-answer w2 gets all four workers and goes green.

Retired by the work-item's Retires section (ruled reading A; delivery#r17), removed from the feature file:
- "`work run` pulls each work-item … one worker at a time … (deprecated)" (@r1, line 8);
- "two ready work-items whose claims would not share a file are implemented at the same time, and merged one at a time (deprecated)" (@r20, line 395);
- "of three ready work-items whose claims would not share a file, no more than two are implemented at the same time (deprecated)" (@r20, line 429).

## 2. Where the change lands

- `scripts/supervise.py`: `Run.run` hands scheduling to the new pool; `Run.pair` and `Run.together` give way to it; the fault wrapper of `Run.step` used by every stage the pool starts; the stop after a fault becomes a drain.
- `scripts/supervise_pool.py` (new; `supervise.py` has 37 lines of room): the pool of workers — which movable items get a worker each pass (blocked_by guard, claim disjointness for implementers), the cap at the workers number, and the end-ordered merge queue.
- `scripts/supervise_worker.py`: `Workers.delivery` read once at the start and gives the workers number; `Workers.worker` writes the transcript path into `session.json`; `tools` and `session` use the delivery already read.
- `scripts/supervise_merge.py`: `Merge.claimed` merges in the order implementers ended (r61), not in lock-acquisition order.
- `scripts/supervise_review.py`: the branch reviewer's `session.json` gets the transcript path too (decision 4).
- `scripts/supervise_faults.py`: only if the per-thread fault wrapper is placed beside `fault_of`; kept in the claim for that.
- `scripts/workqueue.py`: only if `items` does not expose a work-item's `blocked_by` list; kept in the claim for that.
- `tests/scenarios/supervision_parallel_steps.py` (new; `supervision_then_workers.py` has 15 lines of room): the new Thens (two agents worked at the same time, <limit> workers and never more, own worktree, transcript path, commit order w2 then w1) and the new Givens that do not fit `supervision_given.py`.
- `tests/scenarios/supervision_given.py`: comma list in the items regex; `blocked_by` Given; the two workers-number Givens; the cross-agent, N-starts and end-order variants of "every worker gives DONE".
- `tests/scenarios/supervision_then_workers.py`: removal of the Thens only the retired scenarios use (part 4).
- `tests/scenarios/supervision_world.py`: `item_text` writes `blocked_by`; the world points `CLAUDE_CONFIG_DIR` at a temporary store for the stub's transcripts.
- `tests/scripts/stub_claude.py`: meet across agents, meet on a count of workers started, an end-order control, and a transcript file written into the store under the session id.
- `tests/scenarios/test_supervision.py`: imports the new step module.
- `features/supervision.feature`: the three retired scenarios removed.
- `CLAUDE.md`: the `scripts/supervise*.py` row names the pool of workers.

Dropped from the researcher's set as read-only on the path: `scripts/work`, `scripts/supervise_brief.py`, `scripts/measure_read.py`.

## 3. Decisions

1. **One pool for every stage.** Each pass, `work run` starts a worker for every movable work-item, in the queue's order, while fewer workers than the workers number are running: researchers, planners, implementers and task reviewers alike; an implementer only when its file set shares no file with that of any claimed work-item in flight. Rests on supervision#r59, #r60, #r20, #r1 and design-decision/work-item-lifecycle-as-run (ready → claimed guard), design-decision/the-file-set-is-the-claim.
2. **The workers number** is a top-level `workers` key, a positive integer, in `.shop/delivery.toml`, 4 when the file or the key is absent. Being top-level, the test's Given writes it above the file's first table. Rests on supervision#r60 (the key's name is implementation; beside `[tests]` r29 and `[allowed_tools]` r30).
3. **`.shop/delivery.toml` is read once, before any push verification, log line or worker.** A file that does not parse, or a `workers` that is not a positive integer, ends `work run` with an error saying why and changes nothing (fixes D1: today a traceback and an uncommitted start line). Rests on supervision#r10 and #r60.
4. **The transcript path** is recorded in each stage's `session.json` under a key `transcript_path`, found after the session ends by its session id under Claude Code's store (`$CLAUDE_CONFIG_DIR`, else `~/.claude`, `projects/*/<session-id>.jsonl`), the rule `measure_read.round_trips` already reads by. The branch review counts: r49 names it the stage `branch-review`. Rests on supervision#r62, #r49.
5. **blocked_by.** A work-item whose `blocked_by` names a work-item that is not `green` is not movable; checked each pass, so it moves in the same run once its blockers are green. A name is a work-item's id or its name in the initiative (the forms migration-tools writes). The guard sits in the pool's choice of items, so no start line is logged for it. Rests on supervision#r63, #r37, design-decision/work-item-lifecycle-as-run.
6. **Faults with stages in flight.** Every stage the pool starts runs inside `Run.step`'s wrapper, so a `Fault` or `GitFailed` in any thread makes its `failed` transition and its `## Faults` line (r39, r41, r42, r45). After a fault, `work run` starts no further worker, lets the running ones end and makes their transitions, then exits with r40's error — as `together` already joins both threads before it raises. Rests on supervision#r40, #r33, #r41.
7. **Merge order.** An implementer's end with DONE enters a queue in the order the implementers ended (their end log lines); rebase, scenarios, suite and merge run for one entry at a time from its head. Rests on supervision#r61, #r4, #r18.
8. **Shared state under one lock.** Transitions, commits, pushes, log appends and the r28 check of the main checkout run under one lock; r28's check counts `work run`'s own uncommitted writes as its own and, as r28 says, faults the work-item of the worker that ended. Rests on supervision#r7, #r8, #r28.

## 4. Tests the decisions break

- `test_supervision.py`, scenario at line 8 (@r1 deprecated): its Then `no worker was started before the one before it had ended` breaks under decision 1. Removed with its scenario (Retires); the step in `supervision_then_workers.py` (lines 30-33) is removed, as no other scenario uses it (that text appears only at line 16).
- scenario at line 429 (@r20 deprecated): `two implementers worked at the same time, and never three` with no workers number breaks under decision 2 (default 4). Scenario removed (Retires); the step stays, used by line 438.
- scenario at line 395 (@r20 deprecated): would stay green but is retired; removed. Its Then "the initiative branch has both implementers' commits, one after the other, with no merge commit" is used by no other scenario, so it is removed or folded into the r61 Then.
- No other test found broken: the r20 share-a-file outline holds under decision 1's disjointness; no test reads `session.json` keys from `work run` (batch-measurement writes its own); scenarios with two work-items (lines 221, 229, 257, 570, 578) read sound. Not verified by the researcher: `supervision_faults_steps.py` and `supervision_review_steps.py`; the implementer runs the whole supervision suite after decision 6 and reports any that breaks.

## 5. Open cases

- No transcript found under the store for a session id (decision 4): what `session.json` records then.
- A `blocked_by` naming no work-item, or one in another initiative, or a withdrawn one: not green by r63's text, so never moved; and the exit and print when only such items are left with none awaiting-answer or failed (no r9/r32/r52 case; the Implementation's exit code 1).
- A `blocked_by` cycle within the initiative.
- How the stub's "once <limit> workers have started" counts (from the run's start, across agents), so the fifth researcher of r60 does not wait forever.
- The order in which the pool fills free slots when more items can move than there are slots.
- Two implementers ending at the same instant (r61's order).
