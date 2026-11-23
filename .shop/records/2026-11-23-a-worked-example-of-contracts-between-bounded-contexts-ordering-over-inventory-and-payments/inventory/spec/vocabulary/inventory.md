---
id: vocabulary/example.org/shop/inventory/inventory
area: inventory
---

# The words of inventory

## Terms

- **the inventory service** (proper noun) → service inventory. What answers clients and stock keepers about stock.
- **product** (noun) → object product. A thing kept in stock.
- **warehouse** (noun) → object warehouse. A place stock is kept.
- **allocation** (noun) → object allocation. A quantity of a product held for a client until it is consumed or released.
- **stock** (attribute) → attribute product.stock. How many units of the product are on hand and not held.
- **supply** (attribute) → attribute product.supply. Whether any of the product can be held.
- **available** (adjective) → value product.supply available.
- **exhausted** (adjective) → value product.supply exhausted.
- **quantity** (attribute) → attribute allocation.quantity. How many units an allocation holds.
- **reference** (attribute) → attribute allocation.reference. The client's own key for an allocation: holding again with it gives the same allocation.
- **status** (attribute) → attribute allocation.status. Where an allocation is in its life.
- **placed** (adjective) → value allocation.status placed.
- **consumed** (adjective) → value allocation.status consumed.
- **released** (adjective) → value allocation.status released.
- **lapsed** (adjective) → value allocation.status lapsed.
- **hold** (verb, action) → operation inventory.hold. Forms: holds, held. Frame: <actor> holds <product>.
- **release** (verb, action) → operation inventory.release. Forms: releases, released. Frame: <actor> releases <allocation>.
- **consume** (verb, action) → operation inventory.consume. Forms: consumes, consumed. Frame: <actor> consumes <allocation>.
- **query** (verb, action) → operation inventory.query. Forms: queries, queried. Frame: <actor> queries <product>.
- **lapse** (verb, action) → operation inventory.lapse. Forms: lapses, lapsed. Frame: <actor> lapses <allocation>.
- **restock** (verb, action) → operation inventory.restock. Forms: restocks, restocked. Frame: <actor> restocks <product>.
- **transfer** (verb, action) → operation inventory.transfer. Forms: transfers, transferred. Frame: <actor> transfers <product>.
- **audit** (verb, action) → operation inventory.audit. Forms: audits, audited. Frame: <actor> audits <warehouse>.
