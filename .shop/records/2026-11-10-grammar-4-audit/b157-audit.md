# Audit of b157: feature-file-tools and readiness in grammar 4

This audit covers 62 lines: b157's grammar-4 rewordings (feature-file-tools r45-r87, readiness r20-r37) and
readiness r4, which keeps its id. Each line was judged against its original spec line, that line's coined adjective
and given block, and phase 3's candidate and note. All 62 were laid into a copy of `spec/` (`backlog_lines.lay`), and
every one parses to one form (`model parse --capability <cap> --form`). The verdicts are about meaning. Per-line
evidence is in `audit.tsv`.

## Counts

| | fine | distortion | unsayable | coined | total |
|---|---|---|---|---|---|
| feature-file-tools | 7 | 9 | 0 | 27 | 43 |
| readiness | 9 | 8 | 0 | 2 | 19 |
| all | 16 | 17 | 0 | 29 | 62 |

There are no "unsayable" verdicts, because each meaning that phase 3 found unsayable was moved into a gloss:

- closure ("however deep") went into `subdirectory` (r48); its form reads `in(x1, x2)`, which is one level;
- the counterfactual ("what generate would write") went into `differ` (r61); its form reads
  `differ(subject: x2, from: x1)`;
- distribution ("one scenario per Examples row") went into `count` (r46); its form has `count(e2, features, row)`,
  and nothing ties it to the scenario count.

## Missing constructs, with the number of lines

| Construct | Lines | Which |
|---|---|---|
| Meta level: a line's form named as a noun | 25 | ff r63, r64, r66-r87 |
| Attribute with a value (`language` = `codified-2`), in place of the noun "codified-2 marker" | 25 | ff r65-r87, readiness r31, r35 (the main fault in r65, r31, r35) |
| Declared literal constant, in place of a proper noun named after the printed text | 14 | ff r53, r55, r76-r87 |
| Counterfactual | 4 | ff r61, r64, readiness r27, r30 |
| Conformance to a schema artifact | 3 | readiness r21, r24, r26 |
| "or" between relative clauses | 3 | ff r49, r58, r59 |
| "the number of" | 2 | ff r45, r46 |
| Live against retired (a qualifier dropped) | 2 | readiness r29, r37 |
| Distribution | 1 | ff r46 |
| Transitive closure | 1 | ff r48 |
| Negated relative clause, in place of the polar verb `fail` | 1 | readiness r33 |
| A state left to If precedence | 1 | ff r55 |
| A condition dropped ("codified") | 1 | ff r60 |

## Worst examples

1. **ff r64**: "While a requirement of a capability has a refusal and a premise entails a then step, ... and not
   write the then step." In its form, `x5: then step` is tied to no scenario of the requirement. It is a step
   generate *would* write. The line depends on three glosses: `refusal`, `premise` (a universal condition *or* a pack
   definition) and `entail`.
2. **ff r86/r87**: "not write a scenario line of the requirement group". The row
   `scenario line | of | requirement group` is a category error. The line also negates a K with no antecedent, and
   `features generate` stops on it (b237). It rests on the meta nouns `permission` and `necessity`.
3. **ff r66-r85**: twenty lines with one template, "a requirement of the capability has an X". X is a noun coined
   for a grammar construct (`embedded definite`, `outer definite` and the like): the old coined adjectives made into
   nouns, which is the anti-goal exactly. Their responses are thin.
4. **ff r61**: "a capability has a feature that differs from the capability". Read as English this is always true.
   The comparison with what generate writes exists only in the gloss.
5. **ff r55**: "When the person runs `features bindings`, `features` shall print the all-bound note". The state
   "every binding names a scenario" is gone from the line. It survives only through r56's If precedence and in the
   proper noun's name.
6. **readiness r30**: `lexicon problem` hides a comparison of the lexicon with the item against the lexicon without
   it. It also puts a problem that a *line* brings onto a *term*.
7. **readiness r29/r37**: "a requirement id that no capability has" drops "live". A capability still has a retired
   id under `retired:`, which is the case `--retires` must refuse.

## What a rewording alone fixes

I checked these by parsing the rewordings in the laid copy.

- **ff r55**: "While every binding of a test module names a scenario title that a scenario has, ..." parses, to an
  `every` box in the While.
- **ff r60**: put "codified" back.
- **ff r49**: needs a second line for a scenario's own tag. "every scenario that has the tag or whose feature file
  has the tag" does not parse (it stops at "whose"), so one line cannot say it.
- **ff r65, readiness r31, r35**, and the marker in ff r66-r87: these need a `language` attribute of capability. A
  glossary entry, not grammar, adds it. Today "the language of a capability is `codified-2`" stops at "language".
  With the entry, the conditions become an attribute phrase and the responses a setting response.
- **readiness r33**: "every bar check of the readiness bar that the item does not meet". R4 allows the negated
  relative clause; the verb "meet" needs a frame.
- **readiness r29, r37**: relate the id to a requirement, not to a capability, so that a retired line does not
  count.
- **ff r53** (and the notes in r55 and r76-r87): need a printed message declared as a constant. That is a vocabulary
  form, not grammar.

These need the grammar or an artifact:

- "the number of" and distribution: ff r45, r46.
- "or" over relative clauses: ff r58, r59 (confirmed absent).
- closure: ff r48.
- a counterfactual: ff r61, r64, readiness r27, r30.
- conformance to a schema: readiness r21, r24, r26. `conforms` is in the design, but there is no schema artifact.
- the meta level: ff r63-r87. A construct catalogue, like design-model-check's rule catalogue (b123), would let
  these lines name a construct instead of coining a noun for it.

## Notes

- R10 reads every command code as a **parameter**, for example `command \`features count --by-tag\` (parameter)`.
  So the command a line is about is bound by the scenario, not fixed by the rule. No line is marked down for it here.
- The 16 fine lines are the plain behaviour lines. Phase 3's noun-phrase constructs were enough for them.
