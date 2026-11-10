# feature-file-tools: every live line with its intended reading (b240)

## r88
Retires: r1. From: b157 r45. Audit: distortion ("scenario count", a noun for a count), fixed by the number of Ks (`number-of`).

```reading
While a docstring of a feature file contains a tag and a scenario line, when the person runs `features count` with the `--by-tag` option, `features` shall print the number of scenarios of the feature file.
shall [x5: agent the person (constant), x6: command `features count` (parameter), x7: option `--by-tag` (parameter), x8: tool `features` (constant)]
  while [x1: docstring, x2: feature file, x3: tag, x4: scenario line]
    of(x1, x2)
    contain(subject: x1, object: x3)
    contain(subject: x1, object: x4)
  when
    run(e1, subject: x5, object: x6, with: x7)
  response [x9: number]
    number x9 of [x10: scenario]
      of(x10, x2)
    print(e2, subject: x8, object: x9)
```

## r89
Retires: r2. From: b157 r46. Audit: distortion (one scenario for each examples row hidden in the gloss of "count"), said of a feature file whose only scenarios are its outline's rows. Known limit: #10.

```reading
While a feature file has a scenario outline and the feature file has no scenario, when the person runs `features count` with the `--by-tag` option, `features` shall print the number of examples rows of the scenario outline.
shall [x4: agent the person (constant), x5: command `features count` (parameter), x6: option `--by-tag` (parameter), x7: tool `features` (constant)]
  while [x1: feature file, x2: scenario outline]
    of(x2, x1)
    not [x3: scenario]
      of(x3, x1)
  when
    run(e1, subject: x4, object: x5, with: x6)
  response [x8: number]
    number x8 of [x9: examples row]
      of(x9, x2)
    print(e2, subject: x7, object: x8)
```

## r90
Retires: r3. From: b157 r47. Audit: fine; the option with its argument in the trigger (`option-set-to`).

```reading
While a docstring of a feature file contains a tag and the feature file does not have the tag, when the person runs `features list` with the `--tag` option set to the tag, `features` shall exit successfully and not print the feature file.
shall [x4: agent the person (constant), x5: command `features list` (parameter), x6: option `--tag` (parameter), x7: tool `features` (constant)]
  while [x1: docstring, x2: feature file, x3: tag]
    of(x1, x2)
    contain(subject: x1, object: x3)
    not
      of(x3, x2)
  when
    argument(x6, x3)
    run(e1, subject: x4, object: x5, with: x6)
  response
    exit(e2, subject: x7, successfully)
    not
      print(e3, subject: x7, object: x2)
```

## r91
Retires: r4. From: b157 r48. Audit: coined ("subdirectory" glossed "at any depth"), said of one subdirectory (language.md: a thing in a thing at any depth).

```reading
While a feature file in a subdirectory has a scenario, when the person runs `features list` with the `--title` option set to the scenario title of the scenario, `features` shall print the feature file.
shall [x4: agent the person (constant), x5: command `features list` (parameter), x6: option `--title` (parameter), x8: tool `features` (constant)]
  while [x1: feature file, x2: subdirectory, x3: scenario]
    in(x1, x2)
    of(x3, x1)
  when [x7: scenario title]
    of(x7, x3)
    argument(x6, x7)
    run(e1, subject: x4, object: x5, with: x6)
  response
    print(e2, subject: x8, object: x1)
```

## r92
Retires: r5. From: b157 r49. Audit: distortion (the scenario's own tag left out), split in two by section 5: the feature file's tag here, the scenario's in r93.

```reading
While a feature file has a tag, when the person runs `features list` with the `--tag` option set to the tag, `features` shall print every scenario of the feature file.
shall [x3: agent the person (constant), x4: command `features list` (parameter), x5: option `--tag` (parameter), x6: tool `features` (constant)]
  while [x1: feature file, x2: tag]
    of(x2, x1)
  when
    argument(x5, x2)
    run(e1, subject: x3, object: x4, with: x5)
  response
    every [x7: scenario]
      of(x7, x1)
      scope
        print(e2, subject: x6, object: x7)
```

## r93
Retires: r5. From: b157 r49. Audit: distortion, split in two by section 5: the scenario's own tag.

```reading
While a scenario has a tag, when the person runs `features list` with the `--tag` option set to the tag, `features` shall print the scenario.
shall [x3: agent the person (constant), x4: command `features list` (parameter), x5: option `--tag` (parameter), x6: tool `features` (constant)]
  while [x1: scenario, x2: tag]
    of(x2, x1)
  when
    argument(x5, x2)
    run(e1, subject: x3, object: x4, with: x5)
  response
    print(e2, subject: x6, object: x1)
```

## r94
Retires: r6. From: b157 r50. Audit: fine; the option with its argument in the trigger.

```reading
When the person runs `features list` with the `--title` option set to a search text, `features` shall print every scenario whose scenario title contains the search text.
shall [x1: agent the person (constant), x2: command `features list` (parameter), x3: option `--title` (parameter), x5: tool `features` (constant)]
  when [x4: search text]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    every [x6: scenario, x7: scenario title]
      of(x7, x6)
      contain(subject: x7, object: x4)
      scope
        print(e2, subject: x5, object: x6)
```

## r95
Retires: r7. Audit (b118): r7 restated r6 with `--json`; kept as the line of `--json`, which U8 makes one JSON object.

```reading
When the person runs `features list` with the `--json` option and the `--title` option set to a search text, `features` shall print every scenario whose scenario title contains the search text.
shall [x1: agent the person (constant), x2: command `features list` (parameter), x3: option `--json` (parameter), x4: option `--title` (parameter), x6: tool `features` (constant)]
  when [x5: search text]
    argument(x4, x5)
    run(e1, subject: x1, object: x2, with: x3, with: x4)
  response
    every [x7: scenario, x8: scenario title]
      of(x8, x7)
      contain(subject: x8, object: x5)
      scope
        print(e2, subject: x6, object: x7)
```

## r96
Retires: r8. From: b157 r51. Audit: fine.

```reading
While a feature file has a rule block, if the person runs `features count` with the `--by-tag` option, then `features` shall refuse the command and name the feature file.
shall [x3: agent the person (constant), x4: command `features count` (parameter), x5: option `--by-tag` (parameter), x6: tool `features` (constant)]
  while [x1: feature file, x2: rule block]
    of(x2, x1)
  if
    run(e1, subject: x3, object: x4, with: x5)
  response
    refuse(e2, subject: x6, object: x4)
    name(e3, subject: x6, object: x1)
```

## r97
Retires: r9. From: b157 r52. Audit: fine; "requirement tag" for the `@r<n>` tags `features deprecated` prints, which "every tag" overstated.

```reading
While a replacement of a scenario has a requirement tag and the scenario has the `@deprecated` tag, when the person runs `features deprecated`, `features` shall print the scenario and every requirement tag of the replacement.
shall [x4: tag `@deprecated` (parameter), x5: agent the person (constant), x6: command `features deprecated` (parameter), x7: tool `features` (constant)]
  while [x1: replacement, x2: scenario, x3: requirement tag]
    of(x1, x2)
    of(x3, x1)
    of(x4, x2)
  when
    run(e1, subject: x5, object: x6)
  response
    print(e2, subject: x7, object: x2)
    every [x8: requirement tag]
      of(x8, x1)
      scope
        print(e3, subject: x7, object: x8)
```

## r98
Retires: r10. From: b157 r53. Audit: distortion ("the none-deprecated note", a proper noun named after the printed text), fixed by the printed text as a code.

```reading
While no scenario has the `@deprecated` tag, when the person runs `features deprecated`, `features` shall print `none deprecated`.
shall [x2: tag `@deprecated` (parameter), x3: agent the person (constant), x4: command `features deprecated` (parameter), x5: tool `features` (constant), x6: thing `none deprecated` (parameter)]
  while
    not [x1: scenario]
      of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x6)
```

## r99
Retires: r11. From: b157 r54. Audit: fine.

```reading
While a scenario has the `@deprecated` tag, when the person runs `features deprecated` with the `--json` option, `features` shall print the scenario title of the scenario.
shall [x2: tag `@deprecated` (parameter), x3: agent the person (constant), x4: command `features deprecated` (parameter), x5: option `--json` (parameter), x6: tool `features` (constant)]
  while [x1: scenario]
    of(x2, x1)
  when
    run(e1, subject: x3, object: x4, with: x5)
  response [x7: scenario title]
    of(x7, x1)
    print(e2, subject: x6, object: x7)
```

## r100
Retires: r12. From: b157 r55. Audit: distortion (the state "every binding names a scenario" dropped), fixed by section 5: an "every" While clause.

```reading
While every binding binds a scenario, when the person runs `features bindings`, `features` shall print `every binding names a scenario` and exit successfully.
shall [x3: agent the person (constant), x4: command `features bindings` (parameter), x5: tool `features` (constant), x6: thing `every binding names a scenario` (parameter)]
  while
    every [x1: binding]
      scope [x2: scenario]
        bind(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x6)
    exit(e3, subject: x5, successfully)
```

## r101
Retires: r13. From: b157 r56. Audit: fine; "binds no scenario" for "names a scenario title that no scenario has", and "change no file" kept from r13.

```reading
While a binding of a test module binds no scenario, if the person runs `features bindings`, then `features` shall exit with an error naming the test module and change no file.
shall [x4: agent the person (constant), x5: command `features bindings` (parameter), x6: tool `features` (constant)]
  while [x1: binding, x2: test module]
    of(x1, x2)
    not [x3: scenario]
      bind(subject: x1, object: x3)
  if
    run(e1, subject: x4, object: x5)
  response
    exit(e2, subject: x6, with an error naming: x2)
    not [x7: file]
      change(e3, subject: x6, object: x7)
```

## r102
Retires: r14. From: b157 r57. Audit: coined (the point in the gloss of "scenarios call"), fixed by the response: `features bindings --unbound` prints no scenario of the feature file a scenarios call names (`not-response` over a K named nowhere before).

```reading
While a scenarios call binds a scenario of a feature file, when the person runs `features bindings` with the `--unbound` option, `features` shall exit successfully and not print a scenario of the feature file.
shall [x4: agent the person (constant), x5: command `features bindings` (parameter), x6: option `--unbound` (parameter), x7: tool `features` (constant)]
  while [x1: scenarios call, x2: scenario, x3: feature file]
    of(x2, x3)
    bind(subject: x1, object: x2)
  when
    run(e1, subject: x4, object: x5, with: x6)
  response
    exit(e2, subject: x7, successfully)
    not [x8: scenario]
      of(x8, x3)
      print(e3, subject: x7, object: x8)
```

## r103
Retires: r15. From: b157 r58. Audit: distortion (an "or" in the gloss of "bind"), fixed by one gloss of bind.

```reading
While a feature file has a scenario that no binding binds, if the person runs `features bindings` with the `--unbound` option, then `features` shall exit with an error naming the scenario and change no file.
shall [x4: agent the person (constant), x5: command `features bindings` (parameter), x6: option `--unbound` (parameter), x7: tool `features` (constant)]
  while [x1: feature file, x2: scenario]
    not [x3: binding]
      bind(subject: x3, object: x2)
    of(x2, x1)
  if
    run(e1, subject: x4, object: x5, with: x6)
  response
    exit(e2, subject: x7, with an error naming: x2)
    not [x8: file]
      change(e3, subject: x7, object: x8)
```

## r104
Retires: r16. From: b157 r59. Audit: distortion, as r103; the two options in the trigger.

```reading
While a feature file has a scenario that no binding binds, if the person runs `features bindings` with the `--unbound` and `--json` options, then `features` shall exit with an error naming the scenario and change no file.
shall [x4: agent the person (constant), x5: command `features bindings` (parameter), x6: option `--unbound` (parameter), x7: option `--json` (parameter), x8: tool `features` (constant)]
  while [x1: feature file, x2: scenario]
    not [x3: binding]
      bind(subject: x3, object: x2)
    of(x2, x1)
  if
    run(e1, subject: x4, object: x5, with: x6, with: x7)
  response
    exit(e2, subject: x8, with an error naming: x2)
    not [x9: file]
      change(e3, subject: x8, object: x9)
```

## r106
Retires: r18. From: b157 r61. Audit: coined (the counterfactual in the gloss of "differ"), said of a scenario that no requirement group has. Known limit: #13.

```reading
While the feature of a capability has a scenario that no requirement group has, if the person runs `features generate` with the `--check` option, then `features` shall exit with an error naming the feature and change no file.
shall [x5: agent the person (constant), x6: command `features generate` (parameter), x7: option `--check` (parameter), x8: tool `features` (constant)]
  while [x1: capability, x2: feature, x3: scenario]
    of(x2, x1)
    not [x4: requirement group]
      of(x3, x4)
    of(x3, x2)
  if
    run(e1, subject: x5, object: x6, with: x7)
  response
    exit(e2, subject: x8, with an error naming: x2)
    not [x9: file]
      change(e3, subject: x8, object: x9)
```

## r107
Retires: r19. From: b157 r62. Audit: fine.

```reading
While a step of a feature has no handler, if the person runs `features vocab` with the `--check` option, then `features` shall exit with an error naming the step and the feature and change no file.
shall [x4: agent the person (constant), x5: command `features vocab` (parameter), x6: option `--check` (parameter), x7: tool `features` (constant)]
  while [x1: step, x2: feature]
    of(x1, x2)
    not [x3: handler]
      of(x3, x1)
  if
    run(e1, subject: x4, object: x5, with: x6)
  response
    exit(e2, subject: x7, with an error naming: x1)
    exit(e3, subject: x7, with an error naming: x2)
    not [x8: file]
      change(e4, subject: x7, object: x8)
```

## r108
Retires: r20, r22-r44; covers b236 r45 and b237 r45, the generator's construct lines (b157 r63, r65-r87 their rewordings), each now checked by the corpus and language.md's twins, and by this line's scenario, a capability of every "shall" example of grammar/constructs.md with given blocks of example data: r20 `not-response`, `to-role`; r22 the language attribute; r23 `oblique-role`; r24 R2 ("the K" in a modifier); r25-r27 example data (a value, a docstring, a table); r28 `state-condition` (no object); r29 `of-relation` in `rc-subject`; r30 `of-relation` over `every`; r31 R2 and language.md "the K" outside the box; r32 `set-attribute`; r33, r34 `may`, `always-never` (language.md's Modality: no scenario); r35, r36 `every`; r37 `only`; r38, r39 `count`, `number-of`; r40 `or-condition`; r41 `of-relation`, `has-relation`, `rc-whose-relation`; r42 `attribute-of`; r43 `no-noun`; r44 `not-relative`; b236 a verb of two frames, b237 `not-response` over a K named nowhere before (language.md "What parses is read").

```reading
While the language of a capability is `codified-2` and every requirement of the capability conforms to the language reference and every requirement of the capability uses the `shall` construct, when the person runs `features generate` on the capability, `features` shall write the scenario of every requirement group of the capability.
shall [x3: artifact the language reference (constant), x5: construct `shall` (parameter), x6: agent the person (constant), x7: command `features generate` (parameter), x8: tool `features` (constant)]
  while [x1: capability]
    language(x1) = `codified-2`
    every [x2: requirement]
      of(x2, x1)
      scope
        conforms(x2, x3)
    every [x4: requirement]
      of(x4, x1)
      scope
        use#2(subject: x4, object: x5)
  when
    run(e1, subject: x6, object: x7, on: x1)
  response
    every [x9: requirement group]
      of(x9, x1)
      scope [x10: scenario]
        of(x10, x9)
        write(e2, subject: x8, object: x10)
```

## r109
Retires: r21. From: b157 r64. Audit: coined ("refusal", "premise", "entail" hiding the derivation), said with the universal condition that entails the step.

```reading
While the language of a capability is `codified-2`, when the person runs `features generate` on the capability, `features` shall not write a step that a universal condition entails.
shall [x2: agent the person (constant), x3: command `features generate` (parameter), x4: tool `features` (constant)]
  while [x1: capability]
    language(x1) = `codified-2`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response
    not [x5: step, x6: universal condition]
      entail(subject: x6, object: x5)
      write(e2, subject: x4, object: x5)
```

## r110
Retires: r105. From: b240 phase 25. Audit: the old language's reader is gone (b160): a capability in `codified-1` is refused naming `migrate upgrade`, so only the language of the capability `codified-2` is written.

```reading
While the group of a capability is `service` and the language of the capability is `codified-2`, when the person runs `features generate`, `features` shall write the feature of the capability and print the feature.
shall [x2: agent the person (constant), x3: command `features generate` (parameter), x4: tool `features` (constant)]
  while [x1: capability]
    group(x1) = `service`
    language(x1) = `codified-2`
  when
    run(e1, subject: x2, object: x3)
  response [x5: feature]
    of(x5, x1)
    write(e2, subject: x4, object: x5)
    print(e3, subject: x4, object: x5)
```
