# Plan 6 of the workflow simplification: rulings on the review

The questions of `plan-6-review.md`, **ruled by the main session without the person, 2026-11-05; revisit**. Then what
was done with each finding, and what is left for plan 9.

## Rulings

- **Q1 (D6): keep design-model-check r52 unchanged.** The precedence rule was already ruled by the person on
  2026-11-04, in `spec/universal.md` § "An "If" line takes precedence" (commit `5e6a427c`): an EARS "If" line
  (`IfThen`, `WhileIf`, `WhereIf`) takes precedence over every non-"If" line on the same trigger. It covers both
  pairs. r52 ("Where `--check` is given, when the person runs `model decisions` on a decisions index …") is a
  non-"If" line on the trigger "the person runs `model decisions`" with `--check`; r51 (`WhereIf`, the same trigger and
  feature, a stale index) and decision-tiers r5 (`WhileIf`, "the person runs `model decisions --check`", a failing
  `check` decision) are "If" lines on that trigger. No sentence is added; decision-tiers' Implementation bullet now
  cites the rule.
- **Q2: 0042 is superseded by a new 0077** (`superpowers-composed-not-required`). It keeps "no `dependencies` in
  `plugin.json`, the README names clingo, pytest and pytest-bdd" and allows a skill to name a superpowers skill it
  composes with, never requiring it. `tier: judgement`: no test checks `plugin.json` today. The totals are now 76
  decisions, `{accepted: 27, superseded: 47, rejected: 2}`, in force `{check: 4, requirement: 15, judgement: 8}`.
- **Q3: 0006 stays as it is until plan 9** (below).
- **Q4: 0026 stays superseded** (history); plan 9 restates what survives (below).

## The findings

| # | Done | Commit |
|---|---|---|
| S1 | A run holds only when pytest exits 0, its summary line counts a `passed` and no `skipped`, `xfailed`, `xpassed` or `deselected` (`not run: …`, `nothing passed`). Tests: `test_a_test_that_is_skipped_or_xfailed_is_failing[skipped, xfailed]`, red first. | `5d607da8` |
| S2 | `of_repository`: an entry that is an option or whose file does not resolve under the root; `run` refuses it unrun (`not a test of this repository: <entry>`), `wrong()` gives the file problem. Tests for `--co` and `../outside.py`, red first. | `5d607da8` |
| S3 | `tools_env.project_python(root)`, the lookup `interpreter(args)` now calls; `run` uses it. Test with a stub `.venv/bin/python`, red first. | `5d607da8` |
| S4 | 0053's `enforced_by` narrowed to `tests/scripts/test_agents.py::RoleBoundaries`, which holds. The stale table is for plan 9. | `ac6bc45d` |
| S5 | r32 dropped from 0047. The re-pointing is for plan 9. | `ac6bc45d` |
| M1 | The contract and the D5 bullet: nothing of its own written; what a decision's tests write is the tests'. | `5d607da8` |
| M2 | `Decision.runs`: `check` and not `superseded`/`rejected`, used by `check_tests` and `readiness_bar.rested_on`. Tests in both, red first. | `5d607da8` |
| M3 | A requirement entry is one in `<capability>#r<n>` / `#r<a>-r<b>` form; any other is a test. Test, red first. | `5d607da8` |
| M4 | The bullet reads "`w_untiered` is a warning; a decision gives its tier as `tier:` in its frontmatter." | `5d607da8` |
| M5 | For plan 9 (below). | — |
| M6 | Left as an idea: a `w_unsuperseded` warning needs a line first. | — |
| M7 | No change (the person's call). | — |

## For plan 9

- **0006 (Q3):** supersede it with a `check` decision "feature files are written only by `features generate`", on the
  same test (`test_decision_checks.py::test_the_features_are_what_features_generate_writes`).
- **0026 (Q4):** plan 9's decision on the 2.0 layout restates the records forms that stay: `records/observations.md`
  (one `## <id>` heading an observation, with `about:`, `by:`, `date:`) and the other records' frontmatter (`id`,
  `kind`, `about`), beside `.shop/backlog/b<n>.md` and `.shop/batches/<n>/`.
- **0053 (S4):** its table is stale (lists `feature-formulator`, lacks `batch-analyst`, `delegation-answerer`,
  `pr-reviewer`, `trial-runner`); supersede it with the new agent set.
- **0027, 0036, 0047 (S5):** re-point their `enforced_by` to lines on items (for example a backlog line that refuses
  a reference not in `<capability>#r<n>` form), or drop them to `judgement`, in the commit that retires
  design-model-check r31, r33 and r37; otherwise `test_the_live_decisions_keep_their_tiers` turns red.
- **M5:** the `migrate upgrade` 2.0.0 step regenerates `spec/decisions/index.md`, whose `tier` column makes every
  older index stale. A base exit of 1 for `model decisions --check` in a pull request brief across this change is
  expected.
