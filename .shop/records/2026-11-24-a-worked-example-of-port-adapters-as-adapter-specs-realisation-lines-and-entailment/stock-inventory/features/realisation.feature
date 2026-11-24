# generated from spec/capabilities/realisation.md by features generate; do not edit
Feature: Realising the stock port with inventory
  Narrator: the stock adapter

  @g1 @r1
  Scenario: A reservation is an allocation held at inventory
    Given an order o1
    And the order o1 has no entry
    When the ordering service reserves stock for the order o1
    Then the stock service keeps the entry e1
    And the order o1 has the entry e1
    And the stock service holds the stocked product s1
    And the entry e1 has the stocked product s1

  @g2 @r2
  Scenario: Reserving again for an order that has an entry returns its reservation
    Given a reservation r1
    And an order o1
    And the reservation r1 is for the order o1
    And the reservation r1 exists
    When the ordering service reserves stock for the order o1
    Then the stock service returns the reservation r1
    And the stock service changes nothing

  @g3 @r3
  Scenario: An allocation kept completes the reservation
    Given an allocation a1
    And an entry e1
    And the entry e1 has the allocation a1
    When the inventory service keeps the allocation a1
    Then the stock service completes the reservation r1
    And the entry e1 has the reservation r1

  @g4 @r4
  Scenario: A hold refused refuses the reservation
    Given an entry e1
    When the inventory service refuses the entry e1
    Then the stock service refuses the reservation r1
    And the entry e1 has the reservation r1

  @g5 @r5
  Scenario: Freeing releases the allocation
    Given a reservation r1
    When the ordering service frees the reservation r1
    Then the reservation r1 has the entry e1
    And the stock service releases the allocation a1
    And the entry e1 has the allocation a1
    And the stock service completes the reservation r1

  @g6 @r6
  Scenario: Taking a reservation that stands consumes its allocation
    Given a reservation r1
    And the state of the reservation r1 is `made`
    When the ordering service takes the reservation r1
    Then the reservation r1 has the entry e1
    And the stock service consumes the allocation a1
    And the entry e1 has the allocation a1
    And the stock service completes the reservation r1

  @g7 @r7
  Scenario: Taking a lapsed reservation is refused
    Given a reservation r1
    And the state of the reservation r1 is `lapsed`
    When the ordering service takes the reservation r1
    Then the stock service refuses the reservation r1

  @g8 @r8
  Scenario: A lapse at inventory is a lapse of the reservation
    Given an entry e1
    And a reservation r1
    And the reservation r1 has the entry e1
    And an allocation a1
    And the entry e1 has the allocation a1
    When the inventory service notifies the client of the allocation a1
    Then the stock service sets the state of the reservation r1 to `lapsed`
    And the stock service notifies the ordering service of the reservation r1

  @g9 @r9
  Scenario: Counting queries the product at inventory
    Given a product p1
    And an availability a1
    And the product p1 has the availability a1
    And a stocked product s1
    And an entry e1
    And the entry e1 has the stocked product s1
    And a stocked product s2
    And an entry e2
    And the entry e2 has the stocked product s2
    And a stocked product s3
    And an entry e3
    And the entry e3 does not have the stocked product s3
    When the ordering service counts the product p1
    Then the stock service queries the stocked product s1
    And the stock service queries the stocked product s2
    And the stock service does not query the stocked product s3
    And the stock service returns the availability a1
