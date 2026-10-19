---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i8
title: Migrate a consuming repository to design model v3
summary: Migration tools only, that take a consuming repository from the old system to the final layout of design model v3; the plugin keeps nothing of the old system beyond them.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 3
source: [review-finding/2026-10-13-kb-and-bdd-assessment]
date: 2026-10-15
---

Rewritten 2026-10-19 to the person's direction: there is no intermediate state in a consuming repository,
only the final one (the layout of initiative/i11) and the tools that move a repository there. shopsystem-kb
and shopsystem-knowledge move after the plugin itself is on the model.

Covers:
- adding ids to a repository already on capability files (shipped in 0.19.0, spec-migration);
- the decision ledger in `spec/decisions.md` to one decision file each, with a generated index;
- living slice plans to work-items;
- `@holding` scenarios to `@superseded`;
- the repository layout: `spec/decisions/`, `.shop/work`, `.shop/records`.
