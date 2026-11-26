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

## r18
From: b642 r18.

```reading
When the person declares a bounded context with an id and a subdomain and a shop, the product service shall keep the bounded context in the product and complete the request.
shall [x1: agent the person (constant), x6: service the product service (constant), x7: product "the product this bounded context belongs to" (indexical), x8: request "the request the trigger makes" (indexical)]
  when [x2: bounded context, x3: id, x4: subdomain, x5: shop]
    request(e1, product.declare context, subject: x1, object: x2)
    param(e1, id, x3)
    param(e1, subdomain, x4)
    param(e1, shop, x5)
  response
    in(x2, x7)
    keep(e2, subject: x6, object: x2)
    complete(e3, subject: x6, object: x8)
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
      cover#2(subject: x5, object: x3)
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
