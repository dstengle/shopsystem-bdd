---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/shop
title: Shop
narrator: the person
group: service
area: execution
specifies: service shop
language: codified-2
retired: []
unbuilt: [r1, r2, r3, r4, r5]
---

# Shop

## Purpose
The bounded contexts a shop keeps, each by its id under the product of the shop.

## Behaviour
### [g1] A bounded context entrusted to the shop is kept
- [r1] When the person entrusts a bounded context with an id, the shop service shall keep the bounded context in the shop and complete the request.

### [g2] A bounded context with an id outside the product of the shop is not kept
- [r2] If the person entrusts a bounded context with an id that the product id of the shop does not cover, then the shop service shall refuse the request and name the id.

### [g3] A bounded context is not kept twice under one id
- [r3] While a bounded context that has an id is in the shop, if the person entrusts a bounded context with the id, then the shop service shall refuse the request and name the id.

### [g4] The bounded contexts the shop keeps are listed
- [r4] When the person lists the shop, the shop service shall return every bounded context that is in the shop.

### [g5] A shop that keeps no bounded context lists this bounded context
- [r5] While no bounded context is in the shop, when the person lists the shop, the shop service shall return this bounded context.

