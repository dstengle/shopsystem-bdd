---
id: model/example.org/shop/ordering-stock-ledger/provider
area: provider
kind: provider
imports: [adapter]
assumed: true
---

# The stock ledger, as the adapter's owners describe it (assumed)

## Purpose

The legacy stock ledger, in its own words, only as far as the adapter relies on it. No one publishes it: every
element and line here is assumed, and the sandbox tests of adr/0003 check them.

```model
object line
  attributes: code (text); units (number)

service ledger
  operation decrement(line, amount) by the caller  outcomes: done | refused: amount short
  operation increment(line, amount) by the caller  outcomes: done

actor the caller kind of agent
```
