# Report of w121

## Budget
scripts/work_items.py, tests/scenarios/supervision_tests_steps.py, features/supervision.feature (retire only), tests/scripts/test_work_items.py (supervision_world.py not needed).

## Changed
- work_items.py: `guarantees()` reads `group: guarantees` from spec/capabilities/<cap>.md (beside .shop/); the refusal applies only if some accepted requirement is not of a guarantees capability; otherwise all collected scenarios are deselected; `pytest_sessionfinish` turns exit 5 into 0 for such a work-item. A missing capability file is not a guarantees capability. Docstring updated.
- Steps: general "accepting X [and Y]" Given (anchored, so longer Givens still match theirs), the capability Givens, the "no other test" variant, and the Thens "was not refused, and deselected…" and "exited successfully".
- Retired the deprecated scenario with `features retire`.
- Unit tests: guarantees deselect+exit 0, non-scenario kept, mixed refused.

## Red/green
- Start: Suite record 722 passed, 3 failed (the three w121 scenarios among the failures).
- Red: `python3 -m pytest -q --work-item w121` -> 3 failed (undefined steps). With my steps written: r64, r65 failed with `INTERNALERROR> SystemExit: --work-item w1: w1 accepts none of the scenarios it collected` (exit 3); r56 already refused (plan said so).
- Final: `python3 -m pytest -q --work-item w121 tests/scripts/test_work_items.py` -> scenarios 145 passed, 1 skipped (with the worktree's scripts first, see concern); test_work_items.py 11 passed.
- size --limit 300: nothing printed.

## Tests changed under an allowance
none (the retired scenario's literal Given was generalised; it was used only by it).

## Open questions
- Requirement id with no `#`/capability: unchosen. Refusal still ends as INTERNALERROR exit 3; a work-item with no `accepts:` is "no such work-item" (left as is).

The plan contained no code.

## Concerns
In this session the ambient PYTHONPATH puts /home/vscode/shopsystem-bdd/scripts (the installed old plugin) before the worktree's scripts in `supervise_worker.with_scripts`, so the r64/r65 scenarios fail here unless the worktree's scripts come first. I verified by temporarily swapping the order (all green), then reverted it. If `work run` runs the tests with the same ambient PYTHONPATH, r64/r65 will fail there.

## Now possible
A guarantees-only work-item's `--work-item` run is no longer refused and exits 0.

Commit: 975b45d
