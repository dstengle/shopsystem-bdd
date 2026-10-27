# Research of w208: work-queue r34-r39 (list, show)

Base b4c4ad5e. Tools: `tools refs` and `tools tests-of`/`untested` (no map: `tools map` not run, per brief); counts below by search where noted. Probes in `.shop/scratch/w208-1-research/` (ignored by git; `git status --porcelain` clean).

## 1. Why each scenario is red today

None is red. All six accepted scenarios (seven test cases: the Outline has two examples) pass at base.

- Command: `python3 -m pytest -q -n 0 -p no:cacheprovider` with the seven node ids of `tests/scenarios/test_work_queue.py` (`test_list_prints_each_...`, `test_list_with_json_...`, `test_list_prints_an_initiative_as_waiting_...`, `test_show_of_an_initiative_...`, `test_show_of_a_workitem_...`, `test_show_of_target_with_json_...[i1-...]`, `[w1-...]`). Result: `7 passed`. run
- Command: `python3 -m pytest -q -n 0 -p work_items --work-item w208 tests/scenarios/test_work_queue.py`. Result: `7 passed, 67 deselected`. run
- Step definitions exist for every Given, When and Then: `tests/scenarios/work_queue_list_steps.py:10-80`, `work_queue_status_steps.py:14-31,42-56,91-131`, `test_work_queue.py:71-74,178-181,220-227`. read
- Code behind them: `scripts/work:31-32` (`cmd_list`), `:35-37` (`cmd_show` dispatch to `workqueue_list.show`); `scripts/workqueue_list.py:40-57` (`listing`), `:25-37` (`waiting`, reads `raised.jsonl`, last line per request wins), `:60-76` (`work_item`), `:79-84` (`show`); `scripts/workqueue_status.py:145-170` (`status`, `read`, `render`) reached by `show` of an initiative. read, and run by the passing tests.

## 2. What the system answers today

Probe commands (each run; output trimmed):
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w208-1-research/probe_list_show.py`
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w208-1-research/probe_more.py`
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w208-1-research/probe_hook.py`

Scenario data, today's code (run):
- r34 data, `work list`: `initiative i1 started`, `initiative i2 done`, `initiative i3 abandoned`, `request q1 awaiting-upstream`, `work-item i1/w1 drafted`, `i1/w2 ready`, `i2/w3 green`, `i3/w4 withdrawn`; rc 0. `list --json`: one object, `initiatives`/`requests`/`work-items` each with status; rc 0.
- r35 data, `work list --json`: `{"initiatives": [i1 started, i2 done], "requests": [{"request": "q1", "status": "accepted"}], "work-items": [w1 drafted, w2 green]}`; rc 0.
- r39 data, `work list`: `initiative i1 started`, `initiative i1 waiting on q1 (in ctx-up, accepted)`, `work-item i1/w1 green`; rc 0. The JSON output has no waiting entry (see part 5).
- r36 data, `work show i1` (git repo, branch `i1-delivery` one commit ahead of its remote, `spec/index.md` modified, `notes.txt` untracked, `scratch.log` ignored): `initiative i1 started`, `capability-proposal p1 approved`, `work-item w1 ready`, `work-item w2 awaiting-answer` + `  question: Which reading of r3?`, `branch i1-delivery: the remote does not have every commit of it`, `uncommitted:` `spec/index.md`, `untracked:` `notes.txt` (scratch.log absent), `ledger:` with the last ten lines, `last next: - 2026-10-11: next: answer w2`; rc 0. `show i1 --json`: one object with the same content; rc 0. run
- r37 data, `work show w2`: `work-item i1/w2 awaiting-answer`, `  question: Which reading of r3?`; rc 0. `show w2 --json`: `{"work-item": "w2", "initiative": "i1", "status": "awaiting-answer", "questions": ["Which reading of r3?"]}`; rc 0. run

Nearest cases the scenarios do not give (run unless marked read):
- Queue empty (no `.shop/work/`): `work list` prints nothing, rc 0; `work list --json` gives three empty lists, rc 0; `work show i9` rc 1, `there is no work-item i9 under .shop/work`.
- r39, last record per request wins: `accepted` then `delivered` gives no waiting line; `delivered` then `accepted` gives the waiting line; two requests, one delivered, names only the other. run
- r39, initiative done while its raised request is `accepted`: `initiative i1 done` and `initiative i1 waiting on q1`, rc 0. Whether a done initiative may still wait is a reading question (r23 says done needs the requests it raised delivered only where the asker is this context, so a raised request does not block `done`). run
- r36, no ledger: `ledger:` empty, `last next: none`. run
- r36, ledger with `- 2026-10-02: next:  w1 ready` and an undated `- next: no date here`: `last next:` takes the dated line, the undated one is not counted; the printed `last next:` line keeps the bullet and date. run
- r36, branch pushed: `branch i1-delivery: the remote has every commit of it`. run
- r36 with no repository: NOT clean. The case directory sits inside the checkout's own (detached) repository, so `branch None: the remote cannot be compared with it`, `uncommitted: none`, `untracked: none` reflect that repository, not a bare directory. A true no-repository case was not run. run, with that caveat
- r37, a work-item whose `## Questions` lists two and `## Answers` one: open question is the second (`work show w1` prints `  question: Q two?`). run
- Work-item with no `status` line: `work list` prints `work-item i1/w4 None`; `work show w4` prints `work-item i1/w4 None`; `show i1 --json` gives `"status": null`. run
- Request with no `status` line: `work list` prints `request q2 None`; JSON `"status": null`. run
- Initiative directory with `w8.md` and no `initiative.md`: `work list` prints `work-item i8/w8 ready`; `work show i8` rc 1 `there is no work-item i8 under .shop/work`; `work show w8` prints `work-item i8/w8 ready`. run
- `work show p1` (capability-proposal): rc 1, `p1 is a capability-proposal, not a work-item or an initiative that work show shows`. `work show q7` (request): rc 1, the same form. `work show ../x`: rc 1, `the target ../x is not a name`. `work show w9`: rc 1, `there is no work-item w9 under .shop/work`. run
- `work show i1` with an undecodable ledger: rc 1, `.shop/work/i1/ledger.md is not UTF-8 text` (refused, no traceback). run
- The no-target `work show` (`scripts/work:38-48`, printing each work-item and request with status) was run only on an empty queue (no output). The code path is read.

SessionStart hook (`migrate status --hook`, `scripts/migrate` run from the case directory):
- Good ledger: rc 0, stdout the plugin-version upgrade text (no `.shop/plugin-version` in the case). run
- Undecodable ledger `b"- 2026-01-01: \xff\xfe\n"`: rc 1, stdout empty, stderr ends `workqueue.Refused: .shop/work/i1/ledger.md is not UTF-8 text` with a `Traceback`. run (see defect D2)

## 3. Old assumptions

`work status` is retired by work-queue r16-r18 (in the spec's retired list) and by design-decision 0072, whose "replaced by work list / work show" the accepted lines carry. Its code and its readers are still in place. Table rows are the places that still make the old form's assumption. Search: `tools refs workqueue_status` (module), `tools refs workqueue_status.ledger` (1 ref, `workqueue_status.py:88`), `tools refs workqueue_status.render` (1 ref, `:167`), `tools refs workqueue_list.waiting` (1 ref, `workqueue_list.py:51`); `tools refs` could not resolve `workqueue_status.status`, `workqueue_status.read` or `workqueue_list.listing` as dotted names (the count is by search), and `open_text`/`show` have 0 references; plus text search (`Grep` for `work status|workqueue_status|open_text|open_names|cmd_status`).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/work:66-67` `cmd_status`, `:140-141` argparse `status`, `:172` dispatch | `work status [initiative] [--json]` prints the text or JSON of `workqueue_status.status` | retired by work-queue r16-r18 and decision 0072; `work show <initiative>` (r36) replaces it, so the command is a leftover to retire or keep | `tests/scenarios/test_work_queue.py::test_status_of_an_initiative_..._deprecated`, `..._status_with_no_initiative_..._deprecated`, `..._status_with_json_..._deprecated` (pass with `--whole-suite`); `work_queue_status_steps.py` (its r16-r18 steps). by search | `Grep` for `cmd_status`, `status` in `scripts/work` |
| `scripts/workqueue_status.py:145-170` `status` | the text and JSON of `work status`; for an initiative it is also what `work show <initiative>` prints | r36 keeps its text under the new name; the no-initiative branch (`:158-159`) is the old form only | reached by the r36 and r38 tests (run, pass); `test_status_..._deprecated` (run, pass). by search | `workqueue_list.py:83` call; `tools refs` could not resolve the name |
| `scripts/workqueue_status.py:112-126` `uncited`, `:160-167` the observations lines and JSON key | `work status` with no initiative prints each observation no initiative or request names | not a work-queue line; requests r14 (`spec/capabilities/requests.md:56`) still names `work status` for it. If `work status` is retired, requests r14 is affected too (ledger: requests r13 and r14 are removed in integrate round 5) | `tests/scenarios/test_requests.py::test_status_with_no_initiative_prints_with_its_date_each_observation...` (run, pass, `--whole-suite`); `requests_show_steps.py:49` | `Grep` for `uncited`, `observation` |
| `scripts/migrate_session.py:23-25` `work_text`, `:20,30` `open_names` | SessionStart text = `work status` text for each open initiative | migration-tools r32 (`spec/capabilities/migration-tools.md:54`) still says "what `work status` prints". It conflicts with the retirement of `work status`: no line of w208 settles it (the ledger leaves it as a question); both readings in part 6 | `test_migration_tools.py::test_a_session_starting_in_a_repository_with_initiatives_neither_done_nor_abandoned_is_given_what_work_status_prints_for_each_of_them` (run, pass, `--whole-suite`); `migration_session_steps.py:85-88` (runs `work status` by subprocess) | `Grep` for `work_text`, `open_text` |
| `scripts/migrate_upgrade.py:168-170` `run` (hook branch) | calls `work_text(root)` with no `try` | not in w208's accepts; hook must exit 0 (`scripts/migrate_session.py:5`); see D2 | the good-ledger hook test above (run, pass). none for an undecodable ledger | `Read`; probe_hook.py (run) |
| `scripts/migrate:53` | catches only `Failed` around the hook path; `migrate_session.py:50-53` catches `Refused` only in `compacting` | same as above | none (no test gives an undecodable ledger to the hook) | `Read`; probe_hook.py (run) |
| `scripts/supervise_all.py:30,36` `open_names` | `work run` with no initiative takes each open initiative | none: w208 does not change it; it reads the `work status` module | by search: `supervision_all_steps.py` (its tests pass at base, not run here) | `Grep` for `open_names` |
| `scripts/workqueue_list.py:3` docstring, `scripts/workqueue_status.py:1` docstring | say `work status` | wording: r36 replaces it | none | `Grep` for `work status` |
| `CLAUDE.md:18,23` module map rows | `scripts/workqueue_status.py` row reads `work status`; `migrate_session.py` row reads `work status` at SessionStart | the module map names the retired command; the row's text changes when the module's concern does | none | `Read` of CLAUDE.md |
| `README.md:178-180`, `scripts/migrate:64` help text | document `work status` | docs, not a requirement; retirement changes them | none | `Grep` for `work status` |
| `scripts/work:35-48` no-target `show` | prints each work-item and request with status (old `show` form) | work-queue r3 and r11 (retired) asked for it; r36 names `work show <initiative>`. The code path is left with no line | `test_show_prints_each_workitem_of_every_initiative_..._deprecated` and `test_show_with_json_..._deprecated` (run, pass, `--whole-suite`) | `Read` of `scripts/work`; `tools refs` could not resolve the name |

## 4. Tests the requirements make impossible to keep

`tools tests-of` could not be used: no map (`tools tests-of` answers `tools: no map: make one with tools map`; I did not make one). Searched by text (`by search`).

- Tests of the accepted requirements' functions (`workqueue_list.py` and the r34-r39 steps): the seven accepted tests pass; `tests/scripts/test_workqueue_list.py` (four tests: JSON of list, undecodable ledger refused at `show i1`, no-kind refused at `show w1`, malformed `raised.jsonl` refused) passes (run, 4 passed). Found sound: none can no longer pass.
- Tests asserting the old `work status` form (rows 1-4 of part 3): the three deprecated `test_status_*` tests, `test_status_with_no_initiative_...` in test_requests, `test_a_session_starting_..._what_work_status_prints_...` in test_migration_tools, and `test_show_prints_each_workitem...` / `test_show_with_json_...` (the no-target show). All run and pass today (run, `--whole-suite`). They stop passing only if the plan removes `work status` or the no-target `show`: then they must be deleted or re-pointed, and the plan decides which (part 6 gives both readings for migration-tools r32).
- Found sound: the rest of `tests/scripts/` that calls `work` (not searched in full).

## 5. A step the work-item skips

- `work list --json` skips `waiting()` (`scripts/workqueue_list.py:25-37`), which the text `list` runs. Probe: r39 data, `work list --json` gives `"initiatives": [{"initiative": "i1", "status": "started"}]` with no waiting entry, while `work list` prints `initiative i1 waiting on q1 (in ctx-up, accepted)`. run. Reading A: r35 "nothing besides" the initiatives, requests and work-items keeps the JSON as it is. Reading B: r39 is "print", and the JSON should carry the waiting request as a field. The work-item does not pick one; both are open for the plan.
- `work show <initiative>` and `work show <work-item>` are read-only; nothing is written, so no transition or commit is skipped. read.
- `work show <work-item>` (`work_item`) skips the git and checkout reads of `status()` (branch, uncommitted, untracked). r37 does not ask for them, so the skip is right. read.
- `work show <target>` checks the name with `workqueue.entry` (`workqueue_list.py:81`) before choosing initiative or work-item: a `..` name is refused. run (`work show ../x`).

## 6. Defects

Each is a probe's output as run above. None is fixed here.

### D1. A work-item or request with no `status` line is printed as `None`, rc 0

- Reproduction: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w208-1-research/probe_list_show.py` (test `test_nearest_work_item_cases`, and `test_r35_list_json_data`).
- Came back: `work-item i1/w4 None` from `work list` and `work show w4` (rc 0); `request q2 None` from `work list`, `"status": null` in JSON.
- Why it may be wrong: r34 and r35 say "with its status"; a missing status is printed as the word `None`, not refused, unlike r7 cases elsewhere. Not covered by any scenario. Reading the plan may choose: refuse (r7) or print a stated value.

### D2. The SessionStart hook exits 1 with a traceback on an undecodable ledger

- Reproduction: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w208-1-research/probe_hook.py`. Command behind it: `python3 <worktree>/scripts/migrate status --hook` in a git repository with `.shop/work/i1/initiative.md` (status `started`) and `ledger.md` = `b"- 2026-01-01: \xff\xfe\n"`.
- Came back: rc 1, stdout empty, stderr `workqueue.Refused: .shop/work/i1/ledger.md is not UTF-8 text` and `Traceback`. The good-ledger control gives rc 0.
- Why it matters: `scripts/migrate_session.py:5` says a hook exits 0. `migrate_upgrade.py:168-170` has no `try`, and `scripts/migrate:53` catches only `Failed`. The same file given to `work show i1` is refused cleanly (rc 1, names the ledger). This is review 4's finding 2 (the reviewer could not run it).

### D3. `work show <initiative>` refuses a directory with work-items and no `initiative.md`, with the wrong noun

- Reproduction: probe_list_show.py, `test_initiative_without_initiative_file`.
- Came back: `work list` prints `work-item i8/w8 ready`; `work show i8` rc 1 `there is no work-item i8 under .shop/work`; `work show w8` prints `work-item i8/w8 ready`.
- Why it may be wrong: the message names a work-item for `i8`, which `list` shows as an initiative's work-item. Minor.

### Not defects, for the plan (reading questions)

- A done initiative still prints `waiting on q1` (part 2).
- `list --json` has no waiting entry (part 5).
- migration-tools r32 still names `work status` (part 3).
- The `last next:` line prints the whole dated bullet, not only the note (part 2).

## 7. The file set

Accepted scenarios: no production or test file must change for them to pass, and nothing that passes today must change to keep passing (the scenarios, the unit tests and the old-form tests all pass at base). Fileset: none for the accepts.

Only if the plan takes review 4's findings in this work-item (not accepted by r34-r39):
- `scripts/migrate_upgrade.py:168-170`: catch `workqueue.Refused` around `work_text` on the hook path (D2). Read and probe_hook.py. Test: `tests/scripts/` or `tests/scenarios/migration_session_steps.py` with an undecodable ledger, asserting rc 0 and no Traceback.
- `scripts/workqueue_list.py:21,25-37,40-57` and `scripts/workqueue_status.py:77-79,137-138` if D1/D3 are taken. Read and probe.
- Review 4's findings 1, 3, 4 and 5 (merge in `scripts/supervise_change.py:79-89,108-111`, `supervise_rounds.py:195`) need a line of q20 first (findings file); no code line yet.

Modules on the change path, with lines and room under the 300-line limit (`tools size --limit 300` printed nothing, rc 0; `wc -l`):

| module | lines | room |
|---|---|---|
| `scripts/work` | 181 | 119 |
| `scripts/workqueue.py` | 294 | 6 |
| `scripts/workqueue_list.py` | 84 | 216 |
| `scripts/workqueue_status.py` | 170 | 130 |
| `scripts/migrate_session.py` | 54 | 246 |
| `scripts/migrate_upgrade.py` | 171 | 129 |
| `scripts/migrate` | 76 | 224 |
| `scripts/supervise_all.py` | 83 | 217 |
| `tests/scripts/test_workqueue_list.py` | 55 | 245 |
| `tests/scenarios/test_work_queue.py` | 283 | 17 |
| `tests/scenarios/work_queue_list_steps.py` | 80 | 220 |
| `tests/scenarios/work_queue_status_steps.py` | 160 | 140 |
| `tests/scenarios/requests_show_steps.py` | 72 | 228 |
| `tests/scenarios/migration_session_steps.py` | 97 | 203 |

Searches behind the list: the work-queue step modules and `tests/scripts/test_workqueue_list.py` from the feature's binding (`Grep` for `work_queue`); `Grep` for `workqueue_status|open_names|open_text|work_text` in `scripts/` and `tests/`.
