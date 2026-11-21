---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-70/review-1
kind: review
batch: batch-70
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/94
head: 6cbcdf9fb873266edd5948f61b1eada15fd02a48
range: 03a4bd8df1b7776ab14df7aaf6a12d4ae36d7035..6cbcdf9fb873266edd5948f61b1eada15fd02a48
result: fix-now
---

# batch-70 review 1

## Verdict

The batch builds b59, b81 and b63 inside their chore files, and their checks pass. b68's code does what its four lines ask, but one finding must be fixed: r53's scenario is never collected, so nothing in the generated features tests r53 or `work resolve`'s delivery. There are also two observations.

## Findings

### f1 Important fix now: r53's scenario is shadowed by r54's and never runs
- item: b68
- where: features/context-requests.feature:93
Groups g53 and g54 have the same title, "A request's issue is never left out of step with its record". `tests/scenarios/test_context_requests.py` binds the feature with `scenarios("context-requests.feature")`. pytest-bdd keeps a feature's scenarios in a dict keyed by title, so r54's scenario (`work fits`) replaces r53's (`work resolve`) and r53's is never collected. The batch driver's own note on b518 says the same.

The batch also retires r29 and deletes its scenario (`@g29 @r29`, "An accepted context request resolved is delivered with its resolution"). The net effect is that the generated features no longer test that `work resolve` sets the request to `delivered`, sets its side to `asker`, keeps a resolution and closes the thread. That amounts to a removed test.

`tests/scripts/test_request_commit_first.py::test_a_close_github_refuses_puts_the_record_back_and_a_rerun_closes` covers part of the resolve path in a script test. It does not cover r53's Thens as written.

Fix: give g53 a title of its own on the item, for example "An accepted context request resolved is delivered and its thread closed". Lay it again with `work batch amend b68`, regenerate the feature, and check that both `@r53` and `@r54` are collected.

### f2 Minor observation: the "has the thread" Then cannot fail in g53 and g54
- item: b68
- where: tests/scenarios/requests_handlers_thread.py:574
In g53 and g54, no Given binds t1. So `_url` binds t1 to the issue of the one request a Given wrote. The Then "the context request c1 has the thread t1" then checks `_issue_of(c1) == _url(t1)`, which compares that issue with itself. The Then is real only in g51 and g52, where a Given binds t1 first. The Then about the thread's status (`closed`, read from the stand-in gh) does check something real. Recorded as hardening of the handler.

### f3 Minor observation: a failed close now puts back a refusing turn too
- item: b68
- where: scripts/request_post.py:149
`closed` runs for every posting with `close` set. That includes `turn_posting`'s refused turn (r37), not only `work resolve` and `work fits`. When `gh issue close` fails on a refusing turn, the record is now put back to its state before the turn. Before this batch, the turn stayed committed and only the refusal was raised. r51 and r52 name only resolve and serve, so this changes `work turn` and `work outcome` in a case no line of b68 asks about. It matches the item's title, and no client hits it unless GitHub refuses the close. Reproduction: run a turn that refuses a request with `STUB_GH_FAIL="issue close"`; the record goes back to its state before the turn.
