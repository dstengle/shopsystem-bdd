---
id: i3
title: Requirement ids in the format the plugin teaches
summary: Consuming repositories' capabilities carry [r<n>] ids, scenarios name them by @r<n>, proposals list adds/changes/removes by id, and the gate approves lines with their ids.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 1
source: [obs/2026-10-15-design-model-v3]
date: 2026-10-15
---

Reaches: `docs/capability-format.md`; spec-integration (the gate shows lines with their ids, and the spec
commit names them), formulation (`@r<n>` tags, free titles, held scenarios untouched), spec-migration (ids
added to a repository already on capability files, and tags on a first migration), feature-file-tools
(`features tag` takes `r<n>`; `rebind` stays as it is); the capability-writer and feature-formulator briefs.
One capability-proposal per capability, `requirement-ids/<capability>`. Released as 0.19.0.

The open question of holding is decision/held-scenario-formulates-no-requirement. Not in this release, so
that one workflow change is measured at a time: decisions as files with a generated index in consuming
repositories (`model` reads their ledger meanwhile: decision/model-reads-a-ledger); a `features ids` check,
which `model check` makes unneeded; changes to `rebind`, since a changed line's scenario keeps its title and
needs no rebinding.

Released in 0.19.0 on branch 0.19.0-requirement-ids, 2026-10-16; awaiting the gate and a measured batch.
