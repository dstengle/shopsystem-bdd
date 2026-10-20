---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/decision-files-taught
kind: work-item
part_of: capability-proposal/final-layout-spec-integration
status: green
wkind: capability
under: spec-integration
check: "the T-integrate fixture case with a note that makes one decision, run 3 times with claude -p against the plugin's working copy: each run writes spec/decisions/<next n>-<slug>.md with a summary and a Decision section only, its source ids and by, spec/decisions/index.md current (model decisions --check exits 0) in the spec commit, and no file under .superpowers/ or docs/superpowers/; results in .shop/records/measurements/fixture-runs/"
blocked_by: [work-item/deprecated-and-sources]
fileset: [agents/capability-writer.md, agents/initiative-round.md, skills/integrating-a-proposal/SKILL.md, docs/capability-format.md, skills/formulating-features/SKILL.md, skills/checking-spec-consistency/SKILL.md, agents/feature-formulator.md, agents/spec-checker.md]
---

# The writers write decision files, under the final layout

spec-integration#r20-r22 have no scenarios (workflow; design-decision/workflow-scenarios-run-as-fixture-sessions),
so the check is fixture runs.

- `agents/capability-writer.md`: "The ledger" section becomes "Decisions": a new decision is a whole file
  `<drafts>/round-<n>/spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest in `spec/decisions/`,
  frontmatter as design-decision/light-decisions, `source` ids and `by` words; no `decisions.append.md`.
  Its description and the paths it may read (`spec/` includes `spec/decisions/`).
- `skills/integrating-a-proposal/SKILL.md` and `agents/initiative-round.md` (`apply`): copy decision drafts
  into `spec/decisions/`, run `scripts/model decisions`, commit the index with `spec/`; delegation goes in
  `by`. The spec is `spec/index.md`, `spec/decisions/`, `spec/capabilities/`.
- `docs/capability-format.md`: Layout (the tree of design-decision/final-layout); the capability file without
  `formulated_as` and "the feature file is `features/<name>.feature`"; "The decisions file" becomes "Decision
  files" in the light form, with one worked example; the sentence kinds table (`spec/decisions/`); Checking
  (reads the final layout; labels from rule-labels); requirement ids' paragraph on ledger headings goes.
- Drafts paths: `.superpowers/spec-drafts/` → `.shop/scratch/drafts/` in integrating-a-proposal,
  formulating-features, checking-spec-consistency, initiative-round, capability-writer, feature-formulator,
  spec-checker; the `.gitignore` step adds `.shop/scratch/`.
- Fixture: extend the scratch harness's T-integrate case (`/home/vscode/scratch/shopsystem-bdd/`, the shelf
  fixture) to the final layout and a note with one decision; score the checks above.
