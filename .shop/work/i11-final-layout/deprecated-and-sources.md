---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/deprecated-and-sources
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: green
wkind: capability
under: design-model-check
accepts: [design-model-check#r20, design-model-check#r26, design-model-check#r29, design-model-check#r51, design-model-check#r64]
blocked_by: [work-item/final-layout-read]
fileset: [scripts/model, tests/scenarios/test_design_model_check.py, spec/decisions/, .shop/records/]
---

# @deprecated read, @holding refused, decisions' sources as ids

Goes green: the scenarios of the lines listed, and `model check` on this repository still exits 0.

`scripts/model`:
- `read_features` skips a scenario tagged `@deprecated` (r44, r26's title check); a scenario tagged
  `@holding` is a file problem `<path>: scenario "<title>" is tagged @holding; the tag is @deprecated`
  (r62) and is otherwise read like any scenario.
- `mention()` and `read_mentions`: text inside backticks and double quotes, and `@<word>` tokens, are
  removed before matching (r51), in requirement text and in scenario titles and steps.
- `read_decisions`: a file with no `## Decision` heading is a file problem (r63); each `source` entry is
  qualified and wanted with kind None (r24, r64), and no `source` fact is written; `by` is not read.

This repository (a migration):
- Each Markdown file under `.shop/records/` but `observations.md` and `README.md` gets frontmatter where it
  has none: `id: <kind>/missingmass.io/shopsystem/shopsystem-bdd/<file stem>`, `kind`, `about:
  bounded-context/missingmass.io/shopsystem/shopsystem-bdd`, `date` from the name. Kinds:
  `archive/design-notes/` decision-argument; `archive/plans/` and `archive/requests/` initiative-archive;
  `measurements/fixture-runs/` measurement. Nothing else in a record changes.
- Each decision's `source` string becomes `source: [<ids>]` and `by: "<the rest>"`: a part naming a record
  by path becomes that record's id (`records/archive/design-notes/2026-10-11-green-suite-design.md` →
  `decision-argument/2026-10-11-green-suite-design`; `records/measurements/fixture-runs/2026-10-12-spec-round-test-log.md`
  → `measurement/2026-10-12-spec-round-test-log`; `work/i3-requirement-ids/initiative.md` → `initiative/i3`;
  `design-decision/<x>` and `observation/<x>` stay as ids); every other part (the person and a date, a
  release, a commit, README sections, `docs/design-model/…`, other repositories' decisions) goes to `by`,
  parts joined with "; ". Thirty-six files; `model check` must report no unresolved source.
- `spec/decisions/index.md` regenerated.

Accepts re-synced 2026-10-19 to the EARS lines (initiative/i13): design-model-check#r44 -> r20; design-model-check#r62 -> r26; design-model-check#r63 -> r29.
