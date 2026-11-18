# generated from spec/capabilities/decision-tiers.md by features generate; do not edit
Feature: Decision tiers
  Narrator: a person or session keeping the decisions

  @g13 @r13
  Scenario: A decision in force with no tier is a warning
    Given a design-decision d1
    And the status of the design-decision d1 is not `superseded`
    And the status of the design-decision d1 is not `rejected`
    And the design-decision d1 has no tier
    When the person runs `check spec`
    Then `model` prints `w_untiered`

  @g18 @r18
  Scenario: An accepted decision supersedes no accepted decision
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a design-decision d2
    And the status of the design-decision d2 is `accepted`
    And the design-decision d1 supersedes the design-decision d2
    When the person runs `check spec`
    Then `model` exits with an error naming `v_d8`

  @g19 @r19
  Scenario: `enter decision` writes and commits a decision and the decisions index
    When the person runs `enter decision`
    Then `work` writes the design-decision d1
    And `work` writes this decisions index
    And `work` commits the design-decision d1
    And `work` commits this decisions index

  @g20 @r20
  Scenario: `enter decision` refuses a decision with no tier
    When the person runs `enter decision` without the `tier` option
    Then `work` refuses `enter decision`
    And `work` names the `tier` option

  @g21 @r21
  Scenario: `enter decision` with `route` writes a route
    When the person runs `enter decision` with the `route` option
    Then `work` writes the design-decision d1
    And the design-decision d1 has the route r1
    And `work` commits the design-decision d1

  @g22 @r22
  Scenario: `model check` names a universal condition no decision verifies
    Given a universal condition u1
    And no design-decision verifies the universal condition u1
    And a universal condition u2
    And no design-decision verifies the universal condition u2
    When the person runs `check spec`
    Then `model` prints the universal condition u1
    And `model` prints the universal condition u2

  @g24 @r24
  Scenario: `enter decision` refuses a decision with no summary
    When the person runs `enter decision` without the `summary` option
    Then `work` refuses `enter decision`
    And `work` names the `summary` option

  @g25 @r25
  Scenario: `enter decision` refuses a decision with no text
    When the person runs `enter decision` without the `wording` option
    Then `work` refuses `enter decision`
    And `work` names the `wording` option

  @g26 @r26
  Scenario: A `check` decision names its test
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And no test enforces the design-decision d1
    When the person runs `check spec`
    Then `model` exits with an error naming `v_d6`

  @g27 @r27
  Scenario: A `requirement` decision names its requirement
    Given a design-decision d1
    And the tier of the design-decision d1 is `requirement`
    And no requirement enforces the design-decision d1
    When the person runs `check spec`
    Then `model` exits with an error naming `v_d7`

  @g28 @r28
  Scenario: `audit decisions` runs the tests of the `check` decisions
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the test t1 enforces the design-decision d1
    When the person runs `audit decisions`
    Then `model` runs `pytest` on the test t1

  @g29 @r29
  Scenario: `audit decisions` names each failing decision
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the outcome of the test t1 is `failed`
    And the test t1 enforces the design-decision d1
    When the person runs `audit decisions`
    Then `model` exits with an error naming the design-decision d1

  @g30 @r30
  Scenario: `model check` refuses a route outside the four
    Given a route r1
    And a design-decision d1
    And the design-decision d1 has the route r1
    And the kind of the route r1 is not `scenario`
    And the kind of the route r1 is not `check`
    And the kind of the route r1 is not `judgement`
    And the kind of the route r1 is not `monitor`
    When the person runs `check spec`
    Then `model` exits with an error naming the design-decision d1

  @g31 @r31
  Scenario: `work decision --supersedes` marks the decision it replaces superseded
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    When the person runs `enter decision` with the `supersedes` option set to the design-decision d1
    Then `work` sets the status of the design-decision d1 to `superseded`
    And `work` commits the design-decision d1
    And `work` writes the design-decision d2
    And the design-decision d2 supersedes the design-decision d1

  @g32 @r32
  Scenario: `work decision --supersedes` refuses a decision not in force
    Given a design-decision d1
    And the status of the design-decision d1 is not `accepted`
    When the person runs `enter decision` with the `supersedes` option set to the design-decision d1
    Then `work` refuses `enter decision`
    And `work` names the design-decision d1
