# consistency: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: design-model-check#r156, reworded in request words (0.38.0).

```reading
When the person explains a requirement, the language service shall return the requirement and complete the request.
shall [x1: agent the person (constant), x3: service the language service (constant), x4: request "the request the trigger makes" (indexical)]
  when [x2: requirement]
    request(e1, language.explain, subject: x1, object: x2)
  response
    return(e2, subject: x3, object: x2)
    complete(e3, subject: x3, object: x4)
```

## r2
From: design-model-check#r218, reworded in request words (0.38.0).

```reading
While two requirements of a capability use a code that the specification service does not unify and a requirement of the capability obliges an act that another requirement of the capability forbids, when the person examines this specification, the specification service shall return a requirement and return `L1`.
shall [x5: service the specification service (constant), x9: agent the person (constant), x10: specification "the specification of this bounded context" (indexical), x12: agent `L1` (constant)]
  while [x1: requirement, x2: capability, x4: code, x3: requirement, x6: requirement, x7: act, x8: requirement]
    of(x1, x2)
    not
      unify(subject: x5, object: x4)
    use(subject: x1, object: x4)
    distinct(x3, x1)
    of(x3, x2)
    use(subject: x3, object: x4)
    of(x6, x2)
    distinct(x8, x6)
    of(x8, x2)
    forbid(subject: x8, object: x7)
    oblige(subject: x6, object: x7)
  when
    request(e1, specification.examine, subject: x9, object: x10)
  response [x11: requirement]
    return(e2, subject: x5, object: x11)
    return(e3, subject: x5, object: x12)
```

## r3
From: design-model-check#r247, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `only` and the requirement allows an act that another requirement of the capability obliges, when the person examines this specification, the specification service shall complete the request.
shall [x3: thing `only` (constant), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: capability, x4: act, x5: requirement]
    of(x1, x2)
    use(subject: x1, object: x3)
    distinct(x5, x1)
    of(x5, x2)
    oblige(subject: x5, object: x4)
    allow(subject: x1, object: x4)
  when
    request(e1, specification.examine, subject: x6, object: x7)
  response
    complete(e2, subject: x8, object: x9)
```

## r4
From: design-model-check#r248, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `every` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x3: thing `every` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: agent `L1` (constant)]
  while [x1: requirement, x2: capability, x4: act, x5: requirement, x6: trigger]
    of(x1, x2)
    use(subject: x1, object: x3)
    oblige(subject: x1, object: x4)
    distinct(x5, x1)
    of(x5, x2)
    of(x6, x1)
    of(x6, x5)
    forbid(subject: x5, object: x4)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    return(e2, subject: x9, object: x10)
```

## r5
From: design-model-check#r249, reworded in request words (0.38.0).

```reading
While a requirement of a capability overrides another requirement of the capability, when the person examines this specification, the specification service shall complete the request.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: capability, x3: requirement]
    of(x1, x2)
    distinct(x3, x1)
    of(x3, x2)
    override(subject: x1, object: x3)
  when
    request(e1, specification.examine, subject: x4, object: x5)
  response
    complete(e2, subject: x6, object: x7)
```

## r6
From: design-model-check#r250, reworded in request words (0.38.0).

```reading
While a universal condition forbids an act that a requirement of a capability obliges, when the person examines this specification, the specification service shall return the universal condition.
shall [x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant)]
  while [x1: universal condition, x2: act, x3: requirement, x4: capability]
    of(x3, x4)
    oblige(subject: x3, object: x2)
    forbid(subject: x1, object: x2)
  when
    request(e1, specification.examine, subject: x5, object: x6)
  response
    return(e2, subject: x7, object: x1)
```

## r7
From: design-model-check#r251, reworded in request words (0.38.0).

```reading
While a requirement has a consequence and the requirement adds no consequence, when the person examines this specification, the specification service shall return `L8`.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: agent `L8` (constant)]
  while [x1: requirement, x2: consequence]
    of(x2, x1)
    not [x3: consequence]
      add(subject: x1, object: x3)
  when
    request(e1, specification.examine, subject: x4, object: x5)
  response
    return(e2, subject: x6, object: x7)
```

## r8
From: design-model-check#r253, reworded in request words (0.38.0).

```reading
While a capability holds a count that contradicts a count, when the person examines this specification, the specification service shall return `L1`.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: agent `L1` (constant)]
  while [x1: capability, x2: count, x3: count]
    contradict(subject: x2, object: x3)
    in(x2, x1)
  when
    request(e1, specification.examine, subject: x4, object: x5)
  response
    return(e2, subject: x6, object: x7)
```

## r9
From: design-model-check#r260, reworded in request words (0.38.0).

```reading
While a requirement of a capability forbids an act that another requirement of the capability permits, when the person examines this specification, the specification service shall return `L7`.
shall [x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: agent `L7` (constant)]
  while [x1: requirement, x2: capability, x3: act, x4: requirement]
    of(x1, x2)
    distinct(x4, x1)
    of(x4, x2)
    permit(subject: x4, object: x3)
    forbid(subject: x1, object: x3)
  when
    request(e1, specification.examine, subject: x5, object: x6)
  response
    return(e2, subject: x7, object: x8)
```

## r10
From: design-model-check#r261, reworded in request words (0.38.0).

```reading
While the language of a capability is `codified-2`, when the person examines this specification, the specification service shall complete the request.
shall [x2: agent the person (constant), x3: specification "the specification of this bounded context" (indexical), x4: service the specification service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: capability]
    language(x1) = `codified-2`
  when
    request(e1, specification.examine, subject: x2, object: x3)
  response
    complete(e2, subject: x4, object: x5)
```

## r11
From: design-model-check#r262, reworded in request words (0.38.0).

```reading
When the person explains a requirement that uses a refusal, the language service shall return a universal condition and a term.
shall [x1: agent the person (constant), x4: service the language service (constant)]
  when [x2: requirement, x3: refusal]
    use(subject: x2, object: x3)
    request(e1, language.explain, subject: x1, object: x2)
  response [x5: universal condition, x6: term]
    return(e2, subject: x4, object: x5)
    return(e3, subject: x4, object: x6)
```

## r12
From: design-model-check#r263, reworded in request words (0.38.0).

```reading
When the person explains a requirement that a requirement overrides, the language service shall return a requirement that uses a refusal.
shall [x1: agent the person (constant), x4: service the language service (constant)]
  when [x2: requirement, x3: requirement]
    override(subject: x3, object: x2)
    request(e1, language.explain, subject: x1, object: x2)
  response [x5: requirement, x6: refusal]
    use(subject: x5, object: x6)
    return(e2, subject: x4, object: x5)
```

## r13
From: design-model-check#r264, reworded in request words (0.38.0).

```reading
If the person explains a requirement id that no capability holds, then the language service shall refuse the request and name the requirement id.
shall [x1: agent the person (constant), x4: service the language service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement id]
    not [x3: capability]
      in(x2, x3)
    request(e1, language.explain, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r14
From: design-model-check#r280, reworded in request words (0.38.0).

```reading
While a requirement of a capability conforms to the language reference, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.
shall [x3: artifact the language reference (constant), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    conforms(x1, x3)
  when
    request(e1, specification.examine, subject: x4, object: x5)
    param(e1, capability, x2)
  response [x7: translation]
    of(x7, x1)
    return(e2, subject: x6, object: x7)
```

## r15
From: design-model-check#r288, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `only` and the requirement uses `holds-relation`, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.
shall [x3: thing `only` (constant), x4: thing `holds-relation` (parameter), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
  when
    request(e1, specification.examine, subject: x5, object: x6)
    param(e1, capability, x2)
  response [x8: translation]
    of(x8, x1)
    return(e2, subject: x7, object: x8)
```

## r16
From: design-model-check#r289, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `count` and the requirement uses `holds-relation`, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.
shall [x3: thing `count` (constant), x4: thing `holds-relation` (parameter), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
  when
    request(e1, specification.examine, subject: x5, object: x6)
    param(e1, capability, x2)
  response [x8: translation]
    of(x8, x1)
    return(e2, subject: x7, object: x8)
```

## r17
From: design-model-check#r290, reworded in request words (0.38.0).

```reading
While a requirement of a capability has no translation, when the person examines this specification with the capability, the specification service shall return the requirement and not return `no findings`.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: text `no findings` (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    not [x3: translation]
      of(x3, x1)
  when
    request(e1, specification.examine, subject: x4, object: x5)
    param(e1, capability, x2)
  response
    return(e2, subject: x6, object: x1)
    not
      return(e3, subject: x6, object: x7)
```

## r18
From: design-model-check#r294, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `holds-exactly` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x3: thing `holds-exactly` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: agent `L1` (constant)]
  while [x1: requirement, x2: capability, x4: act, x5: requirement, x6: trigger]
    of(x1, x2)
    use(subject: x1, object: x3)
    oblige(subject: x1, object: x4)
    distinct(x5, x1)
    of(x5, x2)
    of(x6, x1)
    of(x6, x5)
    forbid(subject: x5, object: x4)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    return(e2, subject: x9, object: x10)
```

## r19
From: design-model-check#r292, reworded in request words (0.38.0).

```reading
While a requirement uses `is-in` and the requirement obliges an act and another requirement that forbids the act uses `holds-relation`, when the person examines this specification, the specification service shall return `L1`.
shall [x2: thing `is-in` (parameter), x5: thing `holds-relation` (parameter), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: agent `L1` (constant)]
  while [x1: requirement, x3: act, x4: requirement]
    use(subject: x1, object: x2)
    oblige(subject: x1, object: x3)
    distinct(x4, x1)
    forbid(subject: x4, object: x3)
    use(subject: x4, object: x5)
  when
    request(e1, specification.examine, subject: x6, object: x7)
  response
    return(e2, subject: x8, object: x9)
```

## r20
From: design-model-check#r301, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `value-compare` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x3: thing `value-compare` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: agent `L1` (constant)]
  while [x1: requirement, x2: capability, x4: act, x5: requirement, x6: trigger]
    of(x1, x2)
    use(subject: x1, object: x3)
    oblige(subject: x1, object: x4)
    distinct(x5, x1)
    of(x5, x2)
    of(x6, x1)
    of(x6, x5)
    forbid(subject: x5, object: x4)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    return(e2, subject: x9, object: x10)
```

## r21
From: design-model-check#r302, reworded in request words (0.38.0).

```reading
While a requirement of a capability obliges an act that another requirement of the capability forbids and a comparison of the precondition of the requirement contradicts a comparison, when the person examines this specification, the specification service shall complete the request.
shall [x8: agent the person (constant), x9: specification "the specification of this bounded context" (indexical), x10: service the specification service (constant), x11: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: capability, x3: act, x4: requirement, x5: comparison, x6: precondition, x7: comparison]
    of(x1, x2)
    distinct(x4, x1)
    of(x4, x2)
    forbid(subject: x4, object: x3)
    oblige(subject: x1, object: x3)
    of(x6, x4)
    of(x5, x6)
    contradict(subject: x5, object: x7)
  when
    request(e1, specification.examine, subject: x8, object: x9)
  response
    complete(e2, subject: x10, object: x11)
```

## r22
From: design-model-check#r297, reworded in request words (0.38.0).

```reading
While a capability holds an order that contradicts an order, when the person examines this specification, the specification service shall return `L1`.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: agent `L1` (constant)]
  while [x1: capability, x2: order, x3: order]
    contradict(subject: x2, object: x3)
    in(x2, x1)
  when
    request(e1, specification.examine, subject: x4, object: x5)
  response
    return(e2, subject: x6, object: x7)
```

## r23
From: design-model-check#r310, reworded in request words (0.38.0).

```reading
While a sense of a term has a value order and another sense of the term has the value order and a requirement of a capability uses the term and `value-compare` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x7: thing `value-compare` (parameter), x11: agent the person (constant), x12: specification "the specification of this bounded context" (indexical), x13: service the specification service (constant), x14: agent `L1` (constant)]
  while [x1: sense, x2: term, x3: value order, x4: sense, x5: requirement, x6: capability, x8: act, x9: requirement, x10: trigger]
    of(x1, x2)
    of(x3, x1)
    distinct(x4, x1)
    of(x4, x2)
    of(x3, x4)
    of(x5, x6)
    use(subject: x5, object: x2)
    use(subject: x5, object: x7)
    oblige(subject: x5, object: x8)
    distinct(x9, x5)
    of(x9, x6)
    of(x10, x5)
    of(x10, x9)
    forbid(subject: x9, object: x8)
  when
    request(e1, specification.examine, subject: x11, object: x12)
  response
    return(e2, subject: x13, object: x14)
```

## r24
From: design-model-check#r314, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `holds-exactly` and `rc-object` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x3: thing `holds-exactly` (parameter), x4: thing `rc-object` (parameter), x8: agent the person (constant), x9: specification "the specification of this bounded context" (indexical), x10: service the specification service (constant), x11: agent `L1` (constant)]
  while [x1: requirement, x2: capability, x5: act, x6: requirement, x7: trigger]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
    oblige(subject: x1, object: x5)
    distinct(x6, x1)
    of(x6, x2)
    of(x7, x1)
    of(x7, x6)
    forbid(subject: x6, object: x5)
  when
    request(e1, specification.examine, subject: x8, object: x9)
  response
    return(e2, subject: x10, object: x11)
```

## r25
From: design-model-check#r315, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `nothing` and `rc-subject` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x3: thing `nothing` (parameter), x4: thing `rc-subject` (parameter), x8: agent the person (constant), x9: specification "the specification of this bounded context" (indexical), x10: service the specification service (constant), x11: agent `L1` (constant)]
  while [x1: requirement, x2: capability, x5: act, x6: requirement, x7: trigger]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
    oblige(subject: x1, object: x5)
    distinct(x6, x1)
    of(x6, x2)
    of(x7, x1)
    of(x7, x6)
    forbid(subject: x6, object: x5)
  when
    request(e1, specification.examine, subject: x8, object: x9)
  response
    return(e2, subject: x10, object: x11)
```

## r26
From: design-model-check#r316, reworded in request words (0.38.0).

```reading
While the precondition of a requirement of a capability uses `every` and `not-condition`, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.
shall [x4: thing `every` (parameter), x5: thing `not-condition` (parameter), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant)]
  while [x1: requirement, x2: capability, x3: precondition]
    of(x1, x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    use(subject: x3, object: x5)
  when
    request(e1, specification.examine, subject: x6, object: x7)
    param(e1, capability, x2)
  response [x9: translation]
    of(x9, x1)
    return(e2, subject: x8, object: x9)
```

## r27
From: design-model-check#r321, reworded in request words (0.38.0).

```reading
While a requirement uses `nothing` and `rc-subject` and the requirement obliges an act and another requirement that forbids the act uses `holds-relation`, when the person examines this specification, the specification service shall complete the request.
shall [x2: thing `nothing` (parameter), x3: thing `rc-subject` (parameter), x6: thing `holds-relation` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x4: act, x5: requirement]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    oblige(subject: x1, object: x4)
    distinct(x5, x1)
    forbid(subject: x5, object: x4)
    use(subject: x5, object: x6)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    complete(e2, subject: x9, object: x10)
```

## r28
From: design-model-check#r322, reworded in request words (0.38.0).

```reading
While a requirement uses `no-noun` and `holds-relation` and the requirement obliges an act and another requirement that forbids the act uses `holds-relation`, when the person examines this specification, the specification service shall complete the request.
shall [x2: thing `no-noun` (parameter), x3: thing `holds-relation` (parameter), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x4: act, x5: requirement]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    oblige(subject: x1, object: x4)
    distinct(x5, x1)
    forbid(subject: x5, object: x4)
    use(subject: x5, object: x3)
  when
    request(e1, specification.examine, subject: x6, object: x7)
  response
    complete(e2, subject: x8, object: x9)
```

## r29
From: design-model-check#r320, reworded in request words (0.38.0).

```reading
While a requirement uses `holds-relation` and `rc-subject` and the requirement obliges an act and another requirement that forbids the act uses `holds-relation`, when the person examines this specification, the specification service shall return `L1`.
shall [x2: thing `holds-relation` (parameter), x3: thing `rc-subject` (parameter), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: agent `L1` (constant)]
  while [x1: requirement, x4: act, x5: requirement]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    oblige(subject: x1, object: x4)
    distinct(x5, x1)
    forbid(subject: x5, object: x4)
    use(subject: x5, object: x2)
  when
    request(e1, specification.examine, subject: x6, object: x7)
  response
    return(e2, subject: x8, object: x9)
```

## r30
From: design-model-check#r323, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `holds-exactly` and `of-relation` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x3: thing `holds-exactly` (parameter), x4: thing `of-relation` (parameter), x8: agent the person (constant), x9: specification "the specification of this bounded context" (indexical), x10: service the specification service (constant), x11: agent `L1` (constant)]
  while [x1: requirement, x2: capability, x5: act, x6: requirement, x7: trigger]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
    oblige(subject: x1, object: x5)
    distinct(x6, x1)
    of(x6, x2)
    of(x7, x1)
    of(x7, x6)
    forbid(subject: x6, object: x5)
  when
    request(e1, specification.examine, subject: x8, object: x9)
  response
    return(e2, subject: x10, object: x11)
```

## r31
From: design-model-check#r328, reworded in request words (0.38.0).

```reading
While a requirement uses `not-relative` and a code and the requirement forbids an act and another requirement obliges the act and the requirement uses `rc-whose` and the requirement does not use the code, when the person examines this specification, the specification service shall return `L1`.
shall [x2: thing `not-relative` (parameter), x6: thing `rc-whose` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: agent `L1` (constant)]
  while [x1: requirement, x3: code, x4: act, x5: requirement]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    forbid(subject: x1, object: x4)
    distinct(x5, x1)
    oblige(subject: x5, object: x4)
    use(subject: x5, object: x6)
    not
      use(subject: x5, object: x3)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    return(e2, subject: x9, object: x10)
```

## r32
From: design-model-check#r329, reworded in request words (0.38.0).

```reading
While a requirement uses `not-relative` and a code and the requirement forbids an act and another requirement obliges the act and the requirement uses `rc-whose` and the code, when the person examines this specification, the specification service shall complete the request.
shall [x2: thing `not-relative` (parameter), x6: thing `rc-whose` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: code, x4: act, x5: requirement]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    forbid(subject: x1, object: x4)
    distinct(x5, x1)
    oblige(subject: x5, object: x4)
    use(subject: x5, object: x6)
    use(subject: x5, object: x3)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    complete(e2, subject: x9, object: x10)
```

## r33
From: b309 r33.

```reading
While the precondition of a requirement of a capability uses `holds-exactly` and `rc-subject`, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.
shall [x4: thing `holds-exactly` (parameter), x5: thing `rc-subject` (parameter), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant)]
  while [x1: requirement, x2: capability, x3: precondition]
    of(x1, x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    use(subject: x3, object: x5)
  when
    request(e1, specification.examine, subject: x6, object: x7)
    param(e1, capability, x2)
  response [x9: translation]
    of(x9, x1)
    return(e2, subject: x8, object: x9)
```

## r34
From: b418 r34.

```reading
While a requirement uses `param-of` and the requirement obliges an act and another requirement that forbids the act has the trigger of the requirement, when the person examines this specification, the specification service shall return `L1`.
shall [x2: thing `param-of` (parameter), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: agent `L1` (constant)]
  while [x1: requirement, x3: act, x4: requirement, x5: trigger]
    use(subject: x1, object: x2)
    oblige(subject: x1, object: x3)
    distinct(x4, x1)
    forbid(subject: x4, object: x3)
    of(x5, x4)
  when
    request(e1, specification.examine, subject: x6, object: x7)
  response
    return(e2, subject: x8, object: x9)
```

## r35
From: b544 r35.

```reading
While a term means an element and a requirement that uses the term obliges an act and another term means the element and another requirement that uses the term forbids the act, when the person examines this specification, the specification service shall return `L1`.
shall [x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: agent `L1` (constant)]
  while [x1: term, x2: element, x3: requirement, x4: act, x5: term, x6: requirement]
    mean(subject: x1, object: x2)
    use(subject: x3, object: x1)
    oblige(subject: x3, object: x4)
    distinct(x5, x1)
    mean(subject: x5, object: x2)
    distinct(x6, x3)
    use(subject: x6, object: x5)
    forbid(subject: x6, object: x4)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    return(e2, subject: x9, object: x10)
```

## r36
From: b543 r36.

```reading
While a requirement of a capability uses `response-request`, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.
shall [x3: thing `response-request` (parameter), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
  when
    request(e1, specification.examine, subject: x4, object: x5)
    param(e1, capability, x2)
  response [x7: translation]
    of(x7, x1)
    return(e2, subject: x6, object: x7)
```

## r37
From: b545 r37.

```reading
While a requirement has a trigger and the requirement uses `response-request` and an operation and another requirement that governs the operation has a consequence and a requirement that has the consequence has the trigger, when the person examines this specification, the specification service shall return `L8` and return every requirement that governs the operation.
shall [x3: thing `response-request` (parameter), x8: agent the person (constant), x9: specification "the specification of this bounded context" (indexical), x10: service the specification service (constant), x11: agent `L8` (constant)]
  while [x1: requirement, x2: trigger, x4: operation, x5: requirement, x6: consequence, x7: requirement]
    of(x2, x1)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
    distinct(x5, x1)
    govern(subject: x5, object: x4)
    of(x6, x5)
    of(x6, x7)
    of(x2, x7)
  when
    request(e1, specification.examine, subject: x8, object: x9)
  response
    return(e2, subject: x10, object: x11)
    every [x12: requirement]
      govern(subject: x12, object: x4)
      scope
        return(e3, subject: x10, object: x12)
```

## r38
From: b545 r38.

```reading
While a requirement governs an operation and the requirement has a consequence and a requirement whose trigger uses the consequence has a consequence and a requirement that uses `response-request` and the operation has a trigger and a requirement that has the consequence has the trigger, when the person examines this specification, the specification service shall return `L8`.
shall [x8: thing `response-request` (parameter), x11: agent the person (constant), x12: specification "the specification of this bounded context" (indexical), x13: service the specification service (constant), x14: agent `L8` (constant)]
  while [x1: requirement, x2: operation, x3: consequence, x4: requirement, x5: trigger, x6: consequence, x7: requirement, x9: trigger, x10: requirement]
    govern(subject: x1, object: x2)
    of(x3, x1)
    of(x5, x4)
    use(subject: x5, object: x3)
    of(x6, x4)
    use(subject: x7, object: x8)
    use(subject: x7, object: x2)
    of(x9, x7)
    of(x6, x10)
    of(x9, x10)
  when
    request(e1, specification.examine, subject: x11, object: x12)
  response
    return(e2, subject: x13, object: x14)
```

## r39
From: b545 r39.

```reading
While a requirement has a trigger and the requirement obliges an act and the requirement uses `response-request` and a code and another requirement that has the trigger forbids the act and the requirement does not use the code, when the person examines this specification, the specification service shall complete the request.
shall [x4: thing `response-request` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: trigger, x3: act, x5: code, x6: requirement]
    of(x2, x1)
    oblige(subject: x1, object: x3)
    use(subject: x1, object: x4)
    use(subject: x1, object: x5)
    distinct(x6, x1)
    of(x2, x6)
    forbid(subject: x6, object: x3)
    not
      use(subject: x6, object: x5)
  when
    request(e1, specification.examine, subject: x7, object: x8)
  response
    complete(e2, subject: x9, object: x10)
```
