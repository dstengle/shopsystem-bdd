---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-analysis-tools
kind: capability-proposal
part_of: initiative/i11
status: formulated
date: 2026-10-19
argues: [analysis-tools]
changes: [analysis-tools#r8, analysis-tools#r14]
---

# Analysis tools: the map under .shop/scratch

`tools map` keeps its map in `.shop/scratch/tools/coverage` (r8), since the plugin no longer uses
`.superpowers/` (design-decision/final-layout). r14's "files holding them" becomes "files that contain them".
The proposed file is `capabilities/analysis-tools.md`. This capability's scenarios are the first to move to
pytest-bdd (work-item/analysis-tools-scenarios).

r4 ("the line to give `plan log`") is left to initiative i10, which removes `scripts/plan`.
