# generated from spec/capabilities/shop.md by features generate; do not edit
Feature: Shop
  Narrator: the person

  @g1 @r1
  Scenario: A bounded context entrusted to the shop is kept
    Given a bounded context b1
    And an id i1
    When the person entrusts the bounded context b1 with the id i1
    Then this shop holds the bounded context b1
    And the shop service keeps the bounded context b1
    And the shop service completes this request

  @g2 @r2
  Scenario: A bounded context with an id outside the product of the shop is not kept
    Given a product id p1
    And this shop has the product id p1
    And an id i1
    And the product id p1 does not cover the id i1
    And a bounded context b1
    When the person entrusts the bounded context b1 with the id i1
    Then the shop service refuses this request
    And the shop service names the id i1

  @g3 @r3
  Scenario: A bounded context is not kept twice under one id
    Given an id i1
    And a bounded context b1
    And the bounded context b1 has the id i1
    And this shop holds the bounded context b1
    And a bounded context b2
    When the person entrusts the bounded context b2 with the id i1
    Then the shop service refuses this request
    And the shop service names the id i1

  @g4 @r4
  Scenario: The bounded contexts the shop keeps are listed
    Given a bounded context b1
    And this shop holds the bounded context b1
    And a bounded context b2
    And this shop holds the bounded context b2
    And a bounded context b3
    And this shop does not hold the bounded context b3
    When the person lists this shop
    Then the shop service returns the bounded context b1
    And the shop service returns the bounded context b2
    And the shop service does not return the bounded context b3

  @g5 @r5
  Scenario: A shop that keeps no bounded context lists this bounded context
    Given this shop holds no bounded context
    When the person lists this shop
    Then the shop service returns this bounded context
