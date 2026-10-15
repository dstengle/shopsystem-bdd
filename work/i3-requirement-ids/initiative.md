---
id: i3
title: Requirement ids in the format the plugin teaches
summary: Consuming repositories' capabilities carry [r<n>] ids, scenarios name them by @r<n>, proposals list adds/changes/removes by id, and the gate approves ids.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 1
source: [obs/2026-10-15-design-model-v3]
date: 2026-10-15
---

Reaches: `docs/capability-format.md`; spec-integration (the gate shows ids), formulation (`@r<n>`, free
titles), spec-migration (ids assigned in migration), feature-file-tools (a `features ids` check; `rebind`
kept only for repositories not yet migrated); the capability-writer and feature-formulator briefs;
decisions as files with a generated index. One capability-proposal each, under this initiative.
Open: what holding does when a held scenario and its replacement name the same id
(decision/held-scenarios).
