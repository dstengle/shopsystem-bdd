---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/product
title: Product
narrator: the person
group: service
area: specification
specifies: service product
language: codified-2
retired: []
unbuilt: [r15, r16, r17, r18, r19, r20, r21]
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

### [g15] A subdomain is declared with its id, type and jobs
- [r15] When the person declares a subdomain with an id and a subdomain type and a job, the product service shall keep the subdomain in the product and complete the request.

### [g16] A subdomain of a type outside the subdomain type form is refused
- [r16] If the person declares a subdomain with a subdomain type that does not conform to the subdomain type form, then the product service shall refuse the request and name the subdomain type.

### [g17] A subdomain serving a job the product does not hold is refused
- [r17] If the person declares a subdomain with a job that is not in the product, then the product service shall refuse the request and name the job.

### [g18] A bounded context a shop keeps is declared in the domain map
- [r18] When the person declares a bounded context with an id and a subdomain and a shop, the product service shall keep the bounded context in the product and complete the request.

### [g19] A third-party provider is declared as a bounded context no shop keeps
- [r19] When the person declares a bounded context with an id and a subdomain and without a shop, the product service shall keep the bounded context in the product and complete the request.

### [g20] A bounded context whose id lies outside the product is refused
- [r20] If the person declares a bounded context with an id that the id of this product does not cover, then the product service shall refuse the request and name the id.

### [g21] A bounded context addressing a subdomain the product does not hold is refused
- [r21] If the person declares a bounded context with a subdomain that is not in the product, then the product service shall refuse the request and name the subdomain.

