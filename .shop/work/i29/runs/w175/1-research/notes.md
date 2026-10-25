# Research of w175: requests r22, the empty delegation

Search: `tools refs` ran (0 refs for `workqueue_request.request`, a dispatch by name in `scripts/work`). `tools tests-of` and `untested` could not run: no map (`tools map` not made). Counts below are `by search` unless marked.
Scripts: `/home/vscode/shopsystem-bdd/scripts/tools`. Probes: `.shop/scratch/w175-1-research/probe_delegation.py`, run `-n 0`.

Accepted: `requests#r22` (spec/capabilities/requests.md:23), scenario `features/requests.feature:33`.

## 1. Why the scenario is red today

- Command: `python3 -m pytest -q "tests/scenarios/test_requests.py::test_request_with_an_empty_delegation_is_refused_and_nothing_changes"` (run).
- Fails: `StepDefinitionNotFoundError: Then "the command is refused because the delegation is empty"` (features/requests.feature:38). No step matches it: `tests/scenarios/requests_write_steps.py` has no such `@then` (by search).
- Steps before it run: the When `the asker runs \`work request ... --delegation ""\`` (requests_write_steps.py:44) runs and writes q1 (probe P1, run). So the code step is what fails.
- Missing in step definitions: a `@then` "the command is refused because the delegation is empty" in `tests/scenarios/requests_write_steps.py` (the model is :94, "...names neither an origin nor a job-thread"). The Then `it exits with an error` (:100) and `the upstream keeps no request` (:105) already exist.
- Missing in code: `scripts/workqueue_request.py`, `request()` (line 69). It has the r3 check (lines 75-76) and the r2 check (80-82), but no check for an empty delegation. Line 87 writes `delegation: ""` whenever `delegation is not None`, so an empty string is written.
- Not run after the fix: the two existing Thens above. Expected to pass once `request()` refuses before `workqueue.committed` (read).

## 2. What the system answers today

Probes run with `python3 -m pytest -q -s -n 0 .shop/scratch/w175-1-research/probe_delegation.py`. Each: `python3 /tmp/.../w175-1-research/scripts/work --root <scratch repo> request "Show the queue" --from ctx-a --lines lines.md --source o1 [--delegation ...]`. Scratch repos only.

- P1 scenario, `--delegation ""`: exit 0, stdout `q1`; q1.md kept with `delegation: ""`; git log `work request: q1`. Run. Wrong against r22 (defect D1).
- P2 nearest, `--delegation "   "`: exit 0, `q1`; `delegation: "   "` written. Run. (defect D2)
- P3 baseline, no `--delegation`: exit 0, `q1`; no delegation line. Run.
- P4 baseline, `--delegation "Answer scoping questions"`: exit 0, `q1`; `delegation: "Answer scoping questions"`. Run. The r19 case; matches features/requests.feature:23.
- P5 nearest, `--delegation ""` and no `--source`: exit 1; stderr `work: the request names neither an origin (--source) nor a job-thread (--thread)`; nothing kept; no commit beyond init. Run. The origin check runs first.
- P6 nearest, `--delegation ""`, line 3 `Show the queue to the caller.`: exit 1; stderr `line 3 is not in the strict form model check holds`; nothing kept. Run. The line check runs first.
- P7 nearest, `--delegation ""` twice: both exit 0; q1 then q2, each with `delegation: ""`. Run.
- Read: `scripts/supervise_answers.py:41-46` (`delegation()`) turns a stored `""` into None (`return value or None`). So a request with an empty delegation is treated as having none by `work run`. Read only.
- Read: `scripts/supervise_answers.py:44` for a stored `"   "`: returns `"   "`, truthy, so questions would go to sessions under a whitespace delegation. Read only.

## 3. Old assumptions

The requirement makes an empty delegation a refusal at intake. The old form is "a delegation given, empty or not, is written". Test column by search: no test passes an empty delegation (grep of `tests/` for `--delegation ""` and `delegation=""`: only the red scenario), so `tests that execute it` is `none` where no test runs the branch.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_request.py:request, line 87 | writes `delegation: <json>` when `delegation is not None`, so `""` is written | refuse when empty, before any write (r22) | r19 scenario (features/requests.feature:23, passes); the red r22 scenario does not reach the write | search, probe P1 |
| scripts/workqueue_request.py:request, lines 75-82 | origin and line checks before any write | the new check joins these; order is the plan's choice (P5, P6 show origin and line first) | r3 and r2 scenarios in test_requests.py | read |
| scripts/supervise_answers.py:Answers.delegation, line 44-46 | a `""` value becomes None (`return value or None`): empty means no delegation | with r22, an empty value comes only from a request kept before r22; the branch is still reachable for those | none (by search: no test stores `delegation: ""`) | read, search |
| scripts/supervise_answers.py:Answers.delegation, line 44 | a whitespace value is kept and used as the delegation | with r22 read as literal empty, `"   "` still gets through (P2) | none (by search) | read, probe P2 |
| scripts/work:cmd_request, line 64 and `--delegation` at line 127 | passes `args.delegation` through; argparse gives `""` for `--delegation ""` | no change in the command; the refusal is in the library | test_requests.py via the When step | read |
| spec/index.md:96 (glossary "delegation") | "the person's words, given with a request" | no emptiness in it; no change needed | none (spec text) | search |

## 4. Tests the requirement makes impossible to keep

By search (no map). Search: `tests/` for `--delegation`, `delegation`, `delegation=""`.
- `tests/scenarios/requests_write_steps.py:61-66` (`its delegation is "{text}"`): reads a delegation field; it is used by the r19 scenario with non-empty text. Still passes. Verified sound.
- `tests/scenarios/supervision_delegation_steps.py` (all): every delegation is non-empty ("Please get everything delivered..."). Verified sound: none can fail with r22.
- No test asserts that an empty delegation is written. Found: none.
- The red scenario itself is the only test that uses an empty delegation.

## 5. A step the work-item skips

None found (read). The new refusal sits in `request()` with the r2 and r3 refusals, before `workqueue.committed`, so it skips no step the other paths make. Effects only the write produces, shown by the refused runs:
- the `delegation:` frontmatter field: P1 writes it; P5, P6 do not get that far.
- the commit `work request: qN` (P1 log shows it; P5 and P6 show none).
- the number `q<n>` taken (P7: the second run gives q2; a refused run takes no number, P5, P6).

## 6. Defects

D1. An empty delegation is accepted and committed.
- Commands: `python3 .../scripts/work --root <repo> request "Show the queue" --from ctx-a --lines lines.md --source o1 --delegation ""` (lines.md two strict EARS lines).
- Came back: `q1`, exit 0; q1.md has `delegation: ""`; the commit `work request: q1` is made.
- Contrary to requests r22 (refuse, change nothing).

D2. A whitespace-only delegation is accepted and committed. Reading: r22 says "empty"; if it means the empty string only, this is not a defect; if it includes whitespace, it is.
- Commands: as D1 with `--delegation "   "`.
- Came back: `q1`, exit 0; `delegation: "   "`.
- Not judged; both readings are for the plan.

## 7. The file set

Files the work-item must change:
- `scripts/workqueue_request.py`: `request()` refuses an empty delegation (empty string; reading of D2 open) before the write, with a message naming the delegation. Found by probes P1, D1 and by reading line 87.
- `tests/scenarios/requests_write_steps.py`: add `@then("the command is refused because the delegation is empty")`, checking the exit and stderr (`delegation` named). Found by the NameError in section 1.

Files that must keep passing, to be read but not edited:
- `scripts/work`: passes `args.delegation` (line 64, arg at 127); no edit. Module on the path.
- `scripts/workqueue.py`: `Refused`, `committed`, `read`; no edit. Module on the path.
- `scripts/supervise_answers.py`: reads `delegation`; no edit needed for r22; read section 3.
- `features/requests.feature`, `spec/capabilities/requests.md`: already hold r22. No edit.

Modules on the path, with lines (`wc -l`) and room under 300 (CLAUDE.md gives the 300 limit):
- scripts/work: 151 lines, room 149.
- scripts/workqueue_request.py: 144 lines, room 156.
- scripts/workqueue.py: 290 lines, room 10 (not edited).
- tests/scenarios/requests_write_steps.py: 122 lines, room 178.
- tests/scenarios/test_requests.py: 9 lines (not edited).
- scripts/supervise_answers.py: not measured (not edited); read by section 3.
