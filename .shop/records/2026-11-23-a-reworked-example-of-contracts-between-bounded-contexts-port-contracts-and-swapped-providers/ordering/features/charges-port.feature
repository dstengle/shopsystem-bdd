# generated from spec/capabilities/charges-port.md by features generate; do not edit
Feature: The charges port's contract
  Narrator: the ordering service

  @g1 @r1
  Scenario: Securing again for the same order charges nothing more
    Given a charge c1
    And an order o1
    And the charge c1 is for the order o1
    And the charge c1 exists
    When the ordering service secures a charge c2 for the order o1
    Then the charges service changes nothing

  @g2 @r2
  Scenario: Securing a charge collects nothing
    Given an order o1
    When the ordering service secures a charge c1 for the order o1
    Then the charges service does not collect the charge c1

  @g3 @r3
  Scenario: A charge cancelled is cancelled, and that is final
    Given a charge c1
    When the ordering service cancels the charge c1
    Then the charges service completes the charge c1
    And the charges service does not notify the ordering service of the charge c1

  @g4 @r4
  Scenario: A charge collected is collected
    Given a charge c1
    When the ordering service collects the charge c1
    Then the charges service completes the charge c1
