---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: a session reading or generating feature files
group: service
language: codified-2
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/plugin-scenarios-run-as-pytest-bdd, design-decision/query-commands-answer-in-their-output]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g19, r19, g20, r20, g21, r21, g22, r22, g23, r23, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g40, r40, g41, r41, g42, r42, g43, r43, g44, r44, g105, r105]
unbuilt: []
---

# Feature file tools

## Purpose
`scripts/features` reads Gherkin feature files without the test runner: it counts and lists scenarios by tag or
title, lists the deprecated scenarios kept from before the conversion, and verifies that every scenario has exactly
one test binding it. It writes each codified service capability's feature file from its requirement groups
(`generate`), and checks that every step of a generated feature has a handler (`vocab`). It is not a Gherkin runner
and runs no test; it edits no feature file by hand, since the generator owns them. Which sentences `generate` writes
the scenario of is the language reference's to say (`grammar/language.md`, its constructs and their tested lines),
not a line here for each construct.

## Terms

- **feature file** (noun): a `*.feature` file under the directory `--dir` names (default `features`), read line by line. Kind of: file.
- **test module** (noun): a Python file under the directory `--tests` names (default `tests`), with its bindings. Kind of: file.
- **subdirectory** (noun): a directory under the directory `--dir` names. Kind of: file.
- **docstring** (noun): the text of a step between two lines of `"""` or of three backticks, in a feature file. Kind of: text.
- **tag** (noun): a Gherkin tag of a scenario or of a feature file, as `@deprecated`. Kind of: text.
- **requirement tag** (noun): a tag `@r<n>` of a scenario, which names a requirement of its group. Kind of: text.
- **scenario line** (noun): a line that starts `Scenario:`. Kind of: text.
- **scenario outline** (noun): a Scenario Outline of a feature file, with its Examples tables. Kind of: text.
- **examples row** (noun): one row of values of an Examples table of a scenario outline. Kind of: text.
- **rule block** (noun): a `Rule:` block of a feature file. Kind of: text.
- **scenario title** (noun): the text after `Scenario:` that names a scenario. Kind of: text.
- **replacement** (noun): the scenario that a scenario tagged `@deprecated` names after `Deprecated for:`. Kind of: scenario.
- **binding** (noun): a `scenario(<feature>, "<title>")` or `scenarios(<path>, ...)` call of a test module. Kind of: text.
- **scenarios call** (noun): a `scenarios(<path>, ...)` call of a test module. Kind of: binding.
- **search text** (noun): the text `features list` is given with its `--title` option, which the scenario titles it prints contain. Kind of: text.
- **handler** (noun): a function of `tests/scenarios/` that a step runs. Kind of: thing.
- **contain** (verb, state): a text holds another text within it. Forms: contains, contained. Frame: text contains text.
- **bind** (verb, state): a binding names a scenario, by its title or by its feature file, so that a test runs the scenario. Forms: binds, bound. Frame: binding binds scenario.
- **entail** (verb, state): a universal condition gives a step from the other steps of its scenario. Forms: entails, entailed. Frame: universal condition entails step.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| docstring | of | feature file |  |
| tag | in | docstring |  |
| scenario line | in | docstring |  |
| tag | of | feature file |  |
| tag | of | scenario |  |
| requirement tag | of | scenario |  |
| scenario outline | of | feature file |  |
| examples row | of | scenario outline |  |
| rule block | of | feature file | one |
| feature file | in | subdirectory | one |
| scenario | of | feature file |  |
| scenario title | of | scenario | one |
| replacement | of | scenario | one |
| binding | of | test module |  |
| scenario | of | feature |  |
| feature | of | capability | one |
| step | of | feature |  |
| handler | of | step |  |
| requirement group | of | capability |  |
| requirement | of | requirement group |  |
| scenario | of | requirement group | one |

## Behaviour

### [g88] `features count --by-tag` counts no scenario line of a docstring
Restates: r1@0.29, r4@0.29.
- [r88] While a docstring of a feature file contains a tag and a scenario line, when the person runs `features count` with the `--by-tag` option, `features` shall print the number of scenarios of the feature file.


### [g89] `features count --by-tag` counts each examples row of a scenario outline as a scenario
Restates: r4@0.29.
- [r89] While a feature file has a scenario outline and the feature file has no scenario, when the person runs `features count` with the `--by-tag` option, `features` shall print the number of examples rows of the scenario outline.

### [g90] a tag in a docstring is no tag of its feature file
Restates: r1@0.29, r7@0.29.
- [r90] While a docstring of a feature file contains a tag and the feature file does not have the tag, when the person runs `features list` with the `--tag` option set to the tag, `features` shall exit successfully and not print the feature file.


### [g91] a feature file in a subdirectory is read
Restates: r1@0.29.
- [r91] While a feature file in a subdirectory has a scenario, when the person runs `features list` with the `--title` option set to the scenario title of the scenario, `features` shall print the feature file.


### [g92] `features list --tag` prints every scenario of a feature file that has the tag
Restates: r5@0.29.
- [r92] While a feature file has a tag, when the person runs `features list` with the `--tag` option set to the tag, `features` shall print every scenario of the feature file.


### [g93] `features list --tag` prints a scenario that has the tag
Restates: r5@0.29.
- [r93] While a scenario has a tag, when the person runs `features list` with the `--tag` option set to the tag, `features` shall print the scenario.


### [g94] `features list --title` prints each scenario whose title contains the text
Restates: r5@0.29.
- [r94] When the person runs `features list` with the `--title` option set to a search text, `features` shall print every scenario whose scenario title contains the search text.


### [g95] `features list --json` prints the scenarios it found as one JSON object
Restates: r60@0.29.
- [r95] When the person runs `features list` with the `--json` option and the `--title` option set to a search text, `features` shall print every scenario whose scenario title contains the search text.


### [g96] a feature file with a rule block is refused
Restates: r2@0.29, r46@0.29.
- [r96] While a feature file has a rule block, if the person runs `features count` with the `--by-tag` option, then `features` shall refuse the command and name the feature file.


### [g97] `features deprecated` prints each deprecated scenario with the tags of its replacement
Restates: r21@0.29.
- [r97] While a replacement of a scenario has a requirement tag and the scenario has the `@deprecated` tag, when the person runs `features deprecated`, `features` shall print the scenario and every requirement tag of the replacement.


### [g98] `features deprecated` says when nothing is deprecated
Restates: r21@0.29.
- [r98] While no scenario has the `@deprecated` tag, when the person runs `features deprecated`, `features` shall print `none deprecated`.


### [g99] `features deprecated --json` prints the deprecated scenarios as one JSON object
Restates: r61@0.29.
- [r99] While a scenario has the `@deprecated` tag, when the person runs `features deprecated` with the `--json` option, `features` shall print the scenario title of the scenario.


### [g100] `features bindings` says so when every binding names a scenario
Restates: r26@0.29.
- [r100] While every binding binds a scenario, when the person runs `features bindings`, `features` shall print `every binding names a scenario` and exit successfully.


### [g101] `features bindings` names the test module of a binding that binds no scenario
Restates: r25@0.29.
- [r101] While a binding of a test module binds no scenario, if the person runs `features bindings`, then `features` shall exit with an error naming the test module and change no file.


### [g102] a scenarios call binds every scenario of the feature file it names
Restates: r57@0.29.
- [r102] While a scenarios call binds a scenario of a feature file, when the person runs `features bindings` with the `--unbound` option, `features` shall exit successfully and not print a scenario of the feature file.


### [g103] `features bindings --unbound` names a scenario that no binding binds
Restates: r58@0.29.
- [r103] While a feature file has a scenario that no binding binds, if the person runs `features bindings` with the `--unbound` option, then `features` shall exit with an error naming the scenario and change no file.


### [g104] `features bindings --unbound --json` names a scenario that no binding binds
Restates: r62@0.29.
- [r104] While a feature file has a scenario that no binding binds, if the person runs `features bindings` with the `--unbound` and `--json` options, then `features` shall exit with an error naming the scenario and change no file.


### [g106] `features generate --check` names a feature with a scenario that no requirement group of its capability has
- [r106] While the feature of a capability has a scenario that no requirement group has, if the person runs `features generate` with the `--check` option, then `features` shall exit with an error naming the feature and change no file.

```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-2
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **book** (noun): a thing.
  ## Behaviour
  ## Not yet
  ## Dropped
the feature file `features/shelf.feature` holds:
  Feature: Shelf
    Scenario: Edited by hand
      Given a step
```

### [g107] `features vocab --check` names a step with no handler and its feature
- [r107] While a step of a feature has no handler, if the person runs `features vocab` with the `--check` option, then `features` shall exit with an error naming the step and the feature and change no file.

```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-2
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **book** (noun): a thing.
  ## Behaviour
  ## Not yet
  ## Dropped
the feature file `features/shelf.feature` holds:
  # generated from spec/capabilities/shelf.md by features generate; do not edit
  Feature: shelf
    Narrator: a client
    @g1 @r1
    Scenario: Lending
      When the person lends a book
```

### [g108] `features generate` writes a scenario of every requirement group of a capability in the language reference
- [r108] While the language of a capability is `codified-2` and every requirement of the capability conforms to the language reference and every requirement of the capability uses the `shall` construct, when the person runs `features generate` on the capability, `features` shall write the scenario of every requirement group of the capability.

### [g109] `features generate` leaves out a step that a universal condition entails
- [r109] While the language of a capability is `codified-2`, when the person runs `features generate` on the capability, `features` shall not write a step that a universal condition entails.

### [g110] `features generate` writes the feature of a codified service capability
- [r110] While the group of a capability is `service` and the language of the capability is `codified-2`, when the person runs `features generate`, `features` shall write the feature of the capability and print the feature.

```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-2
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **book** (noun): a thing.
  ## Behaviour
  ## Not yet
  ## Dropped
```

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next scenario's tag
  lines. A Scenario Outline counts once per Examples row, and each scenario takes its feature's tags and its Examples
  table's tags.
- `list --tag` takes the tag with its leading `@` or without; `list` matching nothing prints nothing and exits 0.
- Output lines: `list` prints `<path>: <title>`; `deprecated` prints
  `<path>: <title> | for: <what> | <replacement's path> @r<n>` or `none deprecated`; `bindings` prints
  `<path>:<line>: no scenario titled "<title>" in <feature>`, and with `--unbound`
  `<feature path>: <title> | bound by no test` or `<feature path>: <title> | bound by <module>:<line>, <module>:<line>`.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up among
  the module's own top-level assignments. A `scenario` or `scenarios` path names a feature file by its base name, or
  a directory by every feature file under it. A test module under `--tests` that does not parse is refused, named.
- `bindings --unbound` takes feature files after it; with none, every feature file under `--dir`. A scenario bound by
  more than one call is printed with each call's module and line.
- `generate` and `vocab` are the GF conversion's design §13.4 and §14: `generate --check` with no names prints
  `skipped <c>: not codified` for each service capability not yet codified; naming one exits 2; `--preview <file>`
  prints a draft's feature and writes nothing. `vocab --check --tests <dir> [<feature>...]` loads `<dir>`'s
  `world_*.py` and `*_handlers*.py` and names each step with no handler and each key two handlers claim.
- Exit code: 0 success, 1 a check failed or a file was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.

## Dropped
- r12@0.29: removed with `features move`: the generator owns the feature files (the GF conversion's design §15)
- r13@0.29: removed with `features move`: the generator owns the feature files (the GF conversion's design §15)
- r14@0.29: removed with `features move`: the generator owns the feature files (the GF conversion's design §15)
- r16@0.29: removed with `features verify-moved`: the generator owns the feature files (the GF conversion's design §15)
- r17@0.29: removed with `features verify-moved`: the generator owns the feature files (the GF conversion's design §15)
- r19@0.29: removed with `features deprecate`: the generator owns the feature files (the GF conversion's design §15)
- r23@0.29: removed with `features retire`: the generator owns the feature files (the GF conversion's design §15)
- r24@0.29: removed with `features retire`: the generator owns the feature files (the GF conversion's design §15)
- r28@0.29: removed with `features rebind`: the generator owns the feature files (the GF conversion's design §15)
- r29@0.29: removed with `features rebind`: the generator owns the feature files (the GF conversion's design §15)
- r35@0.29: the title lookup of `tag`, `move`, `deprecate` and `retire`, which are removed: the generator owns the feature files (the GF conversion's design §15)
- r51@0.29: removed with `features tag`: the generator owns the feature files (the GF conversion's design §15)
- r52@0.29: `--file` chose the file of a title for `tag`, `move`, `deprecate` and `retire`, which are removed: the generator owns the feature files (the GF conversion's design §15)
- r56@0.29: removed with `features rebind`: the generator owns the feature files (the GF conversion's design §15)
