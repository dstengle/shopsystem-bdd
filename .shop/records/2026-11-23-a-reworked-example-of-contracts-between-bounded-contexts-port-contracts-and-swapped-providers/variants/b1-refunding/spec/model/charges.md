---
id: model/example.org/shop/ordering/charges
area: charges
kind: port
imports: [orders]
---

# Charges

## Purpose

The port through which ordering secures a charge for an order, collects it or cancels it, and hears later whether a
collected charge settled or bounced. In ordering's words; spec/adapters/charges.toml maps it onto payments.

```model
object charge kind of request
  attributes: amount (number); state: settled | bounced | refunded | unrefunded
  relations: for → order (one)

service charges
  operation secure(order)  outcomes: done → the charge | refused: charge declined
  operation cancel(charge)  outcomes: done | notifies → the charge
  operation collect(charge)  outcomes: done | notifies → the charge
```
