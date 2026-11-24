---
id: capability/example.org/shop/ordering-stock-ledger/realisation
title: Realising the stock port with the stock ledger
narrator: the stock adapter
group: service
area: adapter
specifies: service stock
realises: [stock-port#r1, stock-port#r2, stock-port#r3, stock-port#r4, stock-port#r5]
language: codified-2
retired: []
unbuilt: []
---

# Realising the stock port with the stock ledger

## Purpose

How the stock adapter meets the stock-port lines with a ledger that only decrements and increments: a reservation is a
decrement recorded in the adapter's entry; freeing and lapsing increment it back; taking only marks the entry.
stock-port#r6 (count) is not realised: the ledger cannot be read (adr/0001).

## Behaviour

### [g1] A reservation is a decrement of the order's line
- [r1] While an order has no entry, when the ordering service reserves stock for the order, the stock service shall
  keep an entry of the order and decrement the line of the entry.

### [g2] Reserving again for an order returns its reservation
- [r2] While a reservation for an order exists, when the ordering service reserves stock for the order, the stock
  service shall return the reservation and change nothing.

### [g3] A decrement refused refuses the reservation
- [r3] If the ledger service refuses an entry, then the stock service shall refuse the reservation of the entry.

### [g4] Freeing increments the line back
- [r4] When the ordering service frees a reservation, the stock service shall increment the line of the entry of the
  reservation, set the progress of the entry to `returned` and complete the reservation.

### [g5] Taking a reservation that stands only marks its entry
- [r5] While the state of a reservation is `made`, when the ordering service takes the reservation, the stock service
  shall set the progress of the entry of the reservation to `taken` and complete the reservation.

### [g6] Taking a lapsed reservation is refused
- [r6] While the state of a reservation is `lapsed`, when the ordering service takes the reservation, the stock
  service shall refuse the reservation.

### [g7] An entry not taken by its deadline lapses
- [r7] When the clock reaches the deadline of an entry whose progress is `decremented`, the stock service shall set
  the state of the reservation of the entry to `lapsed` and notify the ordering service of the reservation.

### [g8] A lapsed reservation's units go back to the ledger
- [r8] When the stock service notifies the ordering service of a reservation whose state is `lapsed`, the stock
  service shall increment the line of the entry of the reservation and free the reservation.
