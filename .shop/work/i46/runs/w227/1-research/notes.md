# Research of w227 (fix the findings of branch review 2 of i46)

Method: `tools` has no map (`tools tests-of` and `tools untested` refuse: "no map"); `tools refs` ran. Test lists below are `by search`. Callers are `by search` (Grep) too.

## 1. Why each accepted scenario is red today

Run (`run`): `python3 -m pytest -q --work-item w227`. Result: 189 passed, 1 skipped, 56 subtests passed, 4.58 s. Nothing failed.

- No accepted scenario is red. All seven pass: r161 (`supervision.feature:1809`), r164 (`:1705`), r165 (`:1751`), r166 (`:1767`), r167 (`:1776`), r169 (`:1742`), r170 (`:1727`, both Examples rows). The collected names appear in the run output.
- The 1 skip is not identified (no `-rs` run). Read: it is not one of the seven.
- The 189 count includes tests the plugin keeps as non-scenarios (`work_items.py` r55). Read: `work_items.py:128-144` selects by the accepted requirements.
- Code behind them: `scripts/supervise_glossary.py` (`statuses`, `route`, `withheld`, `glossary_only_done`), `scripts/supervise_rounds.py:58-61, 173-176`, `scripts/supervise_done.py:28-37`, `scripts/supervise.py:230-231`, `scripts/supervise_brief.py:86`, `scripts/supervise_change.py:133-139`.
- The work-item's `findings:` file (`.shop/work/i46/runs/branch-review/2/findings.md`) is the reason for w227; the scenarios it lists were green there too (w225 green, suite 1066 passed). So w227's change is for findings, not for red scenarios.

## 2. Old assumptions

The accepted lines add a glossary route (r161, r164-r170). Old assumptions in code, found from the findings and a read:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_rounds.py:159-161` (`run_round`, gate branch) | a gate round with no question gets an approval question, for any proposal kind | r117 is for a capability-proposal only. Glossary-proposal gets the question with no line asking for it (finding F1; q36 line 1 open) | none (searched: no test or feature asserts this text for a glossary-proposal; r117's scenario `features/supervision.feature:1828` is capability-only) | Grep of the text; branch review F1 |
| `scripts/supervise_rounds.py:47-48` (`due`, started initiative) | integrate round for a started initiative with no capability-proposal, no work-item | r93 says "neither a capability-proposal nor a work-item"; code also requires no glossary-proposal (F2). Needed for r164 and r161 to be reached | by search: the r93 scenarios (`features/supervision.feature:1406-1416`, `:1596`, `:1611`, `:874`) do not set a glossary-proposal, so the glossary branch is not in them: none | Read; branch review F2 |
| `scripts/supervise_done.py:28-37` (`set_glossary_done`) | sets `done` unless already `done`; no check on abandoned | r161 covers only started-equivalent initiatives; an `abandoned` one run by name moves to `done` (branch review observation) | none (searched: r161 scenario `features/supervision.feature:1810` is the only test; no abandoned glossary-only case) | Read `supervise_done.py:31-32`; branch review observation |
| `scripts/supervise_done.py:28-37` (`set_glossary_done`) | checks only `glossary_only_done`, not requests | r105 checks each kept request is `delivered` (`supervise_done.py:43` via `workqueue_done.holds`); r161 is silent on requests (branch review observation) | none (the r161 scenario has no request) | Read; branch review observation |
| `scripts/supervise_glossary.py:29-31` (`route`) | an `awaiting-answer` glossary-proposal with no question returns None, so nothing routes it | if F1 is fixed by option B (no approval question for glossary), a gate round with no question leaves the proposal `awaiting-answer` with no question and no route | none (no scenario gives a glossary gate with no question) | Read; a consequence of F1 option B |

## 3. Tests the requirements make impossible to keep

`by search`, no map. The accepted lines add routes and do not change an existing assertion. Searched `tests/` and `features/` for: the approval question text ("approved as drafted", "lines as drafted"), "neither a capability-proposal nor a work-item", and `set_glossary_done` / `glossary_only_done` / "abandoned".

- None that fails with the accepted lines as they are: the seven scenarios pass (section 1).
- Option A for F1 (keep the glossary approval question) breaks nothing that exists, but needs a line first: no test asserts it.
- Option B for F1 (limit the r117 branch to `capability-proposal`) breaks: none found. The r117 test (`tests/scenarios/supervision_rounds_steps.py:79`) asserts the capability case only.
- r93's integrate path (F2) is not changed by w227 (the findings leave it to q35).

## 4. The file set

Read: the accepted lines need no code change (section 1). The file set is the findings' fix-now item F1, plus optional items.

- `scripts/supervise_rounds.py` (274 lines; room 26 under 300): F1. Option A: no code change, integrate q36 line 1 first. Option B: restrict `if kind == "gate" and not asked` (line 159) to capability-proposals, and route a glossary gate with no question (`supervise_glossary.py` `route`, line 29). Found: Read of `:159-161`, branch review F1.
- `scripts/supervise_glossary.py` (103 lines; room 197): option B only, `route` for a glossary `awaiting-answer` with no question. Found: Read.
- `scripts/supervise_done.py` (48 lines; room 252): optional, the abandoned guard (`:31`) and the request check (`:32`, `set_glossary_done`). Not a fix-now finding; no line asks for either. Found: Read.
- Test files: none required by the accepted scenarios. A test of option B needs a line that says so (r117 widened), so it waits on an integrate round.
- Module path, not edited: `scripts/supervise.py` (295 lines; room 5) calls `set_glossary_done` at `:231`; `scripts/supervise_brief.py` (216; room 84) at `:86`; `scripts/supervise_change.py` (140; room 160) writes `glossary.md` at `:133-139` (F3, not in w227's findings fix-now); `tests/scenarios/supervision_rounds_steps.py` (274 lines; a step module, room 26) holds the r117 step.
- `CLAUDE.md` module row for `scripts/supervise_glossary.py` lacks the routing (F6). Not a production or test file; optional.

Decision for the planner (the person decides, not this research): F1 has two readings. A keeps the approval question for glossary-proposals and needs q36 line 1 integrated first. B restricts r117 to capability-proposals and gives a glossary gate with no question a route (the spec's r130 would say "next transition", but r169 says `awaiting-answer`). Both are stated; neither is chosen here.
