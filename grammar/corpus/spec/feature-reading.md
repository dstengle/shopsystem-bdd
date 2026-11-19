# feature-reading: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: feature-file-tools#r88, reworded in request words (0.38.0).

```reading
While a docstring of a feature file contains a tag and a scenario line, when the person counts the feature file, the feature reading service shall return the number of scenarios of the feature file.
shall [x5: agent the person (constant), x6: service the feature reading service (constant)]
  while [x1: docstring, x2: feature file, x3: tag, x4: scenario line]
    of(x1, x2)
    contain(subject: x1, object: x3)
    contain(subject: x1, object: x4)
  when
    request(e1, feature reading.count, subject: x5, object: x2)
  response [x7: number]
    number x7 of [x8: scenario]
      of(x8, x2)
    return(e2, subject: x6, object: x7)
```

## r2
From: feature-file-tools#r89, reworded in request words (0.38.0).

```reading
While a feature file has a scenario outline and the feature file has no scenario, when the person counts the feature file, the feature reading service shall return the number of examples rows of the scenario outline.
shall [x4: agent the person (constant), x5: service the feature reading service (constant)]
  while [x1: feature file, x2: scenario outline]
    of(x2, x1)
    not [x3: scenario]
      of(x3, x1)
  when
    request(e1, feature reading.count, subject: x4, object: x1)
  response [x6: number]
    number x6 of [x7: examples row]
      of(x7, x2)
    return(e2, subject: x5, object: x6)
```

## r3
From: feature-file-tools#r90, reworded in request words (0.38.0).

```reading
While a docstring of a feature file contains a tag and the feature file does not have the tag, when the person searches this repository with the tag, the feature reading service shall complete the request and not return the feature file.
shall [x4: agent the person (constant), x5: repository "the repository the request is made in" (indexical), x6: service the feature reading service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: docstring, x2: feature file, x3: tag]
    of(x1, x2)
    contain(subject: x1, object: x3)
    not
      of(x3, x2)
  when
    request(e1, feature reading.search, subject: x4, object: x5)
    param(e1, tag, x3)
  response
    complete(e2, subject: x6, object: x7)
    not
      return(e3, subject: x6, object: x2)
```

## r4
From: feature-file-tools#r91, reworded in request words (0.38.0).

```reading
While a feature file in a subdirectory has a scenario, when the person searches this repository with the scenario title of the scenario, the feature reading service shall return the feature file.
shall [x4: agent the person (constant), x5: repository "the repository the request is made in" (indexical), x7: service the feature reading service (constant)]
  while [x1: feature file, x2: subdirectory, x3: scenario]
    in(x1, x2)
    of(x3, x1)
  when [x6: scenario title]
    of(x6, x3)
    request(e1, feature reading.search, subject: x4, object: x5)
    param(e1, scenario title, x6)
  response
    return(e2, subject: x7, object: x1)
```

## r5
From: feature-file-tools#r92, reworded in request words (0.38.0).

```reading
While a feature file has a tag, when the person searches this repository with the tag, the feature reading service shall return every scenario of the feature file.
shall [x3: agent the person (constant), x4: repository "the repository the request is made in" (indexical), x5: service the feature reading service (constant)]
  while [x1: feature file, x2: tag]
    of(x2, x1)
  when
    request(e1, feature reading.search, subject: x3, object: x4)
    param(e1, tag, x2)
  response
    every [x6: scenario]
      of(x6, x1)
      scope
        return(e2, subject: x5, object: x6)
```

## r6
From: feature-file-tools#r93, reworded in request words (0.38.0).

```reading
While a scenario has a tag, when the person searches this repository with the tag, the feature reading service shall return the scenario.
shall [x3: agent the person (constant), x4: repository "the repository the request is made in" (indexical), x5: service the feature reading service (constant)]
  while [x1: scenario, x2: tag]
    of(x2, x1)
  when
    request(e1, feature reading.search, subject: x3, object: x4)
    param(e1, tag, x2)
  response
    return(e2, subject: x5, object: x1)
```

## r7
From: feature-file-tools#r94, reworded in request words (0.38.0).

```reading
When the person searches this repository with a search text, the feature reading service shall return every scenario whose scenario title contains the search text.
shall [x1: agent the person (constant), x2: repository "the repository the request is made in" (indexical), x4: service the feature reading service (constant)]
  when [x3: search text]
    request(e1, feature reading.search, subject: x1, object: x2)
    param(e1, search text, x3)
  response
    every [x5: scenario, x6: scenario title]
      of(x6, x5)
      contain(subject: x6, object: x3)
      scope
        return(e2, subject: x4, object: x5)
```

## r8
From: feature-file-tools#r96, reworded in request words (0.38.0).

```reading
While a feature file has a rule block, if the person counts the feature file, then the feature reading service shall refuse the request and name the feature file.
shall [x3: agent the person (constant), x4: service the feature reading service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: feature file, x2: rule block]
    of(x2, x1)
  if
    request(e1, feature reading.count, subject: x3, object: x1)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r9
From: feature-file-tools#r97, reworded in request words (0.38.0).

```reading
While a replacement of a scenario has a requirement tag and the scenario has the `@deprecated` tag, when the person scans this repository, the feature reading service shall return the scenario and every requirement tag of the replacement.
shall [x4: tag `@deprecated` (parameter), x5: agent the person (constant), x6: repository "the repository the request is made in" (indexical), x7: service the feature reading service (constant)]
  while [x1: replacement, x2: scenario, x3: requirement tag]
    of(x1, x2)
    of(x3, x1)
    of(x4, x2)
  when
    request(e1, feature reading.scan, subject: x5, object: x6)
  response
    return(e2, subject: x7, object: x2)
    every [x8: requirement tag]
      of(x8, x1)
      scope
        return(e3, subject: x7, object: x8)
```

## r10
From: feature-file-tools#r98, reworded in request words (0.38.0).

```reading
While no scenario has the `@deprecated` tag, when the person scans this repository, the feature reading service shall return `none deprecated`.
shall [x2: tag `@deprecated` (parameter), x3: agent the person (constant), x4: repository "the repository the request is made in" (indexical), x5: service the feature reading service (constant), x6: thing `none deprecated` (parameter)]
  while
    not [x1: scenario]
      of(x2, x1)
  when
    request(e1, feature reading.scan, subject: x3, object: x4)
  response
    return(e2, subject: x5, object: x6)
```

## r11
From: feature-file-tools#r100, reworded in request words (0.38.0).

```reading
While every binding binds a scenario, when the person vets this repository, the feature reading service shall return `every binding names a scenario` and complete the request.
shall [x3: agent the person (constant), x4: repository "the repository the request is made in" (indexical), x5: service the feature reading service (constant), x6: thing `every binding names a scenario` (parameter), x7: request "the request the trigger makes" (indexical)]
  while
    every [x1: binding]
      scope [x2: scenario]
        bind(subject: x1, object: x2)
  when
    request(e1, feature reading.vet, subject: x3, object: x4)
  response
    return(e2, subject: x5, object: x6)
    complete(e3, subject: x5, object: x7)
```

## r12
From: feature-file-tools#r101, reworded in request words (0.38.0).

```reading
While a binding of a test module binds no scenario, if the person vets this repository, then the feature reading service shall fail the check, name the test module and change no file.
shall [x4: agent the person (constant), x5: repository "the repository the request is made in" (indexical), x6: service the feature reading service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: binding, x2: test module]
    of(x1, x2)
    not [x3: scenario]
      bind(subject: x1, object: x3)
  if
    request(e1, feature reading.vet, subject: x4, object: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
    not [x8: file]
      change(e4, subject: x6, object: x8)
```

## r13
From: feature-file-tools#r102, reworded in request words (0.38.0).

```reading
While a scenarios call binds a scenario of a feature file, when the person vets this repository with the unbound listing, the feature reading service shall complete the request and not return a scenario of the feature file.
shall [x4: agent the person (constant), x5: repository "the repository the request is made in" (indexical), x6: service the feature reading service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: scenarios call, x2: scenario, x3: feature file]
    of(x2, x3)
    bind(subject: x1, object: x2)
  when
    request(e1, feature reading.vet, subject: x4, object: x5)
    param(e1, unbound listing, on)
  response
    complete(e2, subject: x6, object: x7)
    not [x8: scenario]
      of(x8, x3)
      return(e3, subject: x6, object: x8)
```

## r14
From: feature-file-tools#r103, reworded in request words (0.38.0).

```reading
While a feature file has a scenario that no binding binds, if the person vets this repository with the unbound listing, then the feature reading service shall fail the check, name the scenario and change no file.
shall [x4: agent the person (constant), x5: repository "the repository the request is made in" (indexical), x6: service the feature reading service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: feature file, x2: scenario]
    not [x3: binding]
      bind(subject: x3, object: x2)
    of(x2, x1)
  if
    request(e1, feature reading.vet, subject: x4, object: x5)
    param(e1, unbound listing, on)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
    not [x8: file]
      change(e4, subject: x6, object: x8)
```
