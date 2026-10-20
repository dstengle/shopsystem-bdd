---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-takes-the-dependencies-it-needs
summary: "The plugin and its scripts take the dependencies they need (clingo, pytest, pytest-bdd), each named in the plugin's documentation."
date: 2026-10-19
status: accepted
supersedes: design-decision/scripts-stdlib-only
by: "the person, 2026-10-19"
---

# 0035. The plugin takes the dependencies it needs

## Decision

The plugin and its scripts take the dependencies they need: clingo, pytest and pytest-bdd today. Each is named in the plugin's documentation, with the command that installs it. A script's `--help` stays its contract.
