# generated from spec/capabilities/ledger.md by features generate; do not edit
Feature: The stock ledger (assumed)
  Narrator: the caller

  @g1 @r1
  Scenario: A line decremented loses the units
    Given a line l1
    When the caller decrements the line l1 with an amount
    Then the ledger service keeps the line l1

  @g3 @r3
  Scenario: A line incremented gains the units
    Given a line l1
    When the caller increments the line l1 with an amount
    Then the ledger service keeps the line l1
