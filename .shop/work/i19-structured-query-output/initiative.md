---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i19
title: Structured output for query commands
summary: A query command answers in its output, an empty answer exits successfully, and --json prints its whole result as one JSON object.
kind: capability-change
owner-level: shopsystem-bdd
status: done
priority: 1
source: [observation/2026-10-22-deferred-from-0-22-0]
date: 2026-10-22
---

0.23.0, part 2 (the person, during 0.22.0: a query command's result should be structured output that can be
checked explicitly; scope approved 2026-10-22, drafting decisions delegated to the coordinator). Design note:
.shop/records/archive/design-notes/2026-10-22-structured-query-output-design.md. Decision 0058. Lines committed in
fc1a259; analysis-tools' lines (`tools tests-of`, `untested`, `refs`, `map`) are held: the harness refused
the capability-writer's draft of them twice.
