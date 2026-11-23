---
id: capability/example.org/shop/inventory/stockkeeping
title: Keeping stock
narrator: a stock keeper
group: service
area: inventory
specifies: service inventory
language: codified-2
retired: []
unbuilt: []
---

# Keeping stock

## Purpose

A stock keeper restocks products, moves them between warehouses and audits a warehouse.

## Behaviour

### [g1] A product restocked is kept
- [r1] When the stock keeper restocks a product with a quantity and a warehouse, the inventory service shall keep the
  product.

### [g2] A product transferred is kept
- [r2] When the stock keeper transfers a product with a quantity and a warehouse, the inventory service shall keep the
  product.

### [g3] An exhausted product is not transferred
- [r3] If the stock keeper transfers a product whose supply is `exhausted`, then the inventory service shall refuse
  the request and name the product.

### [g4] A warehouse audited returns every product in it
- [r4] When the stock keeper audits a warehouse, the inventory service shall return every product in the warehouse.
