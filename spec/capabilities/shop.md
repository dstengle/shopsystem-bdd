---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/shop
title: Shop
narrator: the person
group: service
area: execution
specifies: service shop
language: codified-2
retired: [g2, r2]
unbuilt: [r6]
---

# Shop

## Purpose
The bounded contexts a shop keeps, each by its id under the product of the shop.

## Behaviour
### [g1] A bounded context entrusted to the shop is kept
- [r1] When the person entrusts a bounded context with an id, the shop service shall keep the bounded context in the shop and complete the request.

### [g3] A bounded context is not kept twice under one id
- [r3] While a bounded context that has an id is in the shop, if the person entrusts a bounded context with the id, then the shop service shall refuse the request and name the id.

### [g4] The bounded contexts the shop keeps are listed
- [r4] When the person lists the shop, the shop service shall return every bounded context that is in the shop.

### [g5] A shop that keeps no bounded context lists this bounded context
- [r5] While no bounded context is in the shop, when the person lists the shop, the shop service shall return this bounded context.

### [g6] The shop's product id is the product's id
- [r6] While the product of the shop has an id, if the person entrusts a bounded context with another id that the id does not cover, then the shop service shall refuse the request and name the id.

