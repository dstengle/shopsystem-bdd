---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/superpowers-not-a-dependency
summary: "The plugin declares no dependency on superpowers and invokes none of its skills; a brainstorming note stays one possible source of a proposal."
date: 2026-10-19
status: proposed
supersedes: design-decision/superpowers-dependency
source: [initiative/i10]
by: "the person, 2026-10-19"
---

# 0042. Superpowers is not a dependency

## Decision

`.claude-plugin/plugin.json` has no `dependencies`. No skill, agent or script of the plugin names a superpowers
skill or a superpowers path; delivery is `delivering-an-initiative` and `work run`. The README names clingo,
pytest and pytest-bdd as the plugin's dependencies (design-decision/plugin-takes-the-dependencies-it-needs).
