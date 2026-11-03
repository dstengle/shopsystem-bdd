---
id: bounded-context/example.org/fixture/e2e
title: The end-to-end fixture
language: codified-1
---

# The end-to-end fixture

A small codified context for the end-to-end test of a request through the requirements system
(`tests/scripts/test_e2e_codified.py`, the GF conversion's plan P15). It is not this repository's spec.

## Glossary

- **the person** (actor): the human who runs the commands.
- **`work`** (actor): the queue's command.
- **`work run`** (actor): the supervisor.

- **initiative** (kind): the delivery of one request.
- **file** (kind): a file of the repository.
- **command** (kind): one run of a tool.
- **reason** (kind): what an error names.
- **worker** (kind): one session `work run` starts.

- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete; `started` → `abandoned`: `work abandon`.

- **open** (condition of initiative): An initiative is open when the initiative is not `done` and the initiative is not `abandoned`.

- **start** (event): a stage begins.
- **give** (event): Forms: gives, given.
- **refuse** (event): Forms: refuses, refused.

- **worker slot** (resource, counted by `workers`): held by every worker.
