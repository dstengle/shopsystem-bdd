# readiness: every live line with its intended reading (b240)

## r23
Retires: r1. From: b157 r32. Audit: fine.

```reading
While an item is `shaped` and the item passes the readiness bar, when the person runs `work ready` on the item, `work` shall set the status of the item to `ready`.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x4: command `work ready` (parameter), x5: tool `work` (constant)]
  while [x1: item]
    status(x1) = `shaped`
    pass#2(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4, on: x1)
  response
    initiates(e2, subject: x5, status(x1) = `ready`)
```

## r24
Retires: r2. From: b157 r33. Audit: distortion, fixed by section 5 ("does not meet": every bar check of the readiness bar that the item does not meet, in place of the verb fail).

```reading
While an item is `shaped` and the item does not pass the readiness bar, if the person runs `work ready` on the item, then `work` shall refuse the command and name every bar check of the readiness bar that the item does not meet.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x4: command `work ready` (parameter), x5: tool `work` (constant)]
  while [x1: item]
    status(x1) = `shaped`
    not
      pass#2(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4, on: x1)
  response
    refuse(e2, subject: x5, object: x4)
    every [x6: bar check]
      of(x6, x2)
      not
        meet(subject: x1, object: x6)
      scope
        name(e3, subject: x5, object: x6)
```

## r25
Retires: r3. From: b157 r34. Audit: fine.

```reading
While an item is not `shaped`, if the person runs `work ready` on the item, then `work` shall refuse the command and name the status of the item.
shall [x2: agent the person (constant), x3: command `work ready` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    not
      status(x1) = `shaped`
  if
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: status]
    refuse(e2, subject: x4, object: x3)
    status(x1) = x5
    name(e3, subject: x4, object: x5)
```

## r4
Kept.

```reading
When the person runs `work ready` on an item, `work` shall not ask a question.
shall [x1: agent the person (constant), x2: command `work ready` (parameter), x4: tool `work` (constant)]
  when [x3: item]
    run(e1, subject: x1, object: x2, on: x3)
  response
    not [x5: question]
      ask(e2, subject: x4, object: x5)
```

## r26
Retires: r5. From: b157 r20. Audit: fine; the option in the trigger with its argument (phase 11), the relation row it is set to the one written.

```reading
When the person runs `work line` with the `--relation` option set to a relation row on an item, `work` shall write the relation row in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--relation` (parameter), x6: tool `work` (constant)]
  when [x4: relation row, x5: item]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    in(x4, x5)
    write(e2, subject: x6, object: x4)
    commit(e3, subject: x6, object: x5)
```

## r27
Retires: r6. From: b157 r21. Audit: coined, fixed by conformance (phase 4): "does not conform to the relation-row form", an artifact, in place of "match" and the adjective malformed.

```reading
If the person runs `work line` with the `--relation` option set to a relation row that does not conform to the relation-row form, then `work` shall refuse the command and name the relation row.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--relation` (parameter), x5: artifact the relation-row form (constant), x6: tool `work` (constant)]
  if [x4: relation row]
    not
      conforms(x4, x5)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r28
Retires: r7. From: b157 r22. Audit: fine; the option in the trigger with its argument (phase 11).

```reading
When the person runs `work line` with the `--universal` option set to a universal condition on an item, `work` shall write the universal condition in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--universal` (parameter), x6: tool `work` (constant)]
  when [x4: universal condition, x5: item]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    in(x4, x5)
    write(e2, subject: x6, object: x4)
    commit(e3, subject: x6, object: x5)
```

## r29
Retires: r8. From: b157 r23. Audit: fine; the option in the trigger with its argument (phase 11).

```reading
When the person runs `work line` with the `--upstream` option set to an upstream entry on an item, `work` shall write the upstream entry in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--upstream` (parameter), x6: tool `work` (constant)]
  when [x4: upstream entry, x5: item]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    in(x4, x5)
    write(e2, subject: x6, object: x4)
    commit(e3, subject: x6, object: x5)
```

## r30
Retires: r9. From: b157 r24. Audit: distortion, fixed by conformance (phase 4): the upstream-entry form an artifact, "does not conform to" in place of "match".

```reading
If the person runs `work line` with the `--upstream` option set to an upstream entry that does not conform to the upstream-entry form, then `work` shall refuse the command and name the upstream entry.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--upstream` (parameter), x5: artifact the upstream-entry form (constant), x6: tool `work` (constant)]
  if [x4: upstream entry]
    not
      conforms(x4, x5)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r31
Retires: r10. From: b157 r25. Audit: fine; the option in the trigger with its argument (phase 11).

```reading
When the person runs `work line` with the `--given` option set to a given block on an item, `work` shall write the given block in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--given` (parameter), x6: tool `work` (constant)]
  when [x4: given block, x5: item]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    in(x4, x5)
    write(e2, subject: x6, object: x4)
    commit(e3, subject: x6, object: x5)
```

## r32
Retires: r11. From: b157 r26. Audit: distortion, fixed by conformance (phase 4): the example-data form an artifact whose entry says the form, not the reader that reads it.

```reading
If the person runs `work line` with the `--given` option set to a given block that does not conform to the example-data form, then `work` shall refuse the command and name the given block.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--given` (parameter), x5: artifact the example-data form (constant), x6: tool `work` (constant)]
  if [x4: given block]
    not
      conforms(x4, x5)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r34
Retires: r13. From: b157 r28. Audit: fine; the option in the trigger (phase 11).

```reading
When the person runs `work line` with the `--retires` option on an item, `work` shall write a requirement in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--retires` (parameter), x5: tool `work` (constant)]
  when [x4: item]
    run(e1, subject: x1, object: x2, with: x3, on: x4)
  response [x6: requirement]
    in(x6, x4)
    write(e2, subject: x5, object: x6)
    commit(e3, subject: x5, object: x4)
```

## r35
Retires: r14. From: b157 r29. Audit: distortion, fixed by section 5: the id related to a requirement ("a requirement id that no requirement has"), so a retired id, which no requirement has, is refused.

```reading
If the person runs `work line` with the `--retires` option set to a requirement id that no requirement has, then `work` shall refuse the command and name the requirement id.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--retires` (parameter), x6: tool `work` (constant)]
  if [x4: requirement id]
    not [x5: requirement]
      of(x4, x5)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r36
Retires: r15. From: b157 r30. Audit: coined, fixed by the spec pack (phase 12.5): "a term in the item violates a rule", in place of the lexicon problem compared with the lexicon without the item.

```reading
While an item is `shaped` and a term in the item violates a rule, if the person runs `work ready` on the item, then `work` shall refuse the command and name the term and the rule.
shall [x4: agent the person (constant), x5: command `work ready` (parameter), x6: tool `work` (constant)]
  while [x1: item, x2: term, x3: rule]
    status(x1) = `shaped`
    in(x2, x1)
    violate(subject: x2, object: x3)
  if
    run(e1, subject: x4, object: x5, on: x1)
  response
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x2)
    name(e4, subject: x6, object: x3)
```

## r37
Retires: r16. From: b157 r31. Audit: distortion, fixed by section 5: the attribute language of capability with its values `codified-1` and `codified-2`, in place of the noun "codified-2 marker".

```reading
When the person runs `work line` with the `--recodify` option set to a capability on an item, `work` shall set the language of the capability in the item to `codified-2` and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--recodify` (parameter), x6: tool `work` (constant)]
  when [x4: capability, x5: item]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    in(x4, x5)
    initiates(e2, subject: x6, language(x4) = `codified-2`)
    commit(e3, subject: x6, object: x5)
```

## r38
Retires: r17. From: b157 r35. Audit: distortion, fixed by section 5: the attribute language, set on the capability `universal` (`spec/universal.md`), in place of the noun "codified-2 marker".

```reading
When the person runs `work line` with the `--recodify` option set to `universal` on an item, `work` shall set the language of the capability in the item to `codified-2` and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--recodify` (parameter), x4: capability `universal` (constant), x6: tool `work` (constant)]
  when [x5: item]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    in(x4, x5)
    initiates(e2, subject: x6, language(x4) = `codified-2`)
    commit(e3, subject: x6, object: x5)
```

## r39
Retires: r18. From: b157 r36. Audit: fine; the two options in the trigger (phase 11).

```reading
When the person runs `work line` with the `--universal` and `--retires` options on an item, `work` shall write a universal condition in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--universal` (parameter), x4: option `--retires` (parameter), x6: tool `work` (constant)]
  when [x5: item]
    run(e1, subject: x1, object: x2, with: x3, with: x4, on: x5)
  response [x7: universal condition]
    in(x7, x5)
    write(e2, subject: x6, object: x7)
    commit(e3, subject: x6, object: x5)
```

## r40
Retires: r19. From: b157 r37. Audit: distortion, fixed by section 5: the id related to a universal condition ("a universal condition id that no universal condition has"), so a retired id is refused.

```reading
If the person runs `work line` with the `--universal` option and the `--retires` option set to a universal condition id that no universal condition has, then `work` shall refuse the command and name the universal condition id.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--universal` (parameter), x4: option `--retires` (parameter), x7: tool `work` (constant)]
  if [x5: universal condition id]
    not [x6: universal condition]
      of(x5, x6)
    argument(x4, x5)
    run(e1, subject: x1, object: x2, with: x3, with: x4)
  response
    refuse(e2, subject: x7, object: x2)
    name(e3, subject: x7, object: x5)
```

## r41
From: b307 r41. A requirement of the item that `model logic` reads no translation of refuses the bar, named by its id.

```reading
While an item is `shaped` and a requirement in the item has no translation, if the person runs `work ready` on the item, then `work` shall refuse the command and name the requirement.
shall [x4: agent the person (constant), x5: command `work ready` (parameter), x6: tool `work` (constant)]
  while [x1: item, x2: requirement]
    status(x1) = `shaped`
    in(x2, x1)
    not [x3: translation]
      of(x3, x2)
  if
    run(e1, subject: x4, object: x5, on: x1)
  response
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x2)
```

## r42
From: b14 r42. An item's own line given a new text under its id: the old text removed, the new one written in the item, the item committed.

```reading
When the person runs `work line` with the `--reword` option set to the requirement id of a requirement in an item on the item, `work` shall remove the requirement, write a requirement in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--reword` (parameter), x7: tool `work` (constant)]
  when [x4: requirement, x5: item, x6: requirement id]
    in(x4, x5)
    of(x6, x4)
    argument(x3, x6)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response [x8: requirement]
    remove(e2, subject: x7, object: x4)
    in(x8, x5)
    write(e3, subject: x7, object: x8)
    commit(e4, subject: x7, object: x5)
```

## r44
From: b14 r44. A live requirement of a capability is no line of an item: `--reword` refuses it, named by its id.

```reading
If the person runs `work line` with the `--reword` option set to the requirement id of a requirement of a capability on an item, then `work` shall refuse the command and name the requirement id.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--reword` (parameter), x8: tool `work` (constant)]
  if [x4: requirement, x5: capability, x6: requirement id, x7: item]
    of(x4, x5)
    of(x6, x4)
    argument(x3, x6)
    run(e1, subject: x1, object: x2, with: x3, on: x7)
  response
    refuse(e2, subject: x8, object: x2)
    name(e3, subject: x8, object: x6)
```

## r45
From: b14 r45. A live requirement of a capability is no line of an item: `--remove` refuses it, named by its id.

```reading
If the person runs `work line` with the `--remove` option set to the requirement id of a requirement of a capability on an item, then `work` shall refuse the command and name the requirement id.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--remove` (parameter), x8: tool `work` (constant)]
  if [x4: requirement, x5: capability, x6: requirement id, x7: item]
    of(x4, x5)
    of(x6, x4)
    argument(x3, x6)
    run(e1, subject: x1, object: x2, with: x3, on: x7)
  response
    refuse(e2, subject: x8, object: x2)
    name(e3, subject: x8, object: x6)
```

## r46
From: b203 r42. A universal condition of the item that `model logic` reads no translation of refuses the bar when spec/universal.md does not exist, named by its id.

```reading
While `universal` does not exist and an item is `shaped` and a universal condition in the item has no translation, if the person runs `work ready` on the item, then `work` shall refuse the command and name the universal condition.
shall [x1: capability `universal` (constant), x5: agent the person (constant), x6: command `work ready` (parameter), x7: tool `work` (constant)]
  while [x2: item, x3: universal condition]
    not
      exists(x1)
    status(x2) = `shaped`
    in(x3, x2)
    not [x4: translation]
      of(x4, x3)
  if
    run(e1, subject: x5, object: x6, on: x2)
  response
    refuse(e2, subject: x7, object: x6)
    name(e3, subject: x7, object: x3)
```

## r47
From: b271 r42. A live requirement retired with no line replacing it: its id written in the item, no requirement written.

```reading
When the person runs `work line` with the `--no-line` option and the `--retires` option set to a requirement id on an item, `work` shall write the requirement id in the item, not write a requirement in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--no-line` (parameter), x4: option `--retires` (parameter), x7: tool `work` (constant)]
  when [x5: requirement id, x6: item]
    argument(x4, x5)
    run(e1, subject: x1, object: x2, with: x3, with: x4, on: x6)
  response
    in(x5, x6)
    write(e2, subject: x7, object: x5)
    not [x8: requirement]
      in(x8, x6)
      write(e3, subject: x7, object: x8)
    commit(e4, subject: x7, object: x6)
```

## r48
From: b271 r43. As r35, with `--no-line`: an id no requirement has is refused, named.

```reading
If the person runs `work line` with the `--no-line` option and the `--retires` option set to a requirement id that no requirement has, then `work` shall refuse the command and name the requirement id.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--no-line` (parameter), x4: option `--retires` (parameter), x7: tool `work` (constant)]
  if [x5: requirement id]
    not [x6: requirement]
      of(x5, x6)
    argument(x4, x5)
    run(e1, subject: x1, object: x2, with: x3, with: x4)
  response
    refuse(e2, subject: x7, object: x2)
    name(e3, subject: x7, object: x5)
```

## r50
From: b305 r47. The bar runs every stage after the lexicon whatever the parse found: one run names each line of the item that does not parse and each that has no translation.

```reading
While an item is `shaped` and a requirement in the item has no parse and a different requirement in the item has no translation, if the person runs `work ready` on the item, then `work` shall refuse the command and name every requirement in the item that has no parse and every requirement in the item that has no translation.
shall [x6: agent the person (constant), x7: command `work ready` (parameter), x8: tool `work` (constant)]
  while [x1: item, x2: requirement, x4: requirement]
    status(x1) = `shaped`
    in(x2, x1)
    not [x3: parse]
      of(x3, x2)
    distinct(x4, x2)
    in(x4, x1)
    not [x5: translation]
      of(x5, x4)
  if
    run(e1, subject: x6, object: x7, on: x1)
  response
    refuse(e2, subject: x8, object: x7)
    every [x9: requirement]
      in(x9, x1)
      not [x10: parse]
        of(x10, x9)
      scope
        name(e3, subject: x8, object: x9)
    every [x11: requirement]
      in(x11, x1)
      not [x12: translation]
        of(x12, x11)
      scope
        name(e4, subject: x8, object: x11)
```

## r51
From: b316 r42. Not in the audit (b316 is no reword item).

```reading
When the person runs `work chore` with the `--file` and `--check` options on an item, `work` shall write a chore in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work chore` (parameter), x3: option `--file` (parameter), x4: option `--check` (parameter), x6: tool `work` (constant)]
  when [x5: item]
    run(e1, subject: x1, object: x2, with: x3, with: x4, on: x5)
  response [x7: chore]
    in(x7, x5)
    write(e2, subject: x6, object: x7)
    commit(e3, subject: x6, object: x5)
```

## r52
From: b316 r43. Not in the audit (b316 is no reword item).

```reading
If the person runs `work chore` on an item that holds a requirement, then `work` shall refuse the command and name the requirement.
shall [x1: agent the person (constant), x2: command `work chore` (parameter), x5: tool `work` (constant)]
  if [x3: item, x4: requirement]
    in(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x4)
```

## r53
From: b316 r44. Not in the audit (b316 is no reword item).

```reading
If the person runs `work line` on an item that holds a chore, then `work` shall refuse the command and name the chore.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x5: tool `work` (constant)]
  if [x3: item, x4: chore]
    in(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x4)
```

## r54
From: b316 r45. Not in the audit (b316 is no reword item).

```reading
While an item is `shaped` and the item holds a chore and the item holds no requirement, when the person runs `work ready` on the item, `work` shall set the status of the item to `ready`.
shall [x4: agent the person (constant), x5: command `work ready` (parameter), x6: tool `work` (constant)]
  while [x1: item, x2: chore]
    status(x1) = `shaped`
    in(x2, x1)
    not [x3: requirement]
      in(x3, x1)
  when
    run(e1, subject: x4, object: x5, on: x1)
  response
    initiates(e2, subject: x6, status(x1) = `ready`)
```

## r55
From: b317 r42. Not in the audit (b317 is no reword item).

```reading
When the person runs `work line` with the `--capability` option set to a capability on an item, `work` shall write the capability in the item and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--capability` (parameter), x6: tool `work` (constant)]
  when [x4: capability, x5: item]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    in(x4, x5)
    write(e2, subject: x6, object: x4)
    commit(e3, subject: x6, object: x5)
```

## r56
From: b317 r43. Not in the audit (b317 is no reword item).

```reading
If the person runs `work line` with the `--capability` option set to a capability that exists, then `work` shall refuse the command and name the capability.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--capability` (parameter), x5: tool `work` (constant)]
  if [x4: capability]
    exists(x4)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x4)
```

## r57
Retires: r43. From: b323 r51. Not in the audit (b323 rewords r43: an id the requirement does not retire is kept).

```reading
When the person runs `work line` with the `--remove` option set to the requirement id of a requirement in an item on the item, `work` shall remove the requirement, not remove a requirement id in the item that the requirement does not retire and commit the item.
shall [x1: agent the person (constant), x2: command `work line` (parameter), x3: option `--remove` (parameter), x7: tool `work` (constant)]
  when [x4: requirement, x5: item, x6: requirement id]
    in(x4, x5)
    of(x6, x4)
    argument(x3, x6)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    remove(e2, subject: x7, object: x4)
    not [x8: requirement id]
      in(x8, x5)
      not
        retire(subject: x4, object: x8)
      remove(e3, subject: x7, object: x8)
    commit(e4, subject: x7, object: x5)
```

## r58
Retires: r49. From: b333 r58. The bar runs every rule of `model check` on the laid copy, before and after the lay: a violation the lay brings that names a group of the item is refused, named with the rule.

```reading
While an item is `shaped` and a requirement group in the item violates a rule, if the person runs `work ready` on the item, then `work` shall refuse the command and name the requirement group and the rule.
shall [x4: agent the person (constant), x5: command `work ready` (parameter), x6: tool `work` (constant)]
  while [x1: item, x2: requirement group, x3: rule]
    status(x1) = `shaped`
    in(x2, x1)
    violate(subject: x2, object: x3)
  if
    run(e1, subject: x4, object: x5, on: x1)
  response
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x2)
    name(e4, subject: x6, object: x3)
```
