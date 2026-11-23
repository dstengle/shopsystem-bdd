---
id: bounded-context/example.org/shop/ordering
title: ordering
language: codified-2
imports: [request]
---

# ordering

## Purpose

The shop's ordering: a shopper places an order for a product, the shop sets stock aside and secures a charge for it,
and the order is confirmed or undone. It keeps no stock and takes no payment itself: two ports ask other contexts for
both, in ordering's own words.

## Composition

| area | kind | capabilities |
|---|---|---|
| orders | core | placing, withdrawing, browsing |
| stock | port | |
| charges | port | |

## Upstreams

- bounded-context/example.org/shop/inventory, through the port stock; github: example/inventory
- bounded-context/example.org/shop/payments, through the port charges; github: example/payments
