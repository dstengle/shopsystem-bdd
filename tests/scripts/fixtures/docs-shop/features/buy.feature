# generated from spec/capabilities/buy.md by features generate; do not edit
Feature: buy
  Narrator: a shopper

  @g2 @r9 @r10
  Scenario: Reword buy for grammar 4
    Given a shopper s1
    And the shopper s1 owns no cart
    And a cart c1
    When the shopper s1 picks the cart c1
    Then the shopper s1 watches the till t1
    And the till t2 is for the shopper s1
    And the shopper s1 watches the till t2
