---
id: model/missingmass.io/shopsystem/shopsystem-bdd/registry
area: registry
kind: port
imports: [execution, specification, tracking, upgrades]
---

# Registry

## Purpose

The contracts the specification keeps and finds through a driven port: a contract deposited at a version, and the contract of a bounded context retrieved at a version, wherever an adapter keeps them.

```model
service contract registry
  operation deposit(contract, version)  outcomes: done → the contract
  operation retrieve(contract, bounded context, version)  outcomes: returned → the contract | refused: version not deposited
```
