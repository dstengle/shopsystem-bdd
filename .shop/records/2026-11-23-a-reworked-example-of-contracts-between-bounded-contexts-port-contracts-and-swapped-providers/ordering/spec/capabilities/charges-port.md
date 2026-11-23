---
id: capability/example.org/shop/ordering/charges-port
title: The charges port's contract
narrator: the ordering service
group: service
area: charges
specifies: service charges
language: codified-2
retired: []
unbuilt: []
---

# The charges port's contract

## Purpose

What ordering's core relies on of the charges service, whoever provides it. Its scenarios are the conformance tests
every charges adapter passes.

## Behaviour

### [g1] Securing again for the same order charges nothing more
- [r1] While a charge for an order exists, when the ordering service secures a charge for the order, the charges
  service shall change nothing.

### [g2] Securing a charge collects nothing
- [r2] When the ordering service secures a charge for an order, the charges service shall not collect the charge.

### [g3] A charge cancelled is cancelled, and that is final
- [r3] When the ordering service cancels a charge, the charges service shall complete the charge and not notify the
  ordering service of the charge.

### [g4] A charge collected is collected
- [r4] When the ordering service collects a charge, the charges service shall complete the charge.
