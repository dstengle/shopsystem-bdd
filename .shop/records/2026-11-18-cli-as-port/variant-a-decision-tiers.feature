# generated from spec/capabilities/decision-tiers.md by features generate; do not edit
Feature: Decision tiers
  Narrator: a person or session keeping the decisions

  @g13 @r13
  Scenario: A decision in force with no tier is a warning
    Given a design-decision d1
    And the status of the design-decision d1 is not `superseded`
    And the status of the design-decision d1 is not `rejected`
    And the design-decision d1 has no tier
    When the person examines this spec
    Then `model` flags `w_untiered`

  @g18 @r18
  Scenario: An accepted decision supersedes no accepted decision
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a design-decision d2
    And the status of the design-decision d2 is `accepted`
    And the design-decision d1 supersedes the design-decision d2
    When the person examines this spec
    Then `model` declines this spec
    And `model` names `v_d8`

  @g19 @r19
  Scenario: Entering a decision writes and commits it and the decisions index
    Given a design-decision d1
    When the person enters the design-decision d1
    Then `work` writes the design-decision d1
    And `work` writes this decisions index
    And `work` commits the design-decision d1
    And `work` commits this decisions index

  @g20 @r20
  Scenario: A decision with no tier is declined
    Given a design-decision d1
    And the design-decision d1 has no tier
    When the person enters the design-decision d1
    Then `work` declines the design-decision d1
    And `work` names the tier of the design-decision d1

  @g21 @r21
  Scenario: A decision entered with a route keeps its route
    Given a route r1
    And a design-decision d1
    And the design-decision d1 has the route r1
    When the person enters the design-decision d1
    Then `work` writes the design-decision d2
    And the design-decision d2 has the route r2
    And `work` commits the design-decision d2

  @g22 @r22
  Scenario: Examining the spec names a universal condition no decision verifies
    Given a universal condition u1
    And no design-decision verifies the universal condition u1
    And a universal condition u2
    And no design-decision verifies the universal condition u2
    When the person examines this spec
    Then `model` flags the universal condition u1
    And `model` flags the universal condition u2

  @g24 @r24
  Scenario: A decision with no summary is declined
    Given a design-decision d1
    And the design-decision d1 has no summary
    When the person enters the design-decision d1
    Then `work` declines the design-decision d1
    And `work` names the summary s1
    And the design-decision d1 has the summary s1

  @g25 @r25
  Scenario: A decision with no text is declined
    Given a design-decision d1
    And the design-decision d1 has no wording
    When the person enters the design-decision d1
    Then `work` declines the design-decision d1
    And `work` names the wording w1
    And the design-decision d1 has the wording w1

  @g26 @r26
  Scenario: A `check` decision names its test
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And no test enforces the design-decision d1
    When the person examines this spec
    Then `model` declines this spec
    And `model` names `v_d6`

  @g27 @r27
  Scenario: A `requirement` decision names its requirement
    Given a design-decision d1
    And the tier of the design-decision d1 is `requirement`
    And no requirement enforces the design-decision d1
    When the person examines this spec
    Then `model` declines this spec
    And `model` names `v_d7`

  @g28 @r28
  Scenario: An audit runs the tests of the `check` decisions
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the test t1 enforces the design-decision d1
    When the person audits this decisions index
    Then `model` executes the test t1

  @g29 @r29
  Scenario: An audit names each failing decision
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the outcome of the test t1 is `failed`
    And the test t1 enforces the design-decision d1
    When the person audits this decisions index
    Then `model` declines this decisions index
    And `model` names the design-decision d1

  @g30 @r30
  Scenario: A route outside the four is declined
    Given a route r1
    And a design-decision d1
    And the design-decision d1 has the route r1
    And the kind of the route r1 is not `scenario`
    And the kind of the route r1 is not `check`
    And the kind of the route r1 is not `judgement`
    And the kind of the route r1 is not `monitor`
    When the person examines this spec
    Then `model` declines this spec
    And `model` names the design-decision d1

  @g31 @r31
  Scenario: A decision that supersedes another marks it superseded
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a successor s1
    And the successor s1 supersedes the design-decision d1
    When the person enters the successor s1
    Then `work` sets the status of the successor s1 to `superseded`
    And `work` writes the successor s1

  @g32 @r32
  Scenario: A decision that supersedes one not in force is declined
    Given a design-decision d1
    And the status of the design-decision d1 is not `accepted`
    And a successor s1
    And the successor s1 supersedes the design-decision d1
    When the person enters the successor s1
    Then `work` declines the successor s1
    And `work` names the successor s1
