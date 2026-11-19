# generated from spec/capabilities/reading.md by features generate; do not edit
Feature: Reading
  Narrator: the person

  @g62 @r62
  Scenario: The logical form puts an order after a collection on its members
    Given a requirement r1
    And the requirement r1 uses `order-by`
    When the person parses the requirement r1 with the logical form
    Then the collection c1 has the member m1
    And the member m1 has the order o1
    And the language service returns the logical form l1
    And the logical form l1 uses the order o1
