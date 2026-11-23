---
id: bounded-context/example.org/shop/inventory
title: inventory
language: codified-2
imports: [request]
---

# inventory

## Purpose

The stock the shop keeps in its warehouses: what is on hand, what is held for a client until it is consumed or
released, and how stock is restocked, moved and counted.

## Composition

| area | kind | capabilities |
|---|---|---|
| inventory | core | holding, stockkeeping |
