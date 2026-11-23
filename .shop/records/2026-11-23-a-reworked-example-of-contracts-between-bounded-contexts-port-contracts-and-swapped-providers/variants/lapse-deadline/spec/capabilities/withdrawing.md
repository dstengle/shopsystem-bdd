---
id: capability/example.org/shop/ordering/withdrawing
title: Withdrawing an order
narrator: a shopper
group: service
area: orders
specifies: service ordering
language: codified-2
retired: []
unbuilt: []
---

# Withdrawing an order

## Purpose

A shopper withdraws an order that is not yet confirmed; its stock is freed and its charge cancelled.

## Behaviour

### [g1] A held order withdrawn frees its stock and cancels its charge
- [r1] When the shopper withdraws an order whose status is `held`, the ordering service shall free every reservation
  for the order, cancel every charge for the order and set the status of the order to `withdrawn`.

### [g2] A confirmed order is not withdrawn
- [r2] If the shopper withdraws an order whose status is `confirmed`, then the ordering service shall refuse the
  request and name the order.
