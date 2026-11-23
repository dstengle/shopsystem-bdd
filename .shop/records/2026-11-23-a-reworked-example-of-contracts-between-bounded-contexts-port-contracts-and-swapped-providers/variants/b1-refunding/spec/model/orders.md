---
id: model/example.org/shop/ordering/orders
area: orders
kind: core
imports: [stock, charges]
---

# Orders

## Purpose

The orders shoppers place and the saga each one runs: stock set aside, a charge secured, then confirmed or undone.

```model
object order
  attributes: quantity (number); number (text); card (text); total (number)
  lifecycle status: placed → held; placed → rejected; held → charged; held → cancelled; held → withdrawn;
    held → expired; charged → confirmed; charged → refunding; refunding → expired;
    refunding → unrefunded; confirmed → paid; confirmed → unpaid
  relations: for → product (one)

object product
  attributes: name (text)

service ordering
  operation place(product, quantity, card) by the shopper  outcomes: done → the order | refused: no quantity
  operation withdraw(order) by the shopper  outcomes: done | refused: confirmed order
  operation view(product) by the shopper  outcomes: returned → the product

actor the shopper kind of agent
actor the clerk kind of agent
```
