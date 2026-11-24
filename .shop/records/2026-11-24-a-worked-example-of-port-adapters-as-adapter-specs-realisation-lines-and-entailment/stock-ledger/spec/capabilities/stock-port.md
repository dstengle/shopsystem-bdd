---
id: capability/example.org/shop/ordering-stock-ledger/stock-port
title: The stock port's contract
narrator: the ordering service
group: service
area: port
specifies: service stock
language: codified-2
retired: []
unbuilt: []
---

# The stock port's contract (copied from ordering, read-only)

## Purpose

What ordering's core relies on of the stock service, whoever provides it: each line a guarantee some core line
stands on, and nothing the core does not use. Its scenarios are the conformance tests every stock adapter passes.

## Behaviour

### [g1] Reserving again for the same order gives the same reservation
- [r1] While a reservation for an order exists, when the ordering service reserves stock for the order, the stock
  service shall return the reservation and change nothing.

### [g2] A reservation freed is freed
- [r2] When the ordering service frees a reservation, the stock service shall complete the reservation.

### [g3] A reservation that stands is taken
- [r3] While the state of a reservation is `made`, when the ordering service takes the reservation, the stock service
  shall complete the reservation.

### [g4] A lapsed reservation is not taken
- [r4] While the state of a reservation is `lapsed`, when the ordering service takes the reservation, the stock
  service shall refuse the reservation.

### [g5] A reservation that lapses is freed when ordering is told
- [r5] When the stock service notifies the ordering service of a reservation whose state is `lapsed`, the stock
  service shall free the reservation.

### [g6] A product counted returns its availability
- [r6] When the ordering service counts a product, the stock service shall return the availability of the product.
