# migration-tools: every live line with its intended reading (b240)

## r27
Retires: r1. From: b156 r26. Audit: fine.

```reading
While this repository holds an old-layout directory, when the person runs `migrate run` on a bounded context, `migrate` shall relocate every old-layout directory and rewrite every file that mentions an old-layout directory.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the person (constant), x4: command `migrate run` (parameter), x6: tool `migrate` (constant)]
  while [x2: old-layout directory]
    in(x2, x1)
  when [x5: bounded context]
    run(e1, subject: x3, object: x4, on: x5)
  response
    every [x7: old-layout directory]
      scope
        relocate(e2, subject: x6, object: x7)
    every [x8: file, x9: old-layout directory]
      mention(subject: x8, object: x9)
      scope
        rewrite(e3, subject: x6, object: x8)
```

## r28
Retires: r2. From: b156 r27. Audit: fine.

```reading
While a decision ledger of this repository has a ledger entry, when the person runs `migrate run` on a bounded context, `migrate` shall write a design-decision of the ledger entry, remove the decision ledger, rewrite the decisions index of this repository and exit successfully.
shall [x2: repository "the repository the command runs in" (indexical), x4: agent the person (constant), x5: command `migrate run` (parameter), x7: tool `migrate` (constant)]
  while [x1: decision ledger, x3: ledger entry]
    of(x1, x2)
    of(x3, x1)
  when [x6: bounded context]
    run(e1, subject: x4, object: x5, on: x6)
  response [x8: design-decision, x9: decisions index]
    of(x8, x3)
    write(e2, subject: x7, object: x8)
    remove(e3, subject: x7, object: x1)
    of(x9, x2)
    rewrite(e4, subject: x7, object: x9)
    exit(e5, subject: x7, successfully)
```

## r58
Retires: r29, r30 (r3). From: b240 r179, v15n (r29 and r30 shared their condition and trigger). Audit: fine; the design-decision that supersedes is "another design-decision", the one it supersedes "the design-decision" (construct `another`).

```reading
While a ledger entry supersedes another ledger entry, when the person runs `migrate run` on a bounded context, `migrate` shall write a design-decision of the ledger entry whose status is `superseded` and write another design-decision that supersedes the design-decision.
shall [x3: agent the person (constant), x4: command `migrate run` (parameter), x6: tool `migrate` (constant)]
  while [x1: ledger entry, x2: ledger entry]
    distinct(x2, x1)
    supersede#2(subject: x1, object: x2)
  when [x5: bounded context]
    run(e1, subject: x3, object: x4, on: x5)
  response [x7: design-decision, x8: design-decision]
    of(x7, x2)
    status(x7) = `superseded`
    write(e2, subject: x6, object: x7)
    distinct(x8, x7)
    supersede(subject: x8, object: x7)
    write(e3, subject: x6, object: x8)
```

## r31
Retires: r4. From: b156 r30. Audit: unsayable, said as what the design-decision holds: the qualifier (it goes to its `by`, its supersedes keeping the id alone).

```reading
While a ledger entry that has a qualifier supersedes another ledger entry, when the person runs `migrate run` on a bounded context, `migrate` shall write a design-decision that holds the qualifier.
shall [x4: agent the person (constant), x5: command `migrate run` (parameter), x7: tool `migrate` (constant)]
  while [x1: ledger entry, x2: qualifier, x3: ledger entry]
    of(x2, x1)
    distinct(x3, x1)
    supersede#2(subject: x1, object: x3)
  when [x6: bounded context]
    run(e1, subject: x4, object: x5, on: x6)
  response [x8: design-decision]
    in(x2, x8)
    write(e2, subject: x7, object: x8)
```

## r32
Retires: r5. From: b156 r31. Audit: coined ("next number"), the noun dropped. Known limit: #3 (one above the highest).

```reading
While a ledger entry of a decision ledger has no ledger number, when the person runs `migrate run` on a bounded context, `migrate` shall give a ledger number to the ledger entry.
shall [x4: agent the person (constant), x5: command `migrate run` (parameter), x7: tool `migrate` (constant)]
  while [x1: ledger entry, x2: decision ledger]
    of(x1, x2)
    not [x3: ledger number]
      of(x3, x1)
  when [x6: bounded context]
    run(e1, subject: x4, object: x5, on: x6)
  response [x8: ledger number]
    give(e2, subject: x7, object: x8, to: x1)
```

## r33
Retires: r6. From: b156 r32. Audit: coined ("next id"), the noun dropped. Known limit: #3 (one above the highest).

```reading
While a Behaviour line of a capability has no line id, when the person runs `migrate run` on a bounded context, `migrate` shall give a line id to the Behaviour line.
shall [x4: agent the person (constant), x5: command `migrate run` (parameter), x7: tool `migrate` (constant)]
  while [x1: Behaviour line, x2: capability]
    of(x1, x2)
    not [x3: line id]
      of(x3, x1)
  when [x6: bounded context]
    run(e1, subject: x4, object: x5, on: x6)
  response [x8: line id]
    give(e2, subject: x7, object: x8, to: x1)
```

## r34
Retires: r7. From: b156 r33. Audit: coined ("destination", what `migrate run` would write), said as the stem a ledger entry and a tracked file share (construct `same`).

```reading
While a ledger entry has a stem and a tracked file in an old-layout directory has the same stem, if the person runs `migrate run` on a bounded context, then `migrate` shall refuse the command and name the tracked file.
shall [x5: agent the person (constant), x6: command `migrate run` (parameter), x8: tool `migrate` (constant)]
  while [x1: ledger entry, x2: stem, x3: tracked file, x4: old-layout directory]
    of(x2, x1)
    in(x3, x4)
    of(x2, x3)
  if [x7: bounded context]
    run(e1, subject: x5, object: x6, on: x7)
  response
    refuse(e2, subject: x8, object: x6)
    name(e3, subject: x8, object: x3)
```

## r35
Retires: r8. From: b156 r34. Audit: distortion, fixed by section 5 ("an uncommitted change", not a widened "untracked file").

```reading
While this repository holds an uncommitted change, if the person runs `migrate run` on a bounded context, then `migrate` shall refuse the command and name the uncommitted change.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the person (constant), x4: command `migrate run` (parameter), x6: tool `migrate` (constant)]
  while [x2: uncommitted change]
    in(x2, x1)
  if [x5: bounded context]
    run(e1, subject: x3, object: x4, on: x5)
  response
    refuse(e2, subject: x6, object: x4)
    name(e3, subject: x6, object: x2)
```

## r36
Retires: r9. From: b156 r35. Audit: distortion, fixed by section 5 ("an uncommitted change").

```reading
While this repository holds an uncommitted change, if the person runs `migrate upgrade`, then `migrate` shall refuse the command and name the uncommitted change.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the person (constant), x4: command `migrate upgrade` (parameter), x5: tool `migrate` (constant)]
  while [x2: uncommitted change]
    in(x2, x1)
  if
    run(e1, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x2)
```

## r37
Retires: r10. From: b156 r36. Audit: distortion, fixed by ordered comparison (construct `ordered`: "before `0.24.0`", not lack); every upgrade step is pending before 0.24.0.

```reading
While the release of this repository is before `0.24.0`, when the person runs `migrate status`, `migrate` shall print the release of this repository and every upgrade step and exit successfully.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the person (constant), x3: command `migrate status` (parameter), x4: tool `migrate` (constant)]
  while
    cmp(release(x1)) before `0.24.0`
  when
    run(e1, subject: x2, object: x3)
  response [x5: release]
    release(x1) = x5
    print(e2, subject: x4, object: x5)
    every [x6: upgrade step]
      scope
        print(e3, subject: x4, object: x6)
    exit(e4, subject: x4, successfully)
```

## r38
Retires: r11. From: b156 r37. Audit: distortion (a default as a proper noun), said as what the default prints: every upgrade step. Known limit: #17 (the default release `0.23.1`).

```reading
While this repository has a shop directory and this repository has no plugin version file, when the person runs `migrate status`, `migrate` shall print every upgrade step.
shall [x1: repository "the repository the command runs in" (indexical), x4: agent the person (constant), x5: command `migrate status` (parameter), x6: tool `migrate` (constant)]
  while [x2: shop directory]
    of(x2, x1)
    not [x3: plugin version file]
      of(x3, x1)
  when
    run(e1, subject: x4, object: x5)
  response
    every [x7: upgrade step]
      scope
        print(e2, subject: x6, object: x7)
```

## r39
Retires: r12. From: b156 r38. Audit: fine.

```reading
While a plugin version file of this repository holds no version, if the person runs `migrate status`, then `migrate` shall refuse the command and name the content of the plugin version file.
shall [x2: repository "the repository the command runs in" (indexical), x4: agent the person (constant), x5: command `migrate status` (parameter), x6: tool `migrate` (constant)]
  while [x1: plugin version file]
    of(x1, x2)
    not [x3: version]
      in(x3, x1)
  if
    run(e1, subject: x4, object: x5)
  response [x7: content]
    refuse(e2, subject: x6, object: x5)
    of(x7, x1)
    name(e3, subject: x6, object: x7)
```

## r59
Retires: r40, r41 (r13). From: b240 r179, v15n (r40 and r41 shared their condition and trigger). Audit: fine.

```reading
While the release of this repository is before `0.24.0`, when the person runs `migrate upgrade`, `migrate` shall print every upgrade step, rewrite the plugin version file of this repository, rename every work-item file and every stage directory and rewrite every initiative log.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the person (constant), x3: command `migrate upgrade` (parameter), x4: tool `migrate` (constant)]
  while
    cmp(release(x1)) before `0.24.0`
  when
    run(e1, subject: x2, object: x3)
  response [x6: plugin version file]
    every [x5: upgrade step]
      scope
        print(e2, subject: x4, object: x5)
    of(x6, x1)
    rewrite(e3, subject: x4, object: x6)
    every [x7: work-item file]
      scope
        rename(e4, subject: x4, object: x7)
    every [x8: stage directory]
      scope
        rename(e5, subject: x4, object: x8)
    every [x9: initiative log]
      scope
        rewrite(e6, subject: x4, object: x9)
```

## r42
Retires: r14. From: b156 r41. Audit: distortion, fixed by the plugin's release as a value. Known limit: #6 (a value compared with the plugin's release).

```reading
While the release of this repository is `3.0.1`, when the person runs `migrate upgrade`, `migrate` shall print `no upgrade step is pending` and change no file.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the person (constant), x3: command `migrate upgrade` (parameter), x4: tool `migrate` (constant), x5: text `no upgrade step is pending` (constant)]
  while
    release(x1) = `3.0.1`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x5)
    not [x6: file]
      change(e3, subject: x4, object: x6)
```

## r43
Retires: r15. From: b156 r42. Audit: distortion, fixed by ordered comparison (construct `ordered`: "after `0.23.1` and before `0.25.0`").

```reading
While the release of this repository is after `0.23.1` and before `0.25.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite every work-item file.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the person (constant), x3: command `migrate upgrade` (parameter), x4: tool `migrate` (constant)]
  while
    cmp(release(x1)) after `0.23.1`
    cmp(release(x1)) before `0.25.0`
  when
    run(e1, subject: x2, object: x3)
  response
    every [x5: work-item file]
      scope
        rewrite(e2, subject: x4, object: x5)
```

## r44
Retires: r16. From: b156 r43. Audit: distortion, fixed by ordered comparison and a value's absence (constructs `ordered`, `has-no-value`: "has no language", not `uncodified`).

```reading
While the release of this repository is after `0.25.0` and before `1.0.0` and a capability of this repository has no language, when the person runs `migrate upgrade`, `migrate` shall write a restated file, rewrite the capability and print the restated file and the capability.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the person (constant), x4: command `migrate upgrade` (parameter), x5: tool `migrate` (constant)]
  while [x2: capability]
    cmp(release(x1)) after `0.25.0`
    cmp(release(x1)) before `1.0.0`
    of(x2, x1)
    language(x2) = none
  when
    run(e1, subject: x3, object: x4)
  response [x6: restated file]
    write(e2, subject: x5, object: x6)
    rewrite(e3, subject: x5, object: x2)
    print(e4, subject: x5, object: x6)
    print(e5, subject: x5, object: x2)
```

## r60
Retires: r46, r57 (r16, r45). From: b240 r179, v15n (r46 and r57 shared their condition and trigger). Audit: fine; the tag said as r57 said it, "the `@deprecated` tag".

```reading
While the release of this repository is after `0.25.0` and before `1.0.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite every work-item file that mentions a requirement and rewrite every feature that holds a scenario that has the `@deprecated` tag.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the person (constant), x3: command `migrate upgrade` (parameter), x4: tool `migrate` (constant), x9: tag `@deprecated` (parameter)]
  while
    cmp(release(x1)) after `0.25.0`
    cmp(release(x1)) before `1.0.0`
  when
    run(e1, subject: x2, object: x3)
  response
    every [x5: work-item file, x6: requirement]
      mention(subject: x5, object: x6)
      scope
        rewrite(e2, subject: x4, object: x5)
    every [x7: feature, x8: scenario]
      of(x9, x8)
      in(x8, x7)
      scope
        rewrite(e3, subject: x4, object: x7)
```

## r47
Retires: r17. From: b156 r46. Audit: distortion, fixed by ordered comparison and the note a declared constant.

```reading
While the release of this repository is before `0.24.0`, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print the release of this repository, every upgrade step and `only on the person's yes`.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the SessionStart hook (constant), x3: command `migrate status --hook` (parameter), x4: tool `migrate` (constant), x7: text `only on the person's yes` (constant)]
  while
    cmp(release(x1)) before `0.24.0`
  when
    run(e1, subject: x2, object: x3)
  response [x5: release]
    release(x1) = x5
    print(e2, subject: x4, object: x5)
    every [x6: upgrade step]
      scope
        print(e3, subject: x4, object: x6)
    print(e4, subject: x4, object: x7)
```

## r48
Retires: r18. From: b156 r47. Audit: distortion, fixed by the note a declared constant. Known limit: #6 ("after `3.0.1`", the plugin's release as a value).

```reading
While the release of this repository is after `3.0.1`, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print `update the plugin`.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the SessionStart hook (constant), x3: command `migrate status --hook` (parameter), x4: tool `migrate` (constant), x5: text `update the plugin` (constant)]
  while
    cmp(release(x1)) after `3.0.1`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x5)
```

## r49
Retires: r19. From: b156 r48. Audit: distortion, fixed by section 5 ("of this repository") and a value set (construct `value-set`). Known limit: #6 (the plugin's release as a value).

```reading
While the release of this repository is `3.0.1` and every initiative of this repository is one of `done` or `abandoned`, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit successfully, print no upgrade step and print no initiative.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the SessionStart hook (constant), x4: command `migrate status --hook` (parameter), x5: tool `migrate` (constant)]
  while
    release(x1) = `3.0.1`
    every [x2: initiative]
      of(x2, x1)
      scope
        or
          case
            status(x2) = `done`
          case
            status(x2) = `abandoned`
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
    not [x6: upgrade step]
      print(e3, subject: x5, object: x6)
    not [x7: initiative]
      print(e4, subject: x5, object: x7)
```

## r50
Retires: r20. From: b156 r49. Audit: distortion (only "exit successfully", as the old line said).

```reading
While this repository has no shop directory, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit successfully.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the SessionStart hook (constant), x4: command `migrate status --hook` (parameter), x5: tool `migrate` (constant)]
  while
    not [x2: shop directory]
      of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
```

## r51
Retires: r21. From: b156 r50. Audit: distortion, fixed by the note a declared constant.

```reading
While a plugin version file of this repository holds no version, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print `holds no version` and the content of the plugin version file.
shall [x2: repository "the repository the command runs in" (indexical), x4: agent the SessionStart hook (constant), x5: command `migrate status --hook` (parameter), x6: tool `migrate` (constant), x7: text `holds no version` (constant)]
  while [x1: plugin version file]
    of(x1, x2)
    not [x3: version]
      in(x3, x1)
  when
    run(e1, subject: x4, object: x5)
  response [x8: content]
    print(e2, subject: x6, object: x7)
    of(x8, x1)
    print(e3, subject: x6, object: x8)
```

## r52
Retires: r24. From: b156 r51. Audit: distortion, fixed by ordered comparison (construct `ordered`).

```reading
While the release of this repository is after `0.29.0` and before `2.0.0`, when the person runs `migrate upgrade`, `migrate` shall write a frozen notice and rewrite the decisions index of this repository.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the person (constant), x3: command `migrate upgrade` (parameter), x4: tool `migrate` (constant)]
  while
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `2.0.0`
  when
    run(e1, subject: x2, object: x3)
  response [x5: frozen notice, x6: decisions index]
    write(e2, subject: x4, object: x5)
    of(x6, x1)
    rewrite(e3, subject: x4, object: x6)
```

## r53
Retires: r24. From: b156 r52. Audit: distortion, fixed by section 5 (the asker said of the frozen request, not a glossed "peer request") and a value set (construct `value-set`).

```reading
While the release of this repository is after `0.29.0` and before `2.0.0` and the asker of a frozen request is not `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person runs `migrate upgrade`, `migrate` shall relocate the frozen request.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the person (constant), x4: command `migrate upgrade` (parameter), x5: tool `migrate` (constant)]
  while [x2: frozen request]
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `2.0.0`
    not
      asker(x2) = `internal`
    not
      status(x2) = `delivered`
    not
      status(x2) = `refused`
    not
      status(x2) = `withdrawn`
  when
    run(e1, subject: x3, object: x4)
  response
    relocate(e2, subject: x5, object: x2)
```

## r54
Retires: r24. From: b156 r53. Audit: distortion, fixed by section 5 ("of this repository"), a value set and the step named by its release.

```reading
While the release of this repository is after `0.29.0` and before `2.0.0` and an initiative of this repository is not `done` or `abandoned`, when the person runs `migrate upgrade`, `migrate` shall print every upgrade step whose release is `2.0.0` and the initiative.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the person (constant), x4: command `migrate upgrade` (parameter), x5: tool `migrate` (constant)]
  while [x2: initiative]
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `2.0.0`
    of(x2, x1)
    not
      status(x2) = `done`
    not
      status(x2) = `abandoned`
  when
    run(e1, subject: x3, object: x4)
  response
    every [x6: upgrade step]
      release(x6) = `2.0.0`
      scope
        print(e2, subject: x5, object: x6)
    print(e3, subject: x5, object: x2)
```

## r55
Retires: r24. From: b156 r54. Audit: distortion, fixed by a value set (construct `value-set`), the asker said of the frozen request.

```reading
While the release of this repository is after `0.29.0` and before `2.0.0` and the asker of a frozen request is `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person runs `migrate upgrade`, `migrate` shall print the frozen request.
shall [x1: repository "the repository the command runs in" (indexical), x3: agent the person (constant), x4: command `migrate upgrade` (parameter), x5: tool `migrate` (constant)]
  while [x2: frozen request]
    cmp(release(x1)) after `0.29.0`
    cmp(release(x1)) before `2.0.0`
    asker(x2) = `internal`
    not
      status(x2) = `delivered`
    not
      status(x2) = `refused`
    not
      status(x2) = `withdrawn`
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x2)
```

## r56
Retires: r25. From: b156 r55. Audit: distortion, fixed by ordered comparison ("after `1.0.0` and before `3.0.0`", not "lacks ... and does not lack") and the rule named by its code (violates `v_t11`).

```reading
While the release of this repository is after `1.0.0` and before `3.0.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite the index file of this bounded context and print every upgrade step whose release is `3.0.0` and every term that violates `v_t11`.
shall [x1: repository "the repository the command runs in" (indexical), x2: agent the person (constant), x3: command `migrate upgrade` (parameter), x4: tool `migrate` (constant), x5: bounded context "the bounded context whose repository the command runs in" (indexical), x9: rule `v_t11` (parameter)]
  while
    cmp(release(x1)) after `1.0.0`
    cmp(release(x1)) before `3.0.0`
  when
    run(e1, subject: x2, object: x3)
  response [x6: index file]
    of(x6, x5)
    rewrite(e2, subject: x4, object: x6)
    every [x7: upgrade step]
      release(x7) = `3.0.0`
      scope
        print(e3, subject: x4, object: x7)
    every [x8: term]
      violate(subject: x8, object: x9)
      scope
        print(e4, subject: x4, object: x8)
```
