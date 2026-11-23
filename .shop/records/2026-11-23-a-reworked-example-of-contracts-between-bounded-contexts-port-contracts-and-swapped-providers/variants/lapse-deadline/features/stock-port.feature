# generated from spec/capabilities/stock-port.md by features generate; do not edit
Feature: The stock port's contract
  Narrator: the ordering service

  @g1 @r1
  Scenario: Reserving again for the same order gives the same reservation
    Given a reservation r1
    And an order o1
    And the reservation r1 is for the order o1
    And the reservation r1 exists
    When the ordering service reserves stock for the order o1
    Then the stock service returns the reservation r1
    And the stock service changes nothing

  @g2 @r2
  Scenario: A reservation freed is freed
    Given a reservation r1
    When the ordering service frees the reservation r1
    Then the stock service completes the reservation r1

  @g3 @r3
  Scenario: A reservation that stands is taken
    Given a reservation r1
    And the state of the reservation r1 is `made`
    When the ordering service takes the reservation r1
    Then the stock service completes the reservation r1

  @g4 @r4
  Scenario: A lapsed reservation is not taken
    Given a reservation r1
    And the state of the reservation r1 is `lapsed`
    When the ordering service takes the reservation r1
    Then the stock service refuses the reservation r1

  @g5 @r5
  Scenario: A reservation that lapses is freed when ordering is told
    Given a reservation r1
    And the state of the reservation r1 is `lapsed`
    When the stock service notifies the ordering service of the reservation r1
    Then the stock service frees the reservation r1

  @g6 @r6
  Scenario: A product counted returns its availability
    Given a product p1
    And an availability a1
    And the product p1 has the availability a1
    When the ordering service counts the product p1
    Then the stock service returns the availability a1
