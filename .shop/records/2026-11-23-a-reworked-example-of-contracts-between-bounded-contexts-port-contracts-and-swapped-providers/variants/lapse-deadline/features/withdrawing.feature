# generated from spec/capabilities/withdrawing.md by features generate; do not edit
Feature: Withdrawing an order
  Narrator: a shopper

  @g1 @r1
  Scenario: A held order withdrawn frees its stock and cancels its charge
    Given an order o1
    And the status of the order o1 is `held`
    And a reservation r1
    And the reservation r1 is for the order o1
    And a reservation r2
    And the reservation r2 is for the order o1
    And a reservation r3
    And the reservation r3 is not for the order o1
    And a charge c1
    And the charge c1 is for the order o1
    And a charge c2
    And the charge c2 is for the order o1
    And a charge c3
    And the charge c3 is not for the order o1
    When the shopper withdraws the order o1
    Then the ordering service frees the reservation r1
    And the ordering service frees the reservation r2
    And the ordering service does not free the reservation r3
    And the ordering service cancels the charge c1
    And the ordering service cancels the charge c2
    And the ordering service does not cancel the charge c3
    And the ordering service sets the status of the order o1 to `withdrawn`

  @g2 @r2
  Scenario: A confirmed order is not withdrawn
    Given an order o1
    And the status of the order o1 is `confirmed`
    When the shopper withdraws the order o1
    Then the ordering service refuses this request
    And the ordering service names the order o1
