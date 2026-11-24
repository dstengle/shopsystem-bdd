# generated from spec/capabilities/realisation.md by features generate; do not edit
Feature: Realising the stock port with the stock ledger
  Narrator: the stock adapter

  @g1 @r1
  Scenario: A reservation is a decrement of the order's line
    Given an order o1
    And the order o1 has no entry
    When the ordering service reserves stock for the order o1
    Then the stock service keeps the entry e1
    And the order o1 has the entry e1
    And the stock service decrements the line l1
    And the entry e1 has the line l1

  @g2 @r2
  Scenario: Reserving again for an order returns its reservation
    Given a reservation r1
    And an order o1
    And the reservation r1 is for the order o1
    And the reservation r1 exists
    When the ordering service reserves stock for the order o1
    Then the stock service returns the reservation r1
    And the stock service changes nothing

  @g3 @r3
  Scenario: A decrement refused refuses the reservation
    Given an entry e1
    When the ledger service refuses the entry e1
    Then the stock service refuses the reservation r1
    And the entry e1 has the reservation r1

  @g4 @r4
  Scenario: Freeing increments the line back
    Given a reservation r1
    When the ordering service frees the reservation r1
    Then the stock service increments the line l1
    And the stock service sets the progress of the entry e1 to `returned`
    And the reservation r1 has the entry e1
    And the entry e1 has the line l1
    And the stock service completes the reservation r1

  @g5 @r5
  Scenario: Taking a reservation that stands only marks its entry
    Given a reservation r1
    And the state of the reservation r1 is `made`
    When the ordering service takes the reservation r1
    Then the stock service sets the progress of the entry e1 to `taken`
    And the reservation r1 has the entry e1
    And the stock service completes the reservation r1

  @g6 @r6
  Scenario: Taking a lapsed reservation is refused
    Given a reservation r1
    And the state of the reservation r1 is `lapsed`
    When the ordering service takes the reservation r1
    Then the stock service refuses the reservation r1

  @g7 @r7
  Scenario: An entry not taken by its deadline lapses
    Given an entry e1
    And the progress of the entry e1 is `decremented`
    And a deadline d1
    And the entry e1 has the deadline d1
    And a reservation r1
    And the entry e1 has the reservation r1
    When this clock reaches the deadline d1
    Then the stock service sets the state of the reservation r1 to `lapsed`
    And the stock service notifies the ordering service of the reservation r1

  @g8 @r8
  Scenario: A lapsed reservation's units go back to the ledger
    Given a reservation r1
    And the state of the reservation r1 is `lapsed`
    When the stock service notifies the ordering service of the reservation r1
    Then the reservation r1 has the entry e1
    And the stock service increments the line l1
    And the entry e1 has the line l1
    And the stock service frees the reservation r1
