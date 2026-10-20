---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/bindings-unbound
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: green
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r57-r58]
blocked_by: [work-item/feature-file-tools-scenarios]
fileset: [scripts/features, tests/scenarios/test_feature_file_tools.py]
---

# features bindings sees scenarios() and finds what nothing binds

Goes green: r57-r59's scenarios.

- `binding_calls` also collects `scenarios(<path>, ...)` calls (any number of positional string arguments,
  or names among the module's top-level assignments): each path names a feature file by base name, or a
  directory whose `*.feature` files it binds, resolved against `--dir`.
- `bindings --unbound [<feature file>...]`: after the existing report, list each scenario of the named files
  (default every file under `--dir`) that no call binds, as `<feature path>: <title> | bound by no test`, and
  each bound by more than one call with every call's `<module>:<line>`; exit 1 when any. A Scenario Outline
  is one scenario here, by title.
- Without `--unbound` the command behaves as today (r25, r26).

Accepts re-synced 2026-10-19 to the EARS lines (initiative/i13): feature-file-tools#r59 -> r58.
