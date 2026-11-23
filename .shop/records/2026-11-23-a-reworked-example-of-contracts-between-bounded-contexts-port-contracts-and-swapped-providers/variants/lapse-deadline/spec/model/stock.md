---
id: model/example.org/shop/ordering/stock
area: stock
kind: port
imports: [orders]
---

# Stock

## Purpose

The port through which ordering has stock set aside for an order, freed or taken, and learns how much of a product
can be ordered. In ordering's words; spec/adapters/stock.toml maps it onto inventory.

```model
object reservation kind of request
  attributes: state: made | lapsed
  relations: for → order (one)

object deadline kind of moment
  relations: of → reservation (one)

object availability
  attributes: units (number)
  relations: of → product (one)

service stock
  operation reserve(order)  outcomes: done → the reservation | refused: order out of stock
  operation free(reservation)  outcomes: done
  operation take(reservation)  outcomes: done | refused: lapsed reservation
  operation count(product)  outcomes: returned → the availability
```
