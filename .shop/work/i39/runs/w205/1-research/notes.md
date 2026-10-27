# w205 research: work list and work show (work-queue r34-r39)

Method: `tools refs` resolved only `workqueue.find`; `workqueue.items`, `workqueue.requests`, `workqueue_status.status` gave nothing, so those are by search. `tools tests-of`/`untested`: no map (`tools map` not made, per brief), so test lists are by search. Collection under this runner: the environment's `--work-item w205` deselects every non-accepted scenario ("7/74 collected, 67 deselected"), so out-of-scope scenarios cannot be run by id; they are marked read or probed. Probes: `.shop/scratch/w205-1-research/probe_show_list.py`, `probe_requests_refusals.py`.

## 1. Why each accepted scenario is red today

- r34 `list prints each initiative, each request and each work-item ...` (test_work_queue.py::test_list_prints_each_initiative_each_request_and_each_workitem_under_shopwork_with_its_status). Command: `python3 -m pytest -q "<id>"`. run: StepDefinitionNotFoundError, Given "an initiative i1 under .shop/work/ that is started, whose work-items w1 is drafted and w2 is ready" (feature line 103). Later steps not reached. Code: scripts/work has no `list` subcommand (its subparsers, lines 108-158); probe `work list` exits 2, "invalid choice: 'list'" (run).
- r35 `list with --json ...` (test_list_with_json_...). run: undefined Given "a request q1 under .shop/work/ that is accepted" (feature line 118). Code: no `list --json` (probe, run, exit 2).
- r39 `list prints an initiative as waiting on a request it raised into an upstream ...` (test_list_prints_an_initiative_as_waiting_on...). run: undefined Given "a request q1 that i1 raised into the upstream ctx-up, which is accepted" (feature line 128). Code: no waiting line exists anywhere (read: scripts/workqueue_status.py has no request part).
- r36 `show of an initiative prints where it stands ...` (test_show_of_an_initiative_...). run: undefined Given "an initiative i1 under .shop/work/ that is started, whose capability-proposal p1 is approved" (feature line 136). Read: after it, `work show i1` is refused by argparse (scripts/work:114-115, `show` has no positional; probe exit 2, "unrecognized arguments: i1", run). Read: Thens "work prints i1's status as started" (line 144) and "it prints ... the question" have no step with that wording (test_work_queue.py:219 needs " with "; work_queue_status_steps.py:91 is "work prints i1's status" only).
- r37 `show of a work-item prints its status and its open questions` (test_show_of_a_workitem_...). run: undefined Given "i1's work-item w2 is awaiting-answer with the question "Which reading of r3?" not yet answered" (feature line 156). The existing step work_queue_status_steps.py:34 matches only "i1's work-item w1 is ready, and its work-item w2 ...". Read: `work show w2` is refused as in r36 (run for the same argparse refusal with w1: P-A's pattern).
- r38 `show of <target> with --json` (two examples, test_show_of_target_with_json_...). Givens match (with_items, test_work_queue.py:70). run: When `work show i1 --json` and `work show w1 --json` exit 2, "unrecognized arguments" (work_queue_withdraw_steps.py:41 asserts returncode 0). Read: Then "it gives i1's status as started, and w1 with awaiting-answer and the question ..." has no step (work_queue_status_steps.py:151 handles "with STATUS" only, no question clause).

Run results: 3 list scenarios FAILED (StepDefinitionNotFound); 4 show scenarios FAILED (StepDefinitionNotFound x2, argparse x2). Node ids as above.

## 2. What the system answers today (probes, run)

Each: the command, what came back, mark.

- P-A `probe_show_list.py::test_probe_list_and_show_as_the_brief_names_them`: `work list` and `work list --json` exit 2 "invalid choice: 'list'"; `work show i1`, `work show w2`, `work show i1 --json` exit 2 "unrecognized arguments". run.
- P-B `probe_show_list.py::test_probe_show_with_no_argument_today`: `work show` exit 0, stdout: `i1/w1 drafted` / `i1/w2 awaiting-answer` / `i2/w3 green` / `q1 accepted None`. run. (The no-argument show is the deprecated r3 form.)
- P-C `probe_show_list.py::test_probe_status_today`: `work status i1` exit 0: `initiative i1 started`, `work-item w1 drafted`, `work-item w2 awaiting-answer`, `  question: Which reading of r3?`, `branch master: the remote cannot be compared with it`, `uncommitted: none`, `untracked: none`, `ledger:` (empty), `last next: none`. `work status i1 --json` exit 0: one JSON object, `initiatives[0]` with `work-items` as `{work-item, status, questions}`. run. This is already the content r36 asks of show.
- P-D `probe_show_list.py::test_probe_list_with_no_repository_branch` (detached HEAD): `work status i2` exit 0, `branch None: the remote cannot be compared with it`. run.
- P-E `probe_requests_refusals.py::test_probe_requests_as_show_lists_them_today`: `work show` exit 0: `q1 open upstream` / `q2 awaiting-asker asker`. `work show q1` exit 2. `work list` exit 2. run. (A request with no `turn` prints as `None`; see D1.)
- P-F `...::test_probe_show_refuses_a_non_utf8_file_today`: `work show` exit 1, "work: .shop/work/i1/w1.md is not UTF-8 text"; `work status i1` same. run.
- P-G `...::test_probe_duplicate_name_and_missing_initiative_today`: `work show` exit 0, `i1/w1 drafted` / `i2/w1 drafted`. `work withdraw w1` exit 1, "there is more than one work-item w1 under .shop/work". `work status nope` exit 1, "the initiative nope does not exist (no .shop/work/nope)". `work status ../i1` exit 1, "the initiative ../i1 is not a name". run.

Nearest cases the scenarios do not give: a request with no turn (P-B, P-E); two work-items of one name (P-G); a non-UTF-8 file (P-F); a missing initiative and a path name (P-G); a detached HEAD (P-D).
Read, not probed: `list` on an empty `.shop/work/`; a work-item with no status line (workqueue.items yields None; `show` prints `None`); a request naming an initiative by `part_of` or `source` (the request file has no upstream field: workqueue_request.py:108 writes `asker`, `part_of` or `source`, `status`, `turn` only), so "raised into the upstream ctx-up" (r39 Given) cannot be written in a request file as it stands.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work:cmd_show (lines 30-41) | prints each work-item of every initiative as `<i>/<w> <status>`, then each request, or `--json` `{work-items, requests}` | r34-r35 give this to `list`; r36-r38 make `show` take a target | test_work_queue.py deprecated r3 and r11 scenarios (feature 176-195): by search, not collectable here; features/work-queue.feature:272 and tests/scenarios/work_queue_withdraw_steps.py:39 (read) | search for `work show` in features, tests, scripts |
| scripts/work:114-115 (`show` subparser: no positional, `--json`) | `show` takes no argument | must take `<target>` (initiative or work-item id) | the r36-r38 scenarios, by search; red today (run) | search; `tools refs` not usable |
| scripts/work:cmd_status and scripts/workqueue_status.py:status, read, render, open_text, open_names | per-initiative text and JSON; no-initiative form adds observations | r36 wants show to print the same content; r34-r39 do not retire `status`; decision 0072 does (r3, r11, r16-r18) | work_queue_status_steps.py (r16-r18 deprecated, by search); requests_show_steps.py:49 (requests r14, by search); features/migration-tools.feature:544 via tests/scenarios/migration_session_steps.py:85 (by search) | search for `status(`, `work status`, `open_text` |
| scripts/migrate_session.py:work_text, open_text (lines 23-25) | the SessionStart hook adds `work status`'s text for each open initiative | if `status` is retired, the hook text changes (migration-tools r32; README.md:178-180) | migration-tools.feature:544 (by search; not run) | search for `work_text`, `open_text`, `work status` |
| scripts/workqueue.py:items (109-114), requests (117-124) | each work-item (path order); each request by number | list reuses both; old `show` is their only `work` caller | none named in tests (by search); reached through the show scenarios above | search for `items(` and `requests(` |
| scripts/workqueue_done.py:_named (13-19), _holds (22-38) | a request names an initiative by `part_of` or `source`; the request counts when its asker is `internal` or this context | r39 reads the same fields; the upstream is not in the request file (no field) | tests/scenarios/supervision_done_steps.py:43 (by search) | search for `asker` and `_named` |
| scripts/supervise_worker.py:50 (TOOLS intake) | intake session may run `work outcome`, `turn`, `show` with any arguments | `show <target>` still matches the pattern; the intake session's reliance on no-argument show is read only | none found (read; tests not searched for this list) | read |
| README.md:178-180, 265; CLAUDE.md:18, 23 (module map `workqueue_status.py` row); spec/capabilities/migration-tools.md:54 (r32); spec/capabilities/requests.md:50 (r13), :56 (r14); spec/decisions/0068 | docs and specs name `work status` and `work show` | a new module (if any) needs a CLAUDE.md row; `status` and `show` wording changes with 0072 | none (docs) | search for `work (show|status|list)` in non-code files |

## 4. Tests the requirements make impossible to keep

Searched by name and content (no map, so `by search`). Accepted scenarios are red today (section 1); these are the others.

- test_work_queue.py: deprecated r3 "show prints each work-item of every initiative with its status (deprecated)" (feature 176-185) and r11 (186-195): read; they assert the no-argument show; under r36 a no-argument show is not a form the requirements name. Cannot be run here (collection limited to w205). Breaks if `show` takes a required target.
- test_work_queue.py: r7 "show refuses a file under an initiative that is not UTF-8 text, naming it" (feature 268-275, When `work show`): probe P-F shows today's refusal (run). Breaks if the no-argument show goes. Plan decides.
- test_requests.py: requests r13 "show prints each request with its status and whose turn it is" (requests.feature 327-334; tests/scenarios/requests_show_steps.py:44 runs `work show`). Passes today: probe P-E (run). Requests r13 is not in the work-queue retired list and is not in w205. Both readings: (a) keep a no-argument `show` printing requests, which keeps r13; (b) r13 is replaced by `list`, which needs its line changed in requests.md. Not judged.
- test_work_queue.py r16-r18 deprecated `status` scenarios (feature 425-465) and requests r14 (requests.feature 336-344): keep passing while `status` exists (read). Decision 0072 retires them, and w205 does not.
- migration-tools.feature:544 (r32; migration_session_steps.py:85): keeps passing while the hook text is `status`'s (read).
- Verified sound (read): withdraw and retry's name lookup (workqueue.find) and `status`'s entry check; P-G shows both refusals today.

## 5. A step the work-item skips

r36 and r38 resolve a target by name. The existing ways:
- `workqueue.find` (scripts/workqueue.py:226-231), used by withdraw and retry, refuses zero or more than one match. Effect only it produces: "there is more than one work-item w1" (run, P-G withdraw). A `show <work-item>` that does not use it would print both (P-G `show` prints both `i1/w1` and `i2/w1` today).
- `entry()` (workqueue.py:58-61) refuses `..` and paths (run, P-G `status ../i1`).
- status's initiative check (workqueue_status.py:149-151) refuses a missing initiative (run, P-G `status nope`).
- git calls (workqueue_status.py:51-74): branch and remote comparison, `git status` of the whole checkout. Effect only `status` produces: the branch, uncommitted and untracked lines (run, P-C, P-D). `ls-remote` contacts the remote (read).
- UTF-8 refusal for every file of the initiative (workqueue.read, workqueue.py:50-55): run, P-F.
- For r39 (read): `workqueue.context_path` (workqueue.py:38-47) refuses with no spec/index.md; `_holds` (workqueue_done.py:25) calls it, `status` does not. An initiative listed as waiting on a request would need it.

## 6. Defects

### D1: `work show` prints a request with no turn as `None`
Reproduce: `python3 -m pytest -q -s .shop/scratch/w205-1-research/probe_show_list.py::test_probe_show_with_no_argument_today` (run). Output: `q1 accepted None`. The request file in the probe has no `turn:` line; `workqueue.requests` yields `turn` as None and scripts/work:cmd_show prints it with `%s`.

### D2: a work-item with no status is printed as `None` (read)
`workqueue.items` yields `data.get("status")` (workqueue.py:114) and cmd_show/status print it. Read only; no probe. Fixture work_queue_status_steps.py:145 (`no_status`) exists for the r7 refusal of a transition, not for show.

## 7. The file set

Must change for the accepted scenarios:
- scripts/work (171 lines; room 129): add `list` subparser and `show <target>` with `--json`; route to the new module. Found: section 1 and P-A.
- New module, e.g. scripts/workqueue_list.py (new concern: list and show by target; CLAUDE.md "a new concern gets a new module and a row"). Reuses workqueue.items/requests, workqueue.find, and workqueue_status.read/render for an initiative. Found: section 3.
- CLAUDE.md (module map, line 23 area): one row for the new module. Found: CLAUDE.md:18, 23.
- tests/scenarios/work_queue_list_steps.py (new step module): the undefined Givens and Thens (sections 1, r34-r39). Found: section 1 run results.
- tests/scenarios/test_work_queue.py (282 lines; room 18): one import line for the new step module (it imports every work_queue_*_steps module, lines 19-28). Found: file read.
- tests/scenarios/work_queue_status_steps.py (160 lines; room 140): its `with_state` and `w1_and_w2` steps may need the plural "work-items w1 ... and w2" and the question form (sections 1). Found: file read.

Must not change, but at the limit:
- scripts/workqueue.py (294 lines; room 6): no new code fits without going over 300. Found: `tools size` (below).

Keep passing (change only if the plan decides, section 4):
- scripts/workqueue_status.py (170 lines; room 130), scripts/migrate_session.py (54 lines; room 246): unchanged while `status` stays.
- tests/scenarios/requests_show_steps.py (72 lines; room 228), features/requests.feature:327-334: the requests r13 conflict (section 4).
- features/work-queue.feature: deprecated r3, r11 (176-195) and r7 (268-275): the plan decides whether they are removed (decision 0072 retires r3, r11).
- tests/scenarios/work_queue_withdraw_steps.py (64 lines): its "work prints one JSON object" step is reused by r35 and r38; no change.

`tools size --limit 300` (run): printed no file over 300 lines.
Modules on the change's path, with lines and room under 300: scripts/work 171 (129), scripts/workqueue.py 294 (6), scripts/workqueue_status.py 170 (130), scripts/workqueue_done.py 73 (227), scripts/workqueue_request.py 186 (114), scripts/migrate_session.py 54 (246), tests/scenarios/test_work_queue.py 282 (18), tests/scenarios/work_queue_status_steps.py 160 (140), tests/scenarios/requests_show_steps.py 72 (228), tests/scenarios/work_queue_withdraw_steps.py 64 (236). Line counts from `wc -l`; the migrate_session count is from the file's last line shown by Read.

Git state: `git status --porcelain` was empty at the start; nothing written in the checkout.
