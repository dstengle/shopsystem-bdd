# generated from spec/capabilities/projection.md by features generate; do not edit
Feature: The ports' projection
  Narrator: the ordering service

  @g1 @r1 @r2 @r3
  Scenario: A reservation is completed or refused
    Given an order o1
    When the ordering service reserves stock for the order o1
    Then the stock service completes the reservation r1
    And the reservation r1 is for the order o1

  @g2 @r4
  Scenario: A reservation freed is completed
    Given a reservation r1
    When the ordering service frees the reservation r1
    Then the stock service completes the reservation r1

  @g3 @r5 @r6
  Scenario: A lapsed reservation is not taken
    Given a reservation r1
    And the state of the reservation r1 is `lapsed`
    When the ordering service takes the reservation r1
    Then the stock service refuses the reservation r1
    And the stock service completes the reservation r1

  @g4 @r7
  Scenario: A product counted returns its availability
    Given a product p1
    And an availability a1
    And the product p1 has the availability a1
    When the ordering service counts the product p1
    Then the stock service returns the availability a1

  @g5 @r8 @r9
  Scenario: A charge is secured or refused
    Given an order o1
    When the ordering service secures a charge c1 for the order o1
    Then the charges service completes the charge c1

  @g6 @r10
  Scenario: A charge cancelled is completed
    Given a charge c1
    When the ordering service cancels the charge c1
    Then the charges service completes the charge c1

  @g7 @r11 @r12
  Scenario: A charge collected is completed, then settles or bounces
    Given a charge c1
    When the ordering service collects the charge c1
    Then the charges service completes the charge c1
