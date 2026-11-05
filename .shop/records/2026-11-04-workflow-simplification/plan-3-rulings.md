---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-3-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 3 of the workflow simplification: rulings on the review, and what was done with each finding

`plan-3-review.md` asked the person three questions. The person was not available. Each ruling below was **ruled by
the main session without the person, 2026-11-05; revisit.** The fixes are on branch `workflow-simplification` after
`30ac8d7a` (the review): `faf509f8` (intake), `11ebcd82` (readiness, `work line`, tests, `CLAUDE.md`), `c8a750aa`
(skills) and `ca7143bc` (the timing test).

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-05; revisit) | What was done |
|---|---|---|---|
| S4 | A rewritten line and the request's end | Leave the requests behaviour for now. The skill says so. Plan 4 adds a requests line so that a request whose lines are settled or counter-proposed can close. | `c8a750aa`: `taking-in-a-request` step 2 says the request stays `awaiting-asker` after its counter-proposal is accepted, and that the item is not held by it. `faf509f8`: intake's `## Not yet` names it. See "For plan 4". |
| S5 | The CPU ceiling under xdist | Hold it serially. | `ca7143bc`: `test_model_logic_on_the_live_spec_is_fast` is marked `timing`; `pytest.ini` registers the marker and its `addopts` is `-m "not fixture and not timing"`. |
| Skills | `shaping-items` against superpowers:brainstorming's ending | In this repository `shaping-items` wins: items are the output, and a design record may sit beside them. | `c8a750aa`: said in `shaping-items`'s Overview. |

## The new baseline command

From now on every plan's baseline list runs, next to the suite (`python3 -m pytest -q`):

```
python3 -m pytest -m timing -n 0 -q
```

Expected: `1 passed, 1181 deselected` today (the count of deselected tests grows with the suite). The default
parallel run no longer holds the time ceiling.

## The findings

| # | What was done |
|---|---|
| S1 | Fixed in `faf509f8`. `work intake` refuses, before it writes, a request whose asker is this context's own, where the context lists upstreams and the request names no `source`: `q<n> "<title>" is a request to the upstream <up>; it is taken in there`. Test: `test_intake_refuses_this_contexts_own_request_to_an_upstream`. The skill's description is narrowed to requests from a peer or the product (`c8a750aa`). |
| S2 | Fixed in `faf509f8`. The test runs `model --root <repo> check`, asserts the exit is not 2 and that no output line names `q1.md`. With `Reasons` taken out of `model_requests.SECTIONS`, it fails. |
| S3 | Fixed in `c8a750aa`. Both skills say that a line is reworded by editing its `- [r<n>]` bullet in the item's `## Requirements` (same id) and committing the item, or by withdrawing the item and shaping it again, and that `work line` only adds. `shaping-items` says a line using an item's own term is checked by the readiness bar, not by `model parse`. `taking-in-a-request` says that when every line is refused, the item is refused with `work refuse`. |
| S4 | As ruled. |
| S5 | As ruled. The suite then passed in 4 of 4 full runs, and the timing run passed (1.7 s). |
| M1 | Fixed in `faf509f8`: on intake's path, a word outside the glossary's `line outcome` values is refused, naming them. The old path is unchanged. |
| M2 | Fixed in `faf509f8`: `allow_abbrev=False` on the `outcome` subparser only; `work line` gives `--in` and `--into` both, so neither is read as the other there. `--in` on `work outcome` now exits 2. |
| M3 | Fixed in `11ebcd82`: the test calls `well_formed` in-process with `features_generate.generate` patched to raise; with the guarantees skip removed, it fails. |
| M4 | Fixed in `11ebcd82`: `test_a_line_with_the_items_term_readies` and `test_an_l1_elsewhere_does_not_refuse_on_the_solver` (DONE written into the fixture's `spec/`, an L1 confirmed by the solver, ABANDON on the item readies). |
| M5 | Fixed in `11ebcd82`: `features_generate.generate(root, path, skipped=None)` fills `skipped` with each group's reason; `readiness_bar._scenarios` reads it instead of matching stderr. Test: `test_a_group_generate_skips_is_the_reason`. |
| M6 | Fixed in `11ebcd82`: the `backlog_moves.py` row names `ready` and its refusal, `backlog_items.py` the `request`/`asked_by` fields; the `features_generate.py` and `intake_moves.py` rows name the changes above. |
| M7 | Fixed in `faf509f8`: `work outcome: the counter-proposal does not parse in this context's requirement grammar: <line> …`. |
| M8 | Fixed in `11ebcd82`: `work line: b1 "<title>": the line starts with #, …`; on `work outcome`'s accepted path it names `work outcome`. |
| M9 | Partly fixed in `11ebcd82`: `work line b1 --into CAP -- TEXT` takes TEXT (test `test_a_line_after_a_double_dash_is_the_line`). The class swap `p.__class__ = _LineParser` is kept; replacing it with `parse_intermixed_args` changes how every subcommand parses. Left for when `backlog_cli.py` is next changed. |
| M10 | Fixed in `faf509f8`: `line 1 of request q1 accepted into work-queue#r5: fits`. |
| M11 | Fixed in `faf509f8`: `handles` lets a malformed backlog's refusal through (a missing `.shop/backlog/` is still no item). Test: `test_a_malformed_backlog_is_refused_not_passed_over`. |
| M12 | Partly fixed in `faf509f8`: `backlog_lines` and `workqueue_lines` are imported at the top, and `workqueue_lines_check` is gone. The five `_private` helpers of `workqueue_request` are still imported; they become public when `workqueue_request.py` is next split (plan 4). |
| M13 | Fixed in `faf509f8`: `work intake` refuses a request with `turn: asker`, naming the asker's turn; a row of `test_intake_refuses_a_request_out_of_turn`. |

## For plan 4

- **A requests line (S4):** a `rewritten` line whose counter-proposal has a settled outcome counts as settled for `work
  turn`, so the request can reach `accepted`. Build it next to the batch intake session. Lift `turn`'s edit to a
  module-level `_turned(text)` in `workqueue_request.py` and call it from `intake_moves.outcome` (the implementer's
  ruling 7), so the turn rule is written once.
- **Rewording or removing an item's line** with a command (S3): until then the skills say to edit the bullet.
- **The `_private` helpers** `intake_moves` imports from `workqueue_request` made public when that file is split (M12).
- **`_LineParser`'s class swap** replaced (M9).
- **Duplicate `<cap>#r<n>` across items** (D3), as before.
- **The test of the skills' commands** may exempt a command named on the same line as its unbuilt id (the implementer's
  ruling 12), so `` `work quote` `` can be written when it is built.

## Verification after the fixes

| Check | Got |
|---|---|
| `python3 -m pytest -q` | **1153 passed**, 1 skipped, 27 xfailed, 131 subtests, in 4 of 4 runs (1142 without the timing test, + 11 new tests) |
| `python3 -m pytest -m timing -n 0 -q` | 1 passed, 1181 deselected |
| `model check \| tail -1` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems |
| `model logic \| tail -1` | 11 findings: 6 L5, 5 L6 |
| `model lexicon --check \| tail -1` | 401 terms, 0 problems |
| `features generate --check` | exit 0 |
| `features vocab --check \| tail -1` | every step has one handler |
| `features bindings --unbound` | every binding names a scenario |
| `tools size --limit 300` | silent, exit 0 (`scripts/work` 211, `intake_moves.py` 157) |
| `tools check` over the branch's Python files and `scripts/work` | ruff and vulture clean; import-linter states no contracts |
