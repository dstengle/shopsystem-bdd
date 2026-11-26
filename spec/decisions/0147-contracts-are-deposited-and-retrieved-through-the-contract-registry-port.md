---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/contracts-are-deposited-and-retrieved-through-the-contract-registry-port
summary: "Publish deposits and fetch and obtain retrieve a contract through the contract registry port and act on its replies; where contracts are kept is the adapter's, and no line or core code names a path."
date: 2026-11-26
status: accepted
tier: requirement
enforced_by: [checking#r127, checking#r131, checking#r126, checking#r128, checking#r129, checking#r130, contract-registry#r1, contract-registry#r2, contract-registry#r3]
verified_by: [scenario]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/contracts-are-located-and-kept-through-a-driven-port]
---

# 0147. Contracts are deposited and retrieved through the contract registry port

## Context

b636 delivered the port in batch-131; decision 0139 was its judgement-tier forerunner.

## Decision

Publishing deposits the contract at its version, and fetching and obtaining retrieve it, through the contract registry, a driven port of the specification. The specification keeps the contract once the registry completes the deposit, returns what the registry returns, and on a refusal names the version and changes nothing. Where and how contracts are kept and found is an adapter's (decision 0125 for which is wired). No requirement line and no core code names a path. Keeping an obtained contract in its provider's adapter spec still writes a folder layout itself (decision 0137) until the registry has an operation for it.
