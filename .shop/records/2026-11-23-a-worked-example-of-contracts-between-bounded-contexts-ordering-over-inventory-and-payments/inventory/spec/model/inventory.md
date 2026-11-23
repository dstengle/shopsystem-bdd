---
id: model/example.org/shop/inventory/inventory
area: inventory
kind: core
imports: []
---

# Inventory

## Purpose

Products on hand in warehouses, and the allocations clients hold of them.

```model
object product
  attributes: name (text); stock (number); supply: available | exhausted
  relations: in → warehouse (many)

object warehouse
  attributes: name (text)

object allocation
  attributes: quantity (number); reference (text)
  lifecycle status: placed → consumed; placed → released; placed → lapsed
  relations: on → product (one); from → warehouse (one, optional)

service inventory
  operation hold(product, quantity, reference, warehouse) by the client
    outcomes: done → the allocation | refused: product out of stock, no quantity
  operation release(allocation) by the client  outcomes: done | refused: consumed allocation
  operation consume(allocation) by the client  outcomes: done | refused: lapsed allocation
  operation query(product) by the client  outcomes: returned → the product
  operation lapse(allocation) by the clock  outcomes: done
  operation restock(product, quantity, warehouse) by the stock keeper  outcomes: done
  operation transfer(product, quantity, warehouse) by the stock keeper  outcomes: done | refused: product out of stock
  operation audit(warehouse) by the stock keeper  outcomes: returned → every product

event an allocation lapses: raised by inventory.lapse

actor the client kind of agent
actor the stock keeper kind of agent
actor the clock kind of agent
```
