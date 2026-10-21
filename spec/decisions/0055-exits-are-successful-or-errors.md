---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/exits-are-successful-or-errors
summary: "A Behaviour line says a command exits successfully or exits with an error, never an exit code; codes live in Implementation."
date: 2026-10-21
status: accepted
source: [observation/2026-10-21-one-requirement-per-scenario]
by: "the person, 2026-10-21"
---

# 0055. Exits are successful or errors

## Decision

A Behaviour line, and the scenario that formulates it, says a command exits successfully or exits with an error, and never names an exit code. Where a command has several error codes, they are listed in its capability's Implementation section and checked by unit tests. A command that stops because it waits on the person (a work-item awaiting a ruling) exits with an error.
