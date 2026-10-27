# Research of w208 (2-research): work-queue r34-r39 (list, show)

Base b4c4ad5e. Accepts: work-queue#r34-r39 (r34, r35, r36, r37, r38, r39). Prior stage (`1-research`) read; its probes not re-run except where marked. Probes: `.shop/scratch/w208-2-research/` (ignored; `git status --porcelain` clean at the end).
Tools: `tools refs` ran (counts below say `refs`); `tools tests-of` answered `tools: no map: make one with tools map` (not made) so test lists are `by search`; `tools size --limit 300` printed nothing.

## 1. Why each scenario is red today

None is red. All six accepted scenarios (seven cases: r38 is an Outline with two examples) pass at base.
- Command: `python3 -m pytest -q -n 0 -p no:cacheprovider -p work_items --work-item w208 tests/scenarios/test_work_queue.py`. Result: `7 passed, 67 deselected`. run
- Steps: `tests/scenarios/work_queue_list_steps.py:10-22` (requests, raised record), `:37-47` (`work prints ... with`, `... as waiting on`), `:60-67` (`it gives ... with`); `work_queue_status_steps.py:75-79` (twelve-line ledger), `:91-131` (show of i1, ledger, last next); `work_queue_withdraw_steps.py:39-43` (`one JSON object and nothing else`, `json.loads` of the whole stdout). read
- Code behind them: `scripts/work:31-32` (`cmd_list` to `workqueue_list.listing`), `:35-37` (`cmd_show` to `workqueue_list.show`); `scripts/workqueue_list.py:25-37` `waiting`, `:40-57` `listing`, `:60-76` `work_item`, `:79-84` `show`; `scripts/workqueue_status.py:145-170` `status` (reached from `workqueue_list.py:83`), `:96-109` `render`, `:84-93` `read`. read; run by the passing tests.
- `tools refs` does not see the calls from `scripts/work` (`listing`, `show`: 0 refs) nor the call at `workqueue_list.py:83` (`status`: 1 ref, `workqueue_status.py:141`, which is `open_text`). Found by search (Grep of `workqueue_list\.|workqueue_status\.`).

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w208-2-research/probe_list_show.py` → `5 passed`. run. Each case in its own directory under the scratch dir; the r36 case is its own git repo with a bare remote there.

Scenario data:
- r34 (`work list`): rc 0; `initiative i1 started`, `initiative i2 done`, `initiative i3 abandoned`, `request q1 awaiting-upstream`, `work-item i1/w1 drafted`, `i1/w2 ready`, `i2/w3 green`, `i3/w4 withdrawn`. run
- r35 (`work list --json`): rc 0; one object `{"initiatives":[i1 started, i2 done],"requests":[{"request":"q1","status":"accepted"}],"work-items":[w1 drafted, w2 green]}`. run
- r39 (`work list`): rc 0; `initiative i1 started`, `initiative i1 waiting on q1 (in ctx-up, accepted)`, `work-item i1/w1 green`. `list --json`: rc 0, no waiting entry (`"initiatives": [{"initiative": "i1", "status": "started"}]`). run
- r36 (`work show i1`, own repo, branch `i1-delivery` with one local commit the bare remote lacks, `spec/index.md` edited, `notes.txt` untracked, `scratch.log` ignored, ledger of 12 lines written by `work note`): rc 0; `initiative i1 started`, `capability-proposal p1 approved`, `work-item w1 ready`, `work-item w2 awaiting-answer` + `  question: Which reading of r3?`, `branch i1-delivery: the remote does not have every commit of it`, `uncommitted:` `  spec/index.md`, `untracked:` `  notes.txt` (no scratch.log), `ledger:` the last ten lines, `last next: - 2026-10-27: next: answer w2`. run
- r36 `--json`: one object, `initiatives[0]` with `proposals`, `work-items` (with `questions`), `branch {"name":"i1-delivery","pushed":false}`, `uncommitted`, `untracked`, `ledger` (10), `next`. run
- r37 / r38 (`work show w2` and `--json`): `work-item i1/w2 awaiting-answer`, `  question: Which reading of r3?`; JSON `{"work-item": "w2", "initiative": "i1", "status": "awaiting-answer", "questions": ["Which reading of r3?"]}`. run

Nearest cases (all run unless marked read):
- Empty queue: `list` prints nothing, rc 0; `list --json` gives three empty lists, rc 0; `show i9` rc 1 `there is no work-item i9 under .shop/work`.
- r39 last record per request wins: accepted then delivered → no waiting line; delivered then accepted → waiting line; q1 delivered and q2 accepted → waiting on q2 only; `raised.jsonl` says accepted but `requests/q1.md` says delivered → still `waiting on q1` and `request q1 delivered` both printed (the upstream is never read; the context's own request file is not consulted); no `raised.jsonl` → no waiting line. run
- r39 initiative done with raised request accepted: `initiative i1 done` then `initiative i1 waiting on q1 (in ctx-up, accepted)`, rc 0. run
- r39 malformed record: see D4. run
- r37 with two questions and one answer (`w3`): `question: Q two?` (the open one). run
- Work-item with no `status` line, request with no status: see D1. run
- `show w4` / `show i8` / `show w8`: see D3 (run).
- `show p1` (capability-proposal) and `show q7` (request): rc 1, `p1 is a capability-proposal, not a work-item or an initiative that work show shows` (same form for q7). `show ../x`: rc 1 `the target ../x is not a name`. `show w9`: rc 1 `there is no work-item w9 under .shop/work`. run
- r36 with no ledger: `ledger:` empty, `last next: none` (prior stage, run; not re-run).
- r36 `show` of an initiative whose directory is not its own repository: reads the enclosing checkout (`workqueue_status.py:51-74`, `git(root, ...)` in `root`). The case's `branch` was `null` because the enclosing worktree is detached. read; run only as the detached-case reading in `show i1 --json` of the `kinds` case.

## 3. Old assumptions

The accepts replace nothing directly: `work list` and `work show <id>` are the new forms of `work status` (retired by spec work-queue r16-r18, design-decision 0072) and of the no-target `work show` (r3, r11, retired); r39 takes over the job of r33 (retired; ledger 2026-10-27). The old readers below still make the old assumption.

Searches: `tools refs workqueue_status.status` (1 ref, `:141`), `tools refs workqueue_status.read` (1 ref, `:157`), `tools refs workqueue_list.waiting` (1 ref, `workqueue_list.py:51`); the prior stage's `tools refs workqueue_status.ledger` (1 ref, `:88`); `Grep` for `cmd_status|open_text|open_names|work_text|workqueue_status\.|workqueue_list\.|work status|uncited` in `scripts/`, `tests/`, `spec/`, `CLAUDE.md`.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/work:66-67` `cmd_status`, `:140-141` argparse `status`, `:172` dispatch | `work status [initiative] [--json]` prints `workqueue_status.status` | retired by work-queue r16-r18 and decision 0072; `work show <initiative>` (r36) replaces its initiative case; the command is a leftover to retire or keep | deprecated `status` scenarios of `tests/scenarios/test_work_queue.py` (pass with `--whole-suite`, w208-1 run; not re-run here) | Grep `cmd_status` |
| `scripts/workqueue_status.py:145-170` `status` | text/JSON of `work status`; for an initiative also what `work show <initiative>` prints (`workqueue_list.py:83`) | r36 keeps its initiative text; the no-initiative branch (`:158-159`) is the old form only | r36 and r38 accepted cases (run, pass); deprecated status scenarios (w208-1 run, pass). by search | `Grep workqueue_status\.`; refs gives 1 ref only |
| `scripts/workqueue_status.py:112-126` `uncited`, `:160-167` observation lines and JSON key | `work status` with no initiative prints observations no initiative or request names | not a work-queue line; requests r14 (`spec/capabilities/requests.md:56`) still names `work status` | `tests/scenarios/test_requests.py` deprecated status scenario (w208-1 run, pass); `requests_show_steps.py:49` | Grep `uncited` |
| `scripts/workqueue_status.py:129-143` `open_names`, `open_text` | names of open initiatives; `work status` text for them | unchanged by the accepts; the plan decides whether `open_text` keeps its name | SessionStart test in `test_migration_tools` (w208-1 run, pass); `supervise_all` tests by search, not run here | Grep `open_text|open_names` |
| `scripts/migrate_session.py:20,23-25,30` `open_names`, `work_text`, `open_text` | SessionStart text = `work status` text for each open initiative | migration-tools r32 (`spec/capabilities/migration-tools.md:54`) still says "what `work status` prints": a conflict with the retirement; no accepted line settles it (both readings in part 6) | `test_migration_tools.py` SessionStart test (w208-1 run, pass); `migration_session_steps.py:85-88` | Grep `work_text` |
| `scripts/migrate_upgrade.py:168-170` (`:169` calls `work_text`) | hook branch with no `try` | not an accepted line; the hook must exit 0 (D2) | none for an undecodable ledger | read; D2 (prior run) |
| `scripts/supervise_all.py:30,36` `open_names` | `work run` with no initiative takes each open initiative | none: the accepts do not change it | by search: `supervision_all_steps.py` (not run here) | Grep `open_names` |
| `scripts/workqueue_list.py:3`, `scripts/workqueue_status.py:1` docstrings | say `work status` | wording | none | Grep `work status` |
| `scripts/workqueue_list.py:21` (`workqueue_status.natural`), `:83` (`workqueue_status.status`) | `list` and `show` depend on the module of the retired command | if `work status` goes, `workqueue_status.py` stays (show uses it) | r36, r38, r35 accepted cases (run, pass) | Grep `workqueue_status\.` |
| `scripts/work:35-48` no-target `show` | prints each work-item and request with status (old r3, r11 form) | no accepted line; r36 names `work show <initiative>`; the path has no spec line now | deprecated no-target `show` scenarios (w208-1 run with `--whole-suite`, pass) | read; refs does not resolve it |
| `CLAUDE.md` module map rows for `scripts/workqueue_status.py` and `scripts/migrate_session.py` | name `work status` | the row text changes if the concern changes | none | Read |
| `README.md:178-180`, `scripts/migrate` help text | document `work status` | docs | none | Grep (prior stage) |

## 4. Tests the requirements make impossible to keep

`tools tests-of`: no map, so by search.
- The six accepted scenarios (seven cases): pass today (run). Under either reading of r35 and r39 (JSON with or without waiting), they still pass: `gives_pairs` (`work_queue_list_steps.py:60-67`) checks membership only, and `one_json_object` (`work_queue_withdraw_steps.py:39-43`) accepts an added key. Found sound.
- `tests/scripts/test_workqueue_list.py`: four tests (`test_list_json_gives_each_request_and_its_status_and_nothing_besides`, `test_show_of_an_initiative_whose_ledger_is_not_utf8_is_refused_naming_the_ledger`, `test_show_of_a_work_item_file_with_no_kind_is_refused_saying_it_has_no_kind`, `test_a_raised_record_line_that_cannot_be_read_is_refused_naming_the_file_and_line`). Run: `4 passed`. Under reading B of r39 (waiting in JSON) the first still passes (it checks requests only). Found sound.
- Old-form tests (deprecated `status` scenarios, `test_requests` observations scenario, `test_migration_tools` SessionStart scenario, deprecated no-target `show` scenarios): pass today (w208-1 run). They assert the old form and would stop passing only if the plan removes `work status`, `open_text` or the no-target `show`. Not impossible under the accepts. Not run here. by search.
- None found impossible under the accepts.

## 5. A step the work-item skips

- `work list --json` skips `waiting()` (`workqueue_list.py:51` runs only in the text branch, `:40-48` returns before it). run (r39 data). Reading A: r35 "nothing besides" keeps the JSON as it is. Reading B: r39 "print" also in JSON, needing a field. Both open for the plan.
- Nothing writes `.shop/work/<initiative>/raised.jsonl`. The reader is `workqueue_list.py:25-37`; `Grep -i raised` in `scripts/`, `spec/`, `features/`, `CLAUDE.md` finds no writer (only the reader, its docstring, and the test writers `tests/scenarios/work_queue_list_steps.py:21`, `tests/scripts/test_workqueue_list.py:17`). read. Review 4's coupling note says the same and names the candidate writers: requests r29 and supervision r135 (both xfail, read). So in real use `waiting` never prints. Both readings for the plan: (a) the writer is a line of requests or supervision, outside these accepts; (b) the record is written by work-queue, which needs a line of its own. I do not choose.
- `work show <initiative>` reads git of the checkout (`branch`, `changes`) where r36 asks for it; `work show <work-item>` (`work_item`, `:60-76`) reads no git, and r37 does not ask for it. read.
- `work list` and `work show` are read-only: no transition, no commit, no log line is skipped. read.

## 6. Defects

Each is a probe's output as run in this stage unless marked.

### D1. A work-item or request with no `status` line is printed as `None`, rc 0
- Reproduction: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w208-2-research/probe_list_show.py` (test `test_nearest_list_and_show_cases`, dir `nostatus`).
- Came back: `work-item i1/w4 None` (`list`, `show w4`), `request q2 None`, JSON `"status": null`, rc 0.
- Source: `workqueue_list.py:68` (`data.get("status")`), `workqueue.py:117-124` (`requests`), `workqueue.py:109-114` (`items`), `workqueue_list.py:55-56`, `:53-54`. read.
- Not covered by any scenario. r7 refuses other unperformable asks; no line says what a missing status prints.

### D2. The SessionStart hook exits 1 with a traceback on an undecodable ledger
- Reproduction (prior stage, run in `w208-1-research` `probe_hook.py`; NOT re-run here): `python3 <worktree>/scripts/migrate status --hook` in a repository with `.shop/work/i1/initiative.md` (status `started`) and `ledger.md` = `b"- 2026-01-01: \xff\xfe\n"`. Came back: rc 1, stdout empty, stderr ends `workqueue.Refused: .shop/work/i1/ledger.md is not UTF-8 text` with `Traceback`.
- Path (read): `scripts/migrate_upgrade.py:168-170` no `try`; `scripts/migrate:53` catches `Failed` only; `scripts/migrate_session.py:50-53` catches `Refused` only in `compacting`. Review 4 finding 2 says the same (read).
- The same ledger given to `work show i1` is refused cleanly (`test_show_of_an_initiative_whose_ledger_is_not_utf8_is_refused_naming_the_ledger`, run, pass).

### D3. `work show <initiative>` on a directory with work-items and no `initiative.md` says "no work-item"
- Reproduction: probe `test_nearest_list_and_show_cases`, dir `noinit`.
- Came back: `work list` → `work-item i8/w8 ready`; `work show i8` → rc 1 `there is no work-item i8 under .shop/work`; `work show w8` → `work-item i8/w8 ready`.
- Source: `workqueue_list.py:82-84` (initiative test is the file `initiative.md`; else `work_item`), `workqueue.py:226-231` (`find`).

### D4. `work list` prints part of its output, then refuses, when one raised record is malformed; `list --json` ignores the same record
- Reproduction: probe `test_r39_malformed_record_partial_output`: i1 with `raised.jsonl` = a good line then `not json`; i2 started after it.
- Came back: `work list` → rc 1, stdout `initiative i1 started` only (no line for i2 or the work-items); stderr `work: .../i1/raised.jsonl line 2 is not a record of a raised request (upstream, request, status)`. `work list --json` → rc 0, all initiatives, no error.
- Source: `workqueue_list.py:40-57` prints per initiative and calls `waiting()` inside the loop (`:51`); `waiting()` raises at `:36`. read.

### Reading questions (not defects)
- A done initiative still prints `waiting on q1` (r39 vs r23; part 2).
- `list --json` has no waiting entry (part 5).
- migration-tools r32 still names `work status` (part 3).
- `last next:` prints the dated bullet, not only the note (part 2).
- `requests/q1.md` (delivered) and `raised.jsonl` (accepted) disagree and both print (part 2).

## 7. The file set

Accepts: no production or test file must change for the six scenarios to pass, and nothing that passes today must change (all pass at base: run). Fileset given in the result: none.

Review 4 (`.shop/work/i39/runs/branch-review/4/findings.md`, read) triages one finding fix-now (finding 1: a redraft round merges ids into another held proposal, `scripts/supervise_change.py:79-89,108-111`, called from `scripts/supervise_rounds.py:195`). Its only line is q20 line 3, still open, so it needs a request line first, not code. Findings 2-5 are observations, finding 6 drop. Optional code if the plan takes the observations (not required by the accepts):
- `scripts/migrate_upgrade.py`: catch `workqueue.Refused` around `work_text` on the hook path (D2). Test: a migration session or tests/scripts case with an undecodable ledger, exit 0, no Traceback.
- `scripts/workqueue_list.py`: D3 noun at `:82-84`; D4 partial output at `:40-57` (and `waiting` on JSON, per reading B).
- `scripts/workqueue.py`: D1 `None` status at `:109-124` (or the reader at `workqueue_list.py:68`).
- A writer of `raised.jsonl`: none named in any line yet (part 5).

Modules on the change path, edited or not (`wc -l`; room = 300 minus lines; `tools size --limit 300` printed nothing, exit 0):

| module | lines | room |
|---|---|---|
| `scripts/work` | 181 | 119 |
| `scripts/workqueue.py` | 294 | 6 |
| `scripts/workqueue_list.py` | 84 | 216 |
| `scripts/workqueue_status.py` | 170 | 130 |
| `scripts/migrate_session.py` | 54 | 246 |
| `scripts/migrate_upgrade.py` | 171 | 129 |
| `scripts/migrate` | 76 | 224 |
| `scripts/supervise_change.py` | 126 | 174 |
| `scripts/supervise_rounds.py` | 229 | 71 |
| `scripts/supervise_all.py` | 83 (prior) | 217 |
| `tests/scripts/test_workqueue_list.py` | 55 | 245 |
| `tests/scenarios/test_work_queue.py` | 283 | 17 |
| `tests/scenarios/work_queue_list_steps.py` | 80 | 220 |
| `tests/scenarios/work_queue_status_steps.py` | 160 | 140 |

Searches: `Grep` for `workqueue_list|workqueue_status|raised|open_names|open_text|work_text` in `scripts/` and `tests/`; `tools size`; `wc -l`.
