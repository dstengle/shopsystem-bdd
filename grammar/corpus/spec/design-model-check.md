# design-model-check: every live line with its intended reading (b240)

## r50
Kept. Audit: fine.

```reading
When the person runs `model decisions`, `model` shall write a decisions index.
shall [x1: agent the person (constant), x2: command `model decisions` (parameter), x3: tool `model` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response [x4: decisions index]
    write(e2, subject: x3, object: x4)
```

## r54
Kept. Audit: fine.

```reading
When the person runs `model rules`, `model` shall print every rule and exit successfully.
shall [x1: agent the person (constant), x2: command `model rules` (parameter), x3: tool `model` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: rule]
      scope
        print(e2, subject: x3, object: x4)
    exit(e3, subject: x3, successfully)
```

## r55
Kept. Audit: fine.

```reading
When the person runs `model forms`, `model` shall print every file form and exit successfully.
shall [x1: agent the person (constant), x2: command `model forms` (parameter), x3: tool `model` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: file form]
      scope
        print(e2, subject: x3, object: x4)
    exit(e3, subject: x3, successfully)
```

## r56
Kept. Audit: fine.

```reading
When the person runs `work record`, `work` shall write a record and commit the record.
shall [x1: agent the person (constant), x2: command `work record` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response [x4: record]
    write(e2, subject: x3, object: x4)
    commit(e3, subject: x3, object: x4)
```

## r156
Kept. Audit: fine.

```reading
When the person runs `model explain` on a requirement, `model` shall print the requirement and exit successfully.
shall [x1: agent the person (constant), x2: command `model explain` (parameter), x4: tool `model` (constant)]
  when [x3: requirement]
    run(e1, subject: x1, object: x2, on: x3)
  response
    print(e2, subject: x4, object: x3)
    exit(e3, subject: x4, successfully)
```

## r174
Retires: r1. From: b152 r174. Audit: distortion, fixed by section 5 ("0 violations" restored; the condition said as "nothing violates a rule", not in the gloss of "the design model").

```reading
While nothing violates a rule, when the person runs `model check`, `model` shall print `0 violations` and exit successfully.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant), x6: thing `0 violations` (parameter)]
  while
    not [x1: thing, x2: rule]
      violate(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x6)
    exit(e3, subject: x5, successfully)
```

## r175
Retires: r2. From: b152 r175. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a capability violates `v15a`, if the person runs `model check`, then `model` shall exit with an error naming `v15a`.
shall [x2: rule `v15a` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: capability]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r176
Retires: r3. From: b152 r176. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a capability violates `v15b`, if the person runs `model check`, then `model` shall exit with an error naming `v15b`.
shall [x2: rule `v15b` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: capability]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r177
Retires: r4. From: b152 r177. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a capability violates `v15c`, if the person runs `model check`, then `model` shall exit with an error naming `v15c`.
shall [x2: rule `v15c` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: capability]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r178
Retires: r5. From: b152 r178. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a requirement group violates `v15l`, if the person runs `model check`, then `model` shall exit with an error naming `v15l`.
shall [x2: rule `v15l` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r179
Retires: r6. From: b152 r179. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a requirement group violates `v15n`, if the person runs `model check`, then `model` shall exit with an error naming `v15n`.
shall [x2: rule `v15n` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r180
Retires: r7. From: b152 r180. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a requirement group violates `v15m`, if the person runs `model check`, then `model` shall exit with an error naming `v15m`.
shall [x2: rule `v15m` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r181
Retires: r10. From: b152 r181. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a requirement group violates `v_s3`, if the person runs `model check`, then `model` shall exit with an error naming `v_s3`.
shall [x2: rule `v_s3` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: requirement group]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r182
Retires: r11. From: b152 r182. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a scenario violates `v_s2`, if the person runs `model check`, then `model` shall exit with an error naming `v_s2`.
shall [x2: rule `v_s2` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: scenario]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r183
Retires: r19. From: b152 r183. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a request violates `v17`, if the person runs `model check`, then `model` shall exit with an error naming `v17`.
shall [x2: rule `v17` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: request]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r184
Retires: r20. From: b152 r184. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a request violates `v3`, if the person runs `model check`, then `model` shall exit with an error naming `v3`.
shall [x2: rule `v3` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: request]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r185
Retires: r22. From: b152 r185. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a requirement violates `v_t1`, if the person runs `model check`, then `model` shall exit with an error naming `v_t1`.
shall [x2: rule `v_t1` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: requirement]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r186
Retires: r23. From: b152 r186. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a term violates `v_t2`, if the person runs `model check`, then `model` shall exit with an error naming `v_t2`.
shall [x2: rule `v_t2` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r187
Retires: r24. From: b152 r187. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a term violates `v_t3`, if the person runs `model check`, then `model` shall exit with an error naming `v_t3`.
shall [x2: rule `v_t3` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r188
Retires: r25. From: b152 r188. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a requirement violates `v_p1`, if the person runs `model check`, then `model` shall exit with an error naming `v_p1`.
shall [x2: rule `v_p1` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: requirement]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r189
Retires: r28. From: b152 r189. Audit: fine, conformance to an artifact (phase 4).

```reading
While a request does not conform to the request form, if the person runs `model check`, then `model` shall exit with an error naming the request.
shall [x2: artifact the request form (constant), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: request]
    not
      conforms(x1, x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r190
Retires: r30. From: b152 r190. Audit: fine.

```reading
While a scenario refers to a requirement id that the capability of the scenario does not hold, if the person runs `model check`, then `model` shall exit with an error naming the scenario.
shall [x4: agent the person (constant), x5: command `model check` (parameter), x6: tool `model` (constant)]
  while [x1: scenario, x2: requirement id, x3: capability]
    of(x3, x1)
    not
      in(x2, x3)
    refer(subject: x1, to: x2)
  if
    run(e1, subject: x4, object: x5)
  response
    exit(e2, subject: x6, with an error naming: x1)
```

## r191
Retires: r36. From: b152 r191. Audit: distortion, the pattern declared as an artifact the capability conforms to (phase 4).

```reading
While a capability does not conform to the capability id form, if the person runs `model check`, then `model` shall exit with an error naming the capability.
shall [x2: artifact the capability id form (constant), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: capability]
    not
      conforms(x1, x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r192
Retires: r36. From: b152 r192. Audit: distortion, fixed by section 5 (a section by its heading; r36's two rules split, the id in r191).

```reading
While a capability has no section whose heading is `Behaviour`, if the person runs `model check`, then `model` shall exit with an error naming the capability.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: capability]
    not [x2: section]
      heading(x2) = `Behaviour`
      of(x2, x1)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r193
Retires: r38. From: b152 r193. Audit: distortion, the path declared as an artifact the feature conforms to (phase 4).

```reading
While a feature does not conform to the feature form, if the person runs `model check`, then `model` shall exit with an error naming the feature.
shall [x2: artifact the feature form (constant), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: feature]
    not
      conforms(x1, x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r194
Retires: r40. From: b152 r194. Audit: distortion, fixed by section 5 (the id and the Decision section split into r194 and r286).

```reading
While a design-decision has no id, if the person runs `model check`, then `model` shall exit with an error naming the design-decision.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: design-decision]
    not [x2: id]
      of(x2, x1)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r195
Retires: r41. From: b152 r195. Audit: fine, conformance to an artifact (phase 4).

```reading
While a term does not conform to the entry form, if the person runs `model check`, then `model` shall exit with an error naming the term.
shall [x2: artifact the entry form (constant), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    not
      conforms(x1, x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r196
Retires: r42. From: b152 r196. Audit: fine, conformance to an artifact (phase 4).

```reading
While this bounded context does not conform to the final layout, if the person runs `model check`, then `model` shall exit with an error naming `scripts/migrate`.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x2: artifact the final layout (constant), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant), x6: thing `scripts/migrate` (parameter)]
  while
    not
      conforms(x1, x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x6)
```

## r197
Retires: r43. From: b152 r197. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While an observation violates `w_uncited_obs`, when the person runs `model check`, `model` shall print `w_uncited_obs` and exit successfully.
shall [x2: rule `w_uncited_obs` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: observation]
    violate(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x2)
    exit(e3, subject: x5, successfully)
```

## r198
Retires: r44. From: b152 r198. Audit: fine, said as "print no capability that violates `w_unserved_cap`", so that `model logic` does not read the code, a parameter, as a thing r246 or U8 prints.

```reading
While this bounded context has no job, when the person runs `model check`, `model` shall print no capability that violates `w_unserved_cap`.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant), x7: rule `w_unserved_cap` (parameter)]
  while
    not [x2: job]
      of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    not [x6: capability]
      violate(subject: x6, object: x7)
      print(e2, subject: x5, object: x6)
```

## r199
Retires: r47. From: b152 r199. Audit: distortion, fixed with identity ("another interpreter", phase 8); "0 violations" restored as the old r47 had it.

```reading
While the interpreter of the command does not import `clingo` and another interpreter imports `clingo`, when the person runs `model check`, `model` shall print `0 violations`.
shall [x1: command "the command the run runs" (indexical), x3: thing `clingo` (constant), x5: agent the person (constant), x6: command `model check` (parameter), x7: tool `model` (constant), x8: thing `0 violations` (parameter)]
  while [x2: interpreter, x4: interpreter]
    of(x2, x1)
    not
      import(subject: x2, object: x3)
    distinct(x4, x2)
    import(subject: x4, object: x3)
  when
    run(e1, subject: x5, object: x6)
  response
    print(e2, subject: x7, object: x8)
```

## r200
Retires: r48. From: b152 r200. Audit: fine.

```reading
While no interpreter imports `clingo`, if the person runs `model check`, then `model` shall refuse the command and name `pip install clingo`.
shall [x2: thing `clingo` (constant), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant), x6: thing `pip install clingo` (parameter)]
  while
    not [x1: interpreter]
      import(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x6)
```

## r201
Retires: r49. From: b152 r201. Audit: fine.

```reading
When the person runs `model facts`, `model` shall print every fact of this bounded context.
shall [x1: agent the person (constant), x2: command `model facts` (parameter), x3: tool `model` (constant), x5: bounded context "the bounded context whose repository the command runs in" (indexical)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: fact]
      of(x4, x5)
      scope
        print(e2, subject: x3, object: x4)
```

## r202
Retires: r51. From: b152 r202. Audit: unsayable. Known limit: #13 (what a command would write: the stale index said by the index entry it does not hold).

```reading
While a design-decision has an index entry that a decisions index does not hold, if the person runs `model decisions` with the `--check` option, then `model` shall exit with an error naming the decisions index and change no file.
shall [x4: agent the person (constant), x5: command `model decisions` (parameter), x6: option `--check` (parameter), x7: tool `model` (constant)]
  while [x1: design-decision, x2: index entry, x3: decisions index]
    not
      in(x2, x3)
    of(x2, x1)
  if
    run(e1, subject: x4, object: x5, with: x6)
  response
    exit(e2, subject: x7, with an error naming: x3)
    not [x8: file]
      change(e3, subject: x7, object: x8)
```

## r203
Retires: r52. From: b152 r203. Audit: unsayable. Known limit: #13 (what a command would write: "no decisions index lacks an index entry").

```reading
While no decisions index lacks an index entry, when the person runs `model decisions` with the `--check` option, `model` shall exit successfully.
shall [x3: agent the person (constant), x4: command `model decisions` (parameter), x5: option `--check` (parameter), x6: tool `model` (constant)]
  while
    not [x1: decisions index, x2: index entry]
      lack(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4, with: x5)
  response
    exit(e2, subject: x6, successfully)
```

## r204
Retires: r57. From: b152 r204. Audit: distortion, the option with its argument (phase 11) and conformance (phase 4).

```reading
If the person runs `work record` with the `--about` option set to a text that does not conform to the node id form, then `work` shall refuse the command and name `--about`.
shall [x1: agent the person (constant), x2: command `work record` (parameter), x3: option `--about` (parameter), x5: artifact the node id form (constant), x6: tool `work` (constant)]
  if [x4: text]
    not
      conforms(x4, x5)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x3)
```

## r205
Retires: r58. From: b152 r205. Audit: distortion. Known limit: #1 (the verb omit for a word a frame needs and the line leaves out).

```reading
If the person runs `model parse` on a requirement that omits an object of a term, then `model` shall refuse the command and name the term.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: object, x5: term]
    of(x4, x5)
    omit(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x5)
```

## r206
Retires: r59. From: b152 r206. Audit: distortion. Known limit: #1 (the verb omit for a word a frame needs and the line leaves out).

```reading
If the person runs `model parse` on a requirement that omits a recipient of a term, then `model` shall refuse the command and name the term.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: recipient, x5: term]
    of(x4, x5)
    omit(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x5)
```

## r207
Retires: r60. From: b152 r207. Audit: distortion, fixed by section 5 ("a verb has no frame").

```reading
While a verb has no frame, if the person runs `model check`, then `model` shall exit with an error naming the verb.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: verb]
    not [x2: frame]
      of(x2, x1)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r208
Retires: r61. From: b152 r208. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a term violates `v_t12`, if the person runs `model check`, then `model` shall exit with an error naming the term.
shall [x2: rule `v_t12` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r209
Retires: r62. From: b152 r209. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `not-condition`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `not-condition` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r210
Retires: r63. From: b152 r210. Audit: distortion, the verb mismatch said with structure ("a noun phrase of a term that no frame takes").

```reading
If the person runs `model parse` on a requirement that uses a noun phrase of a term that no frame takes, then `model` shall refuse the command and name the term.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x7: tool `model` (constant)]
  if [x3: requirement, x4: noun phrase, x5: term]
    of(x4, x5)
    not [x6: frame]
      take(subject: x6, object: x4)
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x7, object: x2)
    name(e3, subject: x7, object: x5)
```

## r211
Retires: r64. From: b152 r211. Audit: fine.

```reading
When the person runs `model parse` on a requirement whose precondition uses a term whose aspect is `state`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  when [x3: requirement, x4: precondition, x5: term]
    of(x4, x3)
    aspect(x5) = `state`
    use#2(subject: x4, object: x5)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x6, successfully)
```

## r212
Retires: r65. From: b152 r212. Audit: fine.

```reading
If the person runs `model parse` on a requirement that uses a passive form that has no by-phrase, then `model` shall refuse the command and name the passive form.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: passive form]
    not [x5: by-phrase]
      of(x5, x4)
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r213
Retires: r66. From: b152 r213. Audit: fine.

```reading
When the person runs `model parse` on a requirement whose trigger uses a recipient, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  when [x3: requirement, x4: trigger, x5: recipient]
    of(x4, x3)
    use#2(subject: x4, object: x5)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x6, successfully)
```

## r214
Retires: r67. From: b152 r214. Audit: distortion, fixed by section 5 ("a term has no part of speech").

```reading
While a term has no part of speech, if the person runs `model check`, then `model` shall exit with an error naming the term.
shall [x2: agent the person (constant), x3: command `model check` (parameter), x4: tool `model` (constant)]
  while [x1: term]
    part of speech(x1) = none
  if
    run(e1, subject: x2, object: x3)
  response
    exit(e2, subject: x4, with an error naming: x1)
```

## r215
Retires: r68. From: b152 r215. Audit: fine.

```reading
While a frame of a term has a preposition, when the person runs `model check`, `model` shall exit successfully.
shall [x4: agent the person (constant), x5: command `model check` (parameter), x6: tool `model` (constant)]
  while [x1: frame, x2: term, x3: preposition]
    of(x1, x2)
    of(x3, x1)
  when
    run(e1, subject: x4, object: x5)
  response
    exit(e2, subject: x6, successfully)
```

## r216
Retires: r69. From: b152 r216. Audit: fine.

```reading
When the person runs `model parse` on a requirement that uses a term whose frame has a preposition, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x7: tool `model` (constant)]
  when [x3: requirement, x4: term, x5: frame, x6: preposition]
    of(x5, x4)
    of(x6, x5)
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x7, successfully)
```

## r217
Retires: r70. From: b152 r217. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a term violates `v_t13`, if the person runs `model check`, then `model` shall exit with an error naming the term.
shall [x2: rule `v_t13` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r218
Retires: r71. From: b152 r218. Audit: coined, fixed with identity ("two requirements", "another requirement", phase 8); the coined "unification failure" and "clash" said with structure; "print a requirement" restored.

```reading
While two requirements of a capability use a code that `model` does not unify and a requirement of the capability obliges an act that another requirement of the capability forbids, when the person runs `model logic`, `model` shall print a requirement and print `L1`.
shall [x5: tool `model` (constant), x9: agent the person (constant), x10: command `model logic` (parameter), x12: thing `L1` (constant)]
  while [x1: requirement, x2: capability, x4: code, x3: requirement, x6: requirement, x7: act, x8: requirement]
    of(x1, x2)
    not
      unify(subject: x5, object: x4)
    use#2(subject: x1, object: x4)
    distinct(x3, x1)
    of(x3, x2)
    use#2(subject: x3, object: x4)
    of(x6, x2)
    distinct(x8, x6)
    of(x8, x2)
    forbid(subject: x8, object: x7)
    oblige(subject: x6, object: x7)
  when
    run(e1, subject: x9, object: x10)
  response [x11: requirement]
    print(e2, subject: x5, object: x11)
    print(e3, subject: x5, object: x12)
```

## r219
Retires: r74. From: b152 r219. Audit: fine, the option in the trigger (phase 11).

```reading
When the person runs `model rules` with the `--write` option, `model` shall write a rule catalogue and exit successfully.
shall [x1: agent the person (constant), x2: command `model rules` (parameter), x3: option `--write` (parameter), x4: tool `model` (constant)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response [x5: rule catalogue]
    write(e2, subject: x4, object: x5)
    exit(e3, subject: x4, successfully)
```

## r220
Retires: r75. From: b152 r220. Audit: unsayable. Known limit: #13 (what a command would write: the stale catalogue said by the catalogue entry it does not hold).

```reading
While a rule has a catalogue entry that a rule catalogue does not hold, if the person runs `model rules` with the `--check` option, then `model` shall exit with an error naming the rule catalogue and change no file.
shall [x4: agent the person (constant), x5: command `model rules` (parameter), x6: option `--check` (parameter), x7: tool `model` (constant)]
  while [x1: rule, x2: catalogue entry, x3: rule catalogue]
    not
      in(x2, x3)
    of(x2, x1)
  if
    run(e1, subject: x4, object: x5, with: x6)
  response
    exit(e2, subject: x7, with an error naming: x3)
    not [x8: file]
      change(e3, subject: x7, object: x8)
```

## r221
Retires: r76. From: b152 r221. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a term violates `v_t14`, if the person runs `model check`, then `model` shall exit with an error naming the term.
shall [x2: rule `v_t14` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r222
Retires: r77. From: b152 r222. Audit: fine.

```reading
While a term has more than one frame, when the person runs `model check`, `model` shall exit successfully.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    count more than 1 [x2: frame]
      scope
        of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
```

## r223
Retires: r78. From: b152 r223. Audit: distortion.

```reading
While a term has more than one sense, when the person runs `model check`, `model` shall exit successfully.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    count more than 1 [x2: sense]
      scope
        of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
```

## r224
Retires: r79. From: b152 r224. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a term violates `v_t15`, if the person runs `model check`, then `model` shall exit with an error naming the term.
shall [x2: rule `v_t15` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r225
Retires: r80. From: b152 r225. Audit: fine.

```reading
While this bounded context imports a pack, when the person runs `model lexicon`, `model` shall print every term of the pack and exit successfully.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `model lexicon` (parameter), x5: tool `model` (constant)]
  while [x2: pack]
    import#2(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    every [x6: term]
      of(x6, x2)
      scope
        print(e2, subject: x5, object: x6)
    exit(e3, subject: x5, successfully)
```

## r226
Retires: r81. From: b152 r226. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While this bounded context imports a pack that violates `v_t17`, if the person runs `model check`, then `model` shall exit with an error naming the pack.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: rule `v_t17` (parameter), x4: agent the person (constant), x5: command `model check` (parameter), x6: tool `model` (constant)]
  while [x2: pack]
    violate(subject: x2, object: x3)
    import#2(subject: x1, object: x2)
  if
    run(e1, subject: x4, object: x5)
  response
    exit(e2, subject: x6, with an error naming: x2)
```

## r227
Retires: r82. From: b152 r227. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a term violates `v_t16`, if the person runs `model check`, then `model` shall exit with an error naming the term.
shall [x2: rule `v_t16` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term]
    violate(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r228
Retires: r83. From: b152 r228. Audit: fine.

```reading
While a term redefines a pack, when the person runs `model check`, `model` shall exit successfully.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: term, x2: pack]
    redefine(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
```

## r229
Retires: r84. From: b152 r229. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `bare-plural`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `bare-plural` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r230
Retires: r85. From: b152 r230. Audit: distortion, fixed by section 5 ("does not agree").

```reading
If the person runs `model parse` on a requirement that uses a term that does not agree with its subject, then `model` shall refuse the command and name the term.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: term, x5: subject]
    of(x5, x4)
    not
      agree(subject: x4, with: x5)
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r231
Retires: r86. From: b152 r231. Audit: fine, R2 fixed (phase 3): the two cases of the "or" split into r231 and r285.

```reading
If the person runs `model parse` on a requirement whose precondition uses a term whose aspect is `action`, then `model` shall refuse the command and name the requirement.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: precondition, x5: term]
    of(x4, x3)
    aspect(x5) = `action`
    use#2(subject: x4, object: x5)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x3)
```

## r232
Retires: r87. From: b152 r232. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `option-set-to`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `option-set-to` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r233
Retires: r88. From: b152 r233. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `of-relation`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `of-relation` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r234
Retires: r89. From: b152 r234. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `no-noun`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `no-noun` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r235
Retires: r90. From: b152 r235. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `compound`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `compound` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r236
Retires: r91. From: b152 r236. Audit: coined, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `only`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `only` (constant), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r237
Retires: r92. From: b152 r237. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `rc-object`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `rc-object` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r238
Retires: r93. From: b152 r238. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `rc-whose`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `rc-whose` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r239
Retires: r94. From: b152 r239. Audit: fine.

```reading
If the person runs `model parse` on a requirement that has more than one logical form, then `model` shall refuse the command and name the requirement.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x5: tool `model` (constant)]
  if [x3: requirement]
    count more than 1 [x4: logical form]
      scope
        of(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x3)
```

## r240
Retires: r95. From: b152 r240, plan phase 22. Audit: fine, the artifact line (phase 22): one logical form of a requirement that conforms to the language reference; the option in the trigger (phase 11).

```reading
When the person runs `model parse` with the `--form` option on a requirement that conforms to the language reference, `model` shall print one logical form of the requirement and exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x3: option `--form` (parameter), x5: artifact the language reference (constant), x6: tool `model` (constant)]
  when [x4: requirement]
    conforms(x4, x5)
    run(e1, subject: x1, object: x2, with: x3, on: x4)
  response
    count exactly 1 [x7: logical form]
      of(x7, x4)
      scope
        print(e2, subject: x6, object: x7)
    exit(e3, subject: x6, successfully)
```

## r241
Retires: r96. From: b152 r241. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `this`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `this` (constant), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r242
Retires: r97. From: b152 r242. Audit: fine.

```reading
If the person runs `model parse` on a requirement that uses a definite noun phrase that has no antecedent, then `model` shall refuse the command and name the definite noun phrase.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: definite noun phrase]
    not [x5: antecedent]
      of(x5, x4)
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r243
Retires: r98. From: b152 r243. Audit: fine.

```reading
If the person runs `model parse` on a requirement whose precondition uses a negated indefinite, then `model` shall refuse the command and name the negated indefinite.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: precondition, x5: negated indefinite]
    of(x4, x3)
    use#2(subject: x4, object: x5)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x5)
```

## r244
Retires: r99. From: b152 r244. Audit: fine, the modal adverb named by its code in grammar/constructs.md.

```reading
While a requirement has no trigger and the requirement does not use `always-never`, if the person runs `model parse` on the requirement, then `model` shall refuse the command and name the requirement.
shall [x3: thing `always-never` (parameter), x4: agent the person (constant), x5: command `model parse` (parameter), x6: tool `model` (constant)]
  while [x1: requirement]
    not [x2: trigger]
      of(x2, x1)
    not
      use#2(subject: x1, object: x3)
  if
    run(e1, subject: x4, object: x5, on: x1)
  response
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x1)
```

## r245
Retires: r100. From: b152 r245. Audit: fine.

```reading
If the person runs `model parse` on a fragment, then `model` shall refuse the command, name the fragment and print a term.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: tool `model` (constant)]
  if [x3: fragment]
    run(e1, subject: x1, object: x2, on: x3)
  response [x5: term]
    refuse(e2, subject: x4, object: x2)
    name(e3, subject: x4, object: x3)
    print(e4, subject: x4, object: x5)
```

## r246
Retires: r101. From: b152 r246. Audit: distortion, kept by the person's choice of the rule catalogue (b123).

```reading
While a requirement violates `w_example`, when the person runs `model check`, `model` shall print the requirement.
shall [x2: rule `w_example` (parameter), x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: requirement]
    violate(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x1)
```

## r247
Retires: r131. From: b152 r247. Audit: coined, fixed with identity ("another requirement", phase 8); "restriction" named by its code.

```reading
While a requirement of a capability uses `only` and the requirement allows an act that another requirement of the capability obliges, when the person runs `model logic`, `model` shall exit successfully.
shall [x3: thing `only` (constant), x6: agent the person (constant), x7: command `model logic` (parameter), x8: tool `model` (constant)]
  while [x1: requirement, x2: capability, x4: act, x5: requirement]
    of(x1, x2)
    use#2(subject: x1, object: x3)
    distinct(x5, x1)
    of(x5, x2)
    oblige(subject: x5, object: x4)
    allow(subject: x1, object: x4)
  when
    run(e1, subject: x6, object: x7)
  response
    exit(e2, subject: x8, successfully)
```

## r248
Retires: r132. From: b152 r248. Audit: distortion, fixed with identity ("another requirement" that "has the trigger of the requirement", phase 8); the universal quantifier named by its code.

```reading
While a requirement of a capability uses `every` and the requirement obliges an act and another requirement of the capability that has the trigger of the requirement forbids the act, when the person runs `model logic`, `model` shall print `L1`.
shall [x3: thing `every` (parameter), x7: agent the person (constant), x8: command `model logic` (parameter), x9: tool `model` (constant), x10: thing `L1` (constant)]
  while [x1: requirement, x2: capability, x4: act, x5: requirement, x6: trigger]
    of(x1, x2)
    use#2(subject: x1, object: x3)
    oblige(subject: x1, object: x4)
    distinct(x5, x1)
    of(x5, x2)
    of(x6, x1)
    of(x6, x5)
    forbid(subject: x5, object: x4)
  when
    run(e1, subject: x7, object: x8)
  response
    print(e2, subject: x9, object: x10)
```

## r249
Retires: r133. From: b152 r249. Audit: distortion, fixed with identity ("another requirement", phase 8).

```reading
While a requirement of a capability overrides another requirement of the capability, when the person runs `model logic`, `model` shall exit successfully.
shall [x4: agent the person (constant), x5: command `model logic` (parameter), x6: tool `model` (constant)]
  while [x1: requirement, x2: capability, x3: requirement]
    of(x1, x2)
    distinct(x3, x1)
    of(x3, x2)
    override(subject: x1, object: x3)
  when
    run(e1, subject: x4, object: x5)
  response
    exit(e2, subject: x6, successfully)
```

## r250
Retires: r134. From: b152 r250. Audit: distortion.

```reading
While a universal condition forbids an act that a requirement of a capability obliges, when the person runs `model logic`, `model` shall print the universal condition.
shall [x5: agent the person (constant), x6: command `model logic` (parameter), x7: tool `model` (constant)]
  while [x1: universal condition, x2: act, x3: requirement, x4: capability]
    of(x3, x4)
    oblige(subject: x3, object: x2)
    forbid(subject: x1, object: x2)
  when
    run(e1, subject: x5, object: x6)
  response
    print(e2, subject: x7, object: x1)
```

## r251
Retires: r135. From: b152 r251. Audit: distortion. Known limit: a `not` over a verb inside a "no" box ("no consequence that no premise entails" is not read by `model logic`), said with the verb add.

```reading
While a requirement has a consequence and the requirement adds no consequence, when the person runs `model logic`, `model` shall print `L8`.
shall [x4: agent the person (constant), x5: command `model logic` (parameter), x6: tool `model` (constant), x7: thing `L8` (constant)]
  while [x1: requirement, x2: consequence]
    of(x2, x1)
    not [x3: consequence]
      add(subject: x1, object: x3)
  when
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x7)
```

## r252
Retires: r136. From: b152 r252. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `count`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `count` (constant), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r253
Retires: r137. From: b152 r253. Audit: distortion. Known limit: #1 (the verb contradict carries "of one act under one trigger and condition").

```reading
While a capability holds a count that contradicts a count, when the person runs `model logic`, `model` shall print `L1`.
shall [x4: agent the person (constant), x5: command `model logic` (parameter), x6: tool `model` (constant), x7: thing `L1` (constant)]
  while [x1: capability, x2: count, x3: count]
    contradict(subject: x2, object: x3)
    in(x2, x1)
  when
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x7)
```

## r254
Retires: r138. From: b152 r254. Audit: coined, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `moment-compare`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `moment-compare` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r255
Retires: r139. From: b152 r255. Audit: fine. Known limit: #1 (the clock trigger: the time pack is not imported here).

```reading
When the person runs `model parse` on a requirement that uses a clock trigger, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x5: tool `model` (constant)]
  when [x3: requirement, x4: clock trigger]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r256
Retires: r140. From: b152 r256. Audit: fine. Known limit: #1 (the perfect: the construct's code `done` is a value of this bounded context).

```reading
When the person runs `model parse` on a requirement whose precondition uses a perfect, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  when [x3: requirement, x4: precondition, x5: perfect]
    of(x4, x3)
    use#2(subject: x4, object: x5)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x6, successfully)
```

## r257
Retires: r141. From: b152 r257. Audit: coined. Known limit: #1 (a number where a duration is due, and its unit).

```reading
If the person runs `model parse` on a requirement that uses a number that has no unit, then `model` shall refuse the command and name the requirement.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: number]
    not [x5: unit]
      of(x5, x4)
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x3)
```

## r258
Retires: r142. From: b152 r258. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `may`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `may` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r259
Retires: r143. From: b152 r259. Audit: fine, the construct named by its code in grammar/constructs.md (phase 12.5).

```reading
When the person runs `model parse` on a requirement that uses `always-never`, `model` shall exit successfully.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: thing `always-never` (parameter), x5: tool `model` (constant)]
  when [x3: requirement]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, successfully)
```

## r260
Retires: r144. From: b152 r260. Audit: fine, fixed with identity ("another requirement", phase 8).

```reading
While a requirement of a capability forbids an act that another requirement of the capability permits, when the person runs `model logic`, `model` shall print `L7`.
shall [x5: agent the person (constant), x6: command `model logic` (parameter), x7: tool `model` (constant), x8: thing `L7` (constant)]
  while [x1: requirement, x2: capability, x3: act, x4: requirement]
    of(x1, x2)
    distinct(x4, x1)
    of(x4, x2)
    permit(subject: x4, object: x3)
    forbid(subject: x1, object: x3)
  when
    run(e1, subject: x5, object: x6)
  response
    print(e2, subject: x7, object: x8)
```

## r261
Retires: r145. From: b152 r261. Audit: fine.

```reading
While the language of a capability is `codified-2`, when the person runs `model logic`, `model` shall exit successfully.
shall [x2: agent the person (constant), x3: command `model logic` (parameter), x4: tool `model` (constant)]
  while [x1: capability]
    language(x1) = `codified-2`
  when
    run(e1, subject: x2, object: x3)
  response
    exit(e2, subject: x4, successfully)
```

## r262
Retires: r157. From: b152 r262. Audit: fine.

```reading
When the person runs `model explain` on a requirement that uses a refusal, `model` shall print a universal condition and a term.
shall [x1: agent the person (constant), x2: command `model explain` (parameter), x5: tool `model` (constant)]
  when [x3: requirement, x4: refusal]
    use#2(subject: x3, object: x4)
    run(e1, subject: x1, object: x2, on: x3)
  response [x6: universal condition, x7: term]
    print(e2, subject: x5, object: x6)
    print(e3, subject: x5, object: x7)
```

## r263
Retires: r158. From: b152 r263. Audit: distortion.

```reading
When the person runs `model explain` on a requirement that a requirement overrides, `model` shall print a requirement that uses a refusal.
shall [x1: agent the person (constant), x2: command `model explain` (parameter), x5: tool `model` (constant)]
  when [x3: requirement, x4: requirement]
    override(subject: x4, object: x3)
    run(e1, subject: x1, object: x2, on: x3)
  response [x6: requirement, x7: refusal]
    use#2(subject: x6, object: x7)
    print(e2, subject: x5, object: x6)
```

## r264
Retires: r159. From: b152 r264. Audit: fine.

```reading
If the person runs `model explain` on a requirement id that no capability holds, then `model` shall refuse the command and name the requirement id.
shall [x1: agent the person (constant), x2: command `model explain` (parameter), x5: tool `model` (constant)]
  if [x3: requirement id]
    not [x4: capability]
      in(x3, x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x3)
```

## r279
Retires: r160-r173 (the construct lines of b197 and b215-b222; b152 r265-r278 and b238 r174-r175 not laid). From: plan phase 22 (the artifact lines). The corpus and language.md's twins check each construct.

```reading
If the person runs `model parse` on a requirement that does not conform to the language reference, then `model` shall refuse the command and name the requirement.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x4: artifact the language reference (constant), x5: tool `model` (constant)]
  if [x3: requirement]
    not
      conforms(x3, x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x3)
```

## r280
Retires: r160-r173 (the construct lines of b197 and b215-b222; b152 r265-r278 and b238 r174-r175 not laid). From: plan phase 22 (the artifact lines). The corpus and language.md's twins check each construct.

```reading
While a requirement of a capability conforms to the language reference, when the person runs `model logic` on the capability, `model` shall translate the requirement.
shall [x3: artifact the language reference (constant), x4: agent the person (constant), x5: command `model logic` (parameter), x6: tool `model` (constant)]
  while [x1: requirement, x2: capability]
    of(x1, x2)
    conforms(x1, x3)
  when
    run(e1, subject: x4, object: x5, on: x2)
  response
    translate(e2, subject: x6, object: x1)
```

## r281
Retires: r160-r173 (the construct lines of b197 and b215-b222; b152 r265-r278 and b238 r174-r175 not laid). From: plan phase 22 (the artifact lines). The corpus and language.md's twins check each construct.

```reading
While the corpus holds a logical form of a requirement, when the person runs `model parse` with the `--form` option on the requirement, `model` shall print the logical form.
shall [x1: corpus "the corpus of the bounded context the command runs in" (indexical), x4: agent the person (constant), x5: command `model parse` (parameter), x6: option `--form` (parameter), x7: tool `model` (constant)]
  while [x2: logical form, x3: requirement]
    of(x2, x3)
    in(x2, x1)
  when
    run(e1, subject: x4, object: x5, with: x6, on: x3)
  response
    print(e2, subject: x7, object: x2)
```

## r282
From: b239 r174. Known limit: #16 ("unchanged since": the parse cache's key, the requirement's text, its grammar's sources and its lexicon's words, carries it).

```reading
While a parse cache holds the parse of a requirement, when the person runs `model parse` on the requirement, `model` shall read the parse cache, write no compiled grammar and exit successfully.
shall [x4: agent the person (constant), x5: command `model parse` (parameter), x6: tool `model` (constant)]
  while [x1: parse cache, x2: requirement, x3: parse]
    of(x3, x2)
    in(x3, x1)
  when
    run(e1, subject: x4, object: x5, on: x2)
  response
    read(e2, subject: x6, object: x1)
    not [x7: compiled grammar]
      write(e3, subject: x6, object: x7)
    exit(e4, subject: x6, successfully)
```

## r283
From: b239 r175. Known limit: #16 ("unchanged since": the parse cache's key, the requirement's text, its grammar's sources and its lexicon's words, carries it).

```reading
While a requirement has a parse that no parse cache holds, when the person runs `model parse` on the requirement, `model` shall write a parse cache and exit successfully.
shall [x4: agent the person (constant), x5: command `model parse` (parameter), x6: tool `model` (constant)]
  while [x1: requirement, x2: parse]
    not [x3: parse cache]
      in(x2, x3)
    of(x2, x1)
  when
    run(e1, subject: x4, object: x5, on: x1)
  response [x7: parse cache]
    write(e2, subject: x6, object: x7)
    exit(e3, subject: x6, successfully)
```

## r284
From: b239 r176. Known limit: #16 ("unchanged since": the parse cache's key, the requirement's text, its grammar's sources and its lexicon's words, carries it).

```reading
While a requirement has a parse that no parse cache holds and the compiled grammar of the requirement exists, when the person runs `model parse` on the requirement, `model` shall use the compiled grammar, write no compiled grammar and exit successfully.
shall [x5: agent the person (constant), x6: command `model parse` (parameter), x7: tool `model` (constant)]
  while [x1: requirement, x2: parse, x4: compiled grammar]
    not [x3: parse cache]
      in(x2, x3)
    of(x2, x1)
    of(x4, x1)
    exists(x4)
  when
    run(e1, subject: x5, object: x6, on: x1)
  response
    use(e2, subject: x7, object: x4)
    not [x8: compiled grammar]
      write(e3, subject: x7, object: x8)
    exit(e4, subject: x7, successfully)
```

## r285
From: b152 r231 (its second case). Audit: fine; R2 fixed (phase 3): the two cases of the "or" split into r231 and r285.

```reading
If the person runs `model parse` on a requirement whose trigger uses a term whose aspect is `state`, then `model` shall refuse the command and name the requirement.
shall [x1: agent the person (constant), x2: command `model parse` (parameter), x6: tool `model` (constant)]
  if [x3: requirement, x4: trigger, x5: term]
    of(x4, x3)
    aspect(x5) = `state`
    use#2(subject: x4, object: x5)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x3)
```

## r286
Retires: r40 (with r194). From: b152 r194 (its second case). Audit: distortion, fixed by section 5 (a section by its heading).

```reading
While a design-decision has no section whose heading is `Decision`, if the person runs `model check`, then `model` shall exit with an error naming the design-decision.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: design-decision]
    not [x2: section]
      heading(x2) = `Decision`
      of(x2, x1)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r287
From: b160 r71, in the grammar 4 form b160's notes give. Not in the audit (b160 is no reword item); its coined "unrecodified" is said with the language attribute of the capability.

```reading
If the person runs `model check` on a capability whose language is `codified-1`, then `model` shall refuse the command and name `migrate upgrade`.
shall [x1: agent the person (constant), x2: command `model check` (parameter), x4: tool `model` (constant), x5: thing `migrate upgrade` (parameter)]
  if [x3: capability]
    language(x3) = `codified-1`
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x4, object: x2)
    name(e3, subject: x4, object: x5)
```
