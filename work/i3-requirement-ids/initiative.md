---
id: i3
title: Requirement ids in the format the plugin teaches
summary: Consuming repositories' capabilities carry [r<n>] ids, scenarios name them by @r<n>, proposals list adds/changes/removes by id, and the gate approves ids.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 1
source: [obs/2026-10-15-design-model-v3]
date: 2026-10-15
---

Reaches: `docs/capability-format.md`; spec-integration (the gate shows ids), formulation (`@r<n>`, free
titles), spec-migration (ids assigned in migration), feature-file-tools (a `features ids` check; `rebind`
kept only for repositories not yet migrated); the capability-writer and feature-formulator briefs;
decisions as files with a generated index. One capability-proposal per capability, `requirement-ids/<capability>`. Released as 0.19.0.
The open question of holding is decision/held-scenario-formulates-no-requirement. Not in this release, so
that one workflow change is measured at a time: decisions as files with a generated index in consuming
repositories (`model` reads their ledger meanwhile: decision/model-reads-a-ledger); a `features ids` check,
which `model check` makes unneeded; `rebind`, which stays as it is, since a changed line's scenario keeps its
title and needs no rebinding.
