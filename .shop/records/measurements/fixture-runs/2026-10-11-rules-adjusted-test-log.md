---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-rules-adjusted-test-log
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Rules adjusted: test log (0.13.0)

Spec: `docs/superpowers/specs/2026-10-11-rules-adjusted-design.md`. Scripts: 70 OK, unchanged.

## The two allowances, and the implementer without the Skill tool

Fixture `/home/vscode/scratch/shopsystem-bdd/allow/` (`make_allow.py`, `run.sh`, `show.py`): a `shelf` library
with a slice 3 whose two decisions are that the client names an item's version, an add naming none being refused,
and that an id carries its version. Its brief lists no test under "Tests the decisions break".

- **X.** `tests/test_listing.py`, from before the batch, calls `add` with no version in its setup and asserts a
  count. `tests/test_add.py`, committed after the brief's `Batch base:`, pins the interim state ("version one for
  now").
- **Y.** X, and `tests/test_ids.py`, from before the batch, asserts an id equals `"book/dune"`.

A controller on Sonnet dispatches one `bdd-implementer` with the brief and a report file and relays the reply.

| | X | Y |
|---|---|---|
| 0.12.0 | `BLOCKED`, 2 of 2, naming both tests; neither touched | `BLOCKED`, 1 of 1, naming all three |
| 0.13.0 | done, 3 of 3: both tests changed, both listed; suite 4 passed | `BLOCKED`, 2 of 2, naming `test_ids.py`, which is not touched |

- **Listed as asked.** Every 0.13.0 report has `## Tests changed under an allowance` with two rows, for example:
  "tests/test_listing.py::test_the_shelf_counts_what_was_added: setup; add calls now pass version 1; assertion
  unchanged." and "tests/test_add.py::…_is_at_version_one_for_now: interim (first committed a280acf after batch
  base); now asserts ValueError when no version named (decision 1)". No assertion line of a test from before the
  batch differs in any run's diff.
- **The stop still holds.** In both Y runs the implementer used the two allowances, left `test_ids.py` failing as
  it was, and replied `BLOCKED` for it alone.
- **Replies were `DONE_WITH_CONCERNS`**, the concern being that the brief's "none" was wrong. That is the right
  reading: the planner hears of the omission without a stop.
- **The renamed test.** In four of five runs the interim test was renamed as it was rewritten, and one report
  remarked on it. A reviewer follows a rename ("a renamed test is still the old test").
- **Starting context.** The implementer's first request: 19.6k on 0.12.0 (three runs), 12.2k on 0.13.0 (five
  runs). On this fixture the listing of installed skills and the tool's own definition were 7.4k.
- **Still under `bdd-red-green`.** Each 0.13.0 report shows the scenario red on its Then line first ("Red:
  `pytest -m slice-3` -> `assert 'book/dune' == 'book/dune@2'`"), with no tool to load the skill.

## Not tested

- **The reviewers' check of the allowance rows.** No reviewer was run on a report with the list, nor on a diff
  where a "setup" row hides a changed expected value.
- **Changes 2, 4, 5, 6 and 7** (Steps by order, steps-only tasks, sizes one batch ahead, lanes, the controller's
  line a slice and session a batch): text for the planner and the controller, not run. The batch that runs on this
  version is their test, read with `measure compare` against `docs/superpowers/testing/2026-10-11-kb-baseline/`.
  The spec names the number each should move.
- **The scout's `steps only` line.**
