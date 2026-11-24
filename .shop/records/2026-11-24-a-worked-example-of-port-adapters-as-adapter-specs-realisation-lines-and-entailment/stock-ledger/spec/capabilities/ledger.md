---
id: capability/example.org/shop/ordering-stock-ledger/ledger
title: The stock ledger (assumed)
narrator: the caller
group: service
area: provider
specifies: service ledger
assumed: true
language: codified-2
retired: []
unbuilt: []
---

# The stock ledger (assumed)

## Purpose

What the adapter relies on of the legacy stock ledger, in its words. Assumed, not published: each line is checked by
a sandbox test (adr/0003), never by a static check.

## Behaviour

### [g1] A line decremented loses the units
- [r1] When the caller decrements a line with an amount, the ledger service shall keep the line.

### [g2] A line short of units is not decremented
- [r2] If the caller decrements a line with an amount, then the ledger service may refuse the request and name the amount.

### [g3] A line incremented gains the units
- [r3] When the caller increments a line with an amount, the ledger service shall keep the line.
