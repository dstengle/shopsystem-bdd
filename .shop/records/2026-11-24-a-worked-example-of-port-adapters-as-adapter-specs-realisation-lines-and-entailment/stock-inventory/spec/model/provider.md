---
id: model/example.org/shop/ordering/adapters/stock-inventory/provider
area: provider
kind: provider
imports: [adapter]
---

# inventory, as its published contract 1.4.0 declares it

## Purpose

The part of inventory's published contract this adapter uses, in inventory's words.

```model
object stocked-product
  attributes: stock (number); supply: available | exhausted

object allocation
  attributes: quantity (number); reference (text)
  lifecycle status: placed → consumed; placed → released; placed → lapsed
  relations: on → stocked-product (one)

service inventory
  operation hold(stocked-product, quantity, reference) by the client  outcomes: done → the allocation | refused: product out of stock, no quantity
  operation release(allocation) by the client  outcomes: done | refused: consumed allocation
  operation consume(allocation) by the client  outcomes: done | refused: lapsed allocation
  operation query(stocked-product) by the client  outcomes: returned → the stocked-product
  operation lapse(allocation) by the clock  outcomes: done

actor the client kind of agent
actor the clock kind of agent
```
