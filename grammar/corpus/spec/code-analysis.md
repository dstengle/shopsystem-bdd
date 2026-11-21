# code-analysis: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: analysis-tools#r47, reworded in request words (0.38.0).

```reading
While a test breaks, when the person maps this repository, the code analysis service shall keep a coverage map and complete the request.
shall [x2: agent the person (constant), x3: repository "the repository the request is made in" (indexical), x4: service the code analysis service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: test]
    break(subject: x1)
  when
    request(e1, code analysis.map, subject: x2, object: x3)
  response [x5: coverage map]
    keep(e2, subject: x4, object: x5)
    complete(e3, subject: x4, object: x6)
```

## r2
From: analysis-tools#r48, reworded in request words (0.38.0).

```reading
While a coverage map exists, when the person maps this repository, the code analysis service shall keep a different coverage map.
shall [x2: agent the person (constant), x3: repository "the repository the request is made in" (indexical), x4: service the code analysis service (constant)]
  while [x1: coverage map]
    exists(x1)
  when
    request(e1, code analysis.map, subject: x2, object: x3)
  response [x5: coverage map]
    distinct(x5, x1)
    keep(e2, subject: x4, object: x5)
```

## r3
From: analysis-tools#r50, reworded in request words (0.38.0).

```reading
While a coverage map exists, when the person traces a function, the code analysis service shall return every test that executes the function, the number of tests that execute the function and the revision of the coverage map.
shall [x2: agent the person (constant), x4: service the code analysis service (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x3: function]
    request(e1, code analysis.trace, subject: x2, object: x3)
  response [x6: number, x8: revision]
    every [x5: test]
      execute(subject: x5, object: x3)
      scope
        return(e2, subject: x4, object: x5)
    number x6 of [x7: test]
      execute(subject: x7, object: x3)
    return(e3, subject: x4, object: x6)
    revision(x1) = x8
    return(e4, subject: x4, object: x8)
```

## r4
From: analysis-tools#r51, reworded in request words (0.38.0).

```reading
While a coverage map exists, when the person traces a function with the file view, the code analysis service shall return every Python file that holds a test that executes the function.
shall [x2: agent the person (constant), x4: service the code analysis service (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x3: function]
    request(e1, code analysis.trace, subject: x2, object: x3)
    param(e1, file view, on)
  response
    every [x5: Python file, x6: test]
      execute(subject: x6, object: x3)
      in(x6, x5)
      scope
        return(e2, subject: x4, object: x5)
```

## r5
From: analysis-tools#r52, reworded in request words (0.38.0).

```reading
While a coverage map exists, when the person traces a function that no test executes, the code analysis service shall return the revision of the coverage map and complete the request.
shall [x2: agent the person (constant), x5: service the code analysis service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: coverage map]
    exists(x1)
  when [x3: function]
    not [x4: test]
      execute(subject: x4, object: x3)
    request(e1, code analysis.trace, subject: x2, object: x3)
  response [x6: revision]
    revision(x1) = x6
    return(e2, subject: x5, object: x6)
    complete(e3, subject: x5, object: x7)
```

## r6
From: analysis-tools#r54, reworded in request words (0.38.0).

```reading
While a coverage map exists, if the person traces an identifier that no Python file defines, then the code analysis service shall refuse the request and name the identifier.
shall [x2: agent the person (constant), x5: service the code analysis service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: coverage map]
    exists(x1)
  if [x3: identifier]
    not [x4: Python file]
      define(subject: x4, object: x3)
    request(e1, code analysis.trace, subject: x2, object: x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r7
From: analysis-tools#r55, reworded in request words (0.38.0).

```reading
While no coverage map exists, if the person traces a function, then the code analysis service shall refuse the request and name the coverage map.
shall [x2: agent the person (constant), x4: service the code analysis service (constant), x5: request "the request the trigger makes" (indexical), x6: coverage map "the coverage map of this repository" (indexical)]
  while
    not [x1: coverage map]
      exists(x1)
  if [x3: function]
    request(e1, code analysis.trace, subject: x2, object: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x6)
```

## r8
From: analysis-tools#r56, reworded in request words (0.38.0).

```reading
While a coverage map exists, when the person screens a Python file, the code analysis service shall return every function of the Python file that no test executes and the revision of the coverage map and complete the request.
shall [x2: agent the person (constant), x4: service the code analysis service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: coverage map]
    exists(x1)
  when [x3: Python file]
    request(e1, code analysis.screen, subject: x2, object: x3)
  response [x7: revision]
    every [x5: function]
      of(x5, x3)
      not [x6: test]
        execute(subject: x6, object: x5)
      scope
        return(e2, subject: x4, object: x5)
    revision(x1) = x7
    return(e3, subject: x4, object: x7)
    complete(e4, subject: x4, object: x8)
```

## r9
From: analysis-tools#r58, reworded in request words (0.38.0).

```reading
When the person locates an identifier that a Python file defines, the code analysis service shall return every reference to the identifier and the number of references to the identifier and complete the request.
shall [x1: agent the person (constant), x4: service the code analysis service (constant), x8: request "the request the trigger makes" (indexical)]
  when [x2: identifier, x3: Python file]
    define(subject: x3, object: x2)
    request(e1, code analysis.locate, subject: x1, object: x2)
  response [x6: number]
    every [x5: reference]
      to(x5, x2)
      scope
        return(e2, subject: x4, object: x5)
    number x6 of [x7: reference]
      to(x7, x2)
    return(e3, subject: x4, object: x6)
    complete(e4, subject: x4, object: x8)
```

## r10
From: analysis-tools#r59, reworded in request words (0.38.0).

```reading
If the person locates an identifier that no Python file defines, then the code analysis service shall refuse the request and name the identifier.
shall [x1: agent the person (constant), x4: service the code analysis service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: identifier]
    not [x3: Python file]
      define(subject: x3, object: x2)
    request(e1, code analysis.locate, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r11
From: analysis-tools#r60, reworded in request words (0.38.0).

```reading
While a file holds a finding of an analysis tool, when the person lints the file, the code analysis service shall return the heading of the analysis tool and the finding, fail the check and name the finding.
shall [x4: agent the person (constant), x5: service the code analysis service (constant), x7: check "the check the trigger makes" (indexical)]
  while [x1: file, x2: finding, x3: analysis tool]
    of(x2, x3)
    in(x2, x1)
  when
    request(e1, code analysis.lint, subject: x4, object: x1)
  response [x6: heading]
    of(x6, x3)
    return(e2, subject: x5, object: x6)
    return(e3, subject: x5, object: x2)
    fail(e4, subject: x5, object: x7)
    name(e5, subject: x5, object: x2)
```

## r12
From: analysis-tools#r61, reworded in request words (0.38.0).

```reading
While `vulture` is `missing`, when the person lints a file, the code analysis service shall fail the check and name `vulture`.
shall [x1: analysis tool `vulture` (constant), x2: agent the person (constant), x4: service the code analysis service (constant), x5: check "the check the trigger makes" (indexical)]
  while
    presence(x1) = `missing`
  when [x3: file]
    request(e1, code analysis.lint, subject: x2, object: x3)
  response
    fail(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r13
From: analysis-tools#r64, reworded in request words (0.38.0).

```reading
While a Python file exceeds a size limit, when the person sizes this repository with the size limit, the code analysis service shall return the Python file, fail the check and name the Python file.
shall [x3: agent the person (constant), x4: repository "the repository the request is made in" (indexical), x5: service the code analysis service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: Python file, x2: size limit]
    exceed(subject: x1, object: x2)
  when
    request(e1, code analysis.size, subject: x3, object: x4)
    param(e1, size limit, x2)
  response
    return(e2, subject: x5, object: x1)
    fail(e3, subject: x5, object: x6)
    name(e4, subject: x5, object: x1)
```

## r14
From: analysis-tools#r65, reworded in request words (0.38.0).

```reading
While no Python file exceeds the `300` size limit, when the person sizes this repository without a size limit, the code analysis service shall complete the request.
shall [x2: size limit `300` (parameter), x3: agent the person (constant), x4: repository "the repository the request is made in" (indexical), x5: service the code analysis service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    not [x1: Python file]
      exceed(subject: x1, object: x2)
  when
    request(e1, code analysis.size, subject: x3, object: x4)
    noparam(e1, size limit)
  response
    complete(e2, subject: x5, object: x6)
```

## r15
From: b490 r15.

```reading
While a Python file differs from the base branch and the Python file holds a finding of an analysis tool, when the person lints this repository, the code analysis service shall return the finding and fail the check.
shall [x2: base branch "the base branch of the repository the request is made in" (indexical), x5: agent the person (constant), x6: repository "the repository the request is made in" (indexical), x7: service the code analysis service (constant), x8: check "the check the trigger makes" (indexical)]
  while [x1: Python file, x3: finding, x4: analysis tool]
    differ(subject: x1, from: x2)
    of(x3, x4)
    in(x3, x1)
  when
    request(e1, code analysis.lint, subject: x5, object: x6)
  response
    return(e2, subject: x7, object: x3)
    fail(e3, subject: x7, object: x8)
```

## r16
From: b490 r16.

```reading
While a Python file holds a finding of an analysis tool and the Python file does not differ from the base branch, when the person lints this repository, the code analysis service shall complete the request.
shall [x4: base branch "the base branch of the repository the request is made in" (indexical), x5: agent the person (constant), x6: repository "the repository the request is made in" (indexical), x7: service the code analysis service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: Python file, x2: finding, x3: analysis tool]
    of(x2, x3)
    in(x2, x1)
    not
      differ(subject: x1, from: x4)
  when
    request(e1, code analysis.lint, subject: x5, object: x6)
  response
    complete(e2, subject: x7, object: x8)
```
