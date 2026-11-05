---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/superpowers-composed-not-required
summary: "The plugin declares no dependency on superpowers; a skill may name a superpowers skill it composes with, and never requires it."
date: 2026-11-05
status: accepted
tier: judgement
supersedes: [design-decision/superpowers-not-a-dependency]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]
by: "the main session without the person, 2026-11-05 (plan 6's review, Q2); revisit"
---

# 0077. Superpowers is composed with, not required

## Decision

`.claude-plugin/plugin.json` has no `dependencies`, and the README names clingo, pytest and pytest-bdd as the
plugin's dependencies (design-decision/plugin-takes-the-dependencies-it-needs). A skill of the plugin may name a
superpowers skill it composes with, as shaping-items names superpowers:brainstorming and building-a-batch follows
superpowers' subagent-driven development, and it works when superpowers is not installed. It replaces 0042, whose
"no skill names a superpowers skill" the simplified workflow (design goal 5) no longer keeps.
