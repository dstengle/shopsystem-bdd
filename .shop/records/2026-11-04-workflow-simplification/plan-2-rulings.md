---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-2-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Plan 2 of the workflow simplification: rulings on the review, and what was done with each finding

`plan-2-review.md` asked the person two questions (Q1, Q2). The person was not available. Each ruling below was
**ruled by the main session without the person, 2026-11-04; revisit.** The fixes are on branch
`workflow-simplification` after `8466e5a6` (the review): `52eb8076` (backlog), `4a9dda31` (scenarios) and `da16825b`
(`scripts/work`).

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-04; revisit) | What was done |
|---|---|---|---|
| Q1 | Does a dependency on a withdrawn or refused item block for good? | Keep D9's display (`blocked by … (withdrawn)`). Refuse `work depend` on a target that is `refused` or `withdrawn` now. Dropping a dependency comes in plan 4. | `52eb8076`: `work depend` refuses such a target, naming its label and status; `test_depend_refuses_a_closed_target`. backlog's `## Not yet` names `work depend <item> --drop <item>` for plan 4, and its `## Implementation, may change` the refusal. |
| Q2 | Should a negated Then require a successful run? | No. An "the item is not …" Then requires only that the command exists; its exit code is left to the line that builds it. | `4a9dda31`: the Then fails on a usage error (exit 2) instead of on any non-zero exit. batches#r3 stays an expected failure, on argparse's `invalid choice: 'batch'`. |

## The findings

| # | What was done |
|---|---|
| S1 | Fixed in `52eb8076`. `work depend` prints `b2 "…" depends on b1 "…"`; `work show` prints `depends on: b1 "…", b9 (missing)`. Each line has a script test. |
| S2 | Fixed in `4a9dda31`, as Q2. |
| M1 | Known, not fixed. The reviewer's count check would not catch the mutation either: r6's items are all `idea`, so a heading wrongly `idea` with the right count still passes. Catching it in the scenario needs items in two states, which the line does not give. `test_tables_come_in_state_order_and_skip_empty_states` and `test_every_column_of_a_row` catch it. |
| M2 | Known, noted only: r8 runs on an empty backlog; `test_json_is_one_object_in_table_order` pins the content. |
| M3 | Fixed in `52eb8076`. `backlog_items.names` refuses any `.md` in `.shop/backlog/` whose stem is not `b<n>`, as `<rel>: id: the file name is not b<n>`. `items()` and `next_name` both read through it, so `work backlog`, `work show --json` and `work idea` refuse; `work idea` now refuses where it numbered past the file before. |
| M4 | Fixed in `52eb8076`: `kind` other than `item` is refused, naming the field; added to the parametrised malformed-file test. |
| M5 | Fixed in `52eb8076`: `from workqueue_answer import LINE_BREAKS`. |
| M6 | Fixed in `52eb8076`: the test writes an `awaiting-answer` work-item with its `log.jsonl` transition from `done`, runs `work answer w1 x --change` and compares stdout, the file, the log's moves and the commit subject with `workqueue_answer.answer` on a copy of the repository. |
| M7 | Fixed in `da16825b`: the 11 `# noqa: E402` dropped; `tools check` on the branch's files and `scripts/work` is clean. |
| M8 | Fixed with Q1. |
| M9 | Known, noted only: `b0` and `b01` are not item ids, so `work show b01` goes to the work-queue and says it has no such work-item. |
| M10 | Noted for later plans, not edited in `plan-2-backlog.md` (a record). A smoke step that runs `work` repeatedly uses a shell function, which bash and zsh both run: `r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }`, then `W idea "…" && W backlog`. Plan 2's smoke steps ran this way under zsh and bash and gave the expected tables. |

## Verification after the fixes

| Check | Got |
|---|---|
| `python3 -m pytest -q` | 1066 passed, 1 failed, 1 skipped, 37 xfailed, 129 subtests. The failure was the known flake `test_model_logic_on_the_live_spec_is_fast`, which passed alone: **1067 passed** (1059 + 8 new script tests). |
| `model check \| tail -1` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems |
| `model logic \| tail -1` | 11 findings: 6 L5, 5 L6 |
| `model lexicon --check \| tail -1` | 401 terms, 0 problems |
| `features generate --check` | exit 0 |
| `features vocab --check \| tail -1` | every step has one handler |
| `features bindings --unbound` | every binding names a scenario |
| `tools size --limit 300` | silent, exit 0 |
| `tools check` over the branch's Python files and `scripts/work` | ruff, vulture and import-linter clean, exit 0 |
