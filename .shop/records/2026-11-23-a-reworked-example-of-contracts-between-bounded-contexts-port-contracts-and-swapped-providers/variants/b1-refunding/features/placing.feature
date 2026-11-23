# generated from spec/capabilities/placing.md by features generate; do not edit
Feature: Placing an order
  Narrator: a shopper

  @g1 @r1
  Scenario: An order placed is kept and its stock reserved
    Given a product p1
    When the shopper places an order o1 with the product p1 and a quantity and a card
    Then the ordering service keeps the order o1
    And the ordering service reserves stock for the order o1

  @g2 @r2
  Scenario: An order placed without a quantity is refused
    When the shopper places an order o1 without a quantity
    Then the ordering service refuses this request
    And the ordering service names the quantity

  @g3 @r3
  Scenario: Stock reserved for an order holds it and secures a charge
    Given an order o1
    And the status of the order o1 is `placed`
    And a reservation r1
    And the reservation r1 is for the order o1
    When the stock service completes the reservation r1
    Then the ordering service sets the status of the order o1 to `held`
    And the ordering service secures the charge c1 for the order o1

  @g4 @r4
  Scenario: An order whose stock is refused is rejected
    Given an order o1
    And the status of the order o1 is `placed`
    And a reservation r1
    And the reservation r1 is for the order o1
    When the stock service refuses the reservation r1
    Then the ordering service sets the status of the order o1 to `rejected`
    And the ordering service notifies the shopper of the order o1

  @g5 @r5
  Scenario: A charge secured for a held order takes its stock
    Given an order o1
    And the status of the order o1 is `held`
    And a charge c1
    And the charge c1 is for the order o1
    And a reservation r1
    And the reservation r1 is for the order o1
    And a reservation r2
    And the reservation r2 is for the order o1
    And a reservation r3
    And the reservation r3 is not for the order o1
    When the charges service completes the charge c1
    Then the ordering service sets the status of the order o1 to `charged`
    And the ordering service takes the reservation r1
    And the ordering service takes the reservation r2
    And the ordering service does not take the reservation r3

  @g6 @r6
  Scenario: A charge refused for a held order frees its stock and cancels the order
    Given an order o1
    And the status of the order o1 is `held`
    And a charge c1
    And the charge c1 is for the order o1
    And a reservation r1
    And the reservation r1 is for the order o1
    And a reservation r2
    And the reservation r2 is for the order o1
    And a reservation r3
    And the reservation r3 is not for the order o1
    When the charges service refuses the charge c1
    Then the ordering service frees the reservation r1
    And the ordering service frees the reservation r2
    And the ordering service does not free the reservation r3
    And the ordering service sets the status of the order o1 to `cancelled`
    And the ordering service notifies the shopper of the order o1

  @g7 @r7
  Scenario: Stock taken for a charged order confirms it and collects its charge
    Given an order o1
    And the status of the order o1 is `charged`
    And a reservation r1
    And the reservation r1 is for the order o1
    And a charge c1
    And the charge c1 is for the order o1
    And a charge c2
    And the charge c2 is for the order o1
    And a charge c3
    And the charge c3 is not for the order o1
    When the stock service completes the reservation r1
    Then the ordering service sets the status of the order o1 to `confirmed`
    And the ordering service collects the charge c1
    And the ordering service collects the charge c2
    And the ordering service does not collect the charge c3

  @g8 @r12
  Scenario: Stock that cannot be taken for a charged order refunds its charge
    Given an order o1
    And the status of the order o1 is `charged`
    And a reservation r1
    And the reservation r1 is for the order o1
    And a charge c1
    And the charge c1 is for the order o1
    And a charge c2
    And the charge c2 is for the order o1
    And a charge c3
    And the charge c3 is not for the order o1
    When the stock service refuses the reservation r1
    Then the ordering service cancels the charge c1
    And the ordering service cancels the charge c2
    And the ordering service does not cancel the charge c3
    And the ordering service sets the status of the order o1 to `refunding`

  @g9 @r9
  Scenario: A reservation that lapses while a charge is secured expires the order
    Given an order o1
    And the status of the order o1 is `held`
    And a reservation r1
    And the reservation r1 is for the order o1
    And the state of the reservation r1 is `lapsed`
    And a charge c1
    And the charge c1 is for the order o1
    And a charge c2
    And the charge c2 is for the order o1
    And a charge c3
    And the charge c3 is not for the order o1
    When the stock service notifies the ordering service of the reservation r1
    Then the ordering service cancels the charge c1
    And the ordering service cancels the charge c2
    And the ordering service does not cancel the charge c3
    And the ordering service sets the status of the order o1 to `expired`
    And the ordering service notifies the shopper of the order o1

  @g10 @r10
  Scenario: A charge that settles pays the order
    Given an order o1
    And the status of the order o1 is `confirmed`
    And a charge c1
    And the charge c1 is for the order o1
    And the state of the charge c1 is `settled`
    When the charges service notifies the ordering service of the charge c1
    Then the ordering service sets the status of the order o1 to `paid`

  @g11 @r11
  Scenario: A charge that bounces leaves the order unpaid
    Given an order o1
    And the status of the order o1 is `confirmed`
    And a charge c1
    And the charge c1 is for the order o1
    And the state of the charge c1 is `bounced`
    When the charges service notifies the ordering service of the charge c1
    Then the ordering service sets the status of the order o1 to `unpaid`
    And the ordering service notifies the shopper of the order o1

  @g12 @r13
  Scenario: A charge refunded expires the order
    Given an order o1
    And the status of the order o1 is `refunding`
    And a charge c1
    And the charge c1 is for the order o1
    And the state of the charge c1 is `refunded`
    When the charges service notifies the ordering service of the charge c1
    Then the ordering service sets the status of the order o1 to `expired`
    And the ordering service notifies the shopper of the order o1

  @g13 @r14
  Scenario: A refund that fails is left to the clerk
    Given an order o1
    And the status of the order o1 is `refunding`
    And a charge c1
    And the charge c1 is for the order o1
    And the state of the charge c1 is `unrefunded`
    When the charges service notifies the ordering service of the charge c1
    Then the ordering service sets the status of the order o1 to `unrefunded`
    And the ordering service notifies the clerk of the order o1
