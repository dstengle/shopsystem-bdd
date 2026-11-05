---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-2-0-layout
summary: "What a consuming repository keeps under .shop/ in plugin 2.0: the backlog, batches, requests, quotes, records, the plugin version and the delivery settings, and plugin 1.x's queue frozen as history."
date: 2026-11-05
status: accepted
tier: judgement
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-9]
by: "workflow simplification plan 9, decided by the planner; revisit"
---

# 0081. The 2.0 layout

## Context

Decision 0026 gave the forms of `.shop/work/`: initiatives, their parts and records. Plugin 2.0.0 freezes
`.shop/work/` (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired); what of 0026
survives is restated here.

## Decision

A consuming repository keeps, beside `spec/` and `features/`:

- `.shop/backlog/b<n>.md`, one item each;
- `.shop/batches/<n>/`, one batch each, its plan and what its tasks and review left;
- `.shop/requests/q<n>.md`, one live request each, numbered above the frozen ones;
- `.shop/quotes/<n>.md`, the person's words kept with the turns around them;
- `.shop/records/`: records with `id`, `kind` and `about` in their frontmatter, and `observations.md`, one
  `## <id>` heading an observation with its `about:`, `by:` and `date:`;
- `.shop/plugin-version`, the plugin release the repository is on;
- `.shop/delivery.toml`, the batch settings and prices, optional;
- `.shop/work/`, plugin 1.x's queue, frozen: nothing writes it, and `model check` reads only the `source` of its
  initiatives and requests, as citations of observations.
