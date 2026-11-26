# shop: every live line with its intended reading

## r1
From: b576 r1.

```reading
When the person entrusts a bounded context with an id, the shop service shall keep the bounded context in the shop and complete the request.
shall [x1: agent the person (constant), x4: service the shop service (constant), x5: shop "the shop the request is made in" (indexical), x6: request "the request the trigger makes" (indexical)]
  when [x2: bounded context, x3: id]
    request(e1, shop.keep, subject: x1, object: x2)
    param(e1, id, x3)
  response
    in(x2, x5)
    keep(e2, subject: x4, object: x2)
    complete(e3, subject: x4, object: x6)
```

## r2
From: b576 r2.

```reading
If the person entrusts a bounded context with an id that the product id of the shop does not cover, then the shop service shall refuse the request and name the id.
shall [x1: agent the person (constant), x4: shop "the shop the request is made in" (indexical), x6: service the shop service (constant), x7: request "the request the trigger makes" (indexical)]
  if [x2: bounded context, x3: id, x5: product id]
    of(x5, x4)
    not
      cover(subject: x5, object: x3)
    request(e1, shop.keep, subject: x1, object: x2)
    param(e1, id, x3)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r3
From: b576 r3.

```reading
While a bounded context that has an id is in the shop, if the person entrusts a bounded context with the id, then the shop service shall refuse the request and name the id.
shall [x3: shop "the shop the request is made in" (indexical), x4: agent the person (constant), x6: service the shop service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: bounded context, x2: id]
    of(x2, x1)
    in(x1, x3)
  if [x5: bounded context]
    request(e1, shop.keep, subject: x4, object: x5)
    param(e1, id, x2)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
```

## r4
From: b576 r4.

```reading
When the person lists the shop, the shop service shall return every bounded context that is in the shop.
shall [x1: agent the person (constant), x2: shop "the shop the request is made in" (indexical), x3: service the shop service (constant)]
  when
    request(e1, shop.list, subject: x1, object: x2)
  response
    every [x4: bounded context]
      in(x4, x2)
      scope
        return(e2, subject: x3, object: x4)
```

## r5
From: b576 r5.

```reading
While no bounded context is in the shop, when the person lists the shop, the shop service shall return this bounded context.
shall [x2: shop "the shop the request is made in" (indexical), x3: agent the person (constant), x4: service the shop service (constant), x5: bounded context "the bounded context the request is made in" (indexical)]
  while
    not [x1: bounded context]
      in(x1, x2)
  when
    request(e1, shop.list, subject: x3, object: x2)
  response
    return(e2, subject: x4, object: x5)
```
