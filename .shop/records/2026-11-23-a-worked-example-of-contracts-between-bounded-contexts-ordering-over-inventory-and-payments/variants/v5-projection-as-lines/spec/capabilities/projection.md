---
id: capability/example.org/shop/ordering/projection
title: The ports' projection
narrator: the ordering service
group: service
area: orders
language: codified-2
retired: []
unbuilt: []
---

# The ports' projection

## Purpose

What inventory and payments guarantee of the port operations ordering uses, in ordering's words: generated from the
published contracts and the adapter contracts, never written by hand. Here as lines only to run the checks on them.

## Behaviour

### [g1] A reservation is completed or refused
- [r1] When the ordering service reserves stock for an order, the stock service shall complete a reservation for the
  order.
- [r2] When the ordering service reserves stock for an order, the stock service may refuse a reservation for the order.
- [r3] When the ordering service reserves stock for an order, the stock service may notify the ordering service of a
  reservation for the order whose state is `lapsed`.

### [g2] A reservation freed is completed
- [r4] When the ordering service frees a reservation, the stock service shall complete the reservation.

### [g3] A lapsed reservation is not taken
- [r5] When the ordering service takes a reservation whose state is `lapsed`, the stock service shall refuse the
  reservation.
- [r6] When the ordering service takes a reservation whose state is `made`, the stock service shall complete the
  reservation.

### [g4] A product counted returns its availability
- [r7] When the ordering service counts a product, the stock service shall return the availability of the product.

### [g5] A charge is secured or refused
- [r8] When the ordering service secures a charge for an order, the charges service shall complete the charge.
- [r9] When the ordering service secures a charge for an order, the charges service may refuse the charge.

### [g6] A charge cancelled is completed
- [r10] When the ordering service cancels a charge, the charges service shall complete the charge.

### [g7] A charge collected is completed, then settles or bounces
- [r11] When the ordering service collects a charge, the charges service shall complete the charge.
- [r12] When the ordering service collects a charge, the charges service may notify the ordering service of the
  charge.
