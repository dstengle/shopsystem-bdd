# reading: every live line with its intended reading (the domain contract, 0.38.0)

## r62
From: b334 r62.

```reading
When the person parses a requirement that uses `order-by` with the logical form, the language service shall return a logical form that uses an order of a member of a collection.
shall [x1: agent the person (constant), x3: thing `order-by` (parameter), x4: service the language service (constant)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
    param(e1, logical form, on)
  response [x5: logical form, x6: order, x7: member, x8: collection]
    of(x7, x8)
    of(x6, x7)
    use(subject: x5, object: x6)
    return(e2, subject: x4, object: x5)
```
