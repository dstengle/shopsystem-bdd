---
id: vocabulary/example.org/shop/ordering/adapters/stock-inventory/provider
area: provider
---

# inventory's words, from its published contract 1.4.0

## Terms

- **the inventory service** (proper noun) → service inventory. The provider.
- **the client** (proper noun) → service stock. inventory's name for whoever holds stock: here, the stock service.
- **the clock** (proper noun) → actor the clock. inventory's clock.
- **stocked product** (noun) → object stocked-product. inventory's "product": a thing kept in stock. Plural: stocked products.
- **allocation** (noun) → object allocation. A quantity of a product held for a client.
- **stock** (attribute) → attribute stocked-product.stock. How many units are on hand and not held.
- **supply** (attribute) → attribute stocked-product.supply.
- **available** (adjective) → value stocked-product.supply available.
- **exhausted** (adjective) → value stocked-product.supply exhausted.
- **quantity** (attribute) → attribute allocation.quantity. How many units an allocation holds.
- **reference** (attribute) → attribute allocation.reference. The client's own key for an allocation.
- **status** (attribute) → attribute allocation.status.
- **placed** (adjective) → value allocation.status placed.
- **consumed** (adjective) → value allocation.status consumed.
- **released** (adjective) → value allocation.status released.
- **lapsed** (adjective) → value allocation.status lapsed.
- **hold** (verb, action) → operation inventory.hold. Forms: holds, held. Frame: <actor> holds <stocked-product>.
- **release** (verb, action) → operation inventory.release. Forms: releases, released. Frame: <actor> releases <allocation>.
- **consume** (verb, action) → operation inventory.consume. Forms: consumes, consumed. Frame: <actor> consumes <allocation>.
- **query** (verb, action) → operation inventory.query. Forms: queries, queried. Frame: <actor> queries <stocked-product>.
- **lapse** (verb, action) → operation inventory.lapse. Forms: lapses, lapsed. Frame: <actor> lapses <allocation>.
