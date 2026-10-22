---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/upgrades-between-plugin-releases
summary: "A repository on the final layout records the plugin version it is on, and `migrate upgrade`, offered at a session's start and run on the person's yes, is the general means for every change a later release makes to its files."
date: 2026-10-22
status: proposed
source: [design-decision/work-items-named-by-ids]
by: "the person, 2026-10-22 (\"Please create a more general purpose migration capability\"), delegating the drafting decisions to the coordinator; on the design note work-item ids and plugin upgrades (0.24.0)"
---

# 0062. Upgrades between plugin releases

## Decision

`migrate run` takes a repository from the old system to the final layout; an upgrade takes a repository on the
final layout from one plugin release to the next, and is the general means for every later change a release makes
to a repository's files, work-item ids being the first. A repository records its plugin version in
`.shop/plugin-version`; one with `.shop/` and no record is on 0.23.1, the last release without one. The plugin holds
a list of upgrade steps, each with the version that introduced it and a one-line description; `migrate upgrade`
applies the pending ones in one commit, all or none. The plugin's SessionStart hook offers the upgrade to the person
when a step is pending, and runs it only on their yes. Releases before 0.24.0 have no steps: earlier upgrades were
by hand.
