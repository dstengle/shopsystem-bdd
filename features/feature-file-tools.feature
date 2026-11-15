# generated from spec/capabilities/feature-file-tools.md by features generate; do not edit
Feature: Feature file tools
  Narrator: a session reading or generating feature files

  @g88 @r88
  Scenario: `features count --by-tag` counts no scenario line of a docstring
    Given a docstring d1
    And a feature file f1
    And the feature file f1 has the docstring d1
    And a tag t1
    And the docstring d1 contains the tag t1
    And a scenario line s1
    And the docstring d1 contains the scenario line s1
    And a scenario s2
    And the feature file f1 has the scenario s2
    And a scenario s3
    And the feature file f1 has the scenario s3
    When the person runs `features count` with the `--by-tag` option
    Then `features` prints the number of scenarios of the feature file f1

  @g89 @r89
  Scenario: `features count --by-tag` counts each examples row of a scenario outline as a scenario
    Given a scenario outline s1
    And a feature file f1
    And the feature file f1 has the scenario outline s1
    And the feature file f1 has no scenario
    And an examples row e1
    And the scenario outline s1 has the examples row e1
    And an examples row e2
    And the scenario outline s1 has the examples row e2
    When the person runs `features count` with the `--by-tag` option
    Then `features` prints the number of examples rows of the scenario outline s1

  @g90 @r90
  Scenario: a tag in a docstring is no tag of its feature file
    Given a docstring d1
    And a feature file f1
    And the feature file f1 has the docstring d1
    And a tag t1
    And the docstring d1 contains the tag t1
    And the feature file f1 does not have the tag t1
    When the person runs `features list` with the `--tag` option set to the tag t1
    Then `features` exits successfully
    And `features` does not print the feature file f1

  @g91 @r91
  Scenario: a feature file in a subdirectory is read
    Given a feature file f1
    And a subdirectory s1
    And the subdirectory s1 holds the feature file f1
    And a scenario s2
    And the feature file f1 has the scenario s2
    And a scenario title s3
    And the scenario s2 has the scenario title s3
    When the person runs `features list` with the `--title` option set to the scenario title s3
    Then `features` prints the feature file f1

  @g92 @r92
  Scenario: `features list --tag` prints every scenario of a feature file that has the tag
    Given a tag t1
    And a feature file f1
    And the feature file f1 has the tag t1
    And a scenario s1
    And the feature file f1 has the scenario s1
    And a scenario s2
    And the feature file f1 has the scenario s2
    And a scenario s3
    And the feature file f1 does not have the scenario s3
    When the person runs `features list` with the `--tag` option set to the tag t1
    Then `features` prints the scenario s1
    And `features` prints the scenario s2
    And `features` does not print the scenario s3

  @g93 @r93
  Scenario: `features list --tag` prints a scenario that has the tag
    Given a tag t1
    And a scenario s1
    And the scenario s1 has the tag t1
    When the person runs `features list` with the `--tag` option set to the tag t1
    Then `features` prints the scenario s1

  @g94 @r94
  Scenario: `features list --title` prints each scenario whose title contains the text
    Given a search text s1
    And a scenario s2
    And a scenario title s3
    And the scenario s2 has the scenario title s3
    And the scenario title s3 contains the search text s1
    And a scenario s4
    And a scenario title s5
    And the scenario s4 has the scenario title s5
    And the scenario title s5 contains the search text s1
    And a scenario s6
    And a scenario title s7
    And the scenario s6 has the scenario title s7
    And the scenario title s7 does not contain the search text s1
    When the person runs `features list` with the `--title` option set to the search text s1
    Then `features` prints the scenario s2
    And `features` prints the scenario s4
    And `features` does not print the scenario s6

  @g95 @r95
  Scenario: `features list --json` prints the scenarios it found as one JSON object
    Given a search text s1
    And a scenario s2
    And a scenario title s3
    And the scenario s2 has the scenario title s3
    And the scenario title s3 contains the search text s1
    And a scenario s4
    And a scenario title s5
    And the scenario s4 has the scenario title s5
    And the scenario title s5 contains the search text s1
    And a scenario s6
    And a scenario title s7
    And the scenario s6 has the scenario title s7
    And the scenario title s7 does not contain the search text s1
    When the person runs `features list` with the `--json` option and the `--title` option set to the search text s1
    Then `features` prints the scenario s2
    And `features` prints the scenario s4
    And `features` does not print the scenario s6

  @g96 @r96
  Scenario: a feature file with a rule block is refused
    Given a rule block r1
    And a feature file f1
    And the feature file f1 has the rule block r1
    When the person runs `features count` with the `--by-tag` option
    Then `features` refuses `features count`
    And `features` names the feature file f1

  @g97 @r97
  Scenario: `features deprecated` prints each deprecated scenario with the tags of its replacement
    Given a replacement r1
    And a scenario s1
    And the scenario s1 has the replacement r1
    And a requirement tag r2
    And the replacement r1 has the requirement tag r2
    And the scenario s1 has `@deprecated`
    And a requirement tag r3
    And the replacement r1 has the requirement tag r3
    And a requirement tag r4
    And the replacement r1 has the requirement tag r4
    And a requirement tag r5
    And the replacement r1 does not have the requirement tag r5
    When the person runs `features deprecated`
    Then `features` prints the scenario s1
    And `features` prints the requirement tag r3
    And `features` prints the requirement tag r4
    And `features` does not print the requirement tag r5

  @g98 @r98
  Scenario: `features deprecated` says when nothing is deprecated
    Given no scenario has `@deprecated`
    When the person runs `features deprecated`
    Then `features` prints `none deprecated`

  @g99 @r99
  Scenario: `features deprecated --json` prints the deprecated scenarios as one JSON object
    Given a scenario s1
    And the scenario s1 has `@deprecated`
    When the person runs `features deprecated` with the `--json` option
    Then `features` prints the scenario title s2
    And the scenario s1 has the scenario title s2

  @g100 @r100
  Scenario: `features bindings` says so when every binding names a scenario
    Given a binding b1
    And a scenario s1
    And the binding b1 binds the scenario s1
    When the person runs `features bindings`
    Then `features` prints `every binding names a scenario`
    And `features` exits successfully

  @g101 @r101
  Scenario: `features bindings` names the test module of a binding that binds no scenario
    Given a binding b1
    And a test module t1
    And the test module t1 has the binding b1
    And the binding b1 binds no scenario
    When the person runs `features bindings`
    Then `features` exits with an error naming the test module t1
    # entailed: U12 through the definition of refuse

  @g102 @r102
  Scenario: a scenarios call binds every scenario of the feature file it names
    Given a scenario s2
    And a feature file f1
    And the feature file f1 has the scenario s2
    And a scenarios call s1
    And the scenarios call s1 binds the scenario s2
    And a scenario s3
    And the feature file f1 has the scenario s3
    When the person runs `features bindings` with the `--unbound` option
    Then `features` exits successfully
    And `features` does not print the scenario s3

  @g103 @r103
  Scenario: `features bindings --unbound` names a scenario that no binding binds
    Given a scenario s1
    And no binding binds the scenario s1
    And a feature file f1
    And the feature file f1 has the scenario s1
    When the person runs `features bindings` with the `--unbound` option
    Then `features` exits with an error naming the scenario s1
    # entailed: U12 through the definition of refuse

  @g104 @r104
  Scenario: `features bindings --unbound --json` names a scenario that no binding binds
    Given a scenario s1
    And no binding binds the scenario s1
    And a feature file f1
    And the feature file f1 has the scenario s1
    When the person runs `features bindings` with the `--unbound` and `--json` options
    Then `features` exits with an error naming the scenario s1
    # entailed: U12 through the definition of refuse

  @g106 @r106
  Scenario: `features generate --check` names a feature with a scenario that no requirement group of its capability has
    Given the capability `shelf` holds:
      """
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
      """
    And the feature file `features/shelf.feature` holds:
      """
      Feature: Shelf
        Scenario: Edited by hand
          Given a step
      """
    And a feature f1
    And a capability c1
    And the capability c1 has the feature f1
    And a scenario s1
    And no requirement group has the scenario s1
    And the feature f1 has the scenario s1
    When the person runs `features generate` with the `--check` option
    Then `features` exits with an error naming the feature f1
    # entailed: U12 through the definition of refuse

  @g107 @r107
  Scenario: `features vocab --check` names a step with no handler and its feature
    Given the capability `shelf` holds:
      """
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
      """
    And the feature file `features/shelf.feature` holds:
      """
      # generated from spec/capabilities/shelf.md by features generate; do not edit
      Feature: shelf
        Narrator: a client
        @g1 @r1
        Scenario: Lending
          When the person lends a book
      """
    And a step s1
    And a feature f1
    And the feature f1 has the step s1
    And the step s1 has no handler
    When the person runs `features vocab` with the `--check` option
    Then `features` exits with an error naming the step s1
    And `features` exits with an error naming the feature f1
    # entailed: U12 through the definition of refuse

  @g108 @r108
  Scenario: `features generate` writes a scenario of every requirement group of a capability in the language reference
    Given a capability c1
    And the language of the capability c1 is `codified-2`
    And a requirement r1
    And the capability c1 has the requirement r1
    And the requirement r1 conforms to the language reference
    And a requirement r2
    And the capability c1 has the requirement r2
    And the requirement r2 uses `shall`
    And a requirement group r3
    And the capability c1 has the requirement group r3
    And a requirement group r4
    And the capability c1 has the requirement group r4
    When the person runs `features generate` on the capability c1
    Then `features` writes the scenario s1
    And the requirement group r3 has the scenario s1
    And `features` writes the scenario s2
    And the requirement group r4 has the scenario s2

  @g109 @r109
  Scenario: `features generate` leaves out a step that a universal condition entails
    Given a capability c1
    And the language of the capability c1 is `codified-2`
    And a step s1
    And a universal condition u1
    And the universal condition u1 entails the step s1
    When the person runs `features generate` on the capability c1
    Then `features` does not write the step s1

  @g110 @r110
  Scenario: `features generate` writes the feature of a codified service capability
    Given the capability `shelf` holds:
      """
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
      """
    And a capability c1
    And the group of the capability c1 is `service`
    And the language of the capability c1 is `codified-2`
    When the person runs `features generate`
    Then `features` writes the feature f1
    And the capability c1 has the feature f1
    And `features` prints the feature f1

  @g111 @r111
  Scenario: `features generate` writes what a requirement says of a referent after the act that brings it in
    Given the capability `shelf` holds:
      """
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
      - **book** (noun): a thing. Kind of: thing.
      - **status** (attribute of book): where a book is. Values (adjective): `shelved`, `lent`.
      - **lend** (verb, action): a client gives a book to a reader. Forms: lends, lent. Frame: client lends book.
      ## Behaviour
      ### [g1] Lending
      - [r1] When the person runs `shelf add`, `shelf` shall write a book whose status is `shelved` and print the book.
      ## Not yet
      ## Dropped
      """
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And an act a1
    And the requirement r1 has the act a1
    And a referent r2
    And the act a1 brings in the referent r2
    And a description d2
    And the referent r2 has the description d2
    And the description d2 precedes the act a1
    When the person runs `features generate` on the capability c1
    Then `features` writes the description d1
    And the referent r2 has the description d1
    And the description d1 follows the act a1
    And `features` does not write the description d2

  @g112 @r112
  Scenario: `features generate` writes a count over a relation in a response
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `count`
    And the requirement r1 uses `holds-relation`
    When the person runs `features generate` on the capability c1
    Then `features` writes the scenario s1
    And the scenario s1 uses `count`

  @g113 @r113
  Scenario: `features generate` writes only over a relation in a response
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `only`
    And the requirement r1 uses `holds-relation`
    When the person runs `features generate` on the capability c1
    Then `features` writes the scenario s1
    And the scenario s1 uses `only`

  @g114 @r114
  Scenario: `features generate` writes Givens that satisfy a precondition that uses every
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `every`
    When the person runs `features generate` on the capability c1
    Then `features` writes the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 satisfies the precondition p1

  @g115 @r115
  Scenario: `features generate` gives a count in a precondition at its boundary
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And a count c2
    And the precondition p1 holds the count c2
    When the person runs `features generate` on the capability c1
    Then the count c2 has the boundary b1
    And `features` writes the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the boundary b1

  @g116 @r116
  Scenario: `features generate` introduces each instance of two Ks
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `two`
    And a step s1
    And an instance i1
    And no given step introduces the instance i1
    And the step s1 mentions the instance i1
    When the person runs `features generate` on the capability c1
    Then `features` does not write the step s1

  @g117 @r117
  Scenario: `features generate` writes a counter-example of every
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `every`
    And a restriction r3
    And the requirement r1 has the restriction r3
    When the person runs `features generate` on the capability c1
    Then `features` writes the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2

  @g118 @r118
  Scenario: `features generate` writes a counter-example of only and asserts no act that only allows
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `only`
    And a restriction r3
    And the requirement r1 has the restriction r3
    And a step s2
    And an act a1
    And the requirement r1 allows the act a1
    And the step s2 asserts the act a1
    When the person runs `features generate` on the capability c1
    Then `features` writes the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2
    And `features` does not write the step s2

  @g119 @r119
  Scenario: `features generate` writes a counter-example of an upper bound
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And an upper bound u1
    And the requirement r1 has the upper bound u1
    When the person runs `features generate` on the capability c1
    Then `features` writes the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2

  @g120 @r120
  Scenario: `features generate` writes the member a collection must not hold
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `holds-exactly`
    When the person runs `features generate` on the capability c1
    Then the step s1 uses `not-condition`
    And `features` writes the scenario s2
    And the scenario s2 has the step s1

  @g121 @r121
  Scenario: `features generate` writes `nothing` in a precondition
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `nothing`
    When the person runs `features generate` on the capability c1
    Then the step s1 uses `nothing`
    And `features` writes the scenario s2
    And the scenario s2 has the step s1
