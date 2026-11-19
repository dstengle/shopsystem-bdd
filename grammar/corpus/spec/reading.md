# reading: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: design-model-check#r205, reworded in request words (0.38.0).

```reading
If the person parses a requirement that omits an object of a term, then the language service shall refuse the request and name the term.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: object, x4: term]
    of(x3, x4)
    omit(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
```

## r2
From: design-model-check#r206, reworded in request words (0.38.0).

```reading
If the person parses a requirement that omits a recipient of a term, then the language service shall refuse the request and name the term.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: recipient, x4: term]
    of(x3, x4)
    omit(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
```

## r3
From: design-model-check#r209, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `not-condition`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `not-condition` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r4
From: design-model-check#r210, reworded in request words (0.38.0).

```reading
If the person parses a requirement that uses a noun phrase of a term that no frame takes, then the language service shall refuse the request and name the term.
shall [x1: agent the person (constant), x6: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: noun phrase, x4: term]
    of(x3, x4)
    not [x5: frame]
      take(subject: x5, object: x3)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x4)
```

## r5
From: design-model-check#r211, reworded in request words (0.38.0).

```reading
When the person parses a requirement whose precondition uses a term whose aspect is `state`, the language service shall complete the request.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: precondition, x4: term]
    of(x3, x2)
    aspect(x4) = `state`
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x5, object: x6)
```

## r6
From: design-model-check#r212, reworded in request words (0.38.0).

```reading
If the person parses a requirement that uses a passive form that has no by-phrase, then the language service shall refuse the request and name the passive form.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: passive form]
    not [x4: by-phrase]
      of(x4, x3)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r7
From: design-model-check#r213, reworded in request words (0.38.0).

```reading
When the person parses a requirement whose trigger uses a recipient, the language service shall complete the request.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: trigger, x4: recipient]
    of(x3, x2)
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x5, object: x6)
```

## r8
From: design-model-check#r216, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses a term whose frame has a preposition, the language service shall complete the request.
shall [x1: agent the person (constant), x6: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: term, x4: frame, x5: preposition]
    of(x4, x3)
    of(x5, x4)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x6, object: x7)
```

## r9
From: design-model-check#r229, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `bare-plural`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `bare-plural` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r10
From: design-model-check#r230, reworded in request words (0.38.0).

```reading
If the person parses a requirement that uses a term that does not agree with its subject, then the language service shall refuse the request and name the term.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: term, x4: subject]
    of(x4, x3)
    not
      agree(subject: x3, with: x4)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r11
From: design-model-check#r231, reworded in request words (0.38.0).

```reading
If the person parses a requirement whose precondition uses a term whose aspect is `action`, then the language service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: precondition, x4: term]
    of(x3, x2)
    aspect(x4) = `action`
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r12
From: design-model-check#r232, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `request-params`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `request-params` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r13
From: design-model-check#r233, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `of-relation`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `of-relation` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r14
From: design-model-check#r234, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `no-noun`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `no-noun` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r15
From: design-model-check#r235, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `compound`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `compound` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r16
From: design-model-check#r236, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `only`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `only` (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r17
From: design-model-check#r237, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `rc-object`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `rc-object` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r18
From: design-model-check#r238, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `rc-whose`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `rc-whose` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r19
From: design-model-check#r239, reworded in request words (0.38.0).

```reading
If the person parses a requirement that has more than one logical form, then the language service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement]
    count more than 1 [x3: logical form]
      scope
        of(x3, x2)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r20
From: design-model-check#r240, reworded in request words (0.38.0).

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

## r21
From: design-model-check#r241, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `this`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `this` (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r22
From: design-model-check#r242, reworded in request words (0.38.0).

```reading
If the person parses a requirement that uses a definite noun phrase that has no antecedent, then the language service shall refuse the request and name the definite noun phrase.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: definite noun phrase]
    not [x4: antecedent]
      of(x4, x3)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r23
From: design-model-check#r243, reworded in request words (0.38.0).

```reading
If the person parses a requirement whose precondition uses a negated indefinite, then the language service shall refuse the request and name the negated indefinite.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: precondition, x4: negated indefinite]
    of(x3, x2)
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
```

## r24
From: design-model-check#r244, reworded in request words (0.38.0).

```reading
While a requirement has no trigger and the requirement does not use `always-never`, if the person parses the requirement, then the language service shall refuse the request and name the requirement.
shall [x3: thing `always-never` (parameter), x4: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: requirement]
    not [x2: trigger]
      of(x2, x1)
    not
      use(subject: x1, object: x3)
  if
    request(e1, language.parse, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r25
From: design-model-check#r245, reworded in request words (0.38.0).

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

## r26
From: design-model-check#r252, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `count`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `count` (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r27
From: design-model-check#r254, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `moment-compare`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `moment-compare` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r28
From: design-model-check#r255, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses a clock trigger, the language service shall complete the request.
shall [x1: agent the person (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: clock trigger]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r29
From: design-model-check#r256, reworded in request words (0.38.0).

```reading
When the person parses a requirement whose precondition uses a perfect, the language service shall complete the request.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: precondition, x4: perfect]
    of(x3, x2)
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x5, object: x6)
```

## r30
From: design-model-check#r257, reworded in request words (0.38.0).

```reading
If the person parses a requirement that uses a number that has no unit, then the language service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: number]
    not [x4: unit]
      of(x4, x3)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r31
From: design-model-check#r258, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `may`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `may` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r32
From: design-model-check#r259, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `always-never`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `always-never` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r33
From: design-model-check#r279, reworded in request words (0.38.0).

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

## r34
From: design-model-check#r281, reworded in request words (0.38.0).

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

## r35
From: design-model-check#r282, reworded in request words (0.38.0).

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

## r36
From: design-model-check#r283, reworded in request words (0.38.0).

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

## r37
From: design-model-check#r284, reworded in request words (0.38.0).

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

## r38
From: design-model-check#r285, reworded in request words (0.38.0).

```reading
If the person parses a requirement whose trigger uses a term whose aspect is `state`, then the language service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: trigger, x4: term]
    of(x3, x2)
    aspect(x4) = `state`
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r39
From: design-model-check#r293, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `holds-exactly`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `holds-exactly` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r40
From: design-model-check#r295, reworded in request words (0.38.0).

```reading
When the person parses a requirement whose precondition uses `nothing`, the language service shall complete the request.
shall [x1: agent the person (constant), x4: thing `nothing` (parameter), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: precondition]
    of(x3, x2)
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x5, object: x6)
```

## r41
From: design-model-check#r291, reworded in request words (0.38.0).

```reading
When the person parses a requirement whose precondition uses `is-in`, the language service shall complete the request.
shall [x1: agent the person (constant), x4: thing `is-in` (parameter), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: precondition]
    of(x3, x2)
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x5, object: x6)
```

## r42
From: design-model-check#r298, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `value-compare`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `value-compare` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r43
From: design-model-check#r299, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `value-same`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `value-same` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r44
From: design-model-check#r300, reworded in request words (0.38.0).

```reading
While a term has no value order and a requirement uses the term and `value-compare`, if the person parses the requirement, then the language service shall refuse the request and name the term.
shall [x4: thing `value-compare` (parameter), x5: agent the person (constant), x6: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: term, x3: requirement]
    not [x2: value order]
      of(x2, x1)
    use(subject: x3, object: x1)
    use(subject: x3, object: x4)
  if
    request(e1, language.parse, subject: x5, object: x3)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x1)
```

## r45
From: design-model-check#r303, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `order-by`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `order-by` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r46
From: design-model-check#r304, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses `order-by-every`, the language service shall complete the request.
shall [x1: agent the person (constant), x3: thing `order-by-every` (parameter), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    complete(e2, subject: x4, object: x5)
```

## r47
From: design-model-check#r305, reworded in request words (0.38.0).

```reading
When the person parses a requirement that uses an order with the logical form, the language service shall return the order and complete the request.
shall [x1: agent the person (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: requirement, x3: order]
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
    param(e1, logical form, on)
  response
    return(e2, subject: x4, object: x3)
    complete(e3, subject: x4, object: x5)
```

## r48
From: design-model-check#r296, reworded in request words (0.38.0).

```reading
If the person parses a requirement that uses an order on a term that has no value order, then the language service shall refuse the request and name the term.
shall [x1: agent the person (constant), x6: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: order, x4: term]
    not [x5: value order]
      of(x5, x4)
    on(x3, x4)
    use(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x4)
```

## r49
From: design-model-check#r306, reworded in request words (0.38.0).

```reading
If the person parses a requirement whose precondition uses an order, then the language service shall refuse the request and name the order.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: precondition, x4: order]
    of(x3, x2)
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
```

## r50
From: design-model-check#r307, reworded in request words (0.38.0).

```reading
If the person parses a requirement whose trigger uses an order, then the language service shall refuse the request and name the order.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: trigger, x4: order]
    of(x3, x2)
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
```

## r51
From: design-model-check#r308, reworded in request words (0.38.0).

```reading
If the person parses a requirement that forbids an act that holds an order, then the language service shall refuse the request and name the order.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: act, x4: order]
    in(x4, x3)
    forbid(subject: x2, object: x3)
    request(e1, language.parse, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
```

## r52
From: design-model-check#r311, reworded in request words (0.38.0).

```reading
While a sense of a term has a value order and another sense of the term has the value order and a requirement uses the term and `value-compare`, when the person parses the requirement, the language service shall complete the request.
shall [x6: thing `value-compare` (parameter), x7: agent the person (constant), x8: service the language service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: sense, x2: term, x3: value order, x4: sense, x5: requirement]
    of(x1, x2)
    of(x3, x1)
    distinct(x4, x1)
    of(x4, x2)
    of(x3, x4)
    use(subject: x5, object: x2)
    use(subject: x5, object: x6)
  when
    request(e1, language.parse, subject: x7, object: x5)
  response
    complete(e2, subject: x8, object: x9)
```

## r53
From: design-model-check#r312, reworded in request words (0.38.0).

```reading
While a sense of a term has a value order and another sense of the term has the value order and a requirement uses the term and `value-same`, when the person parses the requirement, the language service shall complete the request.
shall [x6: thing `value-same` (parameter), x7: agent the person (constant), x8: service the language service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: sense, x2: term, x3: value order, x4: sense, x5: requirement]
    of(x1, x2)
    of(x3, x1)
    distinct(x4, x1)
    of(x4, x2)
    of(x3, x4)
    use(subject: x5, object: x2)
    use(subject: x5, object: x6)
  when
    request(e1, language.parse, subject: x7, object: x5)
  response
    complete(e2, subject: x8, object: x9)
```

## r54
From: design-model-check#r313, reworded in request words (0.38.0).

```reading
While a sense of a term has a value order and another sense of the term has a different value order and a requirement uses the term and `value-compare`, if the person parses the requirement, then the language service shall refuse the request and name the term.
shall [x7: thing `value-compare` (parameter), x8: agent the person (constant), x9: service the language service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: sense, x2: term, x3: value order, x4: sense, x5: value order, x6: requirement]
    of(x1, x2)
    of(x3, x1)
    distinct(x4, x1)
    of(x4, x2)
    distinct(x5, x3)
    of(x5, x4)
    use(subject: x6, object: x2)
    use(subject: x6, object: x7)
  if
    request(e1, language.parse, subject: x8, object: x6)
  response
    refuse(e2, subject: x9, object: x10)
    name(e3, subject: x9, object: x2)
```

## r55
From: design-model-check#r309, reworded in request words (0.38.0).

```reading
While a sense of a term has a value order and another sense of the term has a different value order and a requirement uses the term and `value-same`, if the person parses the requirement, then the language service shall refuse the request and name the term.
shall [x7: thing `value-same` (parameter), x8: agent the person (constant), x9: service the language service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: sense, x2: term, x3: value order, x4: sense, x5: value order, x6: requirement]
    of(x1, x2)
    of(x3, x1)
    distinct(x4, x1)
    of(x4, x2)
    distinct(x5, x3)
    of(x5, x4)
    use(subject: x6, object: x2)
    use(subject: x6, object: x7)
  if
    request(e1, language.parse, subject: x8, object: x6)
  response
    refuse(e2, subject: x9, object: x10)
    name(e3, subject: x9, object: x2)
```

## r56
From: design-model-check#r317, reworded in request words (0.38.0).

```reading
While a requirement uses `order-by-every` and the requirement uses a verb that has no frame that takes `thing`, when the person parses the requirement, the language service shall complete the request.
shall [x2: thing `order-by-every` (parameter), x5: noun phrase `thing` (constant), x6: agent the person (constant), x7: service the language service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: verb]
    use(subject: x1, object: x2)
    not [x4: frame]
      take(subject: x4, object: x5)
      of(x4, x3)
    use(subject: x1, object: x3)
  when
    request(e1, language.parse, subject: x6, object: x1)
  response
    complete(e2, subject: x7, object: x8)
```

## r57
From: design-model-check#r318, reworded in request words (0.38.0).

```reading
While a requirement uses `order-by-every` and `of-relation`, when the person parses the requirement, the language service shall complete the request.
shall [x2: thing `order-by-every` (parameter), x3: thing `of-relation` (parameter), x4: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: requirement]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
  when
    request(e1, language.parse, subject: x4, object: x1)
  response
    complete(e2, subject: x5, object: x6)
```

## r58
From: design-model-check#r319, reworded in request words (0.38.0).

```reading
If the person parses a requirement whose response uses a term whose aspect is `state`, then the language service shall refuse the request, name the term and the response and not name the trigger.
shall [x1: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: response, x4: term]
    of(x3, x2)
    aspect(x4) = `state`
    use(subject: x3, object: x4)
    request(e1, language.parse, subject: x1, object: x2)
  response [x7: trigger]
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
    name(e4, subject: x5, object: x3)
    of(x7, x2)
    not
      name(e5, subject: x5, object: x7)
```

## r59
From: design-model-check#r326, reworded in request words (0.38.0).

```reading
While a requirement uses `order-by` and a closing comma, when the person parses the requirement, the language service shall complete the request.
shall [x2: thing `order-by` (parameter), x4: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: closing comma]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
  when
    request(e1, language.parse, subject: x4, object: x1)
  response
    complete(e2, subject: x5, object: x6)
```

## r60
From: design-model-check#r327, reworded in request words (0.38.0).

```reading
While a requirement uses `order-by-every` and a closing comma, when the person parses the requirement, the language service shall complete the request.
shall [x2: thing `order-by-every` (parameter), x4: agent the person (constant), x5: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: closing comma]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
  when
    request(e1, language.parse, subject: x4, object: x1)
  response
    complete(e2, subject: x5, object: x6)
```

## r61
From: design-model-check#r325, reworded in request words (0.38.0).

```reading
While a requirement uses `order-by` and a recipient and the requirement uses no closing comma, when the person parses the requirement, the language service shall complete the request.
shall [x2: thing `order-by` (parameter), x5: agent the person (constant), x6: service the language service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: recipient]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    not [x4: closing comma]
      use(subject: x1, object: x4)
  when
    request(e1, language.parse, subject: x5, object: x1)
  response
    complete(e2, subject: x6, object: x7)
```
