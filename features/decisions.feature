# generated from spec/capabilities/decisions.md by features generate; do not edit
Feature: Decisions
  Narrator: the person

  @g1 @r1
  Scenario: A decision in force with no tier is a warning
    Given a design-decision d1
    And the status of the design-decision d1 is not `superseded`
    And the status of the design-decision d1 is not `rejected`
    And the design-decision d1 has no tier
    When the person validates this specification
    Then the specification service returns `w_untiered`

  @g2 @r2
  Scenario: A `check` decision names its test
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And no test enforces the design-decision d1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_d6`

  @g3 @r3
  Scenario: A `requirement` decision names its requirement
    Given a design-decision d1
    And the tier of the design-decision d1 is `requirement`
    And no requirement enforces the design-decision d1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_d7`

  @g4 @r4
  Scenario: `model decisions --check` runs the tests of the `check` decisions
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the test t1 enforces the design-decision d1
    When the person rebuilds this decisions index with the audit
    Then the decisions service returns the verdict of the test t1

  @g5 @r5
  Scenario: `model decisions --check` names each failing decision
    Given a design-decision d1
    And the tier of the design-decision d1 is `check`
    And a test t1
    And the verdict of the test t1 is `failed`
    And the test t1 enforces the design-decision d1
    When the person rebuilds this decisions index with the audit
    Then the decisions service fails this check
    And the decisions service names the design-decision d1

  @g6 @r6
  Scenario: An accepted decision supersedes no accepted decision
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a design-decision d2
    And the status of the design-decision d2 is `accepted`
    And the design-decision d1 supersedes the design-decision d2
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_d8`

  @g7 @r7
  Scenario: `work decision` writes and commits a decision and the decisions index
    Given a design-decision d1
    When the person enters the design-decision d1
    Then the decisions service keeps the design-decision d1
    And the decisions service keeps this decisions index

  @g8 @r8
  Scenario: `work decision` refuses a decision with no tier
    Given a design-decision d1
    When the person enters the design-decision d1 without a tier
    Then the decisions service refuses this request
    And the decisions service names the tier

  @g9 @r9
  Scenario: `work decision` refuses a decision with no summary
    Given a design-decision d1
    When the person enters the design-decision d1 without a summary
    Then the decisions service refuses this request
    And the decisions service names the summary

  @g10 @r10
  Scenario: `work decision` refuses a decision with no text
    Given a design-decision d1
    When the person enters the design-decision d1 without a wording
    Then the decisions service refuses this request
    And the decisions service names the wording

  @g11 @r11
  Scenario: `work decision` with `--verified-by` writes a route
    Given a design-decision d1
    And a route r1
    When the person enters the design-decision d1 with the route r1
    Then the decisions service keeps the design-decision d2
    And the design-decision d2 has the route r2

  @g12 @r12
  Scenario: the check names a universal condition no decision verifies
    Given a universal condition u1
    And no design-decision verifies the universal condition u1
    And a universal condition u2
    And no design-decision verifies the universal condition u2
    When the person validates this specification
    Then the specification service returns the universal condition u1
    And the specification service returns the universal condition u2

  @g13 @r13
  Scenario: the check refuses a route outside the four
    Given a route r1
    And a design-decision d1
    And the design-decision d1 has the route r1
    And the kind of the route r1 is not `scenario`
    And the kind of the route r1 is not `check`
    And the kind of the route r1 is not `judgement`
    And the kind of the route r1 is not `monitor`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the design-decision d1

  @g14 @r14
  Scenario: `work decision --supersedes` marks the decision it replaces superseded
    Given a design-decision d2
    And the status of the design-decision d2 is `accepted`
    And a design-decision d1
    When the person enters the design-decision d1 over the design-decision d2
    Then the decisions service sets the status of the design-decision d2 to `superseded`
    And the decisions service keeps the design-decision d2

  @g15 @r15
  Scenario: `work decision --supersedes` refuses a decision not in force
    Given a design-decision d2
    And the status of the design-decision d2 is not `accepted`
    And a design-decision d1
    When the person enters the design-decision d1 over the design-decision d2
    Then the decisions service refuses this request
    And the decisions service names the design-decision d2

  @g16 @r16
  Scenario: `model decisions` writes the decisions index
    When the person rebuilds this decisions index
    Then the decisions service keeps this decisions index

  @g17 @r17
  Scenario: A decision with no id
    Given a design-decision d1
    And the design-decision d1 has no id
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the design-decision d1

  @g18 @r18
  Scenario: `model decisions --check` refuses an index that lacks an index entry
    Given an index entry i1
    And a decisions index d2
    And the decisions index d2 does not hold the index entry i1
    And a design-decision d1
    And the design-decision d1 has the index entry i1
    When the person rebuilds the decisions index d2 with the audit
    Then the decisions service fails this check
    And the decisions service names the decisions index d2
    And the decisions service does not change a file

  @g19 @r19
  Scenario: `model decisions --check` passes a current index
    Given no decisions index lacks an index entry
    When the person rebuilds this decisions index with the audit
    Then the decisions service completes this request

  @g20 @r20
  Scenario: A decision with no Decision section
    Given a design-decision d1
    And the design-decision d1 has no section
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the design-decision d1

  @g21 @r21
  Scenario: `work decision --amend` adds an enforcer to an accepted decision
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And an enforcer e1
    When the person amends the design-decision d1 with the enforcer e1
    Then the decisions service keeps the design-decision d2
    And the design-decision d2 has the enforcer e2
    And the decisions service keeps this decisions index

  @g22 @r22
  Scenario: `work decision --amend` adds a foundation to an accepted decision
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a foundation f1
    When the person amends the design-decision d1 with the foundation f1
    Then the decisions service keeps the design-decision d2
    And the design-decision d2 has the foundation f2
    And the decisions service keeps this decisions index

  @g23 @r23
  Scenario: `work decision --amend` refuses a decision not in force
    Given a design-decision d1
    And the status of the design-decision d1 is not `accepted`
    When the person amends the design-decision d1
    Then the decisions service refuses this request
    And the decisions service names the design-decision d1

  @g24 @r24
  Scenario: `work decision --amend` with ids the decision names already changes nothing
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And an enforcer e1
    And the design-decision d1 has the enforcer e1
    When the person amends the design-decision d1 with the enforcer e1
    Then the decisions service completes this request
    And the decisions service does not change a file

  @g25 @r25
  Scenario: `work decision --amend` with a foundation the decision names already changes nothing
    Given a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a foundation f1
    And the design-decision d1 has the foundation f1
    When the person amends the design-decision d1 with the foundation f1
    Then the decisions service completes this request
    And the decisions service does not change a file
