---
id: universal/example.org/fixture/logic-cluster
title: Universal conditions
group: guarantees
language: codified-1
retired: []
---

# Universal conditions

## Behaviour

- [U1] `work run` shall hold at most `workers` worker slots at a time.
- [U2] `work run` shall not start a stage that needs a resource that is not free.
