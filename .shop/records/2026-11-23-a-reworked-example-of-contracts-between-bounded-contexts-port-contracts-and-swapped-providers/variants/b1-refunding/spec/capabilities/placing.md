---
id: capability/example.org/shop/ordering/placing
title: Placing an order
narrator: a shopper
group: service
area: orders
specifies: service ordering
language: codified-2
retired: [r8]
unbuilt: []
---

# Placing an order

## Purpose

A shopper places an order and the ordering service runs its saga: stock reserved, a charge secured, the stock taken,
the order confirmed and the charge collected; a refusal or a lapse at any step undoes the steps before it. The
status of the order says which step's outcome a reply is.

## Behaviour

### [g1] An order placed is kept and its stock reserved
- [r1] When the shopper places an order with a product and a quantity and a card, the ordering service shall keep the
  order and reserve stock for the order.

### [g2] An order placed without a quantity is refused
- [r2] If the shopper places an order without a quantity, then the ordering service shall refuse the request and name
  the quantity.

### [g3] Stock reserved for an order holds it and secures a charge
- [r3] While the status of an order is `placed`, when the stock service completes a reservation for the order, the
  ordering service shall set the status of the order to `held` and secure a charge for the order.

### [g4] An order whose stock is refused is rejected
- [r4] While the status of an order is `placed`, if the stock service refuses a reservation for the order, then the
  ordering service shall set the status of the order to `rejected` and notify the shopper of the order.

### [g5] A charge secured for a held order takes its stock
- [r5] While the status of an order is `held`, when the charges service completes a charge for the order, the
  ordering service shall set the status of the order to `charged` and take every reservation for the order.

### [g6] A charge refused for a held order frees its stock and cancels the order
- [r6] While the status of an order is `held`, if the charges service refuses a charge for the order, then the
  ordering service shall free every reservation for the order, set the status of the order to `cancelled` and
  notify the shopper of the order.

### [g7] Stock taken for a charged order confirms it and collects its charge
- [r7] While the status of an order is `charged`, when the stock service completes a reservation for the order, the
  ordering service shall set the status of the order to `confirmed` and collect every charge for the order.

### [g8] Stock that cannot be taken for a charged order refunds its charge
- [r12] While the status of an order is `charged`, if the stock service refuses a reservation for the order, then the
  ordering service shall cancel every charge for the order and set the status of the order to `refunding`.

### [g9] A reservation that lapses while a charge is secured expires the order
- [r9] While the status of an order is `held`, when the stock service notifies the ordering service of a reservation
  for the order whose state is `lapsed`, the ordering service shall cancel every charge for the order, set the status
  of the order to `expired` and notify the shopper of the order.

### [g10] A charge that settles pays the order
- [r10] While the status of an order is `confirmed`, when the charges service notifies the ordering service of a
  charge for the order whose state is `settled`, the ordering service shall set the status of the order to `paid`.

### [g11] A charge that bounces leaves the order unpaid
- [r11] While the status of an order is `confirmed`, when the charges service notifies the ordering service of a
  charge for the order whose state is `bounced`, the ordering service shall set the status of the order to `unpaid`
  and notify the shopper of the order.

### [g12] A charge refunded expires the order
- [r13] While the status of an order is `refunding`, when the charges service notifies the ordering service of a
  charge for the order whose state is `refunded`, the ordering service shall set the status of the order to `expired`
  and notify the shopper of the order.

### [g13] A refund that fails is left to the clerk
- [r14] While the status of an order is `refunding`, when the charges service notifies the ordering service of a
  charge for the order whose state is `unrefunded`, the ordering service shall set the status of the order to
  `unrefunded` and notify the clerk of the order.
