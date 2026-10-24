# Review of w129: work show prints requests; work status prints uncited observations

**Verdict: DONE.** No Critical finding, none triaged fix now. Two Minor observations (hardening).

## Commits reviewed
The branch `work/w129` is gone, so the commits are those between `9048fab work: w129 ready -> claimed` and
`418ae04 work: w129 claimed -> done` on the checked-out history, less `work run`'s own `work:` commits:

- `4e5c8de work show prints requests; work status prints uncited observations (requests r13, r14)`

The implementer's result lists `d39f691` with the same message and author date. `git diff d39f691 4e5c8de -- scripts tests`
is empty: 4e5c8de is `work run`'s rebased copy of d39f691 with the same change. That is not a difference in content.

Files: `scripts/work` (+6/-2), `scripts/workqueue.py` (+10), `scripts/workqueue_status.py` (+33/-6),
`tests/scenarios/requests_show_steps.py` (new, 72), `tests/scenarios/test_requests.py` (+1). All of them are in the
work-item's fileset. Nothing under `features/` changed.

## Removed and weakened tests
None. What I searched for in the diff: deleted `def test_`/step functions, removed `assert` lines, parametrize cases,
skip/xfail markers, and changed files under `tests/`. The only test changes add things: a new step module, and one
import line in `test_requests.py`. The plan's "Tests the decisions break" says none.

## Allowances
The report's `## Tests changed under an allowance` is "none". There is no row to verify.

## Cannot verify
- The report's suite figures (731 passed and 2 failed at start; 144 passed and 1 skipped under `--work-item w129`;
  132 passed in the `--whole-suite` subset). I ran only the two scenarios, and both passed.
- What `work status` prints on this repository's real `.shop/`. Running `scripts/work` directly is not a command this
  session may run. I checked the observations file's form by grep instead: 28 `## ` headings, 28 `date:` lines, and no
  heading with trailing whitespace. That form matches what `uncited`'s regex expects.

## Findings

### 1. Minor (observation): `uncited` counts the `source` of every file one level under `.shop/work/`, not only initiatives and requests
`scripts/workqueue_status.py:117-120`: the glob `.shop/work/*/*.md` also reads capability-proposals and work-items.
requests#r14 asks only for observations that "the `source` of no initiative and of no request names". An observation
named only by a capability-proposal's `source` would be left out of `work status`. A file at that level that is not
UTF-8 (a proposal, say) would also make `work status` refuse, which plan D4 does not name.

Today nothing triggers either case. `grep -H "^source:" .shop/work/i1{2,6,7,8,9}*/*.md` shows that every
capability-proposal's `source` names a `design-decision/…`, never an observation.

Fix: read only `*/initiative.md` and `requests/q*.md`, or filter on `kind` (initiative or capability-change, and
request).

### 2. Minor (observation): an observation with no `date:` line prints the date as `None`
`scripts/workqueue_status.py:124-126` (and `requests()` likewise for a request with no `status` or `turn`). An
observation with no date prints as `observation <id> None`. No line names this edge, and the report lists it as an
open case. In the real file, every one of the 28 observations has a `date:` line.

Fix, if it is wanted: print the observation without a date, or refuse, naming the observation.

### Risks checked, no finding
- The hook text (migration-tools#r32): `open_text` passes `report=False`, so the hook still gets only the initiative
  blocks (plan D3). `scripts/migrate_session.py` is unchanged.
- The existing `work status` and `work show` outputs and JSON keys (`initiatives`, `work-items`) are unchanged. The
  observation lines come after the initiative blocks (D1), and `requests` and `observations` are new keys (D2).
- A request file that is not UTF-8 is read through `workqueue.read`, which refuses (D4).
- Short and full observation ids both count as cited (`uncited` tries the heading and `observation/<slug>`) (D5).
- Code no line asks for: none. Request lines serve r13, observation lines serve r14, the JSON keys follow
  design-decision/query-commands-answer-in-their-output, and `report=False` keeps migration-tools#r32 as it is.

## Commands run
- `git log --format=%H -1 --grep="^work: w129 ready -> claimed$" work/w129`: unknown revision (the branch is gone)
- `git log --oneline -15 --grep=w129`; `git log --oneline 9048fab..418ae04`; `git show --stat 4e5c8de`; `git show 4e5c8de`
- `git diff d39f691 4e5c8de --stat -- scripts tests`: empty
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9048fab`
  - **ruff**: All checks passed!
  - **vulture**: clean
  - **import-linter**: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: prints nothing (no file over the limit)
- `python3 -m pytest -q -n 0 tests/scenarios/test_requests.py -k "show_prints_each_request or status_with_no_initiative"`:
  2 passed
- greps of `.shop/records/observations.md` (headings, `date:` lines, trailing whitespace) and of the `source:`/`kind:`
  lines under `.shop/work/*/`
