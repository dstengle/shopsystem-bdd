# w232 research notes

Method: no `tools map` exists, so `tests-of` and `untested` answer nothing; every test list here is `by search`.
`tools refs` returns 0 for `workqueue.requests`, `workqueue_list.show` and `workqueue_list` because the callers sit in the extensionless `scripts/work`; callers found by search.
Run: `python3 -m pytest -q --work-item w232` (1 failed, 182 passed, 1 skipped, xdist).

## 1. Why each scenario is red today

- features/work-queue.feature:127 `list prints each initiative and each work-item` (@r60): **green** in the run. Not red.
- features/work-queue.feature:138 `list with --json ...` (@r61): **green** in the run. Not red.
- features/work-queue.feature:186 `show of a request prints its status ...` (@r59): **red**. Run stopped at the first undefined step:
  - Given line 188 `a request q1 kept in this context, whose asker is this context, that is delivered and in the asker's turn`: StepDefinitionNotFoundError (run).
  - Then line 194 `it prints that it is the asker's turn`: no step matches (search).
  - Then line 195 `it prints line 1 with accepted and line 2 with refused`: `prints_pairs` (work_queue_list_steps.py:37) cannot match, since `\S+` takes one word (`line`) (read).
  - Then line 196 `it prints the question "..." and the answer "..."`: `prints_question` (work_queue_list_steps.py:55) is a whole-line parse; no match (read).
  - Then line 197 `it prints its resolution, thing#r7 and 0.23.0`: no step matches (search).
  - Given lines 189-191 (outcomes, question with answer, resolution): no step matches (search; `requests_steps.py:78` needs "each found in").
  - Then line 193 `work prints q1's status as delivered`: matches `prints_status_as` (work_queue_list_steps.py:50).
- Code behind it: `scripts/workqueue_list.py:show` lines 82-85 print one line `q1 <status> <turn>` for a request, and never read its `## Lines`, `## Outcomes`, `## Questions`, `## Answers` or `## Resolution` (read). No function reads a request's sections for show; the entry reader `workqueue_request._entries` is private (read).

## 2. Old assumptions

Requirements r60/r61 replace r34/r35 (retired in spec/capabilities/work-queue.md:7), which listed requests. Whether requests stay in `work list` is open:
- Reading (a): keep requests in list. r60/r61 are silent on requests; nothing today breaks.
- Reading (b): drop requests from list. Rows 1-3 change and the tests in part 3 break.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_list.py:listing lines 42, 46-47, 53-54 | prints each request's status, as text lines and as the JSON key `requests` | r60/r61 name initiatives and work-items; under (b) drop these | tests/scripts/test_workqueue_list.py:test_list_json_gives_each_request... (line 22); features/work-queue.feature:101 and :115 (r34/r35 deprecated) | read + search |
| tests/scenarios/work_queue_list_steps.py:gives_pairs lines 60-67 | reads `shown["requests"]` for every `it gives` pair | the r61 scenario (work-queue.feature:138) uses this step; under (b) it raises KeyError unless changed | features/work-queue.feature:138 (run, passes today) | read |
| scripts/work:cmd_list help text line 123 | says "each initiative, request and work-item" | under (b) the help is wrong | none (by search: no test quotes it) | search |
| scripts/work:cmd_show lines 35-47 (no target) | prints work-items and requests, as text and as JSON `requests` | r59-r61 name `work show <request>` and `work list`, not the no-target show; both readings leave it | features/requests.feature:376 (requests_show_steps.py:prints_request, run) | read + search |
| scripts/workqueue_list.py:show lines 82-85 (request branch) | prints `<name> <status> <turn>` on one line | r59 requires status, whose turn, lines with outcomes, questions, answers and resolution | features/work-queue.feature:186 (red); features/requests.feature:413 via requests_flow_steps.py:95-99 (passes today) | read |
| scripts/workqueue_list.py:show line 84 (request, `--json`) | prints the three-key object `request`, `status`, `turn` | r38 (not accepted) asks for one JSON object; r59 is text | none (by search: no test calls show of a request with --json) | read |
| README.md:178-181 (0.28.0 notes) | says `work list` lists requests | stale under (b); a release note, no code | none | search |

## 3. Tests the requirements make impossible to keep

Searched all of tests/ for `show` of a request and `list` assertions (by search; no map).

- tests/scripts/test_workqueue_list.py:test_list_json_gives_each_request_and_its_status_and_nothing_besides (lines 22-25): asserts the JSON `requests` key. Impossible under reading (b); passes under (a).
- features/work-queue.feature:101-112 (@r34 @deprecated) and :115-124 (@r35 @deprecated): pin requests in list output. Pass today; fail under (b). Both are deprecated for removal; the work-item has no `## Retires` section, so nothing removes them here.
- features/requests.feature:408-413 (step tests/scenarios/requests_flow_steps.py:show_prints lines 95-99): asserts `shown["out"].split()[1:] == ["delivered", "asker"]`, the whole stdout of `work show <request>`. Impossible under r59 whatever the reading: r59 prints several lines. Passes today. Not accepted, but it breaks.
- Sound, checked by reading: test_workqueue_list.py:test_show_of_an_initiative_whose_ledger... (32-38), ...work_item_file_with_no_kind... (41-47) and ...raised_record_line... (50-55) go through the initiative and work-item branches, which r59 does not change. tests/scenarios/requests_show_steps.py:prints_request (54-57) reads the default show (no target), which r59 does not change.

## 4. The file set

Production:
- scripts/workqueue_list.py: `show` request branch prints r59's sections (88 lines, room 212).
- scripts/workqueue_request.py: `_entries` reads the sections; import it or add a public reader (228 lines, room 72).
- scripts/work: help text line 123 only, and only under (b) (184 lines, room 116).
- scripts/workqueue.py: on the path (`requests()` and `read`); edit only if a reader moves here (294 lines, room 6).

Tests and features:
- tests/scenarios/work_queue_list_steps.py: new Given and Then steps for lines 188-197 (80 lines, room 220).
- tests/scenarios/requests_flow_steps.py: `show_prints` (95-99) must change for multi-line output (99 lines, room 201).
- tests/scripts/test_workqueue_list.py: line 22 changes under (b) only (55 lines, room 245).
- features/work-queue.feature: remove :101 and :115 under (b) only; the work-item has no `## Retires` (`features/` is not a Python file).
- work_queue_list_steps.py `gives_pairs` (60-67): changes under (b) only.

Modules on the change's path, not edited: scripts/workqueue_status.py (170 lines, room 130; initiative show, not touched).
Size: `tools size --limit 300` printed nothing, so no tracked Python file is over 300 lines (run).
