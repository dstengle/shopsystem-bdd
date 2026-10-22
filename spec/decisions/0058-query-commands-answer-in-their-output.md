---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/query-commands-answer-in-their-output
summary: "A query command answers in its output and exits with an error only when it cannot answer; an empty answer exits successfully, and `--json` prints the whole result as one JSON object."
date: 2026-10-22
status: accepted
supersedes: [design-decision/exits-are-successful-or-errors]
source: [design-decision/exits-are-successful-or-errors]
by: "the person, 2026-10-22, delegated drafting decisions to the coordinator's recommendations"
---

# 0058. Query commands answer in their output

## Context

During 0.22.0 the person asked that a query command's result be structured output that can be checked explicitly, JSON not being required.

## Decision

A Behaviour line, and the scenario that formulates it, says a command exits successfully or exits with an error, and never names an exit code. Where a command has several error codes, they are listed in its capability's Implementation section and checked by unit tests. A command that stops because it waits on the person (a work-item awaiting a ruling) exits with an error.

A query command answers in its output, and its exit says only whether it could answer. A query that finds nothing has answered: it prints an empty result and exits successfully. It exits with an error only when it cannot answer (a missing map, a missing tool, an argument it cannot read). Where `--json` is given, a query command prints its whole result as one JSON object, and without it prints text as today, so the skills that read the text keep working. The keys of the JSON object are Implementation.

## Alternatives

- `--json` (chosen): `model check --json` (design-model-check r33) already gives this repository its form, and JSON is the one structured form needed.
- A `--format` option: not chosen.
