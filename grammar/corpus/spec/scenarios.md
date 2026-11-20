# scenarios: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: feature-file-tools#r106, reworded in request words (0.38.0).

```reading
While the feature of a capability has a scenario that no requirement group has, if the person generates the feature of the capability with the audit, then the scenarios service shall fail the check, name the feature and change no file.
shall [x5: agent the person (constant), x6: service the scenarios service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: capability, x2: feature, x3: scenario]
    of(x2, x1)
    not [x4: requirement group]
      of(x3, x4)
    of(x3, x2)
  if
    request(e1, scenarios.generate, subject: x5, object: x2)
    param(e1, audit, on)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
    not [x8: file]
      change(e4, subject: x6, object: x8)
```

## r2
From: feature-file-tools#r107, reworded in request words (0.38.0).

```reading
While a step of a feature has no handler, if the person audits the feature, then the scenarios service shall fail the check, name the step, name the feature and change no file.
shall [x4: agent the person (constant), x5: service the scenarios service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: step, x2: feature]
    of(x1, x2)
    not [x3: handler]
      of(x3, x1)
  if
    request(e1, scenarios.audit, subject: x4, object: x2)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
    name(e4, subject: x5, object: x2)
    not [x7: file]
      change(e5, subject: x5, object: x7)
```

## r3
From: feature-file-tools#r108, reworded in request words (0.38.0).

```reading
While the language of a capability is `codified-2` and every requirement of the capability conforms to the language reference and every requirement of the capability uses the `shall` construct, when the person generates the feature of the capability, the scenarios service shall keep the scenario of every requirement group of the capability.
shall [x3: artifact the language reference (constant), x5: construct `shall` (parameter), x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: capability]
    language(x1) = `codified-2`
    every [x2: requirement]
      of(x2, x1)
      scope
        conforms(x2, x3)
    every [x4: requirement]
      of(x4, x1)
      scope
        use(subject: x4, object: x5)
  when [x7: feature]
    of(x7, x1)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response
    every [x9: requirement group]
      of(x9, x1)
      scope [x10: scenario]
        of(x10, x9)
        keep(e2, subject: x8, object: x10)
```

## r4
From: feature-file-tools#r109, reworded in request words (0.38.0).

```reading
While the language of a capability is `codified-2`, when the person generates the feature of the capability, the scenarios service shall not keep a step that a universal condition entails.
shall [x2: agent the person (constant), x4: service the scenarios service (constant)]
  while [x1: capability]
    language(x1) = `codified-2`
  when [x3: feature]
    of(x3, x1)
    request(e1, scenarios.generate, subject: x2, object: x3)
  response
    not [x5: step, x6: universal condition]
      entail(subject: x6, object: x5)
      keep(e2, subject: x4, object: x5)
```

## r5
From: feature-file-tools#r110, reworded in request words (0.38.0).

```reading
While the group of a capability is `service` and the language of the capability is `codified-2`, when the person generates the feature of the capability, the scenarios service shall keep the feature of the capability and return the feature.
shall [x2: agent the person (constant), x4: service the scenarios service (constant)]
  while [x1: capability]
    group(x1) = `service`
    language(x1) = `codified-2`
  when [x3: feature]
    of(x3, x1)
    request(e1, scenarios.generate, subject: x2, object: x3)
  response
    keep(e2, subject: x4, object: x3)
    return(e3, subject: x4, object: x3)
```

## r6
From: feature-file-tools#r111, reworded in request words (0.38.0).

```reading
While an act of a requirement of a capability brings in a referent, when the person generates the feature of the capability, the scenarios service shall keep a description of the referent that follows the act and not keep a description of the referent that precedes the act.
shall [x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: act, x2: requirement, x3: capability, x4: referent]
    of(x2, x3)
    of(x1, x2)
    bring in(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x3)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: description]
    of(x8, x4)
    follow(subject: x8, object: x1)
    keep(e2, subject: x7, object: x8)
    not [x9: description]
      of(x9, x4)
      precede(subject: x9, object: x1)
      keep(e3, subject: x7, object: x9)
```

## r7
From: feature-file-tools#r113, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `only` and the requirement uses `holds-relation`, when the person generates the feature of the capability, the scenarios service shall keep a scenario that uses `only`.
shall [x3: thing `only` (constant), x4: thing `holds-relation` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x2)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario]
    use(subject: x8, object: x3)
    keep(e2, subject: x7, object: x8)
```

## r8
From: feature-file-tools#r112, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `count` and the requirement uses `holds-relation`, when the person generates the feature of the capability, the scenarios service shall keep a scenario that uses `count`.
shall [x3: thing `count` (constant), x4: thing `holds-relation` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x2)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario]
    use(subject: x8, object: x3)
    keep(e2, subject: x7, object: x8)
```

## r9
From: feature-file-tools#r117, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `every` and the requirement has a restriction, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has a counter-example.
shall [x4: thing `every` (parameter), x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x5: restriction]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    of(x5, x1)
  when [x7: feature]
    of(x7, x3)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response [x9: scenario, x10: counter-example]
    of(x9, x2)
    of(x10, x9)
    keep(e2, subject: x8, object: x9)
```

## r10
From: feature-file-tools#r118, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `only` and the requirement has a restriction, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has a counter-example and not keep a step that asserts an act that the requirement allows.
shall [x4: thing `only` (constant), x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x5: restriction]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    of(x5, x1)
  when [x7: feature]
    of(x7, x3)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response [x9: scenario, x10: counter-example]
    of(x9, x2)
    of(x10, x9)
    keep(e2, subject: x8, object: x9)
    not [x11: step, x12: act]
      allow(subject: x1, object: x12)
      assert(subject: x11, object: x12)
      keep(e3, subject: x8, object: x11)
```

## r11
From: feature-file-tools#r119, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability has an upper bound, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has a counter-example.
shall [x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x4: upper bound]
    of(x2, x3)
    of(x1, x2)
    of(x4, x1)
  when [x6: feature]
    of(x6, x3)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario, x9: counter-example]
    of(x8, x2)
    of(x9, x8)
    keep(e2, subject: x7, object: x8)
```

## r12
From: feature-file-tools#r114, reworded in request words (0.38.0).

```reading
While the precondition of a requirement of a requirement group of a capability uses `every`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that satisfies the precondition.
shall [x5: thing `every` (parameter), x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x4: precondition]
    of(x2, x3)
    of(x1, x2)
    of(x4, x1)
    use(subject: x4, object: x5)
  when [x7: feature]
    of(x7, x3)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response [x9: scenario]
    of(x9, x2)
    satisfy(subject: x9, object: x4)
    keep(e2, subject: x8, object: x9)
```

## r13
From: feature-file-tools#r115, reworded in request words (0.38.0).

```reading
While the precondition of a requirement of a requirement group of a capability holds a count, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has the boundary of the count.
shall [x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x4: precondition, x5: count]
    of(x2, x3)
    of(x1, x2)
    of(x4, x1)
    in(x5, x4)
  when [x7: feature]
    of(x7, x3)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response [x9: scenario, x10: boundary]
    of(x9, x2)
    of(x10, x5)
    of(x10, x9)
    keep(e2, subject: x8, object: x9)
```

## r14
From: feature-file-tools#r116, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `two`, when the person generates the feature of the capability, the scenarios service shall not keep a step that mentions an instance that no given step introduces.
shall [x4: thing `two` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x3)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response
    not [x8: step, x9: instance]
      not [x10: given step]
        introduce(subject: x10, object: x9)
      mention(subject: x8, object: x9)
      keep(e2, subject: x7, object: x8)
```

## r15
From: feature-file-tools#r120, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `holds-exactly`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.
shall [x3: thing `holds-exactly` (parameter), x4: agent the person (constant), x6: service the scenarios service (constant), x9: thing `not-condition` (parameter)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
  when [x5: feature]
    of(x5, x2)
    request(e1, scenarios.generate, subject: x4, object: x5)
  response [x7: scenario, x8: step]
    of(x8, x7)
    use(subject: x8, object: x9)
    keep(e2, subject: x6, object: x7)
```

## r16
From: feature-file-tools#r121, reworded in request words (0.38.0).

```reading
While the precondition of a requirement of a capability uses `nothing`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `nothing`.
shall [x4: thing `nothing` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: capability, x3: precondition]
    of(x1, x2)
    of(x3, x1)
    use(subject: x3, object: x4)
  when [x6: feature]
    of(x6, x2)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario, x9: step]
    of(x9, x8)
    use(subject: x9, object: x4)
    keep(e2, subject: x7, object: x8)
```

## r17
From: feature-file-tools#r122, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses an order, when the person generates the feature of the capability, the scenarios service shall keep a scenario that has an order counter-example.
shall [x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x4: order]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x3)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario, x9: order counter-example]
    of(x9, x8)
    keep(e2, subject: x7, object: x8)
```

## r18
From: feature-file-tools#r123, reworded in request words (0.38.0).

```reading
While a term has two senses and a requirement of a requirement group of a capability uses the term and `order-by`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has an order counter-example.
shall [x7: thing `order-by` (parameter), x8: agent the person (constant), x10: service the scenarios service (constant)]
  while [x1: term, x2: sense, x3: sense, x4: requirement, x5: requirement group, x6: capability]
    of(x2, x1)
    distinct(x3, x2)
    of(x3, x1)
    of(x5, x6)
    of(x4, x5)
    use(subject: x4, object: x1)
    use(subject: x4, object: x7)
  when [x9: feature]
    of(x9, x6)
    request(e1, scenarios.generate, subject: x8, object: x9)
  response [x11: scenario, x12: order counter-example]
    of(x11, x5)
    of(x12, x11)
    keep(e2, subject: x10, object: x11)
```

## r19
From: feature-file-tools#r124, reworded in request words (0.38.0).

```reading
While a term has two senses and a requirement of a requirement group of a capability uses the term and `order-by-every`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has an order counter-example.
shall [x7: thing `order-by-every` (parameter), x8: agent the person (constant), x10: service the scenarios service (constant)]
  while [x1: term, x2: sense, x3: sense, x4: requirement, x5: requirement group, x6: capability]
    of(x2, x1)
    distinct(x3, x2)
    of(x3, x1)
    of(x5, x6)
    of(x4, x5)
    use(subject: x4, object: x1)
    use(subject: x4, object: x7)
  when [x9: feature]
    of(x9, x6)
    request(e1, scenarios.generate, subject: x8, object: x9)
  response [x11: scenario, x12: order counter-example]
    of(x11, x5)
    of(x12, x11)
    keep(e2, subject: x10, object: x11)
```

## r20
From: feature-file-tools#r125, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `holds-exactly` and `rc-object`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.
shall [x3: thing `holds-exactly` (parameter), x4: thing `rc-object` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant), x10: thing `not-condition` (parameter)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x2)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario, x9: step]
    of(x9, x8)
    use(subject: x9, object: x10)
    keep(e2, subject: x7, object: x8)
```

## r21
From: feature-file-tools#r126, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `nothing` and `rc-subject`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `nothing`.
shall [x3: thing `nothing` (parameter), x4: thing `rc-subject` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x2)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario, x9: step]
    of(x9, x8)
    use(subject: x9, object: x3)
    keep(e2, subject: x7, object: x8)
```

## r22
From: feature-file-tools#r127, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `order-by` and the requirement uses a verb that has no frame that takes `thing`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has an order counter-example.
shall [x4: thing `order-by` (parameter), x7: noun phrase `thing` (constant), x8: agent the person (constant), x10: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x5: verb]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    not [x6: frame]
      take(subject: x6, object: x7)
      of(x6, x5)
    use(subject: x1, object: x5)
  when [x9: feature]
    of(x9, x3)
    request(e1, scenarios.generate, subject: x8, object: x9)
  response [x11: scenario, x12: order counter-example]
    of(x11, x2)
    of(x12, x11)
    keep(e2, subject: x10, object: x11)
```

## r23
From: feature-file-tools#r128, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `no-noun` and `holds-relation` and the precondition of the requirement does not use `no-noun`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has a counter-example.
shall [x4: thing `no-noun` (parameter), x5: thing `holds-relation` (parameter), x7: agent the person (constant), x9: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x6: precondition]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    use(subject: x1, object: x5)
    of(x6, x1)
    not
      use(subject: x6, object: x4)
  when [x8: feature]
    of(x8, x3)
    request(e1, scenarios.generate, subject: x7, object: x8)
  response [x10: scenario, x11: counter-example]
    of(x10, x2)
    of(x11, x10)
    keep(e2, subject: x9, object: x10)
```

## r24
From: feature-file-tools#r129, reworded in request words (0.38.0).

```reading
While the precondition of a requirement of a requirement group of a capability uses `every` and `not-condition`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that satisfies the precondition.
shall [x5: thing `every` (parameter), x6: thing `not-condition` (parameter), x7: agent the person (constant), x9: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x4: precondition]
    of(x2, x3)
    of(x1, x2)
    of(x4, x1)
    use(subject: x4, object: x5)
    use(subject: x4, object: x6)
  when [x8: feature]
    of(x8, x3)
    request(e1, scenarios.generate, subject: x7, object: x8)
  response [x10: scenario]
    of(x10, x2)
    satisfy(subject: x10, object: x4)
    keep(e2, subject: x9, object: x10)
```

## r25
From: feature-file-tools#r130, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `order-by-every` and the requirement uses a verb that has no frame that takes `thing`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has an order counter-example.
shall [x4: thing `order-by-every` (parameter), x7: noun phrase `thing` (constant), x8: agent the person (constant), x10: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x5: verb]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    not [x6: frame]
      take(subject: x6, object: x7)
      of(x6, x5)
    use(subject: x1, object: x5)
  when [x9: feature]
    of(x9, x3)
    request(e1, scenarios.generate, subject: x8, object: x9)
  response [x11: scenario, x12: order counter-example]
    of(x11, x2)
    of(x12, x11)
    keep(e2, subject: x10, object: x11)
```

## r26
From: feature-file-tools#r132, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `holds-relation` and `rc-subject`, when the person generates the feature of the capability, the scenarios service shall not keep a step that mentions an instance that no given step introduces.
shall [x4: thing `holds-relation` (parameter), x5: thing `rc-subject` (parameter), x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    use(subject: x1, object: x5)
  when [x7: feature]
    of(x7, x3)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response
    not [x9: step, x10: instance]
      not [x11: given step]
        introduce(subject: x11, object: x10)
      mention(subject: x9, object: x10)
      keep(e2, subject: x8, object: x9)
```

## r27
From: feature-file-tools#r131, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `order-by`, when the person generates the feature of the capability, the scenarios service shall not keep a step that mentions an instance that no given step introduces.
shall [x4: thing `order-by` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x3)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response
    not [x8: step, x9: instance]
      not [x10: given step]
        introduce(subject: x10, object: x9)
      mention(subject: x8, object: x9)
      keep(e2, subject: x7, object: x8)
```

## r28
From: feature-file-tools#r133, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `order-by-every` and `of-relation`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has an order counter-example.
shall [x4: thing `order-by-every` (parameter), x5: thing `of-relation` (parameter), x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    use(subject: x1, object: x5)
  when [x7: feature]
    of(x7, x3)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response [x9: scenario, x10: order counter-example]
    of(x9, x2)
    of(x10, x9)
    keep(e2, subject: x8, object: x9)
```

## r29
From: feature-file-tools#r134, reworded in request words (0.38.0).

```reading
While a requirement of a requirement group of a capability uses `count` and `holds-relation` and the requirement has an upper bound, when the person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has a counter-example.
shall [x4: thing `count` (constant), x5: thing `holds-relation` (parameter), x7: agent the person (constant), x9: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x6: upper bound]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    use(subject: x1, object: x5)
    of(x6, x1)
  when [x8: feature]
    of(x8, x3)
    request(e1, scenarios.generate, subject: x7, object: x8)
  response [x10: scenario, x11: counter-example]
    of(x10, x2)
    of(x11, x10)
    keep(e2, subject: x9, object: x10)
```

## r30
From: feature-file-tools#r135, reworded in request words (0.38.0).

```reading
While a requirement of a capability uses `holds-exactly` and `of-relation`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.
shall [x3: thing `holds-exactly` (parameter), x4: thing `of-relation` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant), x10: thing `not-condition` (parameter)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    use(subject: x1, object: x3)
    use(subject: x1, object: x4)
  when [x6: feature]
    of(x6, x2)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario, x9: step]
    of(x9, x8)
    use(subject: x9, object: x10)
    keep(e2, subject: x7, object: x8)
```

## r31
From: b309 r31.

```reading
While the precondition of a requirement of a capability uses `holds-exactly`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.
shall [x4: thing `holds-exactly` (parameter), x5: agent the person (constant), x7: service the scenarios service (constant), x10: thing `not-condition` (parameter)]
  while [x1: requirement, x2: capability, x3: precondition]
    of(x1, x2)
    of(x3, x1)
    use(subject: x3, object: x4)
  when [x6: feature]
    of(x6, x2)
    request(e1, scenarios.generate, subject: x5, object: x6)
  response [x8: scenario, x9: step]
    of(x9, x8)
    use(subject: x9, object: x10)
    keep(e2, subject: x7, object: x8)
```

## r32
From: b309 r32.

```reading
While the precondition of a requirement of a capability uses `holds-exactly` and `rc-subject`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.
shall [x4: thing `holds-exactly` (parameter), x5: thing `rc-subject` (parameter), x6: agent the person (constant), x8: service the scenarios service (constant), x11: thing `not-condition` (parameter)]
  while [x1: requirement, x2: capability, x3: precondition]
    of(x1, x2)
    of(x3, x1)
    use(subject: x3, object: x4)
    use(subject: x3, object: x5)
  when [x7: feature]
    of(x7, x2)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response [x9: scenario, x10: step]
    of(x10, x9)
    use(subject: x10, object: x11)
    keep(e2, subject: x8, object: x9)
```

## r33
From: b416 r33.

```reading
While a requirement of a requirement group of a capability uses `of-relation` and the precondition of the requirement does not use `of-relation`, when the person generates the feature of the capability, the scenarios service shall not keep a step that mentions an instance that no given step introduces.
shall [x4: thing `of-relation` (parameter), x6: agent the person (constant), x8: service the scenarios service (constant)]
  while [x1: requirement, x2: requirement group, x3: capability, x5: precondition]
    of(x2, x3)
    of(x1, x2)
    use(subject: x1, object: x4)
    of(x5, x1)
    not
      use(subject: x5, object: x4)
  when [x7: feature]
    of(x7, x3)
    request(e1, scenarios.generate, subject: x6, object: x7)
  response
    not [x9: step, x10: instance]
      not [x11: given step]
        introduce(subject: x11, object: x10)
      mention(subject: x9, object: x10)
      keep(e2, subject: x8, object: x9)
```
