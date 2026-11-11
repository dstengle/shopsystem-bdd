# generated from spec/capabilities/decision-tiers.md by features generate; do not edit
Feature: Decision tiers
  Narrator: a person or session keeping the decisions

  @g13 @r13
  Scenario: A decision in force with no tier is a warning
    Given a design-decision d1
    And the status of the design-decision d1 is not `superseded`
    And the status of the design-decision d1 is not `rejected`
    And the design-decision d1 has no tier
    When the person runs `model check`
    Then `model` prints `w_untiered`

  @g14 @r14
  Scenario: A `check` decision names its test
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And no test enforces the design-decision d1
    When the person runs `model check`
    Then `model` exits with an error naming `v_d6`

  @g15 @r15
  Scenario: A `requirement` decision names its requirement
    Given a design-decision d1
    And the tier of the design-decision d1 is `requirement`
    And no requirement enforces the design-decision d1
    When the person runs `model check`
    Then `model` exits with an error naming `v_d7`

  @g16 @r16
  Scenario: `model decisions --check` runs the tests of the `check` decisions
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the test t1 enforces the design-decision d1
    When the person runs `model decisions --check`
    Then `model` runs `pytest` on the test t1

  @g17 @r17
  Scenario: `model decisions --check` names each failing decision
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the outcome of the test t1 is `failed`
    And the test t1 enforces the design-decision d1
    When the person runs `model decisions --check`
    Then `model` exits with an error naming the design-decision d1

  @g18 @r18
  Scenario: An accepted decision supersedes no accepted decision
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a design-decision d2
    And the status of the design-decision d2 is `accepted`
    And the design-decision d1 supersedes the design-decision d2
    When the person runs `model check`
    Then `model` exits with an error naming `v_d8`

  @g19 @r19
  Scenario: `work decision` writes and commits a decision and the decisions index
    When the person runs `work decision`
    Then `work` writes the design-decision d1
    And `work` writes this decisions index
    And `work` commits the design-decision d1
    And `work` commits this decisions index

  @g20 @r20
  Scenario: `work decision` refuses a decision with no tier
    When the person runs `work decision` without the `--tier` option
    Then `work` refuses `work decision`
    And `work` names the `--tier` option

  @g21 @r21
  Scenario: `work decision` with `--verified-by` writes a route
    When the person runs `work decision` with the `--verified-by` option
    Then the design-decision d1 has the route r1
    And `work` writes the design-decision d1
    And `work` commits the design-decision d1

  @g22 @r22
  Scenario: `model check` names a universal condition no decision verifies
    Given a universal condition u1
    And no design-decision verifies the universal condition u1
    And a universal condition u2
    And no design-decision verifies the universal condition u2
    When the person runs `model check`
    Then `model` prints the universal condition u1
    And `model` prints the universal condition u2

  @g23 @r23
  Scenario: `model check` refuses a route outside the four
    Given a route r1
    And a design-decision d1
    And the design-decision d1 has the route r1
    And the kind of the route r1 is not `scenario`
    And the kind of the route r1 is not `check`
    And the kind of the route r1 is not `judgement`
    And the kind of the route r1 is not `monitor`
    When the person runs `model check`
    Then `model` exits with an error naming the design-decision d1

  @g24 @r24
  Scenario: `work decision` refuses a decision with no summary
    When the person runs `work decision` without the `--summary` option
    Then `work` refuses `work decision`
    And `work` names the `--summary` option

  @g25 @r25
  Scenario: `work decision` refuses a decision with no text
    When the person runs `work decision` without the `--decision` option
    Then `work` refuses `work decision`
    And `work` names the `--decision` option
