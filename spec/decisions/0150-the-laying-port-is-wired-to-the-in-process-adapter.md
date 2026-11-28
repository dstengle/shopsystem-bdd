---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-laying-port-is-wired-to-the-in-process-adapter
summary: "The batches service reaches the specification through the laying port, wired to its in-process adapter."
date: 2026-11-26
status: superseded
tier: judgement
---

# 0150. The laying port is wired to the in-process adapter

## Context

b611 (batch-139) put the work-management context's use of the specification behind the driven port laying.

## Decision

The laying port (lay, lift and check of an item in a workspace) is wired to its in-process adapter, which calls the specification's lay, lift and rule check in the same process. The port module loads it unless the environment names another adapter module, a test seam as the stand-in uses, not configuration. Which adapter is wired is a technical architecture decision (decision 0125), never a requirement line; a remote adapter replaces it when the specification is split into its own shop's context.
