---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-contract-registry-is-wired-to-the-shop-folder-adapter
summary: "The contract registry port runs on the shop-folder adapter, hard-wired in its port module; another adapter is loaded only by the tests' stand-in."
date: 2026-11-26
status: accepted
tier: judgement
---

# 0146. The contract registry is wired to the shop-folder adapter

## Context

b636 (batch-131) put publish, fetch and obtain behind the contract registry port.

## Decision

The specification's contract registry port is reached only through its port module, which runs the shop-folder adapter: a bounded context's published contracts are kept in the shop, a context of the same shop is read from its own folder and any other from its upstream's repository. The choice is hard-wired (decision 0125: hard-wired first, configuration later); the environment variable that names another adapter's file is a test seam, not configuration.
