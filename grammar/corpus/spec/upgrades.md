# upgrades: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: migration-tools#r27, reworded in request words (0.38.0).

```reading
While this repository holds an old-layout directory, when the person relocates a bounded context, the upgrades service shall change every old-layout directory and every file that mentions an old-layout directory.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x5: service the upgrades service (constant)]
  while [x2: old-layout directory]
    in(x2, x1)
  when [x4: bounded context]
    request(e1, upgrades.relocate, subject: x3, object: x4)
  response
    every [x6: old-layout directory]
      scope
        change(e2, subject: x5, object: x6)
    every [x7: file, x8: old-layout directory]
      mention(subject: x7, object: x8)
      scope
        change(e3, subject: x5, object: x7)
```

## r2
From: migration-tools#r28, reworded in request words (0.38.0).

```reading
While a decision ledger of this repository has a ledger entry, when the person relocates a bounded context, the upgrades service shall keep a design-decision of the ledger entry, keep no decision ledger, change the decisions index of this repository and complete the request.
shall [x2: repository "the repository the request is made in" (indexical), x4: agent the person (constant), x6: service the upgrades service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: decision ledger, x3: ledger entry]
    of(x1, x2)
    of(x3, x1)
  when [x5: bounded context]
    request(e1, upgrades.relocate, subject: x4, object: x5)
  response [x7: design-decision, x9: decisions index]
    of(x7, x3)
    keep(e2, subject: x6, object: x7)
    not [x8: decision ledger]
      keep(e3, subject: x6, object: x8)
    of(x9, x2)
    change(e4, subject: x6, object: x9)
    complete(e5, subject: x6, object: x10)
```

## r3
From: migration-tools#r58, reworded in request words (0.38.0).

```reading
While a ledger entry supersedes another ledger entry, when the person relocates a bounded context, the upgrades service shall keep a design-decision of the ledger entry whose status is `superseded` and keep another design-decision that supersedes the design-decision.
shall [x3: agent the person (constant), x5: service the upgrades service (constant)]
  while [x1: ledger entry, x2: ledger entry]
    distinct(x2, x1)
    supersede(subject: x1, object: x2)
  when [x4: bounded context]
    request(e1, upgrades.relocate, subject: x3, object: x4)
  response [x6: design-decision, x7: design-decision]
    of(x6, x2)
    status(x6) = `superseded`
    keep(e2, subject: x5, object: x6)
    distinct(x7, x6)
    supersede(subject: x7, object: x6)
    keep(e3, subject: x5, object: x7)
```

## r4
From: migration-tools#r31, reworded in request words (0.38.0).

```reading
While a ledger entry that has a qualifier supersedes another ledger entry, when the person relocates a bounded context, the upgrades service shall keep a design-decision that holds the qualifier.
shall [x4: agent the person (constant), x6: service the upgrades service (constant)]
  while [x1: ledger entry, x2: qualifier, x3: ledger entry]
    of(x2, x1)
    distinct(x3, x1)
    supersede(subject: x1, object: x3)
  when [x5: bounded context]
    request(e1, upgrades.relocate, subject: x4, object: x5)
  response [x7: design-decision]
    in(x2, x7)
    keep(e2, subject: x6, object: x7)
```

## r5
From: migration-tools#r32, reworded in request words (0.38.0).

```reading
While a ledger entry of a decision ledger has no ledger number, when the person relocates a bounded context, the upgrades service shall keep a ledger number of the ledger entry.
shall [x4: agent the person (constant), x6: service the upgrades service (constant)]
  while [x1: ledger entry, x2: decision ledger]
    of(x1, x2)
    not [x3: ledger number]
      of(x3, x1)
  when [x5: bounded context]
    request(e1, upgrades.relocate, subject: x4, object: x5)
  response [x7: ledger number]
    of(x7, x1)
    keep(e2, subject: x6, object: x7)
```

## r6
From: migration-tools#r33, reworded in request words (0.38.0).

```reading
While a Behaviour line of a capability has no line id, when the person relocates a bounded context, the upgrades service shall keep a line id of the Behaviour line.
shall [x4: agent the person (constant), x6: service the upgrades service (constant)]
  while [x1: Behaviour line, x2: capability]
    of(x1, x2)
    not [x3: line id]
      of(x3, x1)
  when [x5: bounded context]
    request(e1, upgrades.relocate, subject: x4, object: x5)
  response [x7: line id]
    of(x7, x1)
    keep(e2, subject: x6, object: x7)
```

## r7
From: migration-tools#r34, reworded in request words (0.38.0).

```reading
While a ledger entry has a stem and a tracked file in an old-layout directory has the same stem, if the person relocates a bounded context, then the upgrades service shall refuse the request and name the tracked file.
shall [x5: agent the person (constant), x7: service the upgrades service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: ledger entry, x2: stem, x3: tracked file, x4: old-layout directory]
    of(x2, x1)
    in(x3, x4)
    of(x2, x3)
  if [x6: bounded context]
    request(e1, upgrades.relocate, subject: x5, object: x6)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x3)
```

## r8
From: migration-tools#r35, reworded in request words (0.38.0).

```reading
While this repository holds an uncommitted change, if the person relocates a bounded context, then the upgrades service shall refuse the request and name the uncommitted change.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x5: service the upgrades service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x2: uncommitted change]
    in(x2, x1)
  if [x4: bounded context]
    request(e1, upgrades.relocate, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r9
From: migration-tools#r36, reworded in request words (0.38.0).

```reading
While this repository holds an uncommitted change, if the person upgrades this repository, then the upgrades service shall refuse the request and name the uncommitted change.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x4: service the upgrades service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x2: uncommitted change]
    in(x2, x1)
  if
    request(e1, upgrades.upgrade, subject: x3, object: x1)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r10
From: migration-tools#r37, reworded in request words (0.38.0).

```reading
While the release of this repository is before `0.24.0`, when the person queries this repository, the upgrades service shall return the release of this repository and every upgrade step and complete the request.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    cmp(release(x1)) before `0.24.0`
  when
    request(e1, upgrades.query, subject: x2, object: x1)
  response [x4: release]
    release(x1) = x4
    return(e2, subject: x3, object: x4)
    every [x5: upgrade step]
      scope
        return(e3, subject: x3, object: x5)
    complete(e4, subject: x3, object: x6)
```

## r11
From: migration-tools#r38, reworded in request words (0.38.0).

```reading
While this repository has a shop directory and this repository has no plugin version file, when the person queries this repository, the upgrades service shall return every upgrade step.
shall [x1: repository "the repository the request is made in" (indexical), x4: agent the person (constant), x5: service the upgrades service (constant)]
  while [x2: shop directory]
    of(x2, x1)
    not [x3: plugin version file]
      of(x3, x1)
  when
    request(e1, upgrades.query, subject: x4, object: x1)
  response
    every [x6: upgrade step]
      scope
        return(e2, subject: x5, object: x6)
```

## r12
From: migration-tools#r39, reworded in request words (0.38.0).

```reading
While a plugin version file of this repository holds no version, if the person queries this repository, then the upgrades service shall refuse the request and name the content of the plugin version file.
shall [x2: repository "the repository the request is made in" (indexical), x4: agent the person (constant), x5: service the upgrades service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: plugin version file]
    of(x1, x2)
    not [x3: version]
      in(x3, x1)
  if
    request(e1, upgrades.query, subject: x4, object: x2)
  response [x7: content]
    refuse(e2, subject: x5, object: x6)
    of(x7, x1)
    name(e3, subject: x5, object: x7)
```

## r13
From: migration-tools#r59, reworded in request words (0.38.0).

```reading
While the release of this repository is before `0.24.0`, when the person upgrades this repository, the upgrades service shall return every upgrade step and change the plugin version file of this repository, every work-item file, every stage directory and every initiative log.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant)]
  while
    cmp(release(x1)) before `0.24.0`
  when
    request(e1, upgrades.upgrade, subject: x2, object: x1)
  response [x5: plugin version file]
    every [x4: upgrade step]
      scope
        return(e2, subject: x3, object: x4)
    of(x5, x1)
    change(e3, subject: x3, object: x5)
    every [x6: work-item file]
      scope
        change(e4, subject: x3, object: x6)
    every [x7: stage directory]
      scope
        change(e5, subject: x3, object: x7)
    every [x8: initiative log]
      scope
        change(e6, subject: x3, object: x8)
```

## r14
From: migration-tools#r43, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.23.1` and before `0.25.0`, when the person upgrades this repository, the upgrades service shall change every work-item file.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant)]
  while
    cmp(release(x1)) after `0.23.1`
    cmp(release(x1)) before `0.25.0`
  when
    request(e1, upgrades.upgrade, subject: x2, object: x1)
  response
    every [x4: work-item file]
      scope
        change(e2, subject: x3, object: x4)
```

## r15
From: migration-tools#r69, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.25.0` and before `0.30.0` and a capability of this repository has no language, when the person upgrades this repository, the upgrades service shall keep a restated file, change the capability and return the restated file and the capability.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x4: service the upgrades service (constant)]
  while [x2: capability]
    cmp(release(x1)) after `0.25.0`
    cmp(release(x1)) before `0.30.0`
    of(x2, x1)
    language(x2) = none
  when
    request(e1, upgrades.upgrade, subject: x3, object: x1)
  response [x5: restated file]
    keep(e2, subject: x4, object: x5)
    change(e3, subject: x4, object: x2)
    return(e4, subject: x4, object: x5)
    return(e5, subject: x4, object: x2)
```

## r16
From: migration-tools#r70, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.25.0` and before `0.30.0`, when the person upgrades this repository, the upgrades service shall change every work-item file that mentions a requirement and change every feature that holds a scenario that has the `@deprecated` tag.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant), x8: tag `@deprecated` (parameter)]
  while
    cmp(release(x1)) after `0.25.0`
    cmp(release(x1)) before `0.30.0`
  when
    request(e1, upgrades.upgrade, subject: x2, object: x1)
  response
    every [x4: work-item file, x5: requirement]
      mention(subject: x4, object: x5)
      scope
        change(e2, subject: x3, object: x4)
    every [x6: feature, x7: scenario]
      of(x8, x7)
      in(x7, x6)
      scope
        change(e3, subject: x3, object: x6)
```

## r17
From: migration-tools#r47, reworded in request words (0.38.0).

```reading
While the release of this repository is before `0.24.0`, when a session starts, the upgrades service shall notify the session of the release of this repository, every upgrade step and `only on the person's yes`.
shall [x1: repository "the repository the request is made in" (indexical), x3: service the upgrades service (constant), x6: text `only on the person's yes` (constant)]
  while
    cmp(release(x1)) before `0.24.0`
  when [x2: session]
    start(e1, subject: x2)
  response [x4: release]
    release(x1) = x4
    notify(e2, subject: x3, object: x2, of: x4)
    every [x5: upgrade step]
      scope
        notify(e3, subject: x3, object: x2, of: x5)
    notify(e4, subject: x3, object: x2, of: x6)
```

## r18
From: migration-tools#r50, reworded in request words (0.38.0).

```reading
While this repository has no shop directory, when a session starts, the upgrades service shall change nothing.
shall [x1: repository "the repository the request is made in" (indexical), x4: service the upgrades service (constant)]
  while
    not [x2: shop directory]
      of(x2, x1)
  when [x3: session]
    start(e1, subject: x3)
  response
    not [x5: thing]
      change(e2, subject: x4, object: x5)
```

## r19
From: migration-tools#r51, reworded in request words (0.38.0).

```reading
While a plugin version file of this repository holds no version, when a session starts, the upgrades service shall notify the session of `holds no version` and the content of the plugin version file.
shall [x2: repository "the repository the request is made in" (indexical), x5: service the upgrades service (constant), x6: text `holds no version` (constant)]
  while [x1: plugin version file]
    of(x1, x2)
    not [x3: version]
      in(x3, x1)
  when [x4: session]
    start(e1, subject: x4)
  response [x7: content]
    notify(e2, subject: x5, object: x4, of: x6)
    of(x7, x1)
    notify(e3, subject: x5, object: x4, of: x7)
```

## r20
From: migration-tools#r71, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.29.0` and before `0.31.0`, when the person upgrades this repository, the upgrades service shall keep a frozen notice and change the decisions index of this repository.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant)]
  while
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `0.31.0`
  when
    request(e1, upgrades.upgrade, subject: x2, object: x1)
  response [x4: frozen notice, x5: decisions index]
    keep(e2, subject: x3, object: x4)
    of(x5, x1)
    change(e3, subject: x3, object: x5)
```

## r21
From: migration-tools#r72, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.29.0` and before `0.31.0` and the asker of a frozen request is not `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person upgrades this repository, the upgrades service shall change the frozen request.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x4: service the upgrades service (constant)]
  while [x2: frozen request]
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `0.31.0`
    not
      asker(x2) = `internal`
    not
      status(x2) = `delivered`
    not
      status(x2) = `refused`
    not
      status(x2) = `withdrawn`
  when
    request(e1, upgrades.upgrade, subject: x3, object: x1)
  response
    change(e2, subject: x4, object: x2)
```

## r22
From: migration-tools#r73, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.29.0` and before `0.31.0` and an initiative of this repository is not `done` or `abandoned`, when the person upgrades this repository, the upgrades service shall return every upgrade step whose release is `0.31.0` and the initiative.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x4: service the upgrades service (constant)]
  while [x2: initiative]
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `0.31.0`
    of(x2, x1)
    not
      status(x2) = `done`
    not
      status(x2) = `abandoned`
  when
    request(e1, upgrades.upgrade, subject: x3, object: x1)
  response
    every [x5: upgrade step]
      release(x5) = `0.31.0`
      scope
        return(e2, subject: x4, object: x5)
    return(e3, subject: x4, object: x2)
```

## r23
From: migration-tools#r74, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.29.0` and before `0.31.0` and the asker of a frozen request is `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person upgrades this repository, the upgrades service shall return the frozen request.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x4: service the upgrades service (constant)]
  while [x2: frozen request]
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `0.31.0`
    asker(x2) = `internal`
    not
      status(x2) = `delivered`
    not
      status(x2) = `refused`
    not
      status(x2) = `withdrawn`
  when
    request(e1, upgrades.upgrade, subject: x3, object: x1)
  response
    return(e2, subject: x4, object: x2)
```

## r24
From: migration-tools#r75, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.30.0` and before `0.32.0`, when the person upgrades this repository, the upgrades service shall change the index file of this bounded context and return every upgrade step whose release is `0.32.0` and every term that violates `v_t11`.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant), x4: bounded context "the bounded context the request is made in" (indexical), x8: rule `v_t11` (parameter)]
  while
    cmp(release(x1)) after `0.30.0`
    cmp(release(x1)) before `0.32.0`
  when
    request(e1, upgrades.upgrade, subject: x2, object: x1)
  response [x5: index file]
    of(x5, x4)
    change(e2, subject: x3, object: x5)
    every [x6: upgrade step]
      release(x6) = `0.32.0`
      scope
        return(e3, subject: x3, object: x6)
    every [x7: term]
      violate(subject: x7, object: x8)
      scope
        return(e4, subject: x3, object: x7)
```

## r25
From: migration-tools#r76, reworded in request words (0.38.0).

```reading
While the release of this repository is after `0.32.0` and before `0.33.0`, when the person upgrades this repository, the upgrades service shall change the index file of this bounded context and every capability and return every upgrade step whose release is `0.33.0`.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant), x4: bounded context "the bounded context the request is made in" (indexical)]
  while
    cmp(release(x1)) after `0.32.0`
    cmp(release(x1)) before `0.33.0`
  when
    request(e1, upgrades.upgrade, subject: x2, object: x1)
  response [x5: index file]
    of(x5, x4)
    change(e2, subject: x3, object: x5)
    every [x6: capability]
      scope
        change(e3, subject: x3, object: x6)
    every [x7: upgrade step]
      release(x7) = `0.33.0`
      scope
        return(e4, subject: x3, object: x7)
```

## r26
From: migration-tools#r80, reworded in request words (0.38.0).

```reading
While the release of this repository is `0.33.0`, when the person upgrades this repository, the upgrades service shall return every upgrade step whose release is `0.34.0` and every term that violates `w_value_kind`.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x3: service the upgrades service (constant), x6: rule `w_value_kind` (parameter)]
  while
    release(x1) = `0.33.0`
  when
    request(e1, upgrades.upgrade, subject: x2, object: x1)
  response
    every [x4: upgrade step]
      release(x4) = `0.34.0`
      scope
        return(e2, subject: x3, object: x4)
    every [x5: term]
      violate(subject: x5, object: x6)
      scope
        return(e3, subject: x3, object: x5)
```

## r27
From: migration-tools#r81, reworded in request words (0.38.0).

```reading
While the release of this repository is the same as the release of the plugin and the release of this repository is after `0.34.0`, when the person upgrades this repository, the upgrades service shall return `no upgrade step is pending` and change no file.
shall [x1: repository "the repository the request is made in" (indexical), x2: plugin "the plugin the request is made with" (indexical), x3: agent the person (constant), x4: service the upgrades service (constant), x5: text `no upgrade step is pending` (constant)]
  while
    cmp(release(x1), same, release(x2))
    cmp(release(x1)) after `0.34.0`
  when
    request(e1, upgrades.upgrade, subject: x3, object: x1)
  response
    return(e2, subject: x4, object: x5)
    not [x6: file]
      change(e3, subject: x4, object: x6)
```

## r28
From: migration-tools#r82, reworded in request words (0.38.0).

```reading
While the release of this repository is after the release of the plugin, when a session starts, the upgrades service shall notify the session of `update the plugin`.
shall [x1: repository "the repository the request is made in" (indexical), x2: plugin "the plugin the request is made with" (indexical), x4: service the upgrades service (constant), x5: text `update the plugin` (constant)]
  while
    cmp(release(x1), after, release(x2))
  when [x3: session]
    start(e1, subject: x3)
  response
    notify(e2, subject: x4, object: x3, of: x5)
```

## r29
From: migration-tools#r83, reworded in request words (0.38.0).

```reading
While the release of this repository is the same as the release of the plugin and the release of this repository is after `0.24.0` and every initiative of this repository is one of `done` or `abandoned`, when a session starts, the upgrades service shall not notify the session of an upgrade step and not notify the session of an initiative.
shall [x1: repository "the repository the request is made in" (indexical), x2: plugin "the plugin the request is made with" (indexical), x5: service the upgrades service (constant)]
  while
    cmp(release(x1), same, release(x2))
    cmp(release(x1)) after `0.24.0`
    every [x3: initiative]
      of(x3, x1)
      scope
        or
          case
            status(x3) = `done`
          case
            status(x3) = `abandoned`
  when [x4: session]
    start(e1, subject: x4)
  response
    not [x6: upgrade step]
      notify(e2, subject: x5, object: x4, of: x6)
    not [x7: initiative]
      notify(e3, subject: x5, object: x4, of: x7)
```

## r30
From: migration-tools#r84, reworded in request words (0.38.0).

```reading
While the release of this repository is `0.34.0` and the release of the plugin is `0.34.1`, when the person upgrades this repository, the upgrades service shall return `no upgrade step is pending`, change the plugin version file of this repository and keep the plugin version file.
shall [x1: repository "the repository the request is made in" (indexical), x2: plugin "the plugin the request is made with" (indexical), x3: agent the person (constant), x4: service the upgrades service (constant), x5: text `no upgrade step is pending` (constant)]
  while
    release(x1) = `0.34.0`
    release(x2) = `0.34.1`
  when
    request(e1, upgrades.upgrade, subject: x3, object: x1)
  response [x6: plugin version file]
    return(e2, subject: x4, object: x5)
    of(x6, x1)
    change(e3, subject: x4, object: x6)
    keep(e4, subject: x4, object: x6)
```

## r32
From: b318 r32.

```reading
If the person founds this bounded context without a context id, then the upgrades service shall refuse the request and name this bounded context.
shall [x1: agent the person (constant), x2: bounded context "the bounded context the request is made in" (indexical), x3: service the upgrades service (constant), x4: request "the request the trigger makes" (indexical)]
  if
    request(e1, upgrades.found, subject: x1, object: x2)
    noparam(e1, context id)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x2)
```

## r33
From: b318 r33.

```reading
If the person founds this bounded context with a context id that does not conform to the bounded context id form, then the upgrades service shall refuse the request and name the context id.
shall [x1: agent the person (constant), x2: bounded context "the bounded context the request is made in" (indexical), x4: artifact the bounded context id form (constant), x5: service the upgrades service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x3: context id]
    not
      conforms(x3, x4)
    request(e1, upgrades.found, subject: x1, object: x2)
    param(e1, context id, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r34
From: b318 r34.

```reading
While this bounded context has an index file, if the person founds this bounded context with a context id, then the upgrades service shall refuse the request, name the index file and change no file.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x3: agent the person (constant), x5: service the upgrades service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x2: index file]
    of(x2, x1)
  if [x4: context id]
    request(e1, upgrades.found, subject: x3, object: x1)
    param(e1, context id, x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
    not [x7: file]
      change(e4, subject: x5, object: x7)
```

## r35
From: b318 r35.

```reading
While this repository has a shop directory, if the person founds this bounded context with a context id, then the upgrades service shall refuse the request, name the shop directory and change no file.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x4: bounded context "the bounded context the request is made in" (indexical), x6: service the upgrades service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x2: shop directory]
    of(x2, x1)
  if [x5: context id]
    request(e1, upgrades.found, subject: x3, object: x4)
    param(e1, context id, x5)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
    not [x8: file]
      change(e4, subject: x6, object: x8)
```

## r36
From: b423 r36.

```reading
While the release of this repository is before the release of the plugin and the scenario conftest of this repository conforms to the old scenario conftest form, when the person upgrades this repository, the upgrades service shall change the scenario conftest of this repository and keep the scenario conftest.
shall [x1: repository "the repository the request is made in" (indexical), x2: plugin "the plugin the request is made with" (indexical), x4: artifact the old scenario conftest form (constant), x5: agent the person (constant), x6: service the upgrades service (constant)]
  while [x3: scenario conftest]
    cmp(release(x1), before, release(x2))
    of(x3, x1)
    conforms(x3, x4)
  when
    request(e1, upgrades.upgrade, subject: x5, object: x1)
  response
    change(e2, subject: x6, object: x3)
    keep(e3, subject: x6, object: x3)
```

## r37
From: b423 r37.

```reading
While the release of this repository is before the release of the plugin and the scenario conftest of this repository does not conform to the old scenario conftest form and the scenario conftest of this repository does not conform to the scenario conftest form, when the person upgrades this repository, the upgrades service shall return the scenario conftest and not change the scenario conftest.
shall [x1: repository "the repository the request is made in" (indexical), x2: plugin "the plugin the request is made with" (indexical), x4: artifact the old scenario conftest form (constant), x5: artifact the scenario conftest form (constant), x6: agent the person (constant), x7: service the upgrades service (constant)]
  while [x3: scenario conftest]
    cmp(release(x1), before, release(x2))
    of(x3, x1)
    not
      conforms(x3, x4)
    not
      conforms(x3, x5)
  when
    request(e1, upgrades.upgrade, subject: x6, object: x1)
  response
    return(e2, subject: x7, object: x3)
    not
      change(e3, subject: x7, object: x3)
```

## r41
From: b464 r41.

```reading
While this bounded context has no index file and this repository has no shop directory, when the person founds this bounded context with a context id and a context purpose, the upgrades service shall keep an index file that has the context purpose and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x3: repository "the repository the request is made in" (indexical), x5: agent the person (constant), x8: service the upgrades service (constant), x10: request "the request the trigger makes" (indexical)]
  while
    not [x2: index file]
      of(x2, x1)
    not [x4: shop directory]
      of(x4, x3)
  when [x6: context id, x7: context purpose]
    request(e1, upgrades.found, subject: x5, object: x1)
    param(e1, context id, x6)
    param(e1, context purpose, x7)
  response [x9: index file]
    of(x7, x9)
    keep(e2, subject: x8, object: x9)
    complete(e3, subject: x8, object: x10)
```

## r42
Retires: r39. From: b487 r42.

```reading
While this bounded context has no index file and this repository has no shop directory and the ignore file of this repository does not conform to the ignore file form, when the person founds this bounded context with a context id, the upgrades service shall change the ignore file of this repository, keep the context scaffold and the ignore file of this repository and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x3: repository "the repository the request is made in" (indexical), x6: artifact the ignore file form (constant), x7: agent the person (constant), x9: service the upgrades service (constant), x11: request "the request the trigger makes" (indexical)]
  while [x5: ignore file]
    not [x2: index file]
      of(x2, x1)
    not [x4: shop directory]
      of(x4, x3)
    of(x5, x3)
    not
      conforms(x5, x6)
  when [x8: context id]
    request(e1, upgrades.found, subject: x7, object: x1)
    param(e1, context id, x8)
  response [x10: context scaffold]
    change(e2, subject: x9, object: x5)
    of(x10, x3)
    keep(e3, subject: x9, object: x10)
    keep(e4, subject: x9, object: x5)
    complete(e5, subject: x9, object: x11)
```

## r43
Retires: r40. From: b487 r43.

```reading
While this bounded context has no index file and this repository has no shop directory and the ignore file of this repository conforms to the ignore file form, when the person founds this bounded context with a context id, the upgrades service shall keep the context scaffold, not change the ignore file and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x3: repository "the repository the request is made in" (indexical), x6: artifact the ignore file form (constant), x7: agent the person (constant), x9: service the upgrades service (constant), x11: request "the request the trigger makes" (indexical)]
  while [x5: ignore file]
    not [x2: index file]
      of(x2, x1)
    not [x4: shop directory]
      of(x4, x3)
    of(x5, x3)
    conforms(x5, x6)
  when [x8: context id]
    request(e1, upgrades.found, subject: x7, object: x1)
    param(e1, context id, x8)
  response [x10: context scaffold]
    of(x10, x3)
    keep(e2, subject: x9, object: x10)
    not
      change(e3, subject: x9, object: x5)
    complete(e4, subject: x9, object: x11)
```

## r44
From: b632 r44.

```reading
While the release of this repository is before the release of the plugin and an instructions file of this repository holds an old command line, when the person upgrades this repository, the upgrades service shall change the old command line and keep the instructions file.
shall [x1: repository "the repository the request is made in" (indexical), x2: plugin "the plugin the request is made with" (indexical), x5: agent the person (constant), x6: service the upgrades service (constant)]
  while [x3: instructions file, x4: old command line]
    cmp(release(x1), before, release(x2))
    of(x3, x1)
    in(x4, x3)
  when
    request(e1, upgrades.upgrade, subject: x5, object: x1)
  response
    change(e2, subject: x6, object: x4)
    keep(e3, subject: x6, object: x3)
```

## r45
From: b609 r45.

```reading
While this bounded context has no index file and this repository has no shop directory, when the person founds this bounded context with a context id, the upgrades service shall keep a bounded context that imports the `base` pack and complete the request.
shall [x1: bounded context "the bounded context the request is made in" (indexical), x3: repository "the repository the request is made in" (indexical), x5: agent the person (constant), x7: service the upgrades service (constant), x9: pack `base` (parameter), x10: request "the request the trigger makes" (indexical)]
  while
    not [x2: index file]
      of(x2, x1)
    not [x4: shop directory]
      of(x4, x3)
  when [x6: context id]
    request(e1, upgrades.found, subject: x5, object: x1)
    param(e1, context id, x6)
  response [x8: bounded context]
    import#2(subject: x8, object: x9)
    keep(e2, subject: x7, object: x8)
    complete(e3, subject: x7, object: x10)
```
