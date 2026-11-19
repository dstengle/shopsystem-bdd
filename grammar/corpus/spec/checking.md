# checking: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: design-model-check#r54, reworded in request words (0.38.0).

```reading
When the person consults the rule catalogue, the specification service shall return every rule and complete the request.
shall [x1: agent the person (constant), x2: rule catalogue "the rule catalogue of the plugin" (indexical), x3: service the specification service (constant), x5: request "the request the trigger makes" (indexical)]
  when
    request(e1, specification.consult, subject: x1, object: x2)
  response
    every [x4: rule]
      scope
        return(e2, subject: x3, object: x4)
    complete(e3, subject: x3, object: x5)
```

## r2
From: design-model-check#r55, reworded in request words (0.38.0).

```reading
When the person inventories this specification, the specification service shall return every file form and complete the request.
shall [x1: agent the person (constant), x2: specification "the specification of this bounded context" (indexical), x3: service the specification service (constant), x5: request "the request the trigger makes" (indexical)]
  when
    request(e1, specification.inventory, subject: x1, object: x2)
  response
    every [x4: file form]
      scope
        return(e2, subject: x3, object: x4)
    complete(e3, subject: x3, object: x5)
```

## r3
From: design-model-check#r174, reworded in request words (0.38.0).

```reading
While nothing violates a rule, when the person validates this specification, the specification service shall return `0 violations` and complete the request.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: thing `0 violations` (parameter), x7: request "the request the trigger makes" (indexical)]
  while
    not [x1: thing, x2: rule]
      violate(subject: x1, object: x2)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    return(e2, subject: x5, object: x6)
    complete(e3, subject: x5, object: x7)
```

## r4
From: design-model-check#r175, reworded in request words (0.38.0).

```reading
While a capability violates `v15a`, if the person validates this specification, then the specification service shall fail the check and name `v15a`.
shall [x2: rule `v15a` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: capability]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r5
From: design-model-check#r176, reworded in request words (0.38.0).

```reading
While a capability violates `v15b`, if the person validates this specification, then the specification service shall fail the check and name `v15b`.
shall [x2: rule `v15b` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: capability]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r6
From: design-model-check#r177, reworded in request words (0.38.0).

```reading
While a capability violates `v15c`, if the person validates this specification, then the specification service shall fail the check and name `v15c`.
shall [x2: rule `v15c` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: capability]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r7
From: design-model-check#r178, reworded in request words (0.38.0).

```reading
While a requirement group violates `v15l`, if the person validates this specification, then the specification service shall fail the check and name `v15l`.
shall [x2: rule `v15l` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r8
From: design-model-check#r179, reworded in request words (0.38.0).

```reading
While a requirement group violates `v15n`, if the person validates this specification, then the specification service shall fail the check and name `v15n`.
shall [x2: rule `v15n` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r9
From: design-model-check#r180, reworded in request words (0.38.0).

```reading
While a requirement group violates `v15m`, if the person validates this specification, then the specification service shall fail the check and name `v15m`.
shall [x2: rule `v15m` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r10
From: design-model-check#r181, reworded in request words (0.38.0).

```reading
While a requirement group violates `v_s3`, if the person validates this specification, then the specification service shall fail the check and name `v_s3`.
shall [x2: rule `v_s3` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r11
From: design-model-check#r182, reworded in request words (0.38.0).

```reading
While a scenario violates `v_s2`, if the person validates this specification, then the specification service shall fail the check and name `v_s2`.
shall [x2: rule `v_s2` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: scenario]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r12
From: design-model-check#r183, reworded in request words (0.38.0).

```reading
While a request violates `v17`, if the person validates this specification, then the specification service shall fail the check and name `v17`.
shall [x2: rule `v17` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: request]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r13
From: design-model-check#r184, reworded in request words (0.38.0).

```reading
While a request violates `v3`, if the person validates this specification, then the specification service shall fail the check and name `v3`.
shall [x2: rule `v3` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: request]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r14
From: design-model-check#r185, reworded in request words (0.38.0).

```reading
While a requirement violates `v_t1`, if the person validates this specification, then the specification service shall fail the check and name `v_t1`.
shall [x2: rule `v_t1` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: requirement]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r15
From: design-model-check#r186, reworded in request words (0.38.0).

```reading
While a term violates `v_t2`, if the person validates this specification, then the specification service shall fail the check and name `v_t2`.
shall [x2: rule `v_t2` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r16
From: design-model-check#r187, reworded in request words (0.38.0).

```reading
While a term violates `v_t3`, if the person validates this specification, then the specification service shall fail the check and name `v_t3`.
shall [x2: rule `v_t3` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r17
From: design-model-check#r188, reworded in request words (0.38.0).

```reading
While a requirement violates `v_p1`, if the person validates this specification, then the specification service shall fail the check and name `v_p1`.
shall [x2: rule `v_p1` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: requirement]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r18
From: design-model-check#r189, reworded in request words (0.38.0).

```reading
While a request does not conform to the request form, if the person validates this specification, then the specification service shall fail the check and name the request.
shall [x2: artifact the request form (constant), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: request]
    not
      conforms(x1, x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r19
From: design-model-check#r190, reworded in request words (0.38.0).

```reading
While a scenario refers to a requirement id that the capability of the scenario does not hold, if the person validates this specification, then the specification service shall fail the check and name the scenario.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: scenario, x2: requirement id, x3: capability]
    of(x3, x1)
    not
      in(x2, x3)
    refer(subject: x1, to: x2)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x1)
```

## r20
From: design-model-check#r191, reworded in request words (0.38.0).

```reading
While a capability does not conform to the capability id form, if the person validates this specification, then the specification service shall fail the check and name the capability.
shall [x2: artifact the capability id form (constant), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: capability]
    not
      conforms(x1, x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r21
From: design-model-check#r192, reworded in request words (0.38.0).

```reading
While a capability has no section whose heading is `Behaviour`, if the person validates this specification, then the specification service shall fail the check and name the capability.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: capability]
    not [x2: section]
      heading(x2) = `Behaviour`
      of(x2, x1)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r22
From: design-model-check#r193, reworded in request words (0.38.0).

```reading
While a feature does not conform to the feature form, if the person validates this specification, then the specification service shall fail the check and name the feature.
shall [x2: artifact the feature form (constant), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: feature]
    not
      conforms(x1, x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r23
From: design-model-check#r195, reworded in request words (0.38.0).

```reading
While a term does not conform to the entry form, if the person validates this specification, then the specification service shall fail the check and name the term.
shall [x2: artifact the entry form (constant), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    not
      conforms(x1, x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r24
From: design-model-check#r196, reworded in request words (0.38.0).

```reading
While this bounded context does not conform to the final layout, if the person validates this specification, then the specification service shall fail the check and name `scripts/migrate`.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x2: artifact the final layout (constant), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical), x7: thing `scripts/migrate` (parameter)]
  while
    not
      conforms(x1, x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x7)
```

## r25
From: design-model-check#r197, reworded in request words (0.38.0).

```reading
While an observation violates `w_uncited_obs`, when the person validates this specification, the specification service shall return `w_uncited_obs` and complete the request.
shall [x2: rule `w_uncited_obs` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: observation]
    violate(subject: x1, object: x2)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    return(e2, subject: x5, object: x2)
    complete(e3, subject: x5, object: x6)
```

## r26
From: design-model-check#r198, reworded in request words (0.38.0).

```reading
While this bounded context has no job, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x7: rule `w_unserved_cap` (parameter)]
  while
    not [x2: job]
      of(x2, x1)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    not [x6: capability]
      violate(subject: x6, object: x7)
      return(e2, subject: x5, object: x6)
```

## r27
From: design-model-check#r199, reworded in request words (0.38.0).

```reading
While this interpreter does not import `clingo` and another interpreter imports `clingo`, when the person validates this specification, the specification service shall return `0 violations`.
shall [x1: interpreter "the interpreter the request is answered with" (indexical), x2: agent `clingo` (constant), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: thing `0 violations` (parameter)]
  while [x3: interpreter]
    not
      import(subject: x1, object: x2)
    distinct(x3, x1)
    import(subject: x3, object: x2)
  when
    request(e1, specification.check, subject: x4, object: x5)
  response
    return(e2, subject: x6, object: x7)
```

## r28
From: design-model-check#r200, reworded in request words (0.38.0).

```reading
While no interpreter imports `clingo`, if the person validates this specification, then the specification service shall fail the check and name this interpreter.
shall [x2: agent `clingo` (constant), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical), x7: interpreter "the interpreter the request is answered with" (indexical)]
  while
    not [x1: interpreter]
      import(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x7)
```

## r29
From: design-model-check#r201, reworded in request words (0.38.0).

```reading
When the person translates this specification, the specification service shall return every fact of this bounded context.
shall [x1: agent the person (constant), x2: specification "the specification of this bounded context" (indexical), x3: service the specification service (constant), x5: bounded context "the bounded context whose repository the command runs in" (indexical)]
  when
    request(e1, specification.translate, subject: x1, object: x2)
  response
    every [x4: fact]
      of(x4, x5)
      scope
        return(e2, subject: x3, object: x4)
```

## r30
From: design-model-check#r207, reworded in request words (0.38.0).

```reading
While a verb has no frame, if the person validates this specification, then the specification service shall fail the check and name the verb.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: verb]
    not [x2: frame]
      of(x2, x1)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r31
From: design-model-check#r208, reworded in request words (0.38.0).

```reading
While a term violates `v_t12`, if the person validates this specification, then the specification service shall fail the check and name the term.
shall [x2: rule `v_t12` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r32
From: design-model-check#r214, reworded in request words (0.38.0).

```reading
While a term has no part of speech, if the person validates this specification, then the specification service shall fail the check and name the term.
shall [x2: agent the person (constant), x3: specification "the specification of this bounded context" (indexical), x4: service the specification service (constant), x5: check "the check the trigger makes" (indexical)]
  while [x1: term]
    part of speech(x1) = none
  if
    request(e1, specification.check, subject: x2, object: x3)
  response
    fail(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r33
From: design-model-check#r215, reworded in request words (0.38.0).

```reading
While a frame of a term has a preposition, when the person validates this specification, the specification service shall complete the request.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: frame, x2: term, x3: preposition]
    of(x1, x2)
    of(x3, x1)
  when
    request(e1, specification.check, subject: x4, object: x5)
  response
    complete(e2, subject: x6, object: x7)
```

## r34
From: design-model-check#r217, reworded in request words (0.38.0).

```reading
While a term violates `v_t13`, if the person validates this specification, then the specification service shall fail the check and name the term.
shall [x2: rule `v_t13` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r35
From: design-model-check#r219, reworded in request words (0.38.0).

```reading
When the person renews the rule catalogue, the specification service shall keep a rule catalogue and complete the request.
shall [x1: agent the person (constant), x2: rule catalogue "the rule catalogue of the plugin" (indexical), x3: service the specification service (constant), x5: request "the request the trigger makes" (indexical)]
  when
    request(e1, specification.renew, subject: x1, object: x2)
  response [x4: rule catalogue]
    keep(e2, subject: x3, object: x4)
    complete(e3, subject: x3, object: x5)
```

## r36
From: design-model-check#r220, reworded in request words (0.38.0).

```reading
While a rule has a catalogue entry that a rule catalogue does not hold, if the person renews the rule catalogue with the audit, then the specification service shall fail the check, name the rule catalogue and change no file.
shall [x4: agent the person (constant), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: rule, x2: catalogue entry, x3: rule catalogue]
    not
      in(x2, x3)
    of(x2, x1)
  if
    request(e1, specification.renew, subject: x4, object: x3)
    param(e1, audit, on)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
    not [x7: file]
      change(e4, subject: x5, object: x7)
```

## r37
From: design-model-check#r221, reworded in request words (0.38.0).

```reading
While a term violates `v_t14`, if the person validates this specification, then the specification service shall fail the check and name the term.
shall [x2: rule `v_t14` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r38
From: design-model-check#r222, reworded in request words (0.38.0).

```reading
While a term has more than one frame, when the person validates this specification, the specification service shall complete the request.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term]
    count more than 1 [x2: frame]
      scope
        of(x2, x1)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    complete(e2, subject: x5, object: x6)
```

## r39
From: design-model-check#r223, reworded in request words (0.38.0).

```reading
While a term has more than one sense, when the person validates this specification, the specification service shall complete the request.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term]
    count more than 1 [x2: sense]
      scope
        of(x2, x1)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    complete(e2, subject: x5, object: x6)
```

## r40
From: design-model-check#r224, reworded in request words (0.38.0).

```reading
While a term violates `v_t15`, if the person validates this specification, then the specification service shall fail the check and name the term.
shall [x2: rule `v_t15` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r41
From: design-model-check#r225, reworded in request words (0.38.0).

```reading
While this bounded context imports a pack, when the person looks up the pack, the language service shall return every term of the pack and complete the request.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x2: pack]
    import(subject: x1, object: x2)
  when
    request(e1, language.look up, subject: x3, object: x2)
  response
    every [x5: term]
      of(x5, x2)
      scope
        return(e2, subject: x4, object: x5)
    complete(e3, subject: x4, object: x6)
```

## r42
From: design-model-check#r226, reworded in request words (0.38.0).

```reading
While this bounded context imports a pack that violates `v_t17`, if the person validates this specification, then the specification service shall fail the check and name the pack.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: rule `v_t17` (parameter), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x2: pack]
    violate(subject: x2, object: x3)
    import(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
```

## r43
From: design-model-check#r227, reworded in request words (0.38.0).

```reading
While a term violates `v_t16`, if the person validates this specification, then the specification service shall fail the check and name the term.
shall [x2: rule `v_t16` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r44
From: design-model-check#r228, reworded in request words (0.38.0).

```reading
While a term redefines a pack, when the person validates this specification, the specification service shall complete the request.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term, x2: pack]
    redefine(subject: x1, object: x2)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    complete(e2, subject: x5, object: x6)
```

## r45
From: design-model-check#r246, reworded in request words (0.38.0).

```reading
While a requirement violates `w_example`, when the person validates this specification, the specification service shall return the requirement.
shall [x2: rule `w_example` (parameter), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant)]
  while [x1: requirement]
    violate(subject: x1, object: x2)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    return(e2, subject: x5, object: x1)
```

## r46
From: design-model-check#r287, reworded in request words (0.38.0).

```reading
If the person validates this specification with a capability whose language is `codified-1`, then the specification service shall refuse the request and name the capability.
shall [x1: agent the person (constant), x2: specification "the specification of this bounded context" (indexical), x4: service the specification service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x3: capability]
    language(x3) = `codified-1`
    request(e1, specification.check, subject: x1, object: x2)
    param(e1, capability, x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
```

## r47
From: design-model-check#r324, reworded in request words (0.38.0).

```reading
While the writer of a file form is `hand`, when the person inventories this specification with the audit, the specification service shall fail the check and name the file form.
shall [x2: agent the person (constant), x3: specification "the specification of this bounded context" (indexical), x4: service the specification service (constant), x5: check "the check the trigger makes" (indexical)]
  while [x1: file form]
    writer(x1) = `hand`
  when
    request(e1, specification.inventory, subject: x2, object: x3)
    param(e1, audit, on)
  response
    fail(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```
