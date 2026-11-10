---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: a session reading or generating feature files
group: service
language: codified-1
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/plugin-scenarios-run-as-pytest-bdd, design-decision/query-commands-answer-in-their-output]
retired: []
unbuilt: []
---

# Feature file tools

## Purpose
`scripts/features` reads Gherkin feature files without the test runner: it counts and lists scenarios by tag or
title, lists the deprecated scenarios kept from before the conversion, and verifies that every scenario has exactly
one test binding it. It writes each codified service capability's feature file from its requirement groups
(`generate`), and checks that every step of a generated feature has a handler (`vocab`). It is not a Gherkin runner
and runs no test; it edits no feature file by hand, since the generator owns them.

## Terms
- **feature file** (noun): a `*.feature` file under the directory `--dir` names (default `features`), read line by
  line.
- **test module** (noun): a Python file under the directory `--tests` names (default `tests`) that binds scenarios
  with `scenario(<feature>, "<title>")` or `scenarios(<path>, ...)` calls.
- **nested** (adjective of feature file): a feature file with a docstring whose text has a tag and a `Scenario:` line.
- **outlined** (adjective of feature file): a feature file with a Scenario Outline of several Examples tables.
- **sectioned** (adjective of feature file): a feature file with a `Rule:` block.
- **deprecating** (adjective of feature file): a feature file with a scenario tagged `@deprecated` and its replacement.
- **undeprecated** (adjective of feature file): a feature file with no scenario tagged `@deprecated`.
- **resolving** (adjective of test module): a test module each of whose bindings names a scenario a feature file has.
- **dangling** (adjective of test module): a test module with a binding whose title no feature file has.
- **sweeping** (adjective of test module): a test module that binds every scenario of a feature file with one `scenarios(...)` call.
- **partial** (adjective of test module): a test module that leaves a scenario of its feature file unbound.

- **withholding** (adjective of requirement): a requirement whose response says with `shall not` that a verb with a recipient does not happen.

- **declining** (adjective of capability): a capability with a requirement whose response says that a tool shall refuse a command.
- **overstated** (adjective of file): a feature file with a Then step that a universal condition or a pack's definition entails from the other steps of its scenario.

## Behaviour

### [g1] `features count --by-tag` counts every scenario, and a docstring's text is none
Restates: r1@0.29, r4@0.29.
- [r1] While the feature file `features/notes.feature` is nested, when the person runs `features count --by-tag`,
  `features` shall print the number of scenarios.

### [g2] `features count --by-tag` counts a Scenario Outline once for each Examples row
Restates: r4@0.29.
- [r2] While the feature file `features/outline.feature` is outlined, when the person runs `features count --by-tag`,
  `features` shall print the number of scenarios.

### [g3] a docstring's text is no tag
Restates: r1@0.29, r7@0.29.
- [r3] While the feature file `features/notes.feature` is nested, when the person runs `features list --tag slice-9`,
  `features` shall exit successfully, and `features` shall not print the feature file `features/notes.feature`.

### [g4] every feature file under the directory is read, however deep
Restates: r1@0.29.
- [r4] When the person runs `features list --title Deep`, `features` shall print the feature file
  `features/sub/deep.feature`.

```given
the feature file `features/sub/deep.feature` holds:
  Feature: Deep
    Scenario: Deep down
      Given a step
```

### [g5] `features list --tag` prints each scenario whose tags, its feature's included, have the tag
Restates: r5@0.29.
- [r5] When the person runs `features list --tag cart`, `features` shall print the feature file
  `features/cart.feature` and "Adding".

```given
the feature file `features/cart.feature` holds:
  @cart
  Feature: Cart
    Scenario: Adding
      Given a step
```

### [g6] `features list --title` prints each scenario whose title holds the text
Restates: r5@0.29.
- [r6] When the person runs `features list --title Add`, `features` shall print the feature file
  `features/cart.feature` and "Adding".

```given
the feature file `features/cart.feature` holds:
  Feature: Cart
    Scenario: Adding
      Given a step
    Scenario: Paying
      Given a step
```

### [g7] `features list --json` prints the scenarios it found as one JSON object
Restates: r60@0.29.
- [r7] Where `--json` is given, when the person runs `features list --title Add`, `features` shall print the feature
  file `features/cart.feature` and "Adding".

```given
the feature file `features/cart.feature` holds:
  Feature: Cart
    Scenario: Adding
      Given a step
```

### [g8] a feature file with a `Rule:` block is refused
Restates: r2@0.29, r46@0.29.
- [r8] While the feature file `features/rule.feature` is sectioned, if the person runs `features count --by-tag`,
  then `features` shall exit with an error naming the feature file `features/rule.feature` and change nothing.

### [g9] `features deprecated` prints each deprecated scenario with what replaces it
Restates: r21@0.29.
- [r9] While the feature file `features/shelf.feature` is deprecating, when the person runs `features deprecated`,
  `features` shall print "Lending" and "@r4".

```given
the feature file `features/shelf.feature` holds:
  Feature: Shelf
    @deprecated
    Scenario: Lending (deprecated)
      Deprecated for: Lending a book
      Given a step
    @r4
    Scenario: Lending a book
      Given a step
```

### [g10] `features deprecated` says when nothing is deprecated
Restates: r21@0.29.
- [r10] While the feature file `features/shelf.feature` is undeprecated, when the person runs `features deprecated`,
  `features` shall print "none deprecated".

```given
the feature file `features/shelf.feature` holds:
  Feature: Shelf
    Scenario: Lending
      Given a step
```

### [g11] `features deprecated --json` prints the deprecated scenarios as one JSON object
Restates: r61@0.29.
- [r11] Where `--json` is given, when the person runs `features deprecated`, `features` shall print "Lending".

```given
the feature file `features/shelf.feature` holds:
  Feature: Shelf
    @deprecated
    Scenario: Lending (deprecated)
      Deprecated for: removal
      Given a step
```

### [g12] `features bindings` says so when every binding names a scenario
Restates: r26@0.29.
- [r12] While the test module `tests/test_cart.py` is resolving, when the person runs `features bindings`,
  `features` shall print "every binding names a scenario" and exit successfully.

```given
the feature file `features/cart.feature` holds:
  Feature: Cart
    Scenario: Adding
      Given a step
the test module `tests/test_cart.py` holds:
  from pytest_bdd import scenario
  @scenario("cart.feature", "Adding")
  def test_adding():
      pass
```

### [g13] `features bindings` names a binding whose title no feature file has
Restates: r25@0.29.
- [r13] While the test module `tests/test_cart.py` is dangling, if the person runs `features bindings`, then
  `features` shall exit with an error naming the test module `tests/test_cart.py` and change nothing.

```given
the feature file `features/cart.feature` holds:
  Feature: Cart
    Scenario: Adding
      Given a step
the test module `tests/test_cart.py` holds:
  from pytest_bdd import scenario
  @scenario("cart.feature", "Paying")
  def test_paying():
      pass
```

### [g14] a `scenarios(...)` call binds every scenario of the feature file it names
Restates: r57@0.29.
- [r14] While the test module `tests/test_cart.py` is sweeping, when the person runs `features bindings --unbound`,
  `features` shall exit successfully.

```given
the feature file `features/cart.feature` holds:
  Feature: Cart
    Scenario: Adding
      Given a step
    Scenario: Paying
      Given a step
the test module `tests/test_cart.py` holds:
  from pytest_bdd import scenarios
  scenarios("cart.feature")
```

### [g15] `features bindings --unbound` names a scenario no test binds
Restates: r58@0.29.
- [r15] While the test module `tests/test_cart.py` is partial, if the person runs `features bindings --unbound`, then
  `features` shall exit with an error naming "Paying" and change nothing.

```given
the feature file `features/cart.feature` holds:
  Feature: Cart
    Scenario: Adding
      Given a step
    Scenario: Paying
      Given a step
the test module `tests/test_cart.py` holds:
  from pytest_bdd import scenario
  @scenario("cart.feature", "Adding")
  def test_adding():
      pass
```

### [g16] `features bindings --json` prints what it found wrong as one JSON object
Restates: r62@0.29.
- [r16] Where `--json` is given, when the person runs `features bindings --unbound`, `features` shall print "Paying".

```given
the feature file `features/cart.feature` holds:
  Feature: Cart
    Scenario: Adding
      Given a step
    Scenario: Paying
      Given a step
the test module `tests/test_cart.py` holds:
  from pytest_bdd import scenario
  @scenario("cart.feature", "Adding")
  def test_adding():
      pass
```

### [g17] `features generate` writes the feature file of a codified service capability
- [r17] When the person runs `features generate`, `features` shall print the feature file `features/shelf.feature`
  and exit successfully.

```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-1
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

### [g18] `features generate --check` names a feature file that differs from its capability
- [r18] Where `--check` is given, if the person runs `features generate`, then `features` shall exit with an error
  naming the feature file `features/shelf.feature` and change nothing.

```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-1
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

### [g19] `features vocab --check` names a step with no handler
- [r19] If the person runs `features vocab --check`, then `features` shall exit with an error naming the feature file
  `features/shelf.feature` and change nothing.

```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-1
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

### [g20] `features generate` writes the scenario of a negated response with a recipient
- [r20] When the person runs `features generate` on a requirement that is withholding, `features` shall write the feature `features/shelf.feature` and exit successfully.

```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-1
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **`shelf`** (proper noun): the service that lends books.
  - **book** (noun): a thing a reader borrows.
  - **reader** (noun): a person who borrows books.
  - **lend** (verb): `shelf` hands a book to a reader. Forms: lends, lent. Frame: `shelf` lends book to reader.
  ## Behaviour
  ### [g1] `shelf` lends no book to a reader
  - [r1] `shelf` shall not lend a book to a reader.
  ## Not yet
  ## Dropped
```

### [g21] `features generate` leaves out a Then that is entailed
- [r21] When the person runs `features generate` on a capability that is declining, `features` shall not write a file that is overstated.

### [g22] `features generate` writes a capability in the new language
- [r22] When the person runs `features generate` on a capability that is recodified, `features` shall print the feature file `features/shelf.feature`.

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
