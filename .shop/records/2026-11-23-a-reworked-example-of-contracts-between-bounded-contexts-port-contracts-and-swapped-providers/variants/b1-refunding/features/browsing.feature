# generated from spec/capabilities/browsing.md by features generate; do not edit
Feature: Browsing products
  Narrator: a shopper

  @g1 @r1
  Scenario: A product viewed shows how many units can be ordered
    Given a product p1
    And an availability a1
    And the product p1 has the availability a1
    When the shopper views the product p1
    Then the ordering service counts the product p1
    And the ordering service returns the availability a1
