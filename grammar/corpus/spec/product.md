# product: every live line with its intended reading

## r1
From: b602 r1.

```reading
When the person declares a product with an id and a purpose, the product service shall keep the product and complete the request.
shall [x1: agent the person (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: product, x3: id, x4: purpose]
    request(e1, product.declare, subject: x1, object: x2)
    param(e1, id, x3)
    param(e1, purpose, x4)
  response
    keep(e2, subject: x5, object: x2)
    complete(e3, subject: x5, object: x6)
```

## r2
From: b602 r2.

```reading
When the person declares a product actor, the product service shall keep the product actor in the product and complete the request.
shall [x1: agent the person (constant), x3: service the product service (constant), x4: product "the product this bounded context belongs to" (indexical), x5: request "the request the trigger makes" (indexical)]
  when [x2: product actor]
    request(e1, product.declare actor, subject: x1, object: x2)
  response
    in(x2, x4)
    keep(e2, subject: x3, object: x2)
    complete(e3, subject: x3, object: x5)
```

## r3
From: b602 r3.

```reading
When the person declares a job with an id and a product actor and a job statement, the product service shall keep the job in the product and complete the request.
shall [x1: agent the person (constant), x6: service the product service (constant), x7: product "the product this bounded context belongs to" (indexical), x8: request "the request the trigger makes" (indexical)]
  when [x2: job, x3: id, x4: product actor, x5: job statement]
    request(e1, product.declare job, subject: x1, object: x2)
    param(e1, id, x3)
    param(e1, product actor, x4)
    param(e1, job statement, x5)
  response
    in(x2, x7)
    keep(e2, subject: x6, object: x2)
    complete(e3, subject: x6, object: x8)
```

## r4
From: b602 r4.

```reading
If the person declares a job with a job statement that does not conform to the job statement form, then the product service shall refuse the request and name the job statement.
shall [x1: agent the person (constant), x4: artifact the job statement form (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: job, x3: job statement]
    not
      conforms(x3, x4)
    request(e1, product.declare job, subject: x1, object: x2)
    param(e1, job statement, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r5
From: b602 r5.

```reading
If the person declares a job with a product actor that is not in the product, then the product service shall refuse the request and name the product actor.
shall [x1: agent the person (constant), x4: product "the product this bounded context belongs to" (indexical), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: job, x3: product actor]
    not
      in(x3, x4)
    request(e1, product.declare job, subject: x1, object: x2)
    param(e1, product actor, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r6
From: b602 r6.

```reading
If the person declares a job with a need that is not in the product, then the product service shall refuse the request and name the need.
shall [x1: agent the person (constant), x4: product "the product this bounded context belongs to" (indexical), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: job, x3: need]
    not
      in(x3, x4)
    request(e1, product.declare job, subject: x1, object: x2)
    param(e1, need, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r7
From: b602 r7.

```reading
If the person declares a job with a need that depends on the job, then the product service shall refuse the request and name the need.
shall [x1: agent the person (constant), x4: service the product service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: job, x3: need]
    depend on(subject: x3, object: x2)
    request(e1, product.declare job, subject: x1, object: x2)
    param(e1, need, x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
```

## r8
From: b673 r8.

```reading
While this product holds a product detail, when the person declares a product with an id and a purpose, the product service shall keep the product detail in the product and complete the request.
shall [x1: product "the product this bounded context belongs to" (indexical), x3: agent the person (constant), x7: service the product service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x2: product detail]
    in(x2, x1)
  when [x4: product, x5: id, x6: purpose]
    request(e1, product.declare, subject: x3, object: x4)
    param(e1, id, x5)
    param(e1, purpose, x6)
  response
    in(x2, x4)
    keep(e2, subject: x7, object: x2)
    complete(e3, subject: x7, object: x8)
```

## r9
From: b673 r9.

```reading
While this product holds a product detail, when the person declares a product actor, the product service shall keep the product detail in the product and complete the request.
shall [x1: product "the product this bounded context belongs to" (indexical), x3: agent the person (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x2: product detail]
    in(x2, x1)
  when [x4: product actor]
    request(e1, product.declare actor, subject: x3, object: x4)
  response
    in(x2, x1)
    keep(e2, subject: x5, object: x2)
    complete(e3, subject: x5, object: x6)
```

## r10
From: b673 r10.

```reading
While this product holds a product detail, when the person declares a job with an id and a product actor and a job statement, the product service shall keep the product detail in the product and complete the request.
shall [x1: product "the product this bounded context belongs to" (indexical), x3: agent the person (constant), x8: service the product service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x2: product detail]
    in(x2, x1)
  when [x4: job, x5: id, x6: product actor, x7: job statement]
    request(e1, product.declare job, subject: x3, object: x4)
    param(e1, id, x5)
    param(e1, product actor, x6)
    param(e1, job statement, x7)
  response
    in(x2, x1)
    keep(e2, subject: x8, object: x2)
    complete(e3, subject: x8, object: x9)
```

## r11
From: b673 r11.

```reading
While this product does not conform to the product form, if the person declares a product with an id and a purpose, then the product service shall refuse the request and name this product.
shall [x1: product "the product this bounded context belongs to" (indexical), x2: artifact the product form (constant), x3: agent the person (constant), x7: service the product service (constant), x8: request "the request the trigger makes" (indexical)]
  while
    not
      conforms(x1, x2)
  if [x4: product, x5: id, x6: purpose]
    request(e1, product.declare, subject: x3, object: x4)
    param(e1, id, x5)
    param(e1, purpose, x6)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x1)
```

## r12
From: b673 r12.

```reading
While this product does not conform to the product form, if the person declares a product actor, then the product service shall refuse the request and name this product.
shall [x1: product "the product this bounded context belongs to" (indexical), x2: artifact the product form (constant), x3: agent the person (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    not
      conforms(x1, x2)
  if [x4: product actor]
    request(e1, product.declare actor, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r13
From: b673 r13.

```reading
While this product does not conform to the product form, if the person declares a job with an id and a product actor and a job statement, then the product service shall refuse the request and name this product.
shall [x1: product "the product this bounded context belongs to" (indexical), x2: artifact the product form (constant), x3: agent the person (constant), x8: service the product service (constant), x9: request "the request the trigger makes" (indexical)]
  while
    not
      conforms(x1, x2)
  if [x4: job, x5: id, x6: product actor, x7: job statement]
    request(e1, product.declare job, subject: x3, object: x4)
    param(e1, id, x5)
    param(e1, product actor, x6)
    param(e1, job statement, x7)
  response
    refuse(e2, subject: x8, object: x9)
    name(e3, subject: x8, object: x1)
```

## r14
From: b674 r14.

```reading
When the person declares a job with a job statement that conforms to the job statement form, the product service shall keep the job in the product and complete the request.
shall [x1: agent the person (constant), x4: artifact the job statement form (constant), x5: service the product service (constant), x6: product "the product this bounded context belongs to" (indexical), x7: request "the request the trigger makes" (indexical)]
  when [x2: job, x3: job statement]
    conforms(x3, x4)
    request(e1, product.declare job, subject: x1, object: x2)
    param(e1, job statement, x3)
  response
    in(x2, x6)
    keep(e2, subject: x5, object: x2)
    complete(e3, subject: x5, object: x7)
```

## r15
From: b642 r15.

```reading
When the person declares a subdomain with an id and a subdomain type and a job, the product service shall keep the subdomain in the product and complete the request.
shall [x1: agent the person (constant), x6: service the product service (constant), x7: product "the product this bounded context belongs to" (indexical), x8: request "the request the trigger makes" (indexical)]
  when [x2: subdomain, x3: id, x4: subdomain type, x5: job]
    request(e1, product.declare subdomain, subject: x1, object: x2)
    param(e1, id, x3)
    param(e1, subdomain type, x4)
    param(e1, job, x5)
  response
    in(x2, x7)
    keep(e2, subject: x6, object: x2)
    complete(e3, subject: x6, object: x8)
```

## r16
From: b642 r16.

```reading
If the person declares a subdomain with a subdomain type that does not conform to the subdomain type form, then the product service shall refuse the request and name the subdomain type.
shall [x1: agent the person (constant), x4: artifact the subdomain type form (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: subdomain, x3: subdomain type]
    not
      conforms(x3, x4)
    request(e1, product.declare subdomain, subject: x1, object: x2)
    param(e1, subdomain type, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r17
From: b642 r17.

```reading
If the person declares a subdomain with a job that is not in the product, then the product service shall refuse the request and name the job.
shall [x1: agent the person (constant), x4: product "the product this bounded context belongs to" (indexical), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: subdomain, x3: job]
    not
      in(x3, x4)
    request(e1, product.declare subdomain, subject: x1, object: x2)
    param(e1, job, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r19
From: b642 r19.

```reading
When the person declares a bounded context with an id and a subdomain and without a shop, the product service shall keep the bounded context in the product and complete the request.
shall [x1: agent the person (constant), x5: service the product service (constant), x6: product "the product this bounded context belongs to" (indexical), x7: request "the request the trigger makes" (indexical)]
  when [x2: bounded context, x3: id, x4: subdomain]
    request(e1, product.declare context, subject: x1, object: x2)
    param(e1, id, x3)
    param(e1, subdomain, x4)
    noparam(e1, shop)
  response
    in(x2, x6)
    keep(e2, subject: x5, object: x2)
    complete(e3, subject: x5, object: x7)
```

## r20
From: b642 r20.

```reading
If the person declares a bounded context with an id that the id of this product does not cover, then the product service shall refuse the request and name the id.
shall [x1: agent the person (constant), x4: product "the product this bounded context belongs to" (indexical), x6: service the product service (constant), x7: request "the request the trigger makes" (indexical)]
  if [x2: bounded context, x3: id, x5: id]
    of(x5, x4)
    not
      cover(subject: x5, object: x3)
    request(e1, product.declare context, subject: x1, object: x2)
    param(e1, id, x3)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x5)
```

## r21
From: b642 r21.

```reading
If the person declares a bounded context with a subdomain that is not in the product, then the product service shall refuse the request and name the subdomain.
shall [x1: agent the person (constant), x4: product "the product this bounded context belongs to" (indexical), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: bounded context, x3: subdomain]
    not
      in(x3, x4)
    request(e1, product.declare context, subject: x1, object: x2)
    param(e1, subdomain, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r22
From: b675 r22.

```reading
When the person assigns a job to a bounded context, the product service shall keep the job in the bounded context and complete the request.
shall [x1: agent the person (constant), x4: service the product service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: job, x3: bounded context]
    request(e1, product.assign, subject: x1, object: x2, to: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
    complete(e3, subject: x4, object: x5)
```

## r23
From: b675 r23.

```reading
While a bounded context holds a job, if the person assigns the job to a bounded context, then the product service shall refuse the request and name the job.
shall [x3: agent the person (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: bounded context, x2: job]
    in(x2, x1)
  if [x4: bounded context]
    request(e1, product.assign, subject: x3, object: x2, to: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r24
From: b675 r24.

```reading
When the person maps a product actor with a bounded context and an actor, the product service shall keep the product actor in the bounded context and complete the request.
shall [x1: agent the person (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: product actor, x3: bounded context, x4: actor]
    request(e1, product.map, subject: x1, object: x2)
    param(e1, bounded context, x3)
    param(e1, actor, x4)
  response
    in(x2, x3)
    keep(e2, subject: x5, object: x2)
    complete(e3, subject: x5, object: x6)
```

## r25
From: b675 r25.

```reading
If the person maps a product actor that is not in the product, then the product service shall refuse the request and name the product actor.
shall [x1: agent the person (constant), x3: product "the product this bounded context belongs to" (indexical), x4: service the product service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: product actor]
    not
      in(x2, x3)
    request(e1, product.map, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r26
From: b644 r26.

```reading
While a requirement group serves a job and the requirement group has a requirement, when the person traces the job, the product service shall return the requirement.
shall [x4: agent the person (constant), x5: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement]
    serve(subject: x1, object: x2)
    of(x3, x1)
  when
    request(e1, product.trace, subject: x4, object: x2)
  response
    return(e2, subject: x5, object: x3)
```

## r27
From: b644 r27.

```reading
While a requirement group serves a job and a requirement of the requirement group uses an operation and a different requirement governs the operation, when the person traces the job, the product service shall return the requirement.
shall [x6: agent the person (constant), x7: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement, x4: operation, x5: requirement]
    serve(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    distinct(x5, x3)
    govern(subject: x5, object: x4)
  when
    request(e1, product.trace, subject: x6, object: x2)
  response
    return(e2, subject: x7, object: x5)
```

## r28
From: b644 r28.

```reading
While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and an adapter spec realises the requirement id of the port line, when the person traces the job, the product service shall return the adapter spec.
shall [x8: agent the person (constant), x9: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement, x4: operation, x5: port line, x6: adapter spec, x7: requirement id]
    serve(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    govern(subject: x5, object: x4)
    of(x7, x5)
    realise(subject: x6, object: x7)
  when
    request(e1, product.trace, subject: x8, object: x2)
  response
    return(e2, subject: x9, object: x6)
```

## r29
From: b644 r29.

```reading
While a requirement group serves a need and the requirement group has a requirement, when the person traces a job that needs the need, the product service shall return the requirement.
shall [x4: agent the person (constant), x6: service the product service (constant)]
  while [x1: requirement group, x2: need, x3: requirement]
    serve(subject: x1, object: x2)
    of(x3, x1)
  when [x5: job]
    need(subject: x5, object: x2)
    request(e1, product.trace, subject: x4, object: x5)
  response
    return(e2, subject: x6, object: x3)
```

## r30
From: b644 r30.

```reading
If the person traces a job that no requirement group serves, then the product service shall refuse the request and name the job.
shall [x1: agent the person (constant), x4: service the product service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: job]
    not [x3: requirement group]
      serve(subject: x3, object: x2)
    request(e1, product.trace, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r31
From: b680 r31.

```reading
While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and the operation has no property that refers to an operation and no requirement handles an operation outcome of the operation, when the person traces the job, the product service shall return the job whose coordination is `port request`.
shall [x10: agent the person (constant), x11: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement, x4: operation, x5: port line]
    serve(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    govern(subject: x5, object: x4)
    not [x6: property, x7: operation]
      refer#2(subject: x6, to: x7)
      of(x6, x4)
    not [x8: requirement, x9: operation outcome]
      of(x9, x4)
      handle(subject: x8, object: x9)
  when
    request(e1, product.trace, subject: x10, object: x2)
  response
    coordination(x2) = `port request`
    return(e2, subject: x11, object: x2)
```

## r32
From: b680 r32.

```reading
While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and a requirement that handles an operation outcome of the operation uses an operation that performs a transition, when the person traces the job, the product service shall return the job whose coordination is `long-running process`.
shall [x10: agent the person (constant), x11: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement, x4: operation, x5: port line, x6: requirement, x7: operation outcome, x8: operation, x9: transition]
    serve(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    govern(subject: x5, object: x4)
    of(x7, x4)
    handle(subject: x6, object: x7)
    perform(subject: x8, object: x9)
    use(subject: x6, object: x8)
  when
    request(e1, product.trace, subject: x10, object: x2)
  response
    coordination(x2) = `long-running process`
    return(e2, subject: x11, object: x2)
```

## r33
From: b680 r33.

```reading
While a requirement group serves a job and a requirement of the requirement group uses two operations in a driven port that have a property that refers to an operation, when the person traces the job, the product service shall return the job whose coordination is `saga`.
shall [x9: agent the person (constant), x10: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement, x4: operation, x5: driven port, x6: property, x7: operation, x8: operation]
    serve(subject: x1, object: x2)
    of(x3, x1)
    in(x4, x5)
    refer#2(subject: x6, to: x7)
    of(x6, x4)
    use(subject: x3, object: x4)
    distinct(x8, x4)
    in(x8, x5)
    of(x6, x8)
    use(subject: x3, object: x8)
  when
    request(e1, product.trace, subject: x9, object: x2)
  response
    coordination(x2) = `saga`
    return(e2, subject: x10, object: x2)
```

## r34
Retires: r18. From: b706 r34.

```reading
While a shop has a product, when the person declares a bounded context with an id and a subdomain and the shop, the product service shall keep the bounded context in the product and complete the request.
shall [x3: agent the person (constant), x7: service the product service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: shop, x2: product]
    of(x2, x1)
  when [x4: bounded context, x5: id, x6: subdomain]
    request(e1, product.declare context, subject: x3, object: x4)
    param(e1, id, x5)
    param(e1, subdomain, x6)
    param(e1, shop, x1)
  response
    in(x4, x2)
    keep(e2, subject: x7, object: x4)
    complete(e3, subject: x7, object: x8)
```

## r35
From: b637 r35.

```reading
While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and an adapter spec realises the requirement id of the port line and the operation uses another operation and the adapter spec holds a contract that holds a requirement that governs the operation, when the person traces the job, the product service shall return the requirement.
shall [x11: agent the person (constant), x12: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement, x4: operation, x5: port line, x6: adapter spec, x7: requirement id, x8: operation, x9: contract, x10: requirement]
    serve(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    govern(subject: x5, object: x4)
    of(x7, x5)
    realise(subject: x6, object: x7)
    distinct(x8, x4)
    use#2(subject: x4, object: x8)
    govern(subject: x10, object: x8)
    in(x10, x9)
    in(x9, x6)
  when
    request(e1, product.trace, subject: x11, object: x2)
  response
    return(e2, subject: x12, object: x10)
```

## r36
From: b738 r36.

```reading
While a requirement group serves a job and a requirement of the requirement group uses an operation and a port line governs the operation and an adapter spec realises the requirement id of the port line and the operation uses another operation and the adapter spec holds a contract that holds a different requirement that governs the operation and the requirement has the requirement id, when the person traces the job, the product service shall return the requirement.
shall [x11: agent the person (constant), x12: service the product service (constant)]
  while [x1: requirement group, x2: job, x3: requirement, x4: operation, x5: port line, x6: adapter spec, x7: requirement id, x8: operation, x9: contract, x10: requirement]
    serve(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    govern(subject: x5, object: x4)
    of(x7, x5)
    realise(subject: x6, object: x7)
    distinct(x8, x4)
    use#2(subject: x4, object: x8)
    distinct(x10, x5)
    govern(subject: x10, object: x8)
    in(x10, x9)
    in(x9, x6)
    of(x7, x10)
  when
    request(e1, product.trace, subject: x11, object: x2)
  response
    return(e2, subject: x12, object: x10)
```

## r37
From: b793 r37.

```reading
If the person declares a bounded context with an id that does not conform to the context id form, then the product service shall refuse the request and name the id.
shall [x1: agent the person (constant), x4: artifact the context id form (constant), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: bounded context, x3: id]
    not
      conforms(x3, x4)
    request(e1, product.declare context, subject: x1, object: x2)
    param(e1, id, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r38
From: b793 r38.

```reading
If the person assigns a job to a bounded context whose id does not conform to the context id form, then the product service shall refuse the request and name the id.
shall [x1: agent the person (constant), x5: artifact the context id form (constant), x6: service the product service (constant), x7: request "the request the trigger makes" (indexical)]
  if [x2: job, x3: bounded context, x4: id]
    of(x4, x3)
    not
      conforms(x4, x5)
    request(e1, product.assign, subject: x1, object: x2, to: x3)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x4)
```

## r39
From: b793 r39.

```reading
If the person assigns a job to a bounded context that is not in the product, then the product service shall refuse the request and name the bounded context.
shall [x1: agent the person (constant), x4: product "the product this bounded context belongs to" (indexical), x5: service the product service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: job, x3: bounded context]
    not
      in(x3, x4)
    request(e1, product.assign, subject: x1, object: x2, to: x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```
