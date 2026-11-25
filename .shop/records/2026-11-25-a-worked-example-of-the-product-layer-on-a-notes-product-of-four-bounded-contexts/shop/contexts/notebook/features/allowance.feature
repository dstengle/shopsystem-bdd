# generated from spec/capabilities/allowance.md by features generate; do not edit
Feature: Allowance
  Narrator: a client

  @g1 @r1
  Scenario: An allowance enlarged is kept
    Given an allowance a1
    When a client enlarges the allowance a1
    Then the notes service keeps the allowance a1

  @g2 @r2
  Scenario: An allowance reduced is kept
    Given an allowance a1
    When a client reduces the allowance a1
    Then the notes service keeps the allowance a1
