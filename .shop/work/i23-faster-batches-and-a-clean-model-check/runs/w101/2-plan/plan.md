# Plan of w101: work run runs independent work-items side by side

Accepts supervision r1, r20, r59, r60, r61, r62, r63. From the research notes (`1-research/notes.md`); test ids in `tests/scenarios/test_supervision.py`.

## 1. What goes green

- **supervision#r1**: "`work run` pulls each work-item through research, plan, implementation and review until no work-item can make a transition": passes today and must keep passing once stages run side by side.
- **supervision#r59**: "when more than one work-item is drafted or researched, their research and plan stages are started at the same time": red because its stub Given has no step (the stub's `meet` counts only one agent's starts) and its Then has no step. Also, `Run.run` only ever starts `movable[0]`, so no two stages run at once.
- **supervision#r60**: "`work run` runs at most <limit> workers at the same time when .shop/delivery.toml <gives>" (examples 2 and 4): red because the Given for a comma list of five work-items has no step (the regex takes no commas). The workers-number Givens, the stub Given and the Then have no steps either. Nothing reads a number of workers.
- **supervision#r62**: "each stage's session.json records the path of the transcript of that stage's session": red because the Then has no step. `session.json` holds only claude's stdout, with no transcript path.
- **supervision#r20**:
  - "two ready work-items whose claims would share no file are implemented at the same time, each in its own worktree": red because "each of them worked in a worktree of its own" has no step.
  - "of three ready work-items whose claims would share no file, no more are implemented at the same time than .shop/delivery.toml's number of workers": red because its workers-number Given has no step.
  - "two ready work-items whose claims would share a file are implemented one after the other: <how>" (3 examples): passes today and must stay green.
- **supervision#r61**: "implementers working at the same time that end with DONE have their branches merged one at a time, in the order they ended": red because the stub cannot make one worker end before another, so the Given has no step. In the code, the merge is taken in a separate lock hold after the worker ends, so a later end can merge first.
- **supervision#r63**: "no worker is started for a work-item whose blocked_by names a work-item that is not green": red because the Given has no step (no `blocked_by` in the regex or in `item_text`). In `supervise*.py` nothing reads `blocked_by`, and the probe showed w1 run through all four stages while w2 was awaiting-answer.
- **Deprecated scenarios.** The work-item has no `## Retires` section, but three deprecated scenarios carry tags it accepts:
  - feature line 9, r1 "... one worker at a time ... (deprecated)": breaks under r59;
  - line 396, r20 "... and merged one at a time (deprecated)": stays green, and its replacement at line 406 goes green;
  - line 430, r20 "... no more than two are implemented at the same time (deprecated)": breaks under r60's default of 4.
  - See the question at the end.

## 2. Where the change lands

- `scripts/supervise.py`:
  - `Run.run` becomes a loop that fills worker slots up to the workers number. Its candidates are the movable work-items that no `blocked_by` holds back.
  - `pair` and `together` are generalised: implementers whose claims share no file, in any number up to the cap.
  - Every threaded stage keeps `step`'s fault wrapper.
  - The file has only 37 lines of room left, so the slot pool moves out to a new module (next entry).
- `scripts/supervise_pool.py` (new): the slot pool, meaning the threads, the cap, waiting for an end, and draining stages still running after a fault. The existing `scripts/supervise*.py` row of CLAUDE.md's module map covers it.
- `scripts/supervise_worker.py`: `delivery` reads the number of workers. `worker` records the transcript path in `session.json`. The r63 guard sits before the session starts, as a second line of defence.
- `scripts/supervise_merge.py`: an implementer's end and its merge happen in one lock hold, so merges run in the order the implementers ended (r61).
- `scripts/supervise_review.py`: the branch reviewer's `session.json` records its transcript path too (decision 5).
- `tests/scripts/stub_claude.py`:
  - `meet` counts the starts of any agents, not just one;
  - an end-order control lets one named worker end before another;
  - the stub writes a transcript where claude would;
  - its records stay safe when two stubs write at once.
- `tests/scenarios/supervision_given.py`: the comma-list Given, the `blocked_by` Given, the two workers-number Givens, and the stub Givens for the cross-agent meet and the end order.
- `tests/scenarios/supervision_world.py`: `item_text` takes `blocked_by`. The world points `CLAUDE_CONFIG_DIR` at a scratch directory.
- `tests/scenarios/supervision_parallel_steps.py` (new): the new Thens (researcher and planner at the same time, `<limit>` workers and never more, a worktree of its own, the transcript path, w2's commit and then w1's). `supervision_then_workers.py` has only 15 lines of room. The `tests/scenarios/` row of CLAUDE.md's module map covers the new file.
- `tests/scenarios/supervision_then_workers.py`: the `one_at_a_time` step is removed once the line-9 scenario is retired.
- `tests/scenarios/test_supervision.py`: imports the new step module. The bindings of retired scenarios go.
- `features/supervision.feature`: only `features retire` of the three deprecated scenarios, if the question is answered that way.
- **Dropped from the researcher's set:** `scripts/supervise_faults.py`. Its `fail` and `push` already take the lock and nothing in it changes, so leaving it out keeps the claim narrow.

## 3. Decisions

1. **The workers key.** The number of workers is a top-level integer key `workers` in `.shop/delivery.toml`. Where the file or the key is absent, the number is 4 (supervision#r60; the probe already wrote it this way). The file is read once, when `work run` starts, before any worker.
2. **One cap for every worker.** The cap counts all workers at once: researchers, planners, implementers and reviewers (supervision#r60, "at most as many workers at the same time").
   - Any movable stage may take a free slot.
   - The only rule beyond the cap and the guards is supervision#r20's: an implementation starts only if its claim shares no file with an implementation already running.
   - Research and plan stages of different work-items start together (supervision#r59). Work-items keep their stage order (supervision#r1).
3. **blocked_by.** A work-item is not movable while any entry of its `blocked_by` names a work-item whose status is not `green` (supervision#r63, alongside r37's statuses).
   - Names are resolved as `model` resolves them: short or qualified, across every initiative under `.shop/work/`. Work-item ids are global.
   - The same check sits in `Workers.worker` before the session, so implementers started by the pool are covered too.
4. **Merge order.** An implementer's `DONE` is followed by its merge within one hold of the merge lock, taken in end order (supervision#r61). The branches stay one after the other, with no merge commit (r20's line-396 scenario still holds).
5. **The transcript path.** `session.json` gains a `transcript` key: the absolute path `<store>/projects/<project directory>/<session id>.jsonl` (supervision#r62).
   - `<store>` is `CLAUDE_CONFIG_DIR`, else `~/.claude`, as in `measure_read.store_dir`.
   - `<project directory>` is the worker's working directory named the way Claude Code names it, with every character other than a letter, digit or `-` replaced by `-`. The implementer checks this rule against an existing project directory on the machine before relying on it.
   - The branch reviewer's `session.json` gets the key too, because supervision#r49 calls `branch-review` a stage.
   - `measure_read` is not changed here; it belongs to batch-measurement#r53's own work-item.
6. **Faults while stages run side by side.** Every stage started from a thread goes through the same wrapper as `Run.step`: a `Fault` or `GitFailed` moves the work-item to `failed` and writes its `## Faults` line (supervision#r39, r41).
   - After a fault, no new stage starts. Stages already running are left to end and be recorded, and then `work run` exits with r40's error (supervision#r40, design-decision/exits-are-successful-or-errors).
   - Commits and the shared `own`/`unlogged` state are touched only under the lock (supervision#r7).
7. **A malformed `.shop/delivery.toml`.** Because the file is now read at start, a malformed one ends `work run` with r10's error, naming the file and the parse error, before anything changes. It no longer ends in a traceback (supervision#r10; the capability's Implementation section, "not with a traceback"). This also clears defect D1.
8. **The stub's transcript.** The stub writes a transcript under the world's `CLAUDE_CONFIG_DIR` at the path claude would use. The r62 Then checks that each stage's recorded path is that file and that the file holds the stage's session id.

## 4. Tests the decisions break

- **`test_supervision.py`, r1 deprecated (feature line 9).** Decision 2 breaks it: two drafted work-items start their research together, so "no worker was started before the one before it had ended" fails. It is removed with `features retire`, with its binding. The `one_at_a_time` step in `supervision_then_workers.py` then names no scenario and is removed. All of this depends on the question.
- **`test_supervision.py`, r20 deprecated "of three ... no more than two" (line 430).** Decision 2 breaks it: with no workers key the cap is 4, so three implementers run at once and "never three" fails. It is removed with `features retire`. Its Then step stays, because line 439's scenario uses it. This depends on the question too.
- **`test_supervision.py`, r20 deprecated "merged one at a time" (line 396).** No decision breaks it. It is retired only because its replacement goes green (design-decision/held-scenarios).
- **The shared-file outline (lines 415-427).** It stays sound: overlapping claims are never paired (decision 2).
- **What was verified.** I checked by text search that "no worker was started before" and the "worked at the same time" steps are used only by the scenarios above. The notes found nothing in `tests/scripts/test_work_items.py` or `test_work_queue.py` that the accepted requirements touch. Nothing was run under concurrency beyond these, so the whole suite run is the check: a scenario whose stub results depend on the global start order of two work-items would show up there.

## 5. Open cases

- A `blocked_by` that names no existing work-item. `model check` already reports it as a problem, and today `work run` ignores it.
- A `workers` value that is 0, negative, not an integer, or a boolean.
- An empty `blocked_by` list, and a `blocked_by` that names the work-item itself or forms a cycle. The work-items would never become movable, so `work run` ends with no transition possible.
- A worker whose stub transcript is missing. Real claude may not have written it, so the path is recorded whether or not the file exists.
- Two stages of the same work-item can never run at once. The candidates are chosen by work-item, so this already holds.

## Question

w101 has no `## Retires` section. Under delivery#r17 and design-decision/held-scenarios it would list the three deprecated scenarios at feature lines 9, 396 and 430. red-green#r2 lets the implementer retire only what the work-item lists there.
