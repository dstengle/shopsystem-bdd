---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/product
title: Product
narrator: the person
group: service
area: specification
specifies: service product
language: codified-2
retired: []
unbuilt: [r31]
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

### [g22] A job is assigned to the bounded context that serves it
- [r22] When the person assigns a job to a bounded context, the product service shall keep the job in the bounded context and complete the request.

### [g23] A job assigned to a bounded context is not assigned again
- [r23] While a bounded context holds a job, if the person assigns the job to a bounded context, then the product service shall refuse the request and name the job.

### [g24] A product actor is mapped to the actor a bounded context calls it by
- [r24] When the person maps a product actor with a bounded context and an actor, the product service shall keep the product actor in the bounded context and complete the request.

### [g25] A product actor the product does not hold is not mapped
- [r25] If the person maps a product actor that is not in the product, then the product service shall refuse the request and name the product actor.

### [g26] A job's trace holds the requirements of the groups that serve it
- [r26] While a requirement group serves a job and the requirement group has a requirement, when the person traces the job, the product service shall return the requirement.

### [g27] A job's trace holds the requirements that govern the operations its requirements use
- [r27] While a requirement group serves a job and a requirement of the requirement group uses an operation and a different requirement governs the operation, when the person traces the job, the product service shall return the requirement.

### [g28] A job's trace holds the adapter specs that realise the port lines it reaches
- [r28] While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and an adapter spec realises the requirement id of the port line, when the person traces the job, the product service shall return the adapter spec.

### [g29] A job's trace holds the traces of the jobs it needs
- [r29] While a requirement group serves a need and the requirement group has a requirement, when the person traces a job that needs the need, the product service shall return the requirement.

### [g30] A job that no requirement group serves is not traced
- [r30] If the person traces a job that no requirement group serves, then the product service shall refuse the request and name the job.

### [g31] A job whose trace makes a port request no line awaits is coordinated by a port request
- [r31] While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and the operation has no property that refers to an operation and no requirement handles an operation outcome of the operation, when the person traces the job, the product service shall return the job whose coordination is `port request`.

### [g32] A job whose trace awaits a port's reply in a lifecycle is coordinated by a long-running process
- [r32] While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and a requirement that handles an operation outcome of the operation uses an operation that performs a transition, when the person traces the job, the product service shall return the job whose coordination is `long-running process`.

### [g33] A job whose trace makes compensated requests of two ports is coordinated by a saga
- [r33] While a requirement group serves a job and a requirement of the requirement group uses two operations in a driven port that have a property that refers to an operation, when the person traces the job, the product service shall return the job whose coordination is `saga`.

