---
id: model/example.org/shop/ordering/adapters/stock-inventory/port
area: port
kind: port
imports: [adapter]
---

# The stock port, as ordering declares it

## Purpose

ordering's stock port and the core things its operations name, copied from ordering at its commit; never edited here.

```model
object order
  attributes: quantity (number); number (text)
  relations: for → product (one)

object product

object reservation kind of request
  attributes: state: made | lapsed
  relations: for → order (one)

object availability
  attributes: units (number)
  relations: of → product (one)

service ordering

service stock
  operation reserve(order)  outcomes: done → the reservation | refused: order out of stock
  operation free(reservation)  outcomes: done
  operation take(reservation)  outcomes: done | refused: lapsed reservation
  operation count(product)  outcomes: returned → the availability
```
