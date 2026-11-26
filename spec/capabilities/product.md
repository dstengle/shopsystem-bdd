---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/product
title: Product
narrator: the person
group: service
area: specification
specifies: service product
language: codified-2
retired: []
unbuilt: [r8, r9, r10, r11, r12, r13]
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

### [g8] A product declared again keeps the product's details
- [r8] While this product holds a product detail, when the person declares a product with an id and a purpose, the product service shall keep the product detail in the product and complete the request.

### [g9] A product actor declared keeps the product's details
- [r9] While this product holds a product detail, when the person declares a product actor, the product service shall keep the product detail in the product and complete the request.

### [g10] A job declared keeps the product's details
- [r10] While this product holds a product detail, when the person declares a job with an id and a product actor and a job statement, the product service shall keep the product detail in the product and complete the request.

### [g11] A product not of the product form is not declared again
- [r11] While this product does not conform to the product form, if the person declares a product with an id and a purpose, then the product service shall refuse the request and name this product.

### [g12] No product actor is declared in a product not of the product form
- [r12] While this product does not conform to the product form, if the person declares a product actor, then the product service shall refuse the request and name this product.

### [g13] No job is declared in a product not of the product form
- [r13] While this product does not conform to the product form, if the person declares a job with an id and a product actor and a job statement, then the product service shall refuse the request and name this product.

### [g14] A job whose statement's situation holds a comma is declared
- [r14] When the person declares a job with a job statement that conforms to the job statement form, the product service shall keep the job in the product and complete the request.

```given
the job statement `j2` holds "When a change is wanted, reviewed and agreed, the developer wants it specified, so they can build it."
```

