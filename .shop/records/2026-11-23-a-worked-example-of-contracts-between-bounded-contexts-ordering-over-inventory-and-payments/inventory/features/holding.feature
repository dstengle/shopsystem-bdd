# generated from spec/capabilities/holding.md by features generate; do not edit
Feature: Holding stock
  Narrator: a client

  @g1 @r1
  Scenario: A product held is allocated
    Given a product p1
    When the client holds the product p1 with a quantity and a reference
    Then the inventory service keeps the allocation a1
    And the allocation a1 is on the product p1

  @g2 @r2
  Scenario: Holding again with the same reference gives the same allocation
    Given an allocation a1
    And a product p1
    And the allocation a1 is on the product p1
    And the reference of the allocation a1 is `r1`
    When the client holds the product p1 with the reference `r1`
    Then the inventory service returns the allocation a1
    And the inventory service changes nothing

  @g3 @r3
  Scenario: An exhausted product is not held
    Given a product p1
    And the supply of the product p1 is `exhausted`
    When the client holds the product p1
    Then the inventory service refuses this request
    And the inventory service names the product p1

  @g4 @r4
  Scenario: A product held without a quantity is refused
    Given a product p1
    When the client holds the product p1 without a quantity
    Then the inventory service refuses this request
    And the inventory service names the quantity

  @g5 @r5
  Scenario: An allocation released is released
    Given an allocation a1
    When the client releases the allocation a1
    Then the inventory service sets the status of the allocation a1 to `released`

  @g6 @r6
  Scenario: A consumed allocation is not released
    Given an allocation a1
    And the status of the allocation a1 is `consumed`
    When the client releases the allocation a1
    Then the inventory service refuses this request
    And the inventory service names the allocation a1

  @g7 @r7
  Scenario: An allocation consumed is consumed
    Given an allocation a1
    When the client consumes the allocation a1
    Then the inventory service sets the status of the allocation a1 to `consumed`

  @g8 @r8
  Scenario: A lapsed allocation is not consumed
    Given an allocation a1
    And the status of the allocation a1 is `lapsed`
    When the client consumes the allocation a1
    Then the inventory service refuses this request
    And the inventory service names the allocation a1

  @g9 @r9
  Scenario: An allocation not consumed in time lapses and the client is told
    Given an allocation a1
    And the status of the allocation a1 is `placed`
    When the clock lapses the allocation a1
    Then the inventory service sets the status of the allocation a1 to `lapsed`
    And the inventory service notifies the client of the allocation a1

  @g10 @r10
  Scenario: A product queried returns its stock
    Given a product p1
    When the client queries the product p1
    Then the inventory service returns the stock of the product p1
