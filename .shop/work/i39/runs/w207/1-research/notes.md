# Research notes: w207 (work-queue r34-r39)

Method: `tools refs` for names; no coverage map (`tests-of` and `untested` say "no map", and I did not make one), so every test list here is `by search`. `refs` misses the extensionless `scripts/work` and reported 0 for `workqueue_list.listing`, `workqueue_list.show`, `workqueue_status.open_text` and `open_names`, which search finds in `scripts/work`, `scripts/migrate_session.py` and `scripts/supervise_all.py`. Counts from `refs` are a floor.

## 1. Why each scenario is red today

None is red. Each run by node id with `python3 -m pytest -q "<node id>"`, each `1 passed` (run):

- `test_list_prints_each_initiative_each_request_and_each_workitem_under_shopwork_with_its_status` (r34)
- `test_list_with_json_prints_each_initiative_request_and_workitem_with_its_status_as_one_json_object` (r35)
- `test_list_prints_an_initiative_as_waiting_on_a_request_it_raised_into_an_upstream_while_that_request_is_not_delivered` (r39)
- `test_show_of_an_initiative_prints_where_it_stands_for_a_session_to_start_from` (r36)
- `test_show_of_a_workitem_prints_its_status_and_its_open_questions` (r37)
- `test_show_of_target_with_json_prints_its_result_as_one_json_object[i1-...]` (r38, outline row 1)
- `test_show_of_target_with_json_prints_its_result_as_one_json_object[w1-...]` (r38, outline row 2)

Nothing is missing in the step definitions or in the code behind them. That code: `workqueue_list.listing`, `show`, `work_item`, `waiting`; `workqueue_status.status`, `section`; `workqueue.items`, `requests`; reached through `scripts/work` (`cmd_list`, `cmd_show`).

Work-item state: `i39/w207.md` is `drafted`. `w205` and `w206`, which carry the same accepts, are `green` (branch review 3, `.shop/work/i39/runs/branch-review/3/findings.md`).

## 2. What the system answers today

Probe file: `.shop/scratch/w207-1-research/probe_list_show.py` (scratch, ignored). Run: `python3 -m pytest -q -s -n 0 .shop/scratch/w207-1-research/probe_list_show.py`. `-n 0` was added because xdist from `pytest.ini` swallowed the output. Each probe makes its own repository under the scratch directory and runs `scripts/work --root <repo>`. That scratch directory sits inside the worktree's git repository, so the git answers (branch, uncommitted, untracked) describe the worktree, not the probe repository. All probes below: run.

- **p1 empty queue** (`work list`, `work list --json`): text prints nothing, exit 0. JSON `{"initiatives": [], "requests": [], "work-items": []}`, exit 0.
- **p2 waiting cases** (`work list`, `work list --json`):
  - i1 with raised q1 (awaiting-upstream, then delivered) and q2 (accepted): text `initiative i1 waiting on q2 (in ctx-up, accepted)`; q1 not printed. The last line for a request wins.
  - i2 done, raised q3 accepted: text prints `initiative i2 waiting on q3`. Ended initiatives are listed, and waiting too.
  - i3 with raised.jsonl and no initiative.md: nothing printed about it.
  - JSON for i1: `{"initiative": "i1", "status": "started"}` and no waiting entry (D2).
- **p3 list shapes**: w1 with an empty `status:` and w2 with no status print `work-item i1/w1 None` and `work-item i1/w2 None`, exit 0. w3 with no id, kind work-item and status `ready` is printed. notes.md (no frontmatter) and a capability-proposal are not printed. JSON gives `"status": null` for w1 and w2.
- **p4 show with a non-UTF-8 ledger** (`work show i1`): traceback ending `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff`, exit 1 (D1).
- **p5 show refusals** (`work show <target>`):
  - `show w9` (no kind): `work: w9 is a None, not a work-item or an initiative that work show shows`, exit 1 (D3).
  - `show w1` (same name in two initiatives): `there is more than one work-item w1 under .shop/work`, exit 1.
  - `show q1` (a request): `q1 is a request, not a work-item or an initiative that work show shows`, exit 1.
  - `show i1/w1` and `show ../i1`: `the target ... is not a name`, exit 1.
  - `show nothere` and `show i9`: `there is no work-item <x> under .shop/work`, exit 1.
- **p6 questions and next** (`work show w1`, `work show w1 --json`, `work show i1`, `work show i1 --json`): w1 with Questions "first?" and "second?" and one Answer: the open question is `second?` (answers counted by position). `show i1` prints the ledger's last three lines, `branch None: the remote cannot be compared with it` (detached checkout), `last next: - 2026-10-22: next: answer w1`. The `next` value keeps its date and `- ` prefix (observation: the spec says "the ledger's last line").
- **p7 no-target show and status still live** (`work show`, `work status`): `work show` prints `i1/w1 ready` and `q1 accepted upstream`; `work status` prints the initiative block and `last next: none`. Both exit 0.

Read, not run: `workqueue_list.show` for a name with a directory but no initiative.md falls through to `work_item`, which gives the "no work-item" refusal (p5 `i9` shows that path).

## 3. Old assumptions

The requirements in the work-item replace nothing that code relies on: r34-r39 are already met. What they leave behind is the retired `work status` form and the no-target `work show` (work-queue r3, r11, r16, r17, r18, all in the capability's `retired:`), plus three live lines that still name those forms: requests r13 (`work show`) and r14 (`work status`), and migration-tools r32 (the hook gives `work status`). Decision 0072 replaces `work status` with `work list` and `work show`.

The tests column is `by search` (no map).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work:`cmd_status` → scripts/workqueue_status.py:`status` (initiative None) | prints each open initiative and its observations | `work status` is retired (decision 0072) and work-queue r16-r18 are retired; this branch goes dead | by search: tests/scenarios/work_queue_status_steps.py (r16-r18, deprecated); features/work-queue.feature r16-r18 | refs: 1 ref, scripts/workqueue_list.py:81 is the other caller; scripts/work:67 by search |
| scripts/workqueue_status.py:`uncited` | lists observations no initiative or request cites | the only report of requests r14 (live: `work status` with no initiative prints them); no home once `work status` goes | by search: tests/scenarios/requests_show_steps.py; features/requests.feature (r14, around line 342) | refs: 1 ref, inside `status` |
| scripts/work:`cmd_show` no-target branch (`workqueue.items`, `workqueue.requests`, text and JSON) | prints every work-item and request | work-queue r3 and r11 retired; requests r13 (live) says `work show` prints requests | by search: tests/scenarios/work_queue_withdraw_steps.py:50 (r11 `show --json`); tests/scenarios/requests_show_steps.py:44 (`work show`); features/work-queue.feature:268-274 (r7, live, uses no-target `work show` for the non-UTF-8 refusal) | search (extensionless script) |
| scripts/migrate_session.py:`work_text`, `open_root` | the SessionStart hook's text: `work status` for each open initiative | migration-tools r32 (live) names `work status`; the hook text changes with the retirement | by search: tests/scenarios/migration_session_steps.py:85-97 (runs `scripts/work status`) | refs: scripts/migrate_upgrade.py imports `work_text`; search for the rest |
| scripts/workqueue_status.py:`open_text` | renders `status` for each open initiative, for the hook | the hook's text; moves with `status` | none directly (reached only through scripts/migrate_session.py:25); by search the hook's test runs `work status` as a subprocess | refs: 0; search: scripts/migrate_session.py:25 |
| scripts/workqueue_status.py:`open_names`; scripts/migrate_session.py:20,30; scripts/supervise_all.py:30,36 | the open selection (neither done nor abandoned), for the hook and for `work run` with no initiative | needed by `work run`; stays | by search: tests/scenarios/supervision_all_steps.py | refs: 0; search: the three callers |
| scripts/workqueue_list.py:`show` lines 80-81 (initiative branch calls `workqueue_status.status`) | `work show <initiative>` prints the `status` block, as JSON `{"initiatives": [...]}` | decision 0072: after retirement this becomes the `work show <initiative>` code, not a call into `work status` | by search: features/work-queue.feature r36-r38 scenarios (run, passing) | refs: scripts/workqueue_list.py:81 |
| scripts/work argparse help for `status` (line 140) and `show` (line 123) | help text names `work status` as the default | text | none | search |
| CLAUDE.md:23 (module map row `scripts/workqueue_status.py` = `work status`); README.md:178-180; scripts/migrate:64 help | docs and help naming `work status` | text | none | search |
| scripts/workqueue_status.py module docstring line 1; tests/scenarios/work_queue_status_steps.py docstring | name r16-r18 | text | none | search |

Live spec lines that name the retired form, and so conflict with the retirement: requests r13 (`work show`), requests r14 (`work status`), migration-tools r32 (hook gives `work status`). The integrate round of 2026-10-27 proposed removing requests r13 and r14; that was not applied, and it is carried as an internal request after i39 (ledger).

## 4. Tests the requirements make impossible to keep

Accepted requirements r34-r39 change no behaviour that a test asserts. The seven scenario tests pass, and none of them asserts the absence of a waiting entry in JSON.

- `tests/scripts/test_workqueue_list.py` (by read, not run): `test_list_json_gives_each_request_and_its_status_and_nothing_besides` asserts only `requests`, so it stays valid if the JSON gains a waiting key. `test_a_raised_record_line_that_cannot_be_read_is_refused_naming_the_file_and_line`: sound on read.
- `tests/scenarios/work_queue_list_steps.py` `gives_pairs` (read): checks the listed pairs only, not "nothing besides" (r35). Sound but weak (branch review 3's observation).
- By search, tests that break only if r3, r11, r16-r18 are removed (not caused by r34-r39): the deprecated scenarios in `features/work-queue.feature` at lines 176, 186, 425, 445, 457 and their steps (`work_queue_status_steps.py`, `work_queue_withdraw_steps.py:50`); `tests/scenarios/requests_show_steps.py` (requests r13, r14); `tests/scenarios/migration_session_steps.py` (migration-tools r32); and the live r7 scenario at `features/work-queue.feature:268` (no-target `work show`).

Verdict on the accepted requirements: none can no longer pass. Sound on read: the seven scenario tests and `test_workqueue_list.py`.

## 5. A step the work-item skips

The accepted work-item adds no write path: `list` and `show` only read. Steps the existing `work status` path takes that `list` and `show` of a work-item do not:
- the observations report (`uncited`, `work status` with no initiative): read; r34-r39 do not ask for it.
- the `ls-remote` call in `branch()` (remote contact, 30 s timeout) is taken by `show <initiative>` through `status`, and not by `list`: read.

Refusals only the show path produces (run, p5): not a name; a target with no work-item; a work-item with no kind (D3); more than one work-item of a name; a request target. A non-UTF-8 file refusal (`workqueue.read`) is read, and the r7 scenario at `features/work-queue.feature:268` covers it; not run. Effects: none beyond printed output and the refusals.

## 6. Defects

### D1 — `work show <initiative>` crashes on a non-UTF-8 ledger
- Reproduction (run, p4): initiative i1 with work-item w1 `ready`, and `.shop/work/i1/ledger.md` holding the bytes `2026-10-27: \xff\xfe bad bytes`. Command: `python3 scripts/work --root <repo> show i1`.
- Came back: a traceback ending `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 12`; exit 1.
- Cause (read): `scripts/workqueue_status.py:ledger` calls `path.read_text(encoding="utf-8")` with no refusal. The r7 requirement says a command that cannot be done exits with its reason, never a traceback; the r7 scenario covers work-item files only.

### D2 — `work list --json` does not show a waiting initiative (a reading to settle)
- Reproduction (run, p2): i1 started, w1 green, raised q2 accepted in ctx-up. `work list` prints `initiative i1 waiting on q2 (in ctx-up, accepted)`. `work list --json` prints `{"initiatives": [{"initiative": "i1", "status": "started"}], ...}` with no waiting entry.
- Readings: (a) r39 applies to the text listing only; the JSON is r35's "each initiative, request and work-item with its status", which is met. (b) r39 applies to `work list` in any form, so the JSON should carry the waiting. Branch review 3 (observation O3) reads it as (b). The spec does not settle it.

### D3 — a work-item with no kind is refused as "is a None"
- Reproduction (run, p5): `.shop/work/i1/w9.md` with frontmatter and no `kind:`; command `work show w9`.
- Came back: `work: w9 is a None, not a work-item or an initiative that work show shows`, exit 1.
- Cause (read): `scripts/workqueue_list.py:work_item` formats `data.get("kind")` without a default. The refusal is given, but it does not say why (branch review 3, O2).

Not defects (observations): a work-item with an empty or missing status is listed `None` (p3); the `last next:` line keeps its date and `- ` prefix (p6); a `raised.jsonl` under an initiative with no initiative.md is silent (p2).

## 7. The file set

The seven accepted scenarios pass today, and no test that passes today fails, so the requirements alone need no change. The files below are what branch review 3's observations on `list` and `show` (O2, O3) and defect D1 would need. Each is a choice for the plan.

- `scripts/workqueue_status.py`: 170 lines, room 130. D1: `ledger()` reads through a refusal. Found by read (`ledger`, lines 77-81) and probe p4.
- `scripts/workqueue_list.py`: 82 lines, room 218. D3: a default for the kind in `work_item`. D2, if reading (b): a waiting entry in the JSON of `listing`. Found by read; probes p2, p5.
- `tests/scripts/test_workqueue_list.py`: 33 lines, room 267. A test for D1, and for D2 if reading (b). Found by read.
- `tests/scenarios/work_queue_list_steps.py`: 80 lines, room 220. Branch review 3 suggests `gives_pairs` check every key, for D2. Found by read.

On the path, not changed by the requirements:
- `scripts/work`: 181 lines, room 119.
- `scripts/workqueue.py`: 294 lines, room 6. Any addition there needs a split first.
- `tests/scenarios/test_work_queue.py`: 283 lines, room 17.
- `tests/scenarios/work_queue_status_steps.py`: 160 lines, room 140.

Outside the requirements, not in the file set (see the questions in the result):
- `scripts/supervise_change.py`: 125 lines, room 175.
- `tests/scripts/test_supervise_change.py`: 51 lines, room 249.
Branch review 3's fix-now finding 2 (a merge leaves another proposal's drafts pointer wrong) lies there. Its fix is not a requirement of r34-r39.

Size: `tools size --limit 300` printed nothing, so no tracked Python file is over 300 lines. `git status --porcelain` is empty. The scratch directory `.shop/scratch/` is git-ignored.
