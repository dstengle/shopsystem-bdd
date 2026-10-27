# w206 research notes

Tools: `tools refs` (Scripts runner copy), `tools size`. `tools tests-of` NOT used: no coverage map exists and `tools map` would write outside my scratch dir. `untested` not run. Counts are `refs`, `by search` (grep) or `read`, as marked.
Pytest runs need `-n 0` to show output; the runner's `--work-item` plugin needs `--whole-suite` to run tests outside w206's accepts.
Probe file: `.shop/scratch/w206-1-research/probe_list_show.py` (scratch, gitignored). Command: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w206-1-research/probe_list_show.py`.

## 1. Why each scenario is red today

None is red. At HEAD fb9cc6d3, `python3 -m pytest -n 0 -v -p no:cacheprovider tests/scenarios/test_work_queue.py -k "list_prints or list_with_json or show_of or waiting"` → 7 passed (run).
- list prints each initiative, request and work-item (r34): PASS.
- list --json (r35): PASS.
- list waiting on a raised request (r39): PASS. Its Given writes `raised.jsonl` itself (work_queue_list_steps.py:17-22).
- show of an initiative (r36): PASS; it renders through `workqueue_status.status`, via `workqueue_list.show`.
- show of a work-item (r37): PASS.
- show <target> --json, both examples (r38): PASS.

Code behind them: `scripts/workqueue_list.py` (listing, waiting, work_item, show; 78 lines); dispatch `scripts/work:31-37, 121-125`.

## 2. What the system answers today

Each probe runs the entry point `python3 scripts/work --root <scratch repo> ...` (all run, in `probe_list_show.py`):

- p1 empty queue: `list` exit 0, nothing printed; `list --json` → `{"initiatives": [], "requests": [], "work-items": []}`; `show i9` → "there is no work-item i9 under .shop/work", exit 1; `show ..` → "the target .. is not a name", exit 1.
- p2 missing fields: an initiative with no `status` prints `initiative i1 None`; a request with no status prints `request q2 None`; a work-item whose initiative has no initiative.md is still listed (`work-item i2/w2 green`).
- p3 raised record, last line per request wins: q1 accepted then delivered, q2 awaiting-upstream → `initiative i1 waiting on q2 (in ctx-up, awaiting-upstream)` only. Empty record → no waiting line.
- p3 malformed record: D1 and D2 below.
- p4 show w1 with Questions Q1, Q2 and one answer → `question: Q2` only (position rule, as `workqueue_status.py:47`). Empty `## Questions` → no question.
- p4 `show q1` (a request) → "q1 is a request, not a work-item or an initiative that work show shows", exit 1. `show w9` → "there is no work-item w9 under .shop/work", exit 1.
- p4 `list` with a work-item file that is not UTF-8 → "… is not UTF-8 text", exit 1, nothing printed (the whole listing is refused). Consistent with r7; not a defect.
- p5 ledger of 5 lines, two `next:` notes and one undated `next:` line → `last next: - 2026-10-03: next: second` (the undated line is ignored, the dated line printed whole). Last ten lines shown.
- p5 branch: with `i1-delivery` checked out and no remote → `branch i1-delivery: the remote cannot be compared with it`. Detached HEAD → `branch None: …`. The branch printed is the checkout's, not one named for the initiative (read: `workqueue_status.py:51-61`, `symbolic-ref HEAD`).
- p5 `show i1` and `status i1` text are identical.
- p6 `list --json` requests carry `"turn"` (`{"request": "q1", "status": "accepted", "turn": "asker"}`). r35 says "and nothing besides": reading A, the key is extra and goes; reading B, r35 asks only for name and status, so it may stay. The findings file (finding 2) takes A.
- p6 `list` text omits turn; `list --json` has no waiting key (r39 is text only: reading A, JSON needs none; reading B, JSON should carry it).
- p8 no command writes `raised.jsonl` (by search: only `scripts/workqueue_list.py` names it; read). A list with an initiative and no record prints no waiting line.
- p6 old no-target form still prints: `show` → `i1/w1 ready`, `q1 accepted asker`; `show --json` → one object with work-items and requests.
- p6 retired form still prints: `status` gives the queue's initiative text, `status i1 --json` gives the initiative object.
- p7 `migrate status --hook` (cwd = repo) prints the upgrade offer, then the `work status` text for i1 (`initiative i1 started`, `work-item w1 ready`, branch, uncommitted, untracked, ledger, last next).

Probe repositories are fresh `git init` directories under the scratch dir. The checkout was not written; `git status --porcelain` is clean at the end (the scratch dir is in `.gitignore`).

### D1 — `work list` crashes on a raised.jsonl line that is not JSON
Repro (run): probe `test_p3_raised_record_edges`, record = `not json`, then `work list`.
Came back: stdout `initiative i1 started`; stderr traceback ending `json.decoder.JSONDecodeError: Expecting value`; exit 1. Code: `scripts/workqueue_list.py:31`.
Expected under r7 (a refusal naming the file and line, no traceback): not met.

### D2 — `work list` crashes on a raised.jsonl line without `status`
Repro (run): same probe, record = `{"upstream": "ctx-up"}`, then `work list`.
Came back: stdout `initiative i1 started`; traceback `KeyError: 'status'` at `scripts/workqueue_list.py:32`; exit 1.
(The right-hand side is evaluated first, so a line without `status` fails on `status`; a line without `request` but with `status` fails on `request`. Both are the same defect.)

## 3. Old assumptions

Requirement that changes an old form: r34-r38 name list and show; decision 0072 (ledger) retires `work status` and the no-target `show`. Found by `grep` ("by search") unless marked. `refs` misses `scripts/work` (not a .py file) and reported `workqueue_status.status` as "nothing defined" (a tool miss; grep finds scripts/work:67 and workqueue_list.py:77).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work:cmd_show, no-target branch (35-48) | prints `i/w status` and `name status turn` lines, or the JSON of both | list (r34, r35) replaces it; r36-r38 name a target. requests.md r13 still asks for bare `work show` (Q-2) | test_requests.py::test_show_prints_each_request_with_its_status_and_whose_turn_it_is (run PASS); test_work_queue.py::test_show_prints_each_workitem_of_every_initiative_with_its_status_deprecated and …_with_json_…_deprecated (run PASS) | by search; findings file line 151 |
| scripts/work:cmd_status and argparse `status` (66-67, 140-142) | initiative text and JSON, or every open initiative | retired by decision 0072; replacement lines name list or show | test_work_queue.py::test_status_of_an_initiative…_deprecated, …_with_no_initiative…_deprecated, …_with_json…_deprecated (run PASS, 3) | by search |
| scripts/workqueue_status.py:status (145-170), render, read | the initiative text, used by `show <initiative>` and by the hook | show of an initiative (r36) shares it, so it stays reached; the module's concern moves to show (findings file line 145) | the show-of-initiative scenario (run PASS) and the deprecated status tests above | by search (refs: 0, a tool miss) |
| scripts/workqueue_status.py:open_text, open_names (129-142) | the text the SessionStart hook gives | the hook text is "what work status prints" (migration-tools r32); retirement changes it. The ledger leaves r32 as a question (Q-3) | tests/scenarios/test_migration_tools.py: 9 session tests, incl. …_is_given_what_work_status_prints_for_each_of_them (run PASS, all 9) | by search |
| scripts/migrate_session.py:work_text (23-25) | calls open_text when an initiative is open | as the row above | the same 9 session tests (run) | by search |
| scripts/migrate:64 help text; scripts/migrate_session.py docstring line 3 | name `work status` | text only | none (text) | by search |
| scripts/workqueue_status.py:uncited (112-126) | `work status` with no initiative prints observations no source names | retired with status; requests r14 names it (Q-2) | test_requests.py::test_status_with_no_initiative_prints_with_its_date… (run PASS) | by search |
| scripts/workqueue.py:items (109-114) | each work-item of every initiative | list (r34) uses it; the old show branch uses it; supervise.py:72 and supervise_pool.py:63 use it | not counted (no coverage map) | refs (2 production refs) |
| scripts/workqueue.py:requests (117-124) | each request with turn and source | list (r34) uses it; the old show branch uses it | not counted (no map) | by search |
| scripts/workqueue_list.py:listing, request objects with "turn" (41-42, 50) | list --json gives turn | finding 2: drop turn (Q-4); r35 "nothing besides" | test_work_queue.py list-json scenario (run PASS); its step gives_pairs checks only name and status (work_queue_list_steps.py:60-67) | read; probe p6 |
| scripts/workqueue_list.py:waiting (25-33) | reads raised.jsonl, last line per request wins; crashes on a bad line | r39 reads a record no command writes (section 5) | test_work_queue.py r39 scenario (run PASS; its Given writes a good line) | read; probes p3, p8 |
| CLAUDE.md module map, row scripts/workqueue_status.py ("`work status`") | docs | row changes with retirement | none | read |
| README.md:178-180 | says `work status` prints open initiatives and the SessionStart hook gives it | docs | none | by search |
| spec/capabilities/requests.md r13, r14; features/requests.feature:327-345 | bare `work show` (r13) and `work status` (r14) | another capability; Q-2 | test_requests.py r13 and r14 (run PASS) | by search |
| features/supervision.feature:310 | `python3 {scripts}/work show` is refused for an implementer | the worker's command allowlist; a change to show must keep this row true | not run (examples test) | read |

## 4. Tests the requirements make impossible to keep

Accepted r34-r39: none. The 7 scenarios pass today, and no r34-r39 change in the findings breaks them. Verified: work_queue_list_steps.py read in full; its asserts check name and status pairs, question text, and a waiting line; no step reads `turn`, so dropping turn from JSON keeps them (by search: `grep turn` finds none in that file).

Impossible once the old forms go (decision 0072 and the ledger); all PASS today:
- test_work_queue.py::test_show_prints_each_workitem_of_every_initiative_with_its_status_deprecated (r3)
- test_work_queue.py::test_show_with_json_prints_each_workitem_with_its_initiative_and_status_as_one_json_object_deprecated (r11)
- test_work_queue.py::test_status_of_an_initiative…_deprecated (r16), test_status_with_no_initiative…_deprecated (r17), test_status_with_json…_deprecated (r18)
- test_requests.py::test_show_prints_each_request_with_its_status_and_whose_turn_it_is (requests r13; w206 does not retire it: Q-2)
- test_requests.py::test_status_with_no_initiative_prints_with_its_date… (requests r14: Q-2)
- test_migration_tools.py, the 9 session tests, the one on `work status` text above (migration r32: Q-3)
Found by search: `grep -rn "work status\|work show" tests/`. tests/scenarios/requests_show_steps.py:44-49 runs both.

## 5. A step the work-item skips

- The record of raised requests: the path from raising to a waiting line skips its writer. No command writes `raised.jsonl` (by search; read). Probe p8: no record, no waiting line. The findings file names the writers that would come: requests r29 `--raised-for` and supervision r135 (read).
- show's refusals, each run in p1 and p4: no such initiative or work-item; a name that is a path; a request id; a non-UTF-8 file (the whole listing refused); a work-item id in two initiatives ("more than one work-item", read at `workqueue.py:226-231`). show writes nothing (read: only read-only git commands, and `git ls-remote` to the remote, `workqueue_status.py:51-61`).
- show reaches the remote read-only (`git ls-remote`): with no remote it says "cannot be compared" (run, p5). Read: a network call on a read path.

## 6. Defects

D1 and D2 are in section 2 with their reproductions: `scripts/workqueue_list.py:31-32`, a malformed raised.jsonl line crashes `work list` with a traceback after the first line is printed.

Not counted as defects (readings, section 2): list --json turn (p6); the whole-listing refusal on a non-UTF-8 file (p4); the branch printed being the checkout's (p5).

## Questions for the plan (both readings)

- Q-1 (findings file, fix now): finding 1 is `scripts/supervise_change.py:91-99` (write_proposals rewrites another proposal's applied lists). The work-item's `findings:` names it, but no accepted requirement of w206 covers it (w206 accepts work-queue r34-r39). Reading A: fix it under w206. Reading B: it stays out and gets its own work-item. Not probed; its line count is 107.
- Q-2: requests r13 (bare `work show` prints each request with status and turn) and r14 (bare `work status` prints observations) conflict with work-queue r36-r38 and decision 0072 once those forms go. Reading A: keep the no-target forms for requests. Reading B: retire them, and requests r13 and r14 retire too (their own item). Both tests pass today.
- Q-3: migration-tools r32 (SessionStart gives what `work status` prints). Reading A: keep the status text in the hook. Reading B: the hook prints `work show <initiative>` for each open initiative. The ledger leaves r32 as a question.
- Q-4: list --json `turn` (findings finding 2). Reading A: drop it. Reading B: keep it; r35 asks only for name and status.
- Q-5: "the initiative branch" in r36. Reading A: the checked-out branch, as now (read: supervision works on the checked-out initiative branch, `test_supervision.py:4`). Reading B: the branch named for the initiative; no name rule exists in scripts (by search).

## 7. The file set

Accepted scenarios pass today, so no file must change for them. The findings file (`.shop/work/i39/runs/branch-review/2/findings.md`, the work-item's `findings:` field, read) names the fix-now items. The plan decides which go in (Q-1, Q-4, D1, D2).

- scripts/workqueue_list.py (78 lines, room 222): drop `turn` from list --json (Q-4); refuse a malformed raised.jsonl line, naming file and line, catching ValueError and KeyError (D1, D2). Found by read; probes p3, p6.
- tests/scripts/test_workqueue_list.py (new; absent now): a malformed-record refusal with no traceback (findings file line 203). Found by read (`ls`: absent).
- tests/scenarios/work_queue_list_steps.py (80 lines, room 220): RUF015 at line 79 only (finding 5, drop); no change needed for r34-r39. Found by read.
- scripts/supervise_change.py (107 lines, room 193): write_proposals 91-99, only under Q-1 reading A. Found by the findings file; lines not re-read.
- scripts/work (181 lines, room 119), on the path (dispatch 31-37, argparse 121-125): no change for r34-r39; changes under Q-2 and Q-3 (no-target show, status). Found by read.
- scripts/workqueue.py (294 lines, room 6), on the path (frontmatter, read, entry, find, items, requests): no change needed. Found by read.
- scripts/workqueue_status.py (170 lines, room 130), on the path (status, section, natural): no change needed; changes with the retirement of status. Found by read and search.
- scripts/migrate_session.py (54 lines, room 246), on the hook's path: changes under Q-3 only. Found by search.
- scripts/migrate (76 lines, room 224): help text line 64, under Q-3. Found by search.
- CLAUDE.md: module map row for scripts/workqueue_status.py, under retirement only. Found by search.

Size: `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools size --limit 300` printed nothing, exit 0 (run). No tracked Python file is over 300 lines. Room is 300 minus the line count.
