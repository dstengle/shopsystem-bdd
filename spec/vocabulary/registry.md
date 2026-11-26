---
id: vocabulary/missingmass.io/shopsystem/shopsystem-bdd/registry
area: registry
---

# The words of registry

## Terms

- **the contract registry service** (proper noun) → service contract registry. Where this bounded context's contracts are kept and found, whichever adapter keeps them (decision 0139).
- **deposit** (verb, action) → operation contract registry.deposit. The specification service gives the contract registry a contract to keep at its version. Forms: deposits, deposited. Frame: <actor> deposits <contract>.
- **retrieve** (verb, action) → operation contract registry.retrieve. The specification service asks the contract registry for the contract of a bounded context at a version. Forms: retrieves, retrieved. Frame: <actor> retrieves <contract>.
