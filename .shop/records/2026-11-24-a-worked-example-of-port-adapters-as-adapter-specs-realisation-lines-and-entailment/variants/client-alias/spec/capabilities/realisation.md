---
id: capability/example.org/shop/ordering-stock-inventory/realisation
title: Realising the stock port with inventory
narrator: the stock adapter
group: service
area: adapter
specifies: service stock
realises: [stock-port#r1, stock-port#r2, stock-port#r3, stock-port#r4, stock-port#r5, stock-port#r6]
language: codified-2
retired: []
unbuilt: []
---

# Realising the stock port with inventory

## Purpose

How the stock adapter meets each stock-port line with inventory's operations: each line in ordering's words and
inventory's words together, the adapter's entry (its store's record of an order) the one thing that joins them. A line
answering ordering is said on the port's own trigger, so that the check can compare it with the port line it realises.

## Behaviour

### [g1] A reservation is an allocation held at inventory
- [r1] While an order has no entry, when the ordering service reserves stock for the order, the stock service shall
  keep an entry of the order and hold the stocked product of the entry.

### [g2] Reserving again for an order that has an entry returns its reservation
- [r2] While a reservation for an order exists, when the ordering service reserves stock for the order, the stock
  service shall return the reservation and change nothing.

### [g3] An allocation kept completes the reservation
- [r3] When the inventory service keeps the allocation of an entry, the stock service shall complete the reservation
  of the entry.

### [g4] A hold refused refuses the reservation
- [r4] If the inventory service refuses an entry, then the stock service shall refuse the reservation of the entry.

### [g5] Freeing releases the allocation
- [r5] When the ordering service frees a reservation, the stock service shall release the allocation of the entry of
  the reservation and complete the reservation.

### [g6] Taking a reservation that stands consumes its allocation
- [r6] While the state of a reservation is `made`, when the ordering service takes the reservation, the stock service
  shall consume the allocation of the entry of the reservation and complete the reservation.

### [g7] Taking a lapsed reservation is refused
- [r7] While the state of a reservation is `lapsed`, when the ordering service takes the reservation, the stock
  service shall refuse the reservation.

### [g8] A lapse at inventory is a lapse of the reservation
- [r8] When the inventory service notifies the client of the allocation of the entry of a reservation, the stock
  service shall set the state of the reservation to `lapsed` and notify the ordering service of the reservation.

### [g9] Counting queries the product at inventory
- [r9] When the ordering service counts a product, the stock service shall query every stocked product of an entry
  and return the availability of the product.
