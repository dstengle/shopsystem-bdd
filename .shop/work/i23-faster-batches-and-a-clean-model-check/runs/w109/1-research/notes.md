# Research of w109: work run runs independent work-items side by side

Accepted: supervision r1, r20, r59, r60, r61, r62, r63. Scenarios: 15 test ids in `tests/scenarios/test_supervision.py` (the brief's 12 titles; outlines expanded).
Method: `tools refs` for names (`by refs`). `tools tests-of` and `untested`: no map, not made (`by search` for every test list). Tests run by node id, one per id, `python3 -m pytest -q --tb=short -p no:cacheprovider "<id>"`.
Probes: `.shop/scratch/w109-1-research/probe_supervision.py` (own repo, remote and stub per probe), run `-n 0 -s`.
Retires in w109.md: r1 deprecated (feature 8), r20 deprecated (396, 430). `git status --porcelain` clean at the end.

## 1. Why each scenario is red today

Run: each id by node id. PASS or FAIL as run.

- r1 deprecated (feature 8): PASS (run). Retired.
- r1 (19): PASS (run).
- r59 (28): FAIL (run), `StepDefinitionNotFoundError`, Given line 32 "every worker gives DONE, the researcher of w1 and the planner of w2 each ending once both have started". Missing: that Given, the Then "worked at the same time" for two agents, and a stub `meet` across agents (`tests/scripts/stub_claude.py` `meet()` counts starts of one agent: read). Code: `supervise.py:Run.run` (216-226) takes `movable[0]` only, so research and plan never overlap.
- r60 limit 2 (47): FAIL (run), Given line 39 "i1's work-items w1, w2, w3, w4 and w5 are drafted": `supervision_given.py` `work_items` regex (line 54) has `[\w -]+?`, no comma (read). Also unbound: the delivery workers Given (line 40) and the researcher-ends-at-limit Given (line 41). Code: no reader of a workers number: `Workers.delivery` (`supervise_worker.py:84-86`) reads `[tests]` and `[allowed_tools]` only; `tools` (88-94) takes `delivery()`.
- r60 limit 4 (48): FAIL (run), same step as above.
- r62 (210): FAIL (run), Then line 216 "the session.json in each of w1's four stage directories records the path of the transcript" unbound. Code: `Workers.worker` (`supervise_worker.py:157`) writes claude's stdout as `session.json`; no transcript path (probe below).
- r20 share no file, own worktree (406): FAIL (run), Then line 412 "each of them worked in a worktree of its own" unbound. Code: each implementer has its own `worktree(name, name, "work/"+name)` (`supervise_merge.py:95`), read only.
- r20 share a file, 3 outline rows (415-427): PASS (run), all three.
- r20 deprecated, three, no more than two (430): PASS (run). Retired.
- r20 deprecated, two merged one at a time (396): PASS (run). Retired.
- r20 three, workers 2 (439): FAIL (run), Given line 442 `.shop/delivery.toml gives 2 as its number of workers` unbound. Code: `Run.pair` (`supervise.py:159-173`) returns one pair; nothing caps at a workers number.
- r61 (447): FAIL (run), Given line 451 "...once two implementers have started, w2's implementer ending before w1's" unbound. The stub has no end-order control (`meet`, `watch`, `touch` only; read).
- r63 (694): FAIL (run), Given line 697 "its blocked_by naming w2, and w2 is awaiting-answer" unbound. The Given regex (`supervision_given.py:54`) and `item_text` (`supervision_world.py`) take no `blocked_by`. Code: no `blocked_by` read in `scripts/supervise*.py` (by search).

## 2. What the system answers today

Probes, run by me, from `.shop/scratch/w109-1-research/probe_supervision.py`:

- `test_blocked_by_not_green`: `python3 scripts/work run i1` in a repo: w1 drafted with `blocked_by: [w2]`; w2 awaiting-answer with "Which module owns the log?". Came back: RC 3; w1 got code-scout, bdd-planner, bdd-implementer, bdd-task-reviewer and is `green`; w2 `awaiting-answer` with the question. So r63's Given/When gives a worker to a blocked item. Nearest case (absent target, `blocked_by` naming nothing) not run here.
- `test_session_json_keys`: each of w1's four stage `session.json` holds exactly `is_error, num_turns, result, session_id, subtype, total_cost_usd, type`; no transcript path or `.jsonl` (run). r62's Then is unmet.
- `test_five_drafted_workers_key`: five drafted items, `.shop/delivery.toml` with `workers = 2` above `[tests]` (the key name is my probe's choice; the spec names none). Came back: RC 0, all five `green`; events show one worker at a time, most at once: 1 (run). The key is ignored; r59 and r60 unmet.
- `test_malformed_delivery`: `.shop/delivery.toml` = `[tests` (run). See D1.
- Not run by me: r20 own worktree, r61 end order, r59 with two stages. Read only (part 3).

## 3. Old assumptions

Found by read and `tools refs` (refs: `pair` 2 prod uses in `run`, `together` 1, `delivery` 1, `implement` 1, `step` 1, `session` 2 prod + tests). Test column by search; no map.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise.py:Run.run` (211-245) | pulls `movable[0]` one stage at a time; pairs the first two ready | r59/r60/r63: several research or plan stages at once, within the workers number, skipping blocked items | every `work run` id (by search); the r1 ids run it (PASS) | read; refs |
| `scripts/supervise.py:Run.pair` (159-173) | first pair of `ready` items with disjoint file sets | r20/r60: as many disjoint items as the workers number | r20 ids: outline (PASS), 439 and 406 FAIL before; by search | read; refs |
| `scripts/supervise.py:Run.together` (175-191) | one thread per member of the pair; join; raise the first failure | r20/r60: N-way; r61: merge in end order | r20 outline and 396 (run, PASS, by search); r61 unbound | read; refs (1 prod ref, 0 tests) |
| `scripts/supervise.py:Run.step` (129-138) | the only wrapper of `stage()` in `except (Fault, GitFailed)` → `fail()` | r59: research and plan in threads must keep that wrapper | none (no test runs two stages at once; by search) | read |
| `scripts/supervise.py:Run.run` `if self.faults: break` (225) | stops pulling after a failed item | with stages in flight, drain them before stopping | by search: `supervision_faults_steps.py` ids (not run) | read |
| `scripts/supervise_merge.py:Merge.claimed` (93-111) | merge under `self.lock` after the worker ends, branch deleted under the lock | r61: merge in the order implementers ended; the suite run is in the lock | r20 ids (run, PASS), by search; r61 unbound: none for end order | read |
| `scripts/supervise_merge.py:Merge.implement` (68-79) | catches `(Fault, GitFailed)` itself, `failed_claimed` otherwise | a parallel research/plan thread needs its own wrapper | by search: r20 ids; none for research | read |
| `scripts/supervise_worker.py:Workers.worker` (150-158) | writes claude's stdout as `session.json` | r62: also the transcript path, found from the session id | none reads its keys in the supervision tests (by search); `tests/scenarios/batch_measurement_given_steps.py:157-159` writes such files | read; probe `session_json` |
| `scripts/supervise_review.py:branch_review` (66) | same `session.json` for the branch reviewer | r62 says "each stage's": question Q2 | by search: none | read |
| `scripts/supervise_worker.py:Workers.delivery` (84-86) | parses `.shop/delivery.toml` for `[tests]`, `[allowed_tools]` | r60: a workers number from the same file | by search: `supervision_tests_steps.py`, `supervision_given.py` (99-118) | refs (1 prod use, line 91) |
| `scripts/supervise_worker.py:Workers.tools` (88-94), `session` (182-189) | `delivery()` read after `worker()` logged the start line | a malformed file must refuse before any start (D1) | none in the suite (by search); probe D1 only | read; probe D1 |
| `scripts/supervise.py:Run.__init__` (50-51) `self.own`, `self.unlogged` | shared across threads; reset by `commit` | with stages in flight, both change under the lock | by search: r20 ids | read |
| `Workers.worker` (`supervise_worker.py:159-161`) changed-checkout check | a change to `.shop/work/` in the main checkout while one worker ends is that worker's fault | with several workers in flight, the change may belong to another; the fault names the wrong stage | none | read |
| `scripts/measure_read.py:round_trips` (101-112), `store_dir` (96-98) | finds a transcript by session id under `projects/*/`, not by a path | r62 records the path; batch-measurement reads it | by search: `tests/scenarios/test_batch_measurement.py` (not run) | read |

## 4. Tests the requirements make impossible to keep

By search (no map). Each test read in its Then.

- `test_supervision.py` id `…_until_no_workitem_can_make_a_transition_deprecated` (feature 8, retired): Then `no worker was started before the one before it had ended` (`supervision_then_workers.py:30-33`) asserts the whole event list alternates start and end. r59 starts two research stages together: fails. Passes today (run). Conflict: r59 against a retired scenario.
- `…_of_three_…_no_more_than_two_…_deprecated` (feature 430, retired): Then `two implementers worked at the same time, and never three` (`supervision_then_workers.py:257-260`) with no workers number, so r60's default 4 lets three run: fails. Passes today (run). Conflict: r60's default against a retired scenario.
- `…_merged_one_at_a_time_deprecated` (feature 396, retired): one after the other, no merge commit. Would stay sound; retired anyway.
- r20 outline, share a file (415): Then `no implementer was started before the one before it had ended` (`supervision_then_workers.py:251-254`). Sound: overlapping sets are never paired; holds only if the new scheduler keeps the disjointness check per member.
- r20 three, workers 2 (439): Then `two_at_most`; sound with the workers Given (once the key exists).
- Feature 249-251 (`w1` fails on merge, `w2` green) and 221-223: sound by read, from grep; not run.
- Not checked: `supervision_faults_steps.py`, `supervision_review_steps.py` and feature 767-778 (expected failures under r43): not read beyond grep.

## 5. A step the work-item skips

- r63 guard, not in the existing way. Existing: `Run.step` → `stage()` → `worker()`. Only `worker()` is common to both the step path and the pair path (`together`), before `session()` (`supervise_worker.py:144-150`). Refusals today: none for blocked items. Probe `blocked_by` (run): the worker starts anyway. Effect a guard would add: no worker, the item stays put, its `blocked_by` checked each pass. Read.
- r62 transcript path, the step that writes `session.json`: `worker()` (157) and `branch_review` (66). The only effect today is claude's JSON stdout (probe `session_json`, run). The path comes from the session id under Claude Code's store (`measure_read.py:101-104`, read). Read.
- r59 parallel research: `together`'s threads skip `Run.step`'s fault wrapper (`supervise.py:135-138`), so a `Fault` or `GitFailed` from a research thread escapes to `together`'s `failed` list and out of `run()`, with no `failed` move and no `## Faults` line. Read, not probed.
- `verify_push` (`supervise_faults.py:64`) runs in `worker()` for every worker: a parallel path through `worker()` keeps it. Read.

## 6. Defects

### D1. A malformed `.shop/delivery.toml` ends `work run` with a traceback and leaves a start line
Reproduction: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w109-1-research/probe_supervision.py -k malformed` (run). Repo: w1 drafted; `delivery.toml` = `[tests` plus `work_item = `.
Came back: RC 1; stderr ends `tomllib.TOMLDecodeError: Expected ']' at the end of a table declaration (at line 1, column 7)`, a traceback; no worker started; w1 still `drafted`; `log.jsonl` holds a `push verified` line and a code-scout start line with no end, uncommitted.
Spec r10: exit with an error saying why, and change nothing. Read: the next run refuses on the uncommitted `.shop/work/` (`supervise.py:check`, 72-76).

### D2. A work-item blocked by a work-item that is not green is worked on
Reproduction: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w109-1-research/probe_supervision.py -k blocked_by` (run). w1 drafted, `blocked_by: [w2]`; w2 awaiting-answer.
Came back: RC 3; w1 `green` after four workers; w2 `awaiting-answer` with its question. Spec r63: no worker for w1.
Note: the capability's `Not yet` lists "the guards between work-items", and r63 is accepted by this work-item; this is the unmet accepted requirement.

## 7. The file set

Production files the change edits (all read; counts `wc -l`):
- `scripts/supervise.py` (263, room 37): `Run.run` N-way stage pool within the workers number (r1, r59, r60, r63); `Run.pair` N-way (r20, r60); `together` merge in end order (r61); fault drain. A pool may need its own module (new concern: CLAUDE.md row).
- `scripts/supervise_worker.py` (212, room 88): `Workers.delivery` reads the workers number (r60; name unnamed in spec: w101 plan proposed top-level `workers`); `worker` writes the transcript path into `session.json` (r62, line 157); blocked_by guard before `session` (r63, line 144 area). D1 if the plan takes it: the parse before `log` (line 144-151).
- `scripts/supervise_review.py` (77, room 223): `session.json` at line 66 if Q2 says the branch review counts.
- `scripts/supervise_merge.py` (132, room 168): merge order by end (r61, `claimed` 102-111); a lock hold change.
- `scripts/supervise_faults.py` (160, room 140): `fail`, `push`, `verify_push`: read; change only if the research thread needs a wrapper beside `fault_of`.

Test and support files:
- `tests/scenarios/supervision_given.py` (247, room 53): comma in the items regex (line 54, r60); `blocked_by` Given (r63); workers-number Given (r20, r60); end-order and cross-agent meet Givens (r59, r61).
- `tests/scenarios/supervision_then_workers.py` (285, room 15): too full: put the new Thens (r59 span, r20 own worktree, r62 path, r60 cap) in a new module, e.g. `tests/scenarios/supervision_parallel_steps.py` (CLAUDE.md row). `one_at_a_time` (30) and `two_at_most` (257) conflict with retired scenarios (part 4).
- `tests/scenarios/supervision_world.py` (172, room 128): `item_text` takes `blocked_by` (r63).
- `tests/scripts/stub_claude.py` (206, room 94): `meet` counts across agents (r59, r60); an end-order control (r61); transcript path in its output (r62), not read.
- `tests/scenarios/test_supervision.py` (247, room 53): imports of the new step module only.
- `features/supervision.feature`: the retired scenarios (feature 8, 395-404, 429-437) by the Retires section.
- `CLAUDE.md` (30): module map row, if a new module is added.

Modules on the change's path, not edited:
- `scripts/work` (80, room 220): the entry point.
- `scripts/workqueue.py` (262, room 38): `move`, `agrees`, `items`; room small.
- `scripts/supervise_brief.py` (110, room 190): briefs; no change expected.
- `scripts/measure_read.py` (137, room 163): reads `session.json` and transcripts by session id (r62 consumer); not changed by w109.
- `tests/scenarios/supervision_faults_steps.py`, `supervision_review_steps.py`: not counted (read by grep only).
