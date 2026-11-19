# generated from spec/capabilities/feature-reading.md by features generate; do not edit
Feature: Feature reading
  Narrator: the person

  @g1 @r1
  Scenario: Counting by tag counts the scenarios of a feature file whose docstring holds a tag
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
    When the person counts the feature file f1
    Then the feature reading service returns the number of scenarios of the feature file f1

  @g2 @r2
  Scenario: Counting by tag counts the examples rows of a scenario outline
    Given a scenario outline s1
    And a feature file f1
    And the feature file f1 has the scenario outline s1
    And the feature file f1 has no scenario
    And an examples row e1
    And the scenario outline s1 has the examples row e1
    And an examples row e2
    And the scenario outline s1 has the examples row e2
    When the person counts the feature file f1
    Then the feature reading service returns the number of examples rows of the scenario outline s1

  @g3 @r3
  Scenario: A tag only in a docstring finds no feature file
    Given a docstring d1
    And a feature file f1
    And the feature file f1 has the docstring d1
    And a tag t1
    And the docstring d1 contains the tag t1
    And the feature file f1 does not have the tag t1
    When the person searches this repository with the tag t1
    Then the feature reading service completes this request
    And the feature reading service does not return the feature file f1

  @g4 @r4
  Scenario: A search by title finds a feature file in a subdirectory
    Given a feature file f1
    And a subdirectory s1
    And the subdirectory s1 holds the feature file f1
    And a scenario s2
    And the feature file f1 has the scenario s2
    And a scenario title s3
    And the scenario s2 has the scenario title s3
    When the person searches this repository with the scenario title s3
    Then the feature reading service returns the feature file f1

  @g5 @r5
  Scenario: A search by a feature file's tag finds its every scenario
    Given a tag t1
    And a feature file f1
    And the feature file f1 has the tag t1
    And a scenario s1
    And the feature file f1 has the scenario s1
    And a scenario s2
    And the feature file f1 has the scenario s2
    And a scenario s3
    And the feature file f1 does not have the scenario s3
    When the person searches this repository with the tag t1
    Then the feature reading service returns the scenario s1
    And the feature reading service returns the scenario s2
    And the feature reading service does not return the scenario s3

  @g6 @r6
  Scenario: A search by a scenario's tag finds the scenario
    Given a tag t1
    And a scenario s1
    And the scenario s1 has the tag t1
    When the person searches this repository with the tag t1
    Then the feature reading service returns the scenario s1

  @g7 @r7
  Scenario: A search by a search text finds each scenario whose title contains it
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
    When the person searches this repository with the search text s1
    Then the feature reading service returns the scenario s2
    And the feature reading service returns the scenario s4
    And the feature reading service does not return the scenario s6

  @g8 @r8
  Scenario: Counting by tag refuses a feature file with a rule block
    Given a rule block r1
    And a feature file f1
    And the feature file f1 has the rule block r1
    When the person counts the feature file f1
    Then the feature reading service refuses this request
    And the feature reading service names the feature file f1

  @g9 @r9
  Scenario: A scan gives each deprecated scenario with its replacement's requirement tags
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
    When the person scans this repository
    Then the feature reading service returns the scenario s1
    And the feature reading service returns the requirement tag r3
    And the feature reading service returns the requirement tag r4
    And the feature reading service does not return the requirement tag r5

  @g10 @r10
  Scenario: A scan with no deprecated scenario says so
    Given no scenario has `@deprecated`
    When the person scans this repository
    Then the feature reading service returns `none deprecated`

  @g11 @r11
  Scenario: Vetting passes when every binding binds a scenario
    Given a binding b1
    And a scenario s1
    And the binding b1 binds the scenario s1
    When the person vets this repository
    Then the feature reading service returns `every binding names a scenario`
    And the feature reading service completes this request

  @g12 @r12
  Scenario: Vetting fails on a binding that binds no scenario
    Given a binding b1
    And a test module t1
    And the test module t1 has the binding b1
    And the binding b1 binds no scenario
    When the person vets this repository
    Then the feature reading service fails this check
    And the feature reading service names the test module t1
    And the feature reading service does not change a file

  @g13 @r13
  Scenario: Vetting the unbound scenarios passes when a scenarios call binds them
    Given a scenario s2
    And a feature file f1
    And the feature file f1 has the scenario s2
    And a scenarios call s1
    And the scenarios call s1 binds the scenario s2
    And a scenario s3
    And the feature file f1 has the scenario s3
    When the person vets this repository with the unbound listing
    Then the feature reading service completes this request
    And the feature reading service does not return the scenario s3

  @g14 @r14
  Scenario: Vetting the unbound scenarios fails on a scenario no binding binds
    Given a scenario s1
    And no binding binds the scenario s1
    And a feature file f1
    And the feature file f1 has the scenario s1
    When the person vets this repository with the unbound listing
    Then the feature reading service fails this check
    And the feature reading service names the scenario s1
    And the feature reading service does not change a file
