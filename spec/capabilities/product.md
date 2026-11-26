---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/product
title: Product
narrator: the person
group: service
area: specification
specifies: service product
language: codified-2
retired: []
unbuilt: []
---

# Product

## Purpose
The product a bounded context belongs to: its id and purpose, its actors and the jobs to be done it holds.

## Behaviour
### [g1] The product is declared with its id and purpose
- [r1] When the person declares a product with an id and a purpose, the product service shall keep the product and complete the request.

### [g2] An actor of the product is declared
- [r2] When the person declares a product actor, the product service shall keep the product actor in the product and complete the request.

### [g3] A job to be done is declared with its actors and statement
- [r3] When the person declares a job with an id and a product actor and a job statement, the product service shall keep the job in the product and complete the request.

### [g4] A job whose statement is not of the job statement form is refused
- [r4] If the person declares a job with a job statement that does not conform to the job statement form, then the product service shall refuse the request and name the job statement.

### [g5] A job whose actor is not the product's is refused
- [r5] If the person declares a job with a product actor that is not in the product, then the product service shall refuse the request and name the product actor.

### [g6] A job that needs a job the product does not hold is refused
- [r6] If the person declares a job with a need that is not in the product, then the product service shall refuse the request and name the need.

### [g7] A job whose needs close a cycle is refused
- [r7] If the person declares a job with a need that depends on the job, then the product service shall refuse the request and name the need.

