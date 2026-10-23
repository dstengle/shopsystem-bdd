# Research of w101: work run runs independent work-items side by side

Accepted requirements: supervision r1, r20, r59, r60, r61, r62, r63. Accepted scenarios: the 12 the brief lists, 15 test ids (`tests/scenarios/test_supervision.py`).
Search method: `tools tests-of` and `untested` unusable: `no map` (a map runs the whole suite, not made). `tools refs` used for names. Test lists below are `by search`.
Scripts: plugin 0.24.0 `tools`. Probes: `.shop/scratch/w101-1-research/probe_supervision.py`, `probe_delivery.py`; run with `python3 -m pytest -q -s -n 0 -p no:warnings <path>`.
`git status --porcelain` clean at the end (scratch ignored).

## 1. Why each scenario is red today

Run by `python3 -m pytest -q --tb=short -p no:warnings "tests/scenarios/test_supervision.py::<id>"`, one per id.

- r1 (deprecated) and r1: PASS (run).
- r59 (`when more than one work-item ... started at the same time`): StepDefinitionNotFound, Given `every worker gives DONE, the researcher of w1 and the planner of w2 each ending once both have started` (feature line 32). Missing: a Given (no step matches); the stub's `meet` counts starts of one agent only (`tests/scripts/stub_claude.py:108-116`), so a researcher and a planner cannot meet. The Then `the researcher of w1 and the planner of w2 worked at the same time` (line 34) is unbound by search too (only the implementers' span step, `supervision_then_workers.py:243`). Code: `supervise.py:Run.run` (216-226) starts `movable[0]` only; `Run.pair` (159-173) looks at `ready` only. No research/plan concurrency.
- r60 (2 and 4 examples): StepDefinitionNotFound, Given `i1's work-items w1, w2, w3, w4 and w5 are drafted` (line 39). `supervision_given.py:54` regex has `[\w -]+?`: no commas. Also unbound: `.shop/delivery.toml gives 2 as its number of workers` / `gives no number of workers` (line 40), and the stub's "each researcher ending once <limit> workers have started" (line 41). Code: no reader of a workers number anywhere (`by search` for `workers` in scripts/: comments only). `Workers.delivery` (`supervise_worker.py:84-86`) reads `.shop/delivery.toml` for `[tests]`/`[allowed_tools]` only. The key name is named nowhere in spec, README or code.
- r62: StepDefinitionNotFound, Then `the session.json in each of w1's four stage directories records the path of the transcript ...` (line 216). Code: `Workers.worker` (`supervise_worker.py:157`) writes claude's JSON stdout as `session.json`; no transcript path. `Reviews.branch_review` (`supervise_review.py:66`) does the same.
- r20 own worktree: StepDefinitionNotFound, Then `each of them worked in a worktree of its own` (line 412). Code: the implementers each get `worktree(name, name, "work/"+name)` (`supervise_merge.py:95`), distinct labels; read, not run past the step.
- r20 three, workers 2 (line 439): StepDefinitionNotFound, Given `.shop/delivery.toml gives 2 as its number of workers` (line 442). Same missing key as r60. Code caps pairs at two (`supervise.py:Run.pair`, 169-172).
- r61: StepDefinitionNotFound, Given `... each implementer committing a file ... once two implementers have started, w2's implementer ending before w1's` (line 451). Missing: the stub has no way to make one worker end before another (`meet`, `watch`, `touch` only; `stub_claude.py:28-37`). Later steps not reached, so unverified.
- r63: StepDefinitionNotFound, Given `i1's work-item w1 is drafted, its blocked_by naming w2, and w2 is awaiting-answer` (line 697). Missing: the regex (`supervision_given.py:54`) has no `blocked_by`; `item_text` (`supervision_world.py:90`) writes none. Code: no reader of `blocked_by` in `scripts/supervise*.py` (by search); `model_work.py:193` reads it for the design model only.
- r20 two ready, own worktree (line 406): see above (the Then is the red step).
- Passing today (run): r20 deprecated "merged one at a time" (line 396); r20 shared-file outline, 3 examples (lines 415-427); r20 deprecated "of three ... no more than two" (line 430). These are PASS but see part 4: they assert the old sequential/limit-two behaviour.

## 2. What the system answers today

Probes are in `.shop/scratch/w101-1-research/`, each building its own repo, remote and stub under `.shop/scratch/w101-1-research/<name>/` and running `scripts/work run i1` of this worktree.

- Probe `test_blocked_by_awaiting_answer_and_ghost` (run; RC 3). Repo: w1 drafted, `blocked_by: [w2]`; w2 awaiting-answer, question "Which module owns the log?"; w3 drafted, `blocked_by: [ghost]`.
  - Output: `w1 green`, `w2 awaiting-answer` with its question, `w3 green`. ORDER: w1 got code-scout, planner, implementer, reviewer, then w3 got all four.
  - So a worker is started for a work-item whose blocked_by is not green (r63 not met); an absent blocked_by target is ignored too (nearest case, no spec line for it).
- Probe `test_session_json_content` (run). Each of w1's four `session.json` holds exactly the keys `is_error, num_turns, result, session_id, subtype, total_cost_usd, type`. None mentions a transcript or a `.jsonl` path (r62 not met).
- Probe `test_serial_two_stages_and_five_items_with_workers_key` (run; RC 0 both). (a) w1 drafted and w2 researched: w1 through all four stages, then only w2's planner, implementer, reviewer: strictly one worker at a time. (b) Five drafted items, `.shop/delivery.toml` with `workers = 2` above `[tests]`: five full pipelines in turn; the key is ignored (r60 not met; the cap is never read).
- Probe `probe_delivery.py::test_malformed_delivery_toml` (run; RC 1). See part 6, D1.
- Not probed (`read`): a `.shop/delivery.toml` absent (the Background's `delivery.toml gives no [tests]`, `supervision_tests_steps.py:31`, covers that) and an empty `blocked_by`.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise.py:Run.run` (216-226) | pulls one work-item one stage at a time: `step(*movable[0])` | r59/r60/r63: start several research/plan stages at once, within the workers number, and only for unblocked work-items | by search: every `work run` scenario in `test_supervision.py` (all 15 ids run the loop); no map | refs (`run` entry, `scripts/supervise.py:262`), read |
| `scripts/supervise.py:Run.pair` (159-173) | pairs two `ready` work-items with disjoint file sets, never more | r20/r60: as many as the workers number (4 where none) | by search: the r20 ids in `test_supervision.py` (lines 396-445) | read; refs (`pair` 4 refs, 1 prod) |
| `scripts/supervise.py:Run.together` (175-191) | one thread per implementer of a pair | r61: merge order = end order; a bound | by search: r20 ids; r61 unbound | refs (`together`, 1 prod ref) |
| `scripts/supervise.py:Run.step` (129-138) | the only place that wraps `stage()` in `except (Fault, GitFailed) -> fail()` | a parallel research/plan path must keep that wrapper | none (by search: no test runs two stages at once) | read |
| `scripts/supervise.py:Run.run`, `if self.faults: break` (225) | ends the loop after a failed work-item | with stages in flight, the run must drain them first | none | read |
| `scripts/supervise_worker.py:Workers.worker` (157) | writes claude's stdout as `session.json` | r62: add the transcript path | by search: none reads its content in the supervision tests; `batch_measurement_given_steps.py:157-159` writes such files | read, probe B |
| `scripts/supervise_review.py:Reviews.branch_review` (66) | same `session.json` for the branch reviewer | r62 says "a stage's session.json": decide whether the branch review counts (question Q2) | none found by search | read |
| `scripts/supervise_worker.py:Workers.delivery` (84-86) | parses `.shop/delivery.toml` for `[tests]` and `[allowed_tools]` only | r60: a new key (name not given, Q1) read here | by search: `supervision_tests_steps.py`, `supervision_given.py:99-118` | refs (`delivery`, 1 prod ref) |
| `scripts/supervise_worker.py:Workers.session` (182-189) | one claude session, after `tools()` reads delivery | a malformed toml raises here, after the start line is logged (`worker`, 151) | none (probe D1 only) | read, probe D1 |
| `scripts/supervise_merge.py:Merge.claimed` (93-111) and `merge` (113-132) | merge taken under `self.lock` after the worker's end; a separate lock hold at the worker's end | r61: merge order must equal end order; the gap between the two lock holds lets a later end merge first | none (r61 unbound) | read |
| `scripts/supervise.py:Run.__init__` (50-51) `self.own`, `self.unlogged` | shared across threads, reset by `commit` | with two stages in flight, shared under the lock only where held | none | read |
| `scripts/measure_read.py:round_trips` (101-112) and `store_dir` (96-98) | finds a transcript by session id under `projects/*/`, never by a path | batch-measurement r53 reads the `session.json` path (supervision r62); changes with r62 | by search: `tests/scenarios/test_batch_measurement.py` (not run) | read |

## 4. Tests the requirements make impossible to keep

Searched by text (no map). Read each scenario's Then.

- `test_supervision.py` id `..._until_no_workitem_can_make_a_transition_deprecated` (r1 deprecated, feature line 9): PASS today (run). Then `no worker was started before the one before it had ended` (`supervision_then_workers.py:30-33`) asserts the global event list alternates start/end for all workers of w1 and w2. With r59, two drafted work-items start their research together, so two starts precede an end: the assertion fails. Conflict: r59 against this deprecated scenario.
- `..._of_three_ready_workitems_whose_claims_would_not_share_a_file_no_more_than_two_are_implemented_at_the_same_time_deprecated` (r20 deprecated, line 430): PASS today (run). Its Then `two implementers worked at the same time, and never three` (`supervision_then_workers.py:257-260`) and its Givens name no `delivery.toml` workers number. Under r60 the default is 4, so three non-overlapping implementers may run at once: fails. Conflict: r60's default against the scenario's implicit 2.
- `..._merged_one_at_a_time_deprecated` (r20 deprecated, line 396): PASS today (run). Then: one-after-the-other, no merge commit. r61 keeps this; sound by read.
- `..._share_a_file_are_implemented_one_after_the_other: <how>` (3 examples, lines 415-427): PASS today (run). Then `no implementer was started before the one before it had ended` (`supervision_then_workers.py:251-254`, `most_at_once == 1`). Overlapping file sets are never paired under r20, so it stays sound. Sound by read.
- Not affected by the accepted requirements, by search: `tests/scripts/test_work_items.py` and `tests/scenarios/test_work_queue.py` match `work run|supervise|delivery.toml`; not read further.
- Sound: r62, r59, r60, r61, r63 scenarios are unbound, so they cannot be called impossible to keep yet.

## 5. A step the work-item skips

- A parallel research/plan path (r59) that calls `Run.stage()` from threads, as `together()` calls `implement()`, skips `Run.step`'s fault wrapper (`supervise.py:135-138`): a `Fault` or `GitFailed` would escape to the thread, to `together`'s `failed` list and out of `run()`, with no `failed` move and no `## Faults` line. Read, not probed.
- The same path skips `Run.run`'s `if self.faults: break` (225) if it runs its own loop. Read.
- r63 guard: no existing step performs a `blocked_by` check. A guard placed in `Run.step` would not cover `together`'s `implement()` threads (which bypass `step`). The only common point is `Workers.worker` (before `session`, after `verify_push`, `supervise_worker.py:144`): read. Probe A shows no guard today.
- `verify_push` (`supervise_faults.py:64-70`, a `git push --dry-run`) runs in `worker()` for every worker; a parallel path through `worker()` keeps it. Read.
- The planned→ready move (`step`, 129-131) has no guard, as the capability says (its Implementation). Read, consistent.

## 6. Defects

### D1. A malformed `.shop/delivery.toml` ends `work run` with a traceback
Reproduction: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w101-1-research/probe_delivery.py`, which builds w1 drafted and `delivery.toml` = `[tests` + `work_item = `.
Came back: RC 1; stderr ends `tomllib.TOMLDecodeError: Expected ']' at the end of a table declaration (at line 1, column 7)`, a Python traceback. No worker was started (no stub record). w1's file still says `status: drafted`.
Expected by r10 (capability line 35): exit with an error saying why, and change nothing. The state is unchanged, but the message is a traceback, not a sentence.
Read (not probed): `Workers.session` calls `tools()` (`supervise_worker.py:88-91`) which calls `delivery()`, after `worker()` has logged the start line (`supervise_worker.py:151`), so `log.jsonl` is left with a start line and no end.

## 7. The file set

Production files the work-item changes:
- `scripts/supervise.py` (263 lines, room 37): `Run.run` loop for concurrent research/plan within the workers number (r1, r59, r60); `Run.pair` cap (r20, r60); `together` merge order (r61); `blocked_by` check (r63) for the pair path. Found by read and refs.
- `scripts/supervise_worker.py` (212, room 88): `Workers.delivery` reads the workers number (r60, key name Q1); `Workers.worker` writes the transcript path into `session.json` (r62, line 157); the r63 guard before `session()` (line 144 area). Found by read, refs (`delivery`, `session`).
- `scripts/supervise_review.py` (77, room 223): `session.json` at line 66 only if the branch review counts as a stage (Q2). Found by read.
- `scripts/supervise_merge.py` (132, room 168): merge order under one lock hold (r61, `claimed`, lines 102-111). Found by read.
- `scripts/supervise_faults.py` (160, room 140): `fail()` and `push()` already take the lock; no change expected. Found by read; listed because `Run.step`'s wrapper is in its path.

Test and support files the work-item changes:
- `tests/scenarios/supervision_given.py` (247, room 53): the r60 comma regex (line 54), `blocked_by` Given (r63), the workers-number Givens (r20, r60), the cross-agent meet and end-order Givens (r59, r61). Found by search (the undefined-step list).
- `tests/scenarios/supervision_then_workers.py` (285, room 15, too little room): the researcher/planner span Then (r59), the worktree-of-its-own Then (r20), the `session.json` path Then (r62), the cap Thens (r60). `one_at_a_time` (line 30) and `two_at_most` (257) conflict with r59 and r60 (part 4). Put the new steps in a new module, e.g. `tests/scenarios/supervision_parallel_steps.py`, and add its row to `CLAUDE.md`'s module map (CLAUDE: "a new concern gets a new module and a row here").
- `tests/scenarios/supervision_world.py` (172, room 128): `item_text` takes `blocked_by` (r63). Found by read.
- `tests/scripts/stub_claude.py` (206, room 94): `meet` counts across agents (r59, r60); an end-order control for r61 (`stub_claude.py:28-37`). Found by read.
- `tests/scenarios/test_supervision.py` (247, room 53): imports of the new step module only. Found by read.
- `features/supervision.feature`: the deprecated scenarios at lines 9, 396, 430 conflict (part 4). Not changed by this research; decision for the plan (Q3).

Modules on the change's path, not edited:
- `scripts/work` (80, room 220): the entry point, `run` only.
- `scripts/workqueue.py` (262, room 38): `move`, `agrees`, `items`. Its room is small: a change there would need a split first.
- `scripts/supervise_brief.py` (110, room 190): the briefs; not on the r1/r59/r60 path except the brief text for r62 (none needed).
- `scripts/measure_read.py`: outside this work-item's accepted set (batch-measurement r53 owns it); listed in part 3 only.

## Questions for the plan
- Q1: the key of `.shop/delivery.toml` for the number of workers is named nowhere (spec, README, code). Which name?
- Q2: does the branch reviewer's `session.json` (`supervise_review.py:66`) fall under r62's "a stage's session.json"?
- Q3: the deprecated scenarios at feature lines 9 and 430 conflict with r59 and r60 (part 4). Keep, retire, or change them?
