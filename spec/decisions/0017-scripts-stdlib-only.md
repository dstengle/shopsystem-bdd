---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/scripts-stdlib-only
summary: "The plugin's scripts are plain Python 3 on the standard library; --help is each one's contract."
date: 2026-10-07
status: accepted
revisit_when: "a script needs an engine the standard library lacks"
revisit_signal: requests
by: "0.10.0 (72d33af); README, Scripts"
---

# 0017. Scripts stdlib only

## Decision

Scripts under `scripts/` use only the standard library and are tested with `python3 -m unittest discover -s tests/scripts`. Their `--help` text is the contract.

## Context

Scripts run in projects whose environments the plugin does not control.

## Alternatives

A packaged CLI with dependencies.

## Consequences

`tools` drives the project's own analysis tools rather than depending on them. `model check` needs a solver: see design-decision/model-check-solves-with-clingo.
