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
shall [x1: bounded context "the bounded context the request is made in" (indexical), x2: artifact the final layout (constant), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical), x7: thing `scripts/migrate` (parameter)]
  while
    not
      conforms(x1, x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x7)
```

## r26
From: design-model-check#r198, reworded in request words (0.38.0).

```reading
While this bounded context has no job, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x7: rule `w_unserved_cap` (parameter)]
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
shall [x1: agent the person (constant), x2: specification "the specification of this bounded context" (indexical), x3: service the specification service (constant), x5: bounded context "the bounded context the request is made in" (indexical)]
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

## r41
From: design-model-check#r225, reworded in request words (0.38.0).

```reading
While this bounded context imports a pack, when the person looks up the pack, the language service shall return every term of the pack and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x3: agent the person (constant), x4: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
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

## r48
From: b368 r48.

```reading
While a requirement governs an operation that an adapter contract holds, when the person annotates the adapter contract, the specification service shall keep an adapter contract that holds an operation that holds the requirement and complete the request.
shall [x4: agent the person (constant), x5: service the specification service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: operation, x3: adapter contract]
    in(x2, x3)
    govern(subject: x1, object: x2)
  when
    request(e1, specification.annotate, subject: x4, object: x3)
  response [x6: adapter contract, x7: operation]
    in(x1, x7)
    in(x7, x6)
    keep(e2, subject: x5, object: x6)
    complete(e3, subject: x5, object: x8)
```

## r49
From: b368 r49.

```reading
While a requirement governs an operation that an adapter contract holds and the operation does not hold the requirement, if the person validates this specification, then the specification service shall fail the check and name the operation and the requirement.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: requirement, x2: operation, x3: adapter contract]
    in(x2, x3)
    govern(subject: x1, object: x2)
    not
      in(x1, x2)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
    name(e4, subject: x6, object: x1)
```

## r50
From: b368 r50.

```reading
While an adapter contract holds an operation and the operation holds a requirement and the requirement does not govern the operation, if the person validates this specification, then the specification service shall fail the check and name the operation and the requirement.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: adapter contract, x2: operation, x3: requirement]
    in(x2, x1)
    in(x3, x2)
    not
      govern(subject: x3, object: x2)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
    name(e4, subject: x6, object: x3)
```

## r51
From: b368 r51.

```reading
While a requirement governs an operation that an adapter contract holds and the operation does not hold the requirement, if the person annotates the adapter contract with the audit, then the specification service shall fail the check, name the adapter contract and change no file.
shall [x4: agent the person (constant), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: requirement, x2: operation, x3: adapter contract]
    in(x2, x3)
    govern(subject: x1, object: x2)
    not
      in(x1, x2)
  if
    request(e1, specification.annotate, subject: x4, object: x3)
    param(e1, audit, on)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
    not [x7: file]
      change(e4, subject: x5, object: x7)
```

## r52
From: b370 r52.

```reading
While a capability violates a rule whose severity is `error`, if the person validates this specification, then the specification service shall fail the check and name the rule.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: capability, x2: rule]
    severity(x2) = `error`
    violate(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r53
From: b370 r53.

```reading
While a capability violates a rule whose severity is `warning` and nothing violates a rule whose severity is `error`, when the person validates this specification, the specification service shall name the rule and complete the request.
shall [x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: capability, x2: rule]
    severity(x2) = `warning`
    violate(subject: x1, object: x2)
    not [x3: thing, x4: rule]
      severity(x4) = `error`
      violate(subject: x3, object: x4)
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    name(e2, subject: x7, object: x2)
    complete(e3, subject: x7, object: x8)
```

## r54
From: b370 r54.

```reading
While a requirement uses a rule that has no catalogue entry, if the person validates this specification, then the specification service shall fail the check and name the rule.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: requirement, x2: rule]
    not [x3: catalogue entry]
      of(x3, x2)
    use(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
```

## r55
From: b370 r55.

```reading
While a catalogue entry has no purpose, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: catalogue entry]
    not [x2: purpose]
      of(x2, x1)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r57
From: b370 r57.

```reading
While a catalogue entry mentions an item whose status is not `delivered`, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry and the item.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: catalogue entry, x2: item]
    not
      status(x2) = `delivered`
    mention(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
    name(e4, subject: x5, object: x2)
```

## r58
Retires: r56. From: b370 r58.

```reading
While a catalogue entry mentions no item and the catalogue entry mentions no release, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: catalogue entry]
    not [x2: item]
      mention(subject: x1, object: x2)
    not [x3: release]
      mention(subject: x1, object: x3)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x1)
```

## r59
From: b462 r59.

```reading
When the person describes a catalogue entry with a purpose, the specification service shall keep a catalogue entry that has the purpose and complete the request.
shall [x1: agent the person (constant), x4: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: catalogue entry, x3: purpose]
    request(e1, specification.describe, subject: x1, object: x2)
    param(e1, purpose, x3)
  response [x5: catalogue entry]
    of(x3, x5)
    keep(e2, subject: x4, object: x5)
    complete(e3, subject: x4, object: x6)
```

## r60
From: b462 r60.

```reading
When the person describes a catalogue entry with an item, the specification service shall keep a catalogue entry that mentions the item and complete the request.
shall [x1: agent the person (constant), x4: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: catalogue entry, x3: item]
    request(e1, specification.describe, subject: x1, object: x2)
    param(e1, item, x3)
  response [x5: catalogue entry]
    mention(subject: x5, object: x3)
    keep(e2, subject: x4, object: x5)
    complete(e3, subject: x4, object: x6)
```

## r61
From: b462 r61.

```reading
If the person describes a catalogue entry in the rule catalogue that no rule has, then the specification service shall refuse the request and name the catalogue entry.
shall [x1: agent the person (constant), x3: rule catalogue "the rule catalogue of the plugin" (indexical), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: catalogue entry]
    in(x2, x3)
    not [x4: rule]
      of(x2, x4)
    request(e1, specification.describe, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r62
From: b462 r62.

```reading
If the person describes a catalogue entry in the construct catalogue that no construct has, then the specification service shall refuse the request and name the catalogue entry.
shall [x1: agent the person (constant), x3: construct catalogue "the construct catalogue of the bounded context the command runs in" (indexical), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: catalogue entry]
    in(x2, x3)
    not [x4: construct]
      of(x2, x4)
    request(e1, specification.describe, subject: x1, object: x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r63
From: b538 r63.

```reading
While a term whose part of speech is `attribute` has more than one sense, when the person validates this specification, the specification service shall complete the request.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term]
    part of speech(x1) = `attribute`
    count more than 1 [x2: sense]
      scope
        of(x2, x1)
  when
    request(e1, specification.check, subject: x3, object: x4)
  response
    complete(e2, subject: x5, object: x6)
```

## r64
From: b547 r64.

```reading
When the person prepares a contract, the specification service shall return a contract that conforms to the contract form and change nothing.
shall [x1: agent the person (constant), x3: service the specification service (constant), x5: artifact the contract form (constant)]
  when [x2: contract]
    request(e1, specification.prepare, subject: x1, object: x2)
  response [x4: contract]
    conforms(x4, x5)
    return(e2, subject: x3, object: x4)
    not [x6: thing]
      change(e3, subject: x3, object: x6)
```

## r65
From: b547 r65.

```reading
While a requirement governs an operation, when the person prepares a contract, the specification service shall return a contract that holds the requirement.
shall [x3: agent the person (constant), x5: service the specification service (constant)]
  while [x1: requirement, x2: operation]
    govern(subject: x1, object: x2)
  when [x4: contract]
    request(e1, specification.prepare, subject: x3, object: x4)
  response [x6: contract]
    in(x1, x6)
    return(e2, subject: x5, object: x6)
```

## r66
From: b547 r66.

```reading
While an operation has a property, when the person prepares a contract, the specification service shall return a contract that holds the property.
shall [x3: agent the person (constant), x5: service the specification service (constant)]
  while [x1: operation, x2: property]
    of(x2, x1)
  when [x4: contract]
    request(e1, specification.prepare, subject: x3, object: x4)
  response [x6: contract]
    in(x2, x6)
    return(e2, subject: x5, object: x6)
```

## r67
From: b547 r67.

```reading
While a property refers to an operation that does not exist, if the person validates this specification, then the specification service shall fail the check and name the property.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: property, x2: operation]
    not
      exists(x2)
    refer#2(subject: x1, to: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r69
From: b548 r69.

```reading
While an area whose kind is `port` holds an operation and no adapter contract holds an operation table of the operation, when the person validates this specification, the specification service shall complete the request.
shall [x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: area, x2: operation]
    kind(x1) = `port`
    in(x2, x1)
    not [x3: adapter contract, x4: operation table]
      of(x4, x2)
      in(x4, x3)
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    complete(e2, subject: x7, object: x8)
```

## r70
From: b548 r70.

```reading
While a requirement supports a requirement id that no requirement has, if the person validates this specification, then the specification service shall fail the check and name the requirement id.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: requirement, x2: requirement id]
    not [x3: requirement]
      of(x2, x3)
    support(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
```

## r71
From: b543 r71.

```reading
While a requirement uses `response-request` and the requirement uses an operation and no requirement governs the operation, when the person validates this specification, the specification service shall complete the request.
shall [x2: thing `response-request` (parameter), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: operation]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    not [x4: requirement]
      govern(subject: x4, object: x3)
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    complete(e2, subject: x7, object: x8)
```

## r72
From: b543 r72.

```reading
While a requirement uses `response-request` and the requirement uses an operation and another requirement has a trigger that uses a refusal and the operation, when the person validates this specification, the specification service shall complete the request.
shall [x2: thing `response-request` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x3: operation, x4: requirement, x5: trigger, x6: refusal]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    distinct(x4, x1)
    use(subject: x5, object: x6)
    use(subject: x5, object: x3)
    of(x5, x4)
  when
    request(e1, specification.check, subject: x7, object: x8)
  response
    complete(e2, subject: x9, object: x10)
```

## r73
From: b348 r73.

```reading
When the person publishes a contract with the `1.2.0` version, the specification service shall keep a contract that has the `1.2.0` version.
shall [x1: agent the person (constant), x3: version `1.2.0` (parameter), x4: service the specification service (constant)]
  when [x2: contract]
    request(e1, specification.publish, subject: x1, object: x2)
    param(e1, version, x3)
  response [x5: contract]
    of(x3, x5)
    keep(e2, subject: x4, object: x5)
```

## r74
From: b348 r74.

```reading
When the person publishes a contract with the `1.3.0` version, the specification service shall set the status of every contract whose status is `published` to `superseded`.
shall [x1: agent the person (constant), x3: version `1.3.0` (parameter), x4: service the specification service (constant)]
  when [x2: contract]
    request(e1, specification.publish, subject: x1, object: x2)
    param(e1, version, x3)
  response
    every [x5: contract]
      status(x5) = `published`
      scope
        initiates(e2, subject: x4, status(x5) = `superseded`)
```

## r75
From: b348 r75.

```reading
While a contract has the `1.2.0` version, if the person publishes a contract with the `1.2.0` version, then the specification service shall refuse the request and name the version.
shall [x2: version `1.2.0` (parameter), x3: agent the person (constant), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: contract]
    of(x2, x1)
  if [x4: contract]
    request(e1, specification.publish, subject: x3, object: x4)
    param(e1, version, x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r76
From: b348 r76.

```reading
While a requirement does not conform to the language reference, if the person publishes a contract, then the specification service shall refuse the request and name the requirement.
shall [x2: artifact the language reference (constant), x3: agent the person (constant), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: requirement]
    not
      conforms(x1, x2)
  if [x4: contract]
    request(e1, specification.publish, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r77
From: b348 r77.

```reading
When the person publishes a contract, the specification service shall keep a contract whose status is `published` and keep every requirement and every term in the contract.
shall [x1: agent the person (constant), x3: service the specification service (constant)]
  when [x2: contract]
    request(e1, specification.publish, subject: x1, object: x2)
  response [x4: contract]
    status(x4) = `published`
    keep(e2, subject: x3, object: x4)
    every [x5: requirement]
      scope
        keep(e3, subject: x3, object: x5)
    every [x6: term]
      in(x6, x4)
      scope
        keep(e4, subject: x3, object: x6)
```

## r78
From: b348 r78.

```reading
When a downstream context fetches a contract, the specification service shall return the contract whose status is `published` and change nothing.
shall [x3: service the specification service (constant)]
  when [x1: downstream context, x2: contract]
    request(e1, specification.fetch, subject: x1, object: x2)
  response
    status(x2) = `published`
    return(e2, subject: x3, object: x2)
    not [x4: thing]
      change(e3, subject: x3, object: x4)
```

## r79
From: b348 r79.

```reading
While no contract has the `2.0.0` version, if a downstream context fetches a contract with the `2.0.0` version, then the specification service shall refuse the request and name the version.
shall [x2: version `2.0.0` (parameter), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    not [x1: contract]
      of(x2, x1)
  if [x3: downstream context, x4: contract]
    request(e1, specification.fetch, subject: x3, object: x4)
    param(e1, version, x2)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r80
From: b348 r80.

```reading
When a downstream context fetches a contract with the `1.2.0` version, the specification service shall return the contract that has the `1.2.0` version.
shall [x3: version `1.2.0` (parameter), x4: service the specification service (constant)]
  when [x1: downstream context, x2: contract]
    request(e1, specification.fetch, subject: x1, object: x2)
    param(e1, version, x3)
  response
    of(x3, x2)
    return(e2, subject: x4, object: x2)
```

## r81
From: b587 r81.

```reading
When the person obtains a contract from a bounded context, the specification service shall keep the contract and keep no context request.
shall [x1: agent the person (constant), x4: service the specification service (constant)]
  when [x2: contract, x3: bounded context]
    request(e1, specification.obtain, subject: x1, object: x2, from: x3)
  response
    keep(e2, subject: x4, object: x2)
    not [x5: context request]
      keep(e3, subject: x4, object: x5)
```

## r82
From: b587 r82.

```reading
If the person obtains a contract from a bounded context that has no contract, then the specification service shall refuse the request and name the bounded context.
shall [x1: agent the person (constant), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: contract, x3: bounded context]
    not [x4: contract]
      of(x4, x3)
    request(e1, specification.obtain, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r83
From: b589 r83.

```reading
If the person publishes a contract with a version that does not conform to the version form, then the specification service shall refuse the request and name the version and the `version not in the version form` reason.
shall [x1: agent the person (constant), x4: artifact the version form (constant), x5: service the specification service (constant), x6: request "the request the trigger makes" (indexical), x7: reason `version not in the version form` (parameter)]
  if [x2: contract, x3: version]
    not
      conforms(x3, x4)
    request(e1, specification.publish, subject: x1, object: x2)
    param(e1, version, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
    name(e4, subject: x5, object: x7)
```

## r84
From: b540 r84.

```reading
While the id of an adapter spec does not conform to the adapter spec id form, if the person validates the adapter spec, then the specification service shall fail the check and name the id.
shall [x3: artifact the adapter spec id form (constant), x4: agent the person (constant), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: adapter spec, x2: id]
    of(x2, x1)
    not
      conforms(x2, x3)
  if
    request(e1, specification.check, subject: x4, object: x1)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r85
From: b540 r85.

```reading
While an adapter spec realises a requirement id that no requirement has, if the person validates the adapter spec, then the specification service shall fail the check and name the requirement id.
shall [x4: agent the person (constant), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: adapter spec, x2: requirement id]
    not [x3: requirement]
      of(x2, x3)
    realise(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x4, object: x1)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r86
From: b540 r86.

```reading
While a provider of an adapter spec has no contract that the adapter spec holds, if the person validates the adapter spec, then the specification service shall fail the check and name the provider.
shall [x4: agent the person (constant), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: provider, x2: adapter spec]
    of(x1, x2)
    not [x3: contract]
      in(x3, x2)
      of(x3, x1)
  if
    request(e1, specification.check, subject: x4, object: x2)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r87
From: b540 r87.

```reading
While an adapter spec holds an adapter decision and the adapter spec holds a contract of a provider of the adapter spec, when the person validates the adapter spec, the specification service shall complete the request.
shall [x5: agent the person (constant), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: adapter spec, x2: adapter decision, x3: contract, x4: provider]
    in(x2, x1)
    of(x4, x1)
    of(x3, x4)
    in(x3, x1)
  when
    request(e1, specification.check, subject: x5, object: x1)
  response
    complete(e2, subject: x6, object: x7)
```

## r88
From: b591 r88.

```reading
If the person obtains a contract from a bounded context whose id does not conform to the context id form, then the specification service shall refuse the request and name the id and the `id not in the context id form` reason.
shall [x1: agent the person (constant), x5: artifact the context id form (constant), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical), x8: reason `id not in the context id form` (parameter)]
  if [x2: contract, x3: bounded context, x4: id]
    of(x4, x3)
    not
      conforms(x4, x5)
    request(e1, specification.obtain, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x4)
    name(e4, subject: x6, object: x8)
```

## r89
From: b591 r89.

```reading
If the person obtains a contract from a bounded context whose availability is `unreachable`, then the specification service shall refuse the request and name the bounded context and the `bounded context unreachable` reason.
shall [x1: agent the person (constant), x4: service the specification service (constant), x5: request "the request the trigger makes" (indexical), x6: reason `bounded context unreachable` (parameter)]
  if [x2: contract, x3: bounded context]
    availability(x3) = `unreachable`
    request(e1, specification.obtain, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
    name(e4, subject: x4, object: x6)
```

## r90
From: b591 r90.

```reading
While a bounded context has a contract, when the person obtains a contract from another bounded context, the specification service shall keep the contract and change no contract of a bounded context.
shall [x3: agent the person (constant), x6: service the specification service (constant)]
  while [x1: bounded context, x2: contract]
    of(x2, x1)
  when [x4: contract, x5: bounded context]
    distinct(x5, x1)
    request(e1, specification.obtain, subject: x3, object: x4, from: x5)
  response
    keep(e2, subject: x6, object: x4)
    not [x7: contract, x8: bounded context]
      of(x7, x8)
      change(e3, subject: x6, object: x7)
```

## r91
From: b593 r91.

```reading
While an adapter spec has a provider, when the person obtains a contract from the provider, the specification service shall keep the contract that the adapter spec holds.
shall [x3: agent the person (constant), x5: service the specification service (constant)]
  while [x1: adapter spec, x2: provider]
    of(x2, x1)
  when [x4: contract]
    request(e1, specification.obtain, subject: x3, object: x4, from: x2)
  response
    in(x4, x1)
    keep(e2, subject: x5, object: x4)
```

## r92
From: b595 r92.

```reading
While the id of an adapter spec does not match the adapter spec, if the person validates the adapter spec, then the specification service shall fail the check and name the id.
shall [x3: agent the person (constant), x4: service the specification service (constant), x5: check "the check the trigger makes" (indexical)]
  while [x1: adapter spec, x2: id]
    of(x2, x1)
    not
      match(subject: x2, object: x1)
  if
    request(e1, specification.check, subject: x3, object: x1)
  response
    fail(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r93
From: b595 r93.

```reading
While a provider of an adapter spec has a version that does not conform to the version form, if the person validates the adapter spec, then the specification service shall fail the check and name the version.
shall [x4: artifact the version form (constant), x5: agent the person (constant), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: provider, x2: adapter spec, x3: version]
    of(x1, x2)
    not
      conforms(x3, x4)
    of(x3, x1)
  if
    request(e1, specification.check, subject: x5, object: x2)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r95
From: b549 r95.

```reading
While a driven port holds an operation and no core line that uses `response-request` uses the operation, if the person validates this specification, then the specification service shall fail the check and name the operation.
shall [x4: thing `response-request` (parameter), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: check "the check the trigger makes" (indexical)]
  while [x1: driven port, x2: operation]
    in(x2, x1)
    not [x3: core line]
      use(subject: x3, object: x4)
      use(subject: x3, object: x2)
  if
    request(e1, specification.check, subject: x5, object: x6)
  response
    fail(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x2)
```

## r96
From: b549 r96.

```reading
While a driven port holds an operation that has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, if the person validates this specification, then the specification service shall fail the check and name the operation outcome.
shall [x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: check "the check the trigger makes" (indexical)]
  while [x1: driven port, x2: operation, x3: operation outcome]
    of(x3, x2)
    in(x2, x1)
    not [x4: core line]
      handle(subject: x4, object: x3)
    not [x5: port line]
      exclude(subject: x5, object: x3)
  if
    request(e1, specification.check, subject: x6, object: x7)
  response
    fail(e2, subject: x8, object: x9)
    name(e3, subject: x8, object: x3)
```

## r97
From: b549 r97.

```reading
While a port line that governs an operation supports a requirement id and no core line that has the requirement id uses the operation, if the person validates this specification, then the specification service shall fail the check and name the requirement id.
shall [x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: check "the check the trigger makes" (indexical)]
  while [x1: port line, x2: operation, x3: requirement id]
    govern(subject: x1, object: x2)
    support(subject: x1, object: x3)
    not [x4: core line]
      of(x3, x4)
      use(subject: x4, object: x2)
  if
    request(e1, specification.check, subject: x5, object: x6)
  response
    fail(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x3)
```

## r98
From: b549 r98.

```reading
While a port line governs an operation and no core line relies on the port line, if the person validates this specification, then the specification service shall fail the check and name the port line.
shall [x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: port line, x2: operation]
    govern(subject: x1, object: x2)
    not [x3: core line]
      rely on(subject: x3, object: x1)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x1)
```

## r99
From: b549 r99.

```reading
While a core line that uses `response-request` uses an operation and a port line that governs the operation supports no requirement id and the port line excludes an operation outcome that no core line handles, when the person validates this specification, the specification service shall complete the request.
shall [x2: thing `response-request` (parameter), x8: agent the person (constant), x9: specification "the specification of this bounded context" (indexical), x10: service the specification service (constant), x11: request "the request the trigger makes" (indexical)]
  while [x1: core line, x3: operation, x4: port line, x6: operation outcome]
    use(subject: x1, object: x2)
    use(subject: x1, object: x3)
    govern(subject: x4, object: x3)
    not [x5: requirement id]
      support(subject: x4, object: x5)
    not [x7: core line]
      handle(subject: x7, object: x6)
    exclude(subject: x4, object: x6)
  when
    request(e1, specification.check, subject: x8, object: x9)
  response
    complete(e2, subject: x10, object: x11)
```

## r100
From: b599 r100.

```reading
While an adapter spec has a provider and the provider has the `1.2.0` version and the provider has a contract that has the `1.3.0` version, when the person obtains a contract from the provider, the specification service shall keep a contract that has the `1.2.0` version and keep the adapter spec that holds the contract.
shall [x3: version `1.2.0` (parameter), x5: version `1.3.0` (parameter), x6: agent the person (constant), x8: service the specification service (constant)]
  while [x1: adapter spec, x2: provider, x4: contract]
    of(x2, x1)
    of(x3, x2)
    of(x5, x4)
    of(x4, x2)
  when [x7: contract]
    request(e1, specification.obtain, subject: x6, object: x7, from: x2)
  response [x9: contract]
    of(x3, x9)
    keep(e2, subject: x8, object: x9)
    in(x9, x1)
    keep(e3, subject: x8, object: x1)
```

## r101
From: b610 r101.

```reading
While an area holds a lifecycle and the lifecycle has a transition and another area holds an operation that performs the transition, if the person validates this specification, then the specification service shall fail the check and name the transition.
shall [x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: check "the check the trigger makes" (indexical)]
  while [x1: area, x2: lifecycle, x3: transition, x4: area, x5: operation]
    in(x2, x1)
    of(x3, x2)
    distinct(x4, x1)
    perform(subject: x5, object: x3)
    in(x5, x4)
  if
    request(e1, specification.check, subject: x6, object: x7)
  response
    fail(e2, subject: x8, object: x9)
    name(e3, subject: x8, object: x3)
```

## r102
From: b596 r102.

```reading
If the person obtains a contract from a bounded context whose health is `failing`, then the specification service shall refuse the request and name the bounded context and the `bounded context failing` reason.
shall [x1: agent the person (constant), x4: service the specification service (constant), x5: request "the request the trigger makes" (indexical), x6: reason `bounded context failing` (parameter)]
  if [x2: contract, x3: bounded context]
    health(x3) = `failing`
    request(e1, specification.obtain, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
    name(e4, subject: x4, object: x6)
```

## r103
Retires: r94. From: b601 r103.

```reading
While the id of a provider conforms to the context id form and the provider is `available`, if the person obtains a contract from the provider that no adapter spec has, then the specification service shall refuse the request and name the provider and the `no adapter spec has the provider` reason.
shall [x3: artifact the context id form (constant), x4: agent the person (constant), x7: service the specification service (constant), x8: request "the request the trigger makes" (indexical), x9: reason `no adapter spec has the provider` (parameter)]
  while [x1: provider, x2: id]
    of(x2, x1)
    conforms(x2, x3)
    availability(x1) = `available`
  if [x5: contract]
    not [x6: adapter spec]
      of(x1, x6)
    request(e1, specification.obtain, subject: x4, object: x5, from: x1)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x1)
    name(e4, subject: x7, object: x9)
```

## r104
From: b609 r104.

```reading
While this bounded context imports a pack and the pack has a term and an element refers to the term, when the person validates this specification, the specification service shall complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x2: pack, x3: term, x4: element]
    import(subject: x1, object: x2)
    of(x3, x2)
    refer#3(subject: x4, to: x3)
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    complete(e2, subject: x7, object: x8)
```

## r105
From: b609 r105.

```reading
While this bounded context imports the `base` pack, when the person looks up the pack, the language service shall return every term of the pack and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x2: pack `base` (parameter), x3: agent the person (constant), x4: service the language service (constant), x6: request "the request the trigger makes" (indexical)]
  while
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

## r106
From: b550 r106.

```reading
While an adapter spec holds a contract and a requirement of the adapter spec uses a term that the contract holds, when the person validates the adapter spec, the specification service shall complete the request.
shall [x5: agent the person (constant), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: adapter spec, x2: contract, x3: requirement, x4: term]
    in(x2, x1)
    of(x3, x1)
    in(x4, x2)
    use(subject: x3, object: x4)
  when
    request(e1, specification.check, subject: x5, object: x1)
  response
    complete(e2, subject: x6, object: x7)
```

## r107
From: b550 r107.

```reading
While an adapter spec holds a contract that holds a term and the term clashes with another term and the adapter spec renames the term, when the person validates the adapter spec, the specification service shall complete the request.
shall [x5: agent the person (constant), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: adapter spec, x2: contract, x3: term, x4: term]
    in(x3, x2)
    in(x2, x1)
    distinct(x4, x3)
    clash(subject: x3, with: x4)
    rename(subject: x1, object: x4)
  when
    request(e1, specification.check, subject: x5, object: x1)
  response
    complete(e2, subject: x6, object: x7)
```

## r108
From: b550 r108.

```reading
While an adapter spec holds a contract that holds a term and the term clashes with another term and the adapter spec does not rename the term, if the person validates the adapter spec, then the specification service shall fail the check and name the term.
shall [x5: agent the person (constant), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: adapter spec, x2: contract, x3: term, x4: term]
    in(x3, x2)
    in(x2, x1)
    distinct(x4, x3)
    clash(subject: x3, with: x4)
    not
      rename(subject: x1, object: x4)
  if
    request(e1, specification.check, subject: x5, object: x1)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x4)
```

## r109
From: b550 r109.

```reading
While an adapter spec holds an assumed description that holds a requirement id that no scenario refers to, if the person validates the adapter spec, then the specification service shall fail the check and name the requirement id.
shall [x5: agent the person (constant), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: adapter spec, x2: assumed description, x3: requirement id]
    not [x4: scenario]
      refer(subject: x4, to: x3)
    in(x3, x2)
    in(x2, x1)
  if
    request(e1, specification.check, subject: x5, object: x1)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r110
From: b641 r110.

```reading
While this bounded context has a job and a requirement group of a capability serves the job, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x9: rule `w_unserved_cap` (parameter)]
  while [x2: job, x3: requirement group, x4: capability]
    of(x2, x1)
    of(x3, x4)
    serve(subject: x3, object: x2)
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    not [x8: capability]
      violate(subject: x8, object: x9)
      return(e2, subject: x7, object: x8)
```

## r111
From: b604 r111.

```reading
While a requirement has a response that uses an operation and no parameter and no requirement governs the operation, when the person validates this specification, the specification service shall complete the request.
shall [x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: response, x3: operation]
    use(subject: x2, object: x3)
    not [x4: parameter]
      use(subject: x2, object: x4)
    of(x2, x1)
    not [x5: requirement]
      govern(subject: x5, object: x3)
  when
    request(e1, specification.check, subject: x6, object: x7)
  response
    complete(e2, subject: x8, object: x9)
```

## r112
From: b605 r112.

```reading
While a lifecycle has a transition and a requirement that forbids an act uses `set-attribute` and the transition and no operation performs the transition, when the person validates this specification, the specification service shall name the transition and complete the request.
shall [x5: thing `set-attribute` (parameter), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: lifecycle, x2: transition, x3: requirement, x4: act]
    of(x2, x1)
    forbid(subject: x3, object: x4)
    use(subject: x3, object: x5)
    use(subject: x3, object: x2)
    not [x6: operation]
      perform(subject: x6, object: x2)
  when
    request(e1, specification.check, subject: x7, object: x8)
  response
    name(e2, subject: x9, object: x2)
    complete(e3, subject: x9, object: x10)
```

## r113
From: b688 r113.

```reading
While this bounded context imports a pack and the pack has a term and the term spells an element and no term means the element and another element refers to the term, when the person validates this specification, the specification service shall complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x7: agent the person (constant), x8: specification "the specification of this bounded context" (indexical), x9: service the specification service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x2: pack, x3: term, x4: element, x6: element]
    import(subject: x1, object: x2)
    of(x3, x2)
    spell(subject: x3, object: x4)
    not [x5: term]
      mean(subject: x5, object: x4)
    distinct(x6, x4)
    refer#3(subject: x6, to: x3)
  when
    request(e1, specification.check, subject: x7, object: x8)
  response
    complete(e2, subject: x9, object: x10)
```

## r114
From: b643 r114.

```reading
While this product holds a job and no bounded context holds the job, when the person validates this specification, the specification service shall name the job and complete the request.
shall [x1: product "the product this bounded context belongs to" (indexical), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x2: job]
    in(x2, x1)
    not [x3: bounded context]
      in(x2, x3)
  when
    request(e1, specification.check, subject: x4, object: x5)
  response
    name(e2, subject: x6, object: x2)
    complete(e3, subject: x6, object: x7)
```

## r115
From: b643 r115.

```reading
While this bounded context holds a job and no requirement group serves the job, when the person validates this specification, the specification service shall name the job and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x2: job]
    in(x2, x1)
    not [x3: requirement group]
      serve(subject: x3, object: x2)
  when
    request(e1, specification.check, subject: x4, object: x5)
  response
    name(e2, subject: x6, object: x2)
    complete(e3, subject: x6, object: x7)
```

## r116
From: b643 r116.

```reading
While this bounded context holds a job and an agent plays a product actor of the job and the agent triggers no requirement that the job reaches, when the person validates this specification, the specification service shall name the product actor and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x6: agent the person (constant), x7: specification "the specification of this bounded context" (indexical), x8: service the specification service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x2: job, x3: agent, x4: product actor]
    in(x2, x1)
    of(x4, x2)
    play(subject: x3, object: x4)
    not [x5: requirement]
      reach(subject: x2, object: x5)
      trigger(subject: x3, object: x5)
  when
    request(e1, specification.check, subject: x6, object: x7)
  response
    name(e2, subject: x8, object: x4)
    complete(e3, subject: x8, object: x9)
```

## r117
From: b643 r117.

```reading
While this product holds a job and the job needs a need that depends on the job, if the person validates this specification, then the specification service shall fail the check and name the need.
shall [x1: product "the product this bounded context belongs to" (indexical), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x2: job, x3: need]
    in(x2, x1)
    depend on(subject: x3, object: x2)
    need(subject: x2, object: x3)
  if
    request(e1, specification.check, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r118
From: b643 r118.

```reading
While this product holds a subdomain and no bounded context addresses the subdomain, when the person validates this specification, the specification service shall name the subdomain and complete the request.
shall [x1: product "the product this bounded context belongs to" (indexical), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x2: subdomain]
    in(x2, x1)
    not [x3: bounded context]
      address(subject: x3, object: x2)
  when
    request(e1, specification.check, subject: x4, object: x5)
  response
    name(e2, subject: x6, object: x2)
    complete(e3, subject: x6, object: x7)
```

## r119
From: b643 r119.

```reading
While this bounded context holds a job and a subdomain serves the job and the job reaches no bounded context that addresses the subdomain, when the person validates this specification, the specification service shall name the subdomain and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x2: job, x3: subdomain]
    in(x2, x1)
    serve#2(subject: x3, object: x2)
    not [x4: bounded context]
      address(subject: x4, object: x3)
      reach(subject: x2, object: x4)
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    name(e2, subject: x7, object: x3)
    complete(e3, subject: x7, object: x8)
```

## r120
From: b643 r120.

```reading
While this bounded context has a job and the job reaches a capability, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x4: agent the person (constant), x5: specification "the specification of this bounded context" (indexical), x6: service the specification service (constant), x8: rule `w_unserved_cap` (parameter)]
  while [x2: job, x3: capability]
    of(x2, x1)
    reach(subject: x2, object: x3)
  when
    request(e1, specification.check, subject: x4, object: x5)
  response
    not [x7: capability]
      violate(subject: x7, object: x8)
      return(e2, subject: x6, object: x7)
```

## r121
From: b643 r121.

```reading
While this bounded context has a job and a capability has a port line, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x9: rule `w_unserved_cap` (parameter)]
  while [x2: job, x3: capability, x4: port line]
    of(x2, x1)
    of(x4, x3)
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    not [x8: capability]
      violate(subject: x8, object: x9)
      return(e2, subject: x7, object: x8)
```

## r122
From: b643 r122.

```reading
While this bounded context has a job and a requirement group serves the job and the group of a capability is `guarantees`, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x9: rule `w_unserved_cap` (parameter)]
  while [x2: job, x3: requirement group, x4: capability]
    of(x2, x1)
    serve(subject: x3, object: x2)
    group(x4) = `guarantees`
  when
    request(e1, specification.check, subject: x5, object: x6)
  response
    not [x8: capability]
      violate(subject: x8, object: x9)
      return(e2, subject: x7, object: x8)
```

## r123
From: b643 r123.

```reading
While a requirement group serves a job and this bounded context has the job and another bounded context holds the job, if the person validates this specification, then the specification service shall fail the check and name the job.
shall [x3: bounded context "the bounded context the request is made in" (indexical), x5: agent the person (constant), x6: specification "the specification of this bounded context" (indexical), x7: service the specification service (constant), x8: check "the check the trigger makes" (indexical)]
  while [x1: requirement group, x2: job, x4: bounded context]
    serve(subject: x1, object: x2)
    of(x2, x3)
    distinct(x4, x3)
    in(x2, x4)
  if
    request(e1, specification.check, subject: x5, object: x6)
  response
    fail(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x2)
```
