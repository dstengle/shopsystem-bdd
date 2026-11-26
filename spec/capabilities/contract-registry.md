---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/contract-registry
title: Contract registry
narrator: the specification service
group: service
area: registry
specifies: service contract-registry
language: codified-2
retired: []
unbuilt: [r4]
---

# Contract registry

## Purpose
The contracts the specification keeps and finds through a driven port: a contract deposited at a version, and the contract of a bounded context retrieved at a version, wherever an adapter keeps them.

## Behaviour
### [g1] A contract deposited is kept by the registry
- [r1] When the specification service deposits a contract, the contract registry service shall complete the request.
Relied on by: checking#r127

### [g2] A contract retrieved is returned by the registry
- [r2] When the specification service retrieves a contract, the contract registry service shall return the contract.
Relied on by: checking#r131

### [g3] A contract retrieved at a version never deposited is refused by the registry
- [r3] If the specification service retrieves a contract with a version that no contract has, then the contract registry service shall refuse the request and name the version.
Relied on by: checking#r126

### [g4] A contract registered for an adapter spec is kept by the registry
- [r4] When the specification service registers a contract for an adapter spec, the contract registry service shall complete the request.
Relied on by: checking#r137, checking#r138

