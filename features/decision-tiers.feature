# generated from spec/capabilities/decision-tiers.md by features generate; do not edit
Feature: Decision tiers
  Narrator: a person or session keeping the decisions

  @g1 @r1
  Scenario: A decision with no tier is a warning
    Given a design-decision d1
    And the design-decision d1 is untiered
    When the person runs `model check` on the design-decision d1
    Then `model` prints `w_untiered`

  @g2 @r2
  Scenario: A `check` decision names its test
    Given a design-decision d1 that is `check`
    And the design-decision d1 is untested
    When the person runs `model check`
    Then `model` exits with an error naming `v_d6`

  @g3 @r3
  Scenario: A `requirement` decision names its requirement
    Given a design-decision d1 that is `requirement`
    And the design-decision d1 is unrequired
    When the person runs `model check`
    Then `model` exits with an error naming `v_d7`

  @g4 @r4
  Scenario: `model decisions --check` runs the tests of the `check` decisions
    Given a design-decision d1 that is `check`
    And a test t1
    And the design-decision d1 is enforced by the test t1
    When the person runs `model decisions --check`
    Then `model` uses the test t1

  @g5 @r5
  Scenario: `model decisions --check` names each failing decision
    Given a design-decision d1 that is `check`
    And a test t1
    And the test t1 is failing
    And the design-decision d1 is enforced by the test t1
    When the person runs `model decisions --check`
    Then `model` exits with an error naming the design-decision d1

  @g6 @r6
  Scenario: A superseded decision is `superseded`
    Given a design-decision d1 that is `accepted`
    And a design-decision d2
    And the design-decision d2 supersedes the design-decision d1
    When the person runs `model check`
    Then `model` exits with an error naming `v_d8`
