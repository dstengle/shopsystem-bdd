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
