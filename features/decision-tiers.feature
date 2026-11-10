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
    And a design-decision d2 that is `accepted`
    And the design-decision d1 supersedes the design-decision d2
    When the person runs `model check`
    Then `model` exits with an error naming `v_d8`

  @g7 @r7
  Scenario: `work decision` writes and commits a decision
    When the person runs `work decision`
    Then `work` writes the design-decision d1
    And `work` writes the decisions index d2
    And `work` commits the design-decision d1

  @g8 @r8
  Scenario: `work decision` refuses a decision with no tier
    Given a design-decision d1
    And the design-decision d1 is untiered
    When the person runs `work decision` on the design-decision d1
    Then `work` exits with an error naming `--tier`
    And `work` changes nothing

  @g9 @r9
  Scenario: `work decision` names an absent argument
    Given an argument a1
    And the argument a1 is absent
    When the person runs `work decision` on the argument a1
    Then `work` exits with an error naming the argument a1
    And `work` changes nothing

  @g10 @r10
  Scenario: `work decision --verified-by` writes a route
    When the person runs `work decision --verified-by`
    Then `work` writes the design-decision d1
    And `work` commits the design-decision d1

  @g11 @r11
  Scenario: `model check` names a universal condition with no route
    Given an universal condition u1
    And the universal condition u1 is unrouted
    When the person runs `model check` on the universal condition u1
    Then `model` prints the universal condition u1

  @g12 @r12
  Scenario: `model check` refuses a route outside the four
    Given a design-decision d1
    And the design-decision d1 is misrouted
    When the person runs `model check` on the design-decision d1
    Then `model` exits with an error naming the design-decision d1
