---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-l3
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Layer 3 gate: merge of P8–P11

## What merged

`gfc/P8` (67aa6e13), `gfc/P9` (f284511a), `gfc/P10` (422736d0) and `gfc/P11` (39c0064e) were merged into
`gf-conversion` in plan order with `--no-ff`, with no conflicts. P8's extra file `tests/scripts/test_supervise_brief.py`
is accepted. report-P8 to report-P11 were written from the packages' notes.

## Shared changes made at the merge

- **`model parse --file` parses a codified file's statements (asked by P9, P10, P11), test first.**
  `model_report.cmd_parse` now reads a codified capability file's requirements through `spec_read.capability`, and a
  codified `spec/universal.md` through `read_universal`, numbered by the file's own lines; any other file is still
  parsed line by line. Tests: `test_model_output.py::LanguageCommandsTest::test_parse_a_codified_file_*` and
  `test_parse_the_universal_file_parses_its_conditions`. Every capability file and universal.md now exits 0.
- **Term collisions (P9's ask).** The merge gave five terms twice (lexicon v_t6, model check v_t2): commit (event),
  relocate (event), use (event), test (kind), violation (kind). Each now has one entry in the `spec/index.md` glossary
  and the capability entries are deleted. `model lexicon --check`: 335 terms, 0 problems.
- **v15i role-boundaries#r8 (P9's ask).** i59's open proposal adds the 0.29 id role-boundaries#r8, so the converted
  file's fresh r8 was a reuse. The planner's Edit statement now has id r23, as P10 skipped r37–r45. The 1.0.0 upgrade
  (P13) should still decide how open proposals' adds of 0.29 ids are rewritten.
- **LiveRestatesTest (P9's ask).** `test_model_restates.py` now asserts supervision, not spec-migration, is unrestated.

## Gate (SHOPSYSTEM_GF unset, P1's install)

- `model check`: no v_p*, v15[g-k] or v_t[4-6] row (rows left: v10a 19, v17 24, v3 8, v_d1 9; 398 unresolved
  references, expected until P13/P14 rewrite .shop/work references to @0.29).
- `model logic <c>` exits 0 for all 18 capabilities other than supervision.
- `model restates <c>` exits 0 for each of the 18. With no name it exits 1: 164 ids of supervision itself are missing,
  because an uncodified capability has nothing dropped (model_restates' docstring, design §15). Moves into supervision
  show as pending (11). The gate's "exits 0" is read as for the 18 converted capabilities; P12 makes the whole run 0.
- `features generate --check` exits 0 and skips only supervision.
- Cold compile: `XDG_CACHE_HOME=$(mktemp -d) model parse --file spec/capabilities/work-queue.md` exits 0 in about 3 s
  (bound 180 s). No split of `Typed` is needed.
- Suite: 15 failed, 961 passed. 4 are baseline failures; the 11 others are exactly the test_supervision scenarios
  listed in `p8-broken.md`. 19 baseline failures are gone (their tests were deleted or rewritten by the conversion).
- Common checks: `tools size --limit 300` exits 0; `tools check` and ruff clean.

## Carried forward

- P12: rewrite the 11 p8-broken scenarios and restate the new formulate and integrate-check flow; restate the moved
  formulation and spec-integration lines; merge with P11's shared handler keys (or move them to world_*.py).
- P13: open proposals (i59) add 0.29 ids that are now live fresh ids elsewhere; about 400 unresolved/v3 rows from
  .shop/work references to 0.29 ids; `migrate_spec.plan_holding` still runs the removed `features deprecate`.
- P14: README.md (feature-formulator, removed features commands), agents/bdd-implementer.md and three skills name the
  removed commands; CLAUDE.md rows (supervise*.py formulate sessions, features*.py 'editing', the L3 rows in the
  reports); dead `features_gherkin.locate/locate_in`; the `migration_upgrade_steps.py` shim.
- Orchestrator before layer 4 (optional): features_generate's StopIteration in `precondition`, lost given-block
  condition values, the lower-case instance letter, `resolve()` picking relations by term alone; the SDoesTo DoTo
  guard; vocab's catch-all for a kind with no instance; world_nodes' GivenK_A writing every attribute as status.
