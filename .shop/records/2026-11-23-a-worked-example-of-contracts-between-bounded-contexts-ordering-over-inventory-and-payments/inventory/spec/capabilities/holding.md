---
id: capability/example.org/shop/inventory/holding
title: Holding stock
narrator: a client
group: service
area: inventory
specifies: service inventory
language: codified-2
retired: []
unbuilt: []
---

# Holding stock

## Purpose

A client holds a quantity of a product for a while, then consumes the allocation or releases it; an allocation not
consumed in time lapses. A client can ask how much of a product is on hand.

## Behaviour

### [g1] A product held is allocated
- [r1] When the client holds a product with a quantity and a reference, the inventory service shall keep an
  allocation on the product.

### [g2] Holding again with the same reference gives the same allocation
- [r2] When the client holds a product with the reference of an allocation on the product, the inventory service
  shall return the allocation and change nothing.

### [g3] An exhausted product is not held
- [r3] If the client holds a product whose supply is `exhausted`, then the inventory service shall refuse the request
  and name the product.

### [g4] A product held without a quantity is refused
- [r4] If the client holds a product without a quantity, then the inventory service shall refuse the request and name
  the quantity.

### [g5] An allocation released is released
- [r5] When the client releases an allocation, the inventory service shall set the status of the allocation to
  `released`.

### [g6] A consumed allocation is not released
- [r6] If the client releases an allocation whose status is `consumed`, then the inventory service shall refuse the
  request and name the allocation.

### [g7] An allocation consumed is consumed
- [r7] When the client consumes an allocation, the inventory service shall set the status of the allocation to
  `consumed`.

### [g8] A lapsed allocation is not consumed
- [r8] If the client consumes an allocation whose status is `lapsed`, then the inventory service shall refuse the
  request and name the allocation.

### [g9] An allocation not consumed in time lapses and the client is told
- [r9] When the clock lapses an allocation whose status is `placed`, the inventory service shall set the status of
  the allocation to `lapsed` and notify the client of the allocation.

### [g10] A product queried returns its stock
- [r10] When the client queries a product, the inventory service shall return the stock of the product.
