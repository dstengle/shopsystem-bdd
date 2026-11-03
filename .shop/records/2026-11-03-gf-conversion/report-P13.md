---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p13
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# P13 report: the 1.0.0 upgrade step

Branch `gfc/P13`, off `gf-conversion` at 76e79f3e.

## What was built (tests first)

- `scripts/migrate_upgrade_codified.py` (new, 252 lines): the step's `plan(root)`, as the 0.24.0 and 0.25.0 steps do it.
  - **`spec/restated.json`, when it is missing.** It is written from the live `[r<n>]` lines of each capability without
    `language: codified-1`. The step has its own copy of the 0.29 Behaviour reader, because P14 deletes
    `model_legacy.py`. On a copy of the repository at 96818f71 the file it writes is byte-identical to the frozen
    `spec/restated.json` (581 ids).
  - **The scaffold.** Each uncodified capability's Behaviour becomes one group for each old line, titled with its old
    `###` heading and its id. Each group has `Restates: r<n>@0.29.` and the old text as an HTML comment. There are no
    requirement bullets and no marker. `retired:` becomes `[]`, because fresh ids start again from r1, and the file
    gains a `## Dropped` section. Codified files are skipped.
  - **Deprecated scenarios.** Every scenario tagged `@deprecated` under `features/` is deleted. Lines inside a
    docstring are treated as text, which matters because migration-tools.feature now holds a feature inside a
    docstring. The function is `without_tagged(text, tag)`, so `migrate run`'s `@holding` can reuse it (see asks).
  - **Old references.** Every `<cap>#r<n>` under `.shop/work/**` becomes `<cap>#r<n>@0.29`, whether it is written bare
    or as `capability/[<this context path>/]<cap>`. The capability must be one the repository has, or a key prefix of
    restated.json. Another context's references are left alone, and so is anything already `@0.29`. A range is
    listed id by id; a YAML block item becomes one item for each id.
    - Which files predate the conversion: every tracked file when the step writes restated.json itself. Otherwise,
      only files tracked at the commit that first added restated.json, and in a file changed since then only the lines
      it had at that commit (so lines appended to a log later are kept as they are).
  - **The report (`notes`).** It names restated.json when the step writes it, each scaffolded capability with its
    group count, the glossary when `spec/index.md` has no marker, and each open capability-proposal (status not
    merged, formulated or withdrawn).
    - This is the call on the carried item "open proposals (i59) add 0.29 ids". Their references are rewritten to
      `@0.29` like every other reference. They name lines in 0.29 form that the codified spec cannot take, so the step
      reports them for a session to re-integrate rather than guessing new ids.
- `scripts/migrate_upgrade.py`:
  - STEPS gains `1.0.0 "codified requirements"`.
  - The upgrade collects each step's `notes`, prints them after `upgraded to …`, and adds them to the commit message.
    It is still one commit.
- `spec/capabilities/migration-tools.md`:
  - New group g29 (r53–r56): it prints restated.json and the scaffolded capability, and it rewrites the capability,
    the feature and the work-item.
  - A new Implementation bullet describes the step.
  - The given blocks of g18, g24 and g27 now hold "1.0.0" instead of "0.29.0", so they stay true after P14 bumps the
    version.
  - `features/migration-tools.feature` is regenerated.
- `tests/scenarios/migration_old.py`: `plugin()` returns the plugin the scenarios run. While plugin.json is below
  1.0.0, that is a one-time temporary copy of `scripts/` and `hooks/` whose plugin.json says 1.0.0. Once P14 sets 1.0.0
  it is the plugin itself, with no copy.
- `tests/scenarios/migration_tools_handlers.py`:
  - migrate runs and hooks use `plugin()` (runs still go through `vocab.runner`, so the U checks see them).
  - `upgraded` compares against `plugin()`'s version.
  - EXPECTED has entries for g29's three files.
- `tests/scripts/test_migrate_upgrade_codified.py` (new, 13 tests):
  - the plan on a small fixture (restated text and line, the scaffold, the codified skip, deprecated deletion with a
    docstring, references and ranges, the report, open proposals);
  - a converted fixture, where only the references that predate restated.json and `.shop/plugin-version` change and
    nothing is reported;
  - a copy of the repository at 96818f71. One commit writes the scaffold of all 19 capabilities and restated.json
    (identical to the frozen one), deletes the deprecated scenarios and rewrites the references, and the output
    reports the capabilities and the glossary.

## Checks

- `pytest -q tests/scripts/test_migrate_upgrade_codified.py tests/scripts/test_migrate_upgrade.py tests/scenarios/test_migration_tools.py`: 44 passed.
- `model parse --file spec/capabilities/migration-tools.md`, `model logic migration-tools` (2 L2 findings, exit 0),
  `features generate --check migration-tools`: all exit 0. `model restates migration-tools` exits 0, and
  `features vocab --check` says every step has one handler.
- `tools size --limit 300` exits 0. `tools check` and ruff are clean on the changed files.
- Full suite (SHOPSYSTEM_GF unset, P1's install): 15 failed. 4 are in the baseline, and the other 11 are exactly the
  test_supervision scenarios in `p8-broken.md` (P12's), as at the layer 3 gate. None is new.
- `model check`: no v_p*, v15[a-k], v_t* or v_s* row. Unresolved references are still 398, unchanged, because the step
  is not run here.
- Dry run on a copy of this branch (HEAD archived, plugin forced to 1.0.0): it exits 0 and reports
  `supervision.md (164 groups)`, which is uncodified until P12. The other 18 capabilities are skipped.

## Asks and notes for the orchestrator and P14

- **Unresolved 0.29 references after the run.** About 650 rewritten references name 0.29 ids that were already
  retired at 96818f71, such as `feature-file-tools#r22`, which i1 added and a later change retired. restated.json
  holds only the ids that were live at 96818f71, so `model check` reports each one as "names no 0.29 id of
  spec/restated.json". Before the rewrite they were unresolved too. Two possible fixes, both outside P13:
  - `model_facts.resolve_req` accepts any `@0.29` id as history;
  - the step also records the 0.29 `retired:` ids (a new file or a new restated.json form).
  P14 owns model_facts.
- **`migrate_spec.plan_holding` still runs `features deprecate`** (not P13's file). Suggested fix: delete each
  `@holding` scenario with `migrate_upgrade_codified.without_tagged(text, "@holding")` instead of deprecating it,
  which agrees with r3@0.29's Dropped reason.
- **P14 runs `migrate upgrade`** on this repository after P12. The step will then skip every capability, write no
  restated.json, rewrite the references in the files tracked at a344b533, and report i45's and i59's open proposals.
- **Extra file:** `tests/scenarios/migration_old.py` is P13's (it matches `tests/scenarios/migration_*.py`).
  `migration_upgrade_steps.py` is unchanged and is still the shim P14 removes.

## Module-map row (for P14)

| `scripts/migrate_upgrade_codified.py` | the 1.0.0 upgrade step "codified requirements": `spec/restated.json`, the scaffold of each uncodified capability, `@deprecated` scenarios deleted, old references written `<cap>#r<n>@0.29`, and what is left reported |
