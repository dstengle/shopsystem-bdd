# w235 research notes

Scripts: plugin scripts run by path. `tools tests-of` answered "no map": no map exists, so test lists are `by search`. `tools refs` took no qualified name; callers of `request`/`_change`/`field` are from read and search. Worktree HEAD is 147a68de; the brief's base is ae85edd3.

## 1. Why each scenario is red today

Command run once: `python3 -m pytest -q --work-item w235`. Result: 11 failed, 180 passed, 1 skipped. All 11 accepted scenarios (tests/scenarios/test_requests.py) failed. The captured output was truncated, so per-scenario causes below are `run` where shown and `read` otherwise.

- `run`: the `When` step for `the upstream runs \`work delegate\`, giving q1 and the delegation "..."` raises IndexError at tests/scenarios/requests_steps.py:63 (`giving.rsplit("version ")`). That step only knows resolve's `version` form. Seen for r66 commit, r68 withdrawn, r70 upstream/asker, r71 keeps status.
- `read`: no `delegate` subcommand: scripts/work main() has no such parser (lines 117-171) and no dispatch entry (174-177).
- `read`: undefined Given steps, so pytest-bdd fails before the When: "q1 holds no delegation", "q1 holds the delegation \"...\"", "q1 holds no other delegation" (r65, r67, r72). Nothing in tests/scenarios matches them.
- `read`: undefined Then steps: "q1's delegation is \"...\"" (r65, r66, r67, r70, r71, r72). Only `its delegation is "{text}"` exists (requests_write_steps.py:48).
- `read`: undefined Then "the command is refused, naming <status>" (r68). "the command is refused because the delegation is empty" (r67) exists (requests_write_steps.py:67).
- `read`: r72 has undefined steps "the person tells a session, on <date>, that for q1 it may ..." (Given/When), "in its reply to that message the session runs `work delegate` ..." and "when that reply ends, q1's delegation is ..." (Then). No code or stub exists for a session's reply.
- `read`: the Givens "a request q1 ... whose turn is ..." and "... whose status is <s> ... line outcome is <o>" match requests_steps.py:44-56, so they run.

Accepted scenarios, all in features/requests.feature via tests/scenarios/test_requests.py:
- r65 (2 examples): red at undefined Givens and Then.
- r66 commit: red at IndexError in the When (run, and read for the reason).
- r67 empty delegation: red at undefined "q1 holds the delegation" Given.
- r68 (3 examples, delivered/refused/withdrawn): IndexError in the When (run for withdrawn); Then "naming <status>" undefined.
- r72 session: red at undefined steps (see above); no session code.
- r70 (upstream, asker): IndexError in the When (run).
- r71 keeps status and turn: IndexError in the When (run).

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_request.py:_with_field (71-73) | replaces an existing frontmatter line; does nothing when the line is absent | `delegate` on a request with no `delegation:` (r65 example, r72) must add the line | none by map; requests.feature turn/resolve scenarios by search | read |
| scripts/workqueue_request.py:request (130-163) | writes `delegation:` once at take-in, JSON-quoted (json.dumps) | `delegate` rewrites the same field; it keeps the JSON form so readers decode it | requests.feature r19 scenario, passed in run; no map | read, run |
| scripts/workqueue_request.py:SETTLED (17), used by turn (196-211) | accepted, refused, withdrawn | r68 refuses delivered, refused, withdrawn: a different set. Reusing SETTLED would refuse `accepted` requests | requests.feature turn scenarios by search; no map | read |
| scripts/supervise_answers.py:delegation (37-49) | reads the field at each run, json-decodes a quoted value, None when empty | reads the value the request holds now, so a delegate change is picked up; no edit needed | tests/scripts/test_supervise_answers.py and supervision.feature "reads the delegation the request has" by search; no map | read, search |
| scripts/work main() dispatch (174-177) | lists each subcommand; no `delegate` | adds `delegate` | test_work_queue.py "the session runs `work {args}`" by search | read |
| README.md:233 | documents `--delegation` at take-in only | a `work delegate` line would be added | none (docs) | read |
| CLAUDE.md:28 (module map) | lists `work request, outcome, ask, reply, turn, resolve` | adds `delegate` to that row | none (docs) | read |

## 3. Tests the requirements make impossible to keep

- tests/scenarios/requests_steps.py::the_upstream_runs (59-66): assumes every `giving` is resolve's `version` form. It cannot bind the delegate form as is, so it must branch (run: IndexError). It is a step, not a kept test.
- No existing test asserts behaviour the requirements change. Verified by search, not by map: `delegation` appears in tests only in requests_write_steps.py (the delegation_is step), tests/scripts/test_supervise_answers.py and the supervision scenarios that give a delegation through the request's field. The request() shape, the r19/r22 scenarios (passed in run) and tests/scripts/test_workqueue_request_asker.py (no delegation named) are unaffected.
- Sound by search: tests/scenarios/test_requests.py binds every requests.feature scenario, so the new scenarios need no new binding.

## 4. The file set

Production:
- scripts/work: add a `delegate` parser (request, delegation text) and its dispatch entry; ~8 lines. Found by read of main().
- scripts/workqueue_request.py: new `delegate(root, ident, text)` through `_change`: refuse empty ("the delegation is empty"), refuse delivered/refused/withdrawn naming the status, write `delegation` JSON-quoted, inserting it when absent (r65, r66, r67, r68, r70, r71, r72). Read of request/_change/_with_field.
- scripts/workqueue_request.py or the _with_field helper: insert-when-absent is needed (see table). Two readings: extend `_with_field` to insert before the closing `---`, or add a helper beside it. Both in this file.
- scripts/workqueue.py (read only, on the path): `committed` makes the commit (r66). 294 lines, room 6; not edited.

Tests:
- tests/scenarios/requests_steps.py: the_upstream_runs branch for the `delegate` form (argv gets the request and the text). 112 lines.
- tests/scenarios/requests_write_steps.py: Givens "q1 holds no delegation / the delegation / no other delegation", Then "q1's delegation is", "the command is refused, naming <status>", and the r72 session steps. 145 lines.
- The r72 session steps have two readings. (a) A stub session that runs `work delegate` (tests/scripts/stub_claude.py exists, not read). (b) A text check of an instruction a session follows; none exists in skills/, agents/, README.md, CLAUDE.md, hooks/ or docs/ (grep for `work request|--delegation|work delegate`: README.md:184, 189, 233 only). The plan picks one.

Docs (not needed for the scenarios):
- CLAUDE.md:28 and README.md:233: add `delegate`.

Read only, on the path:
- scripts/supervise_answers.py: 147 lines, room 153. Reads the delegation; no edit.

Size: `tools size --limit 300` printed nothing: no tracked Python file is over 300 lines. Room under the 300 limit: scripts/work 116 (184 lines); scripts/workqueue_request.py 65 (235); scripts/workqueue.py 6 (294); scripts/supervise_answers.py 153 (147); tests/scenarios/requests_steps.py 188 (112); tests/scenarios/requests_write_steps.py 155 (145).
