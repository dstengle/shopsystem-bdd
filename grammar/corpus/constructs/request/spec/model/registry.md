---
id: model/example.org/grammar/constructs-request/registry
area: registry
kind: port
imports: [decisions]
---

# Registry

## Purpose

The registry the decisions service publishes a design-decision to, reached through a driven port.

```model
service registry
  operation publish(design-decision, summary)  outcomes: done | refused: summary taken
```
