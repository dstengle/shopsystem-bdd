# parsing: every live line with its intended reading

## r1
From: b369 r1.

```reading
When the person parses a requirement that conforms to the language reference, the language service shall complete the request.
shall [x1: agent the person (constant), x3: artifact the language reference (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    conforms(x2, x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r2
From: b369 r2.

```reading
When the person parses a requirement that conforms to the language reference with the logical form, the language service shall return one logical form of the requirement and complete the request.
shall [x1: agent the person (constant), x3: artifact the language reference (constant), x4: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    conforms(x2, x3)
    request(e1, language.parse, subject: x1, object: x2)
    param(e1, logical form, on)
  response
    count exactly 1 [x5: logical form]
      of(x5, x2)
      scope
        return(e2, subject: x4, object: x5)
    complete(e3, subject: x4, object: x6)
```

## r3
From: b369 r3.

```reading
If the person parses a requirement that does not conform to the language reference, then the language service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x3: artifact the language reference (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement]
    not
      conforms(x2, x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r5
From: b369 r5.

```reading
If the person parses a requirement that violates a reading rule, then the language service shall refuse the request and name the reading rule.
shall [x1: agent the person (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: reading rule]
    violate(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
```

## r6
From: b369 r6.

```reading
If the person parses a requirement that uses a construct that has no catalogue entry, then the language service shall refuse the request and name the construct.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: construct]
    not [x4: catalogue entry]
      of(x4, x3)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r7
From: b369 r7.

```reading
If the person parses a fragment, then the language service shall refuse the request, name the fragment and return a term.
shall [x1: agent the person (constant), x3: service the language service (constant), x4: request "the request the trigger makes" (indexical)]
  if [x2: fragment]
    request(e1, language.parse, subject: x1, object: x2)
  response [x5: term]
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x2)
    return(e4, subject: x3, object: x5)
```

## r8
From: b369 r8.

```reading
While the corpus holds a logical form of a requirement, when the person parses the requirement with the logical form, the language service shall return the logical form.
shall [x1: corpus "the corpus of the bounded context the command runs in" (indexical), x4: agent the person (constant), x5: service the language service (constant)]
  while [x2: logical form, x3: requirement]
    of(x2, x3)
    in(x2, x1)
  when
    request(e1, language.parse, subject: x4, object: x3)
    param(e1, logical form, on)
  response
    return(e2, subject: x5, object: x2)
```

## r9
From: b369 r9.

```reading
While a parse cache holds the parse of a requirement, when the person parses the requirement, the language service shall return the parse of the requirement, keep no compiled grammar and complete the request.
shall [x4: agent the person (constant), x5: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: parse cache, x2: requirement, x3: parse]
    of(x3, x2)
    in(x3, x1)
  when
    request(e1, language.parse, subject: x4, object: x2)
  response
    return(e2, subject: x5, object: x3)
    not [x6: compiled grammar]
      keep(e3, subject: x5, object: x6)
    complete(e4, subject: x5, object: x7)
```

## r10
From: b369 r10.

```reading
While a requirement has a parse that no parse cache holds, when the person parses the requirement, the language service shall keep a parse cache and complete the request.
shall [x4: agent the person (constant), x5: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: parse]
    not [x3: parse cache]
      in(x2, x3)
    of(x2, x1)
  when
    request(e1, language.parse, subject: x4, object: x1)
  response [x6: parse cache]
    keep(e2, subject: x5, object: x6)
    complete(e3, subject: x5, object: x7)
```

## r11
From: b369 r11.

```reading
While a requirement has a parse that no parse cache holds and the compiled grammar of the requirement exists, when the person parses the requirement, the language service shall keep no compiled grammar and complete the request.
shall [x5: agent the person (constant), x6: service the language service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: parse, x4: compiled grammar]
    not [x3: parse cache]
      in(x2, x3)
    of(x2, x1)
    of(x4, x1)
    exists(x4)
  when
    request(e1, language.parse, subject: x5, object: x1)
  response
    not [x7: compiled grammar]
      keep(e2, subject: x6, object: x7)
    complete(e3, subject: x6, object: x8)
```

## r12
From: b370 r12.

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

## r13
From: b420 r13.

```reading
While a verb has two frames, when the person parses a requirement that uses a frame of the verb, the language service shall return one logical form of the requirement and complete the request.
shall [x4: agent the person (constant), x7: service the language service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: verb, x2: frame, x3: frame]
    of(x2, x1)
    distinct(x3, x2)
    of(x3, x1)
  when [x5: requirement, x6: frame]
    of(x6, x1)
    use(subject: x5, object: x6)
    request(e1, language.parse, subject: x4, object: x5)
  response
    count exactly 1 [x8: logical form]
      of(x8, x5)
      scope
        return(e2, subject: x7, object: x8)
    complete(e3, subject: x7, object: x9)
```

## r14
From: b420 r14.

```reading
If the person parses a requirement that has a plural object, then the language service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: plural object]
    of(x3, x2)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r15
Retires: r4. From: b420 r15.

```reading
If the person parses a requirement that has more than one logical form, then the language service shall refuse the request and name the requirement and the ambiguous text of the requirement.
shall [x1: agent the person (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement]
    count more than 1 [x3: logical form]
      scope
        of(x3, x2)
    request(e1, language.parse, subject: x1, object: x2)
  response [x6: ambiguous text]
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
    of(x6, x2)
    name(e4, subject: x4, object: x6)
```

## r16
From: b420 r16.

```reading
If the person parses a requirement whose ambiguous text uses two frames of a verb, then the language service shall refuse the request and name every frame that the ambiguous text uses.
shall [x1: agent the person (constant), x7: service the language service (constant), x8: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: ambiguous text, x4: frame, x5: verb, x6: frame]
    of(x3, x2)
    of(x4, x5)
    use(subject: x3, object: x4)
    distinct(x6, x4)
    of(x6, x5)
    use(subject: x3, object: x6)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x7, object: x8)
    every [x9: frame]
      use(subject: x3, object: x9)
      scope
        name(e3, subject: x7, object: x9)
```

## r17
From: b418 r17.

```reading
When the person parses a requirement that uses `param-of`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `param-of` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r18
From: b418 r18.

```reading
When the person parses a requirement that uses `param-of` with the logical form, the language service shall return a logical form that holds a value in use.
shall [x1: agent the person (constant), x3: thing `param-of` (parameter), x4: service the language service (constant)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
    param(e1, logical form, on)
  response [x5: logical form, x6: value in use]
    in(x6, x5)
    return(e2, subject: x4, object: x5)
```

## r19
From: b452 r19.

```reading
While an item holds a term, when the person previews a requirement that uses the term for the item, the language service shall complete the request.
shall [x3: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: term]
    in(x2, x1)
  when [x4: requirement]
    use(subject: x4, object: x2)
    request(e1, language.preview, subject: x3, object: x4, for: x1)
  response
    complete(e2, subject: x5, object: x6)
```

## r20
From: b452 r20.

```reading
While an item holds a term, when the person previews a requirement that uses the term for the item with the logical form, the language service shall return one logical form of the requirement and complete the request.
shall [x3: agent the person (constant), x5: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: term]
    in(x2, x1)
  when [x4: requirement]
    use(subject: x4, object: x2)
    request(e1, language.preview, subject: x3, object: x4, for: x1)
    param(e1, logical form, on)
  response
    count exactly 1 [x6: logical form]
      of(x6, x4)
      scope
        return(e2, subject: x5, object: x6)
    complete(e3, subject: x5, object: x7)
```

## r22
From: b452 r22.

```reading
If the person previews a requirement that does not conform to the language reference for an item, then the language service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x3: artifact the language reference (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x4: item]
    not
      conforms(x2, x3)
    request(e1, language.preview, subject: x1, object: x2, for: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r23
From: b543 r23.

```reading
When the person parses a requirement that uses `response-request`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `response-request` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r24
From: b543 r24.

```reading
When the person parses a requirement that uses `response-request` with the logical form, the language service shall return a logical form that uses `request-params`.
shall [x1: agent the person (constant), x3: thing `response-request` (parameter), x4: service the language service (constant), x6: thing `request-params` (parameter)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
    param(e1, logical form, on)
  response [x5: logical form]
    use(subject: x5, object: x6)
    return(e2, subject: x4, object: x5)
```

## r25
From: b626 r25.

```reading
When the person parses a requirement that uses `reply-trigger`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `reply-trigger` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r26
From: b626 r26.

```reading
When the person parses a requirement that uses `reply-trigger` with the logical form, the language service shall return a logical form that holds a replied request.
shall [x1: agent the person (constant), x3: thing `reply-trigger` (parameter), x4: service the language service (constant)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
    param(e1, logical form, on)
  response [x5: logical form, x6: replied request]
    in(x6, x5)
    return(e2, subject: x4, object: x5)
```

## r27
From: b726 r27.

```reading
While a requirement uses `reply-trigger` and the requirement has a plural object, if the person parses the requirement, then the language service shall refuse the request and name the requirement.
shall [x2: thing `reply-trigger` (parameter), x4: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: plural object]
    use(subject: x1, object: x2)
    of(x3, x1)
  if
    request(e1, language.parse, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r28
From: b727 r28.

```reading
When the person parses a requirement that uses `reply-failure` with the logical form, the language service shall return a logical form that holds a replied request.
shall [x1: agent the person (constant), x3: thing `reply-failure` (parameter), x4: service the language service (constant)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
    param(e1, logical form, on)
  response [x5: logical form, x6: replied request]
    in(x6, x5)
    return(e2, subject: x4, object: x5)
```

## r29
From: b727 r29.

```reading
When the person parses a requirement that uses `reply-failure`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `reply-failure` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```
