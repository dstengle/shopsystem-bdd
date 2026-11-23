# generated from spec/capabilities/stockkeeping.md by features generate; do not edit
Feature: Keeping stock
  Narrator: a stock keeper

  @g1 @r1
  Scenario: A product restocked is kept
    Given a product p1
    And a warehouse w1
    When the stock keeper restocks the product p1 with a quantity and the warehouse w1
    Then the inventory service keeps the product p1

  @g2 @r2
  Scenario: A product transferred is kept
    Given a product p1
    And a warehouse w1
    When the stock keeper transfers the product p1 with a quantity and the warehouse w1
    Then the inventory service keeps the product p1

  @g3 @r3
  Scenario: An exhausted product is not transferred
    Given a product p1
    And the supply of the product p1 is `exhausted`
    When the stock keeper transfers the product p1
    Then the inventory service refuses this request
    And the inventory service names the product p1

  @g4 @r4
  Scenario: A warehouse audited returns every product in it
    Given a warehouse w1
    And a product p1
    And the warehouse w1 holds the product p1
    And a product p2
    And the warehouse w1 holds the product p2
    And a product p3
    And the warehouse w1 does not hold the product p3
    When the stock keeper audits the warehouse w1
    Then the inventory service returns the product p1
    And the inventory service returns the product p2
    And the inventory service does not return the product p3
