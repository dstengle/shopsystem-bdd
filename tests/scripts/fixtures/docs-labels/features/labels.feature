# generated from spec/capabilities/labels.md by features generate; do not edit
Feature: Labels
  Narrator: a person grouping items

  @g1 @r1
  Scenario: An item shown returns its labels
    Given an item i1
    And a label l1
    And the item i1 has the label l1
    And a label l2
    And the item i1 has the label l2
    And a label l3
    And the item i1 does not have the label l3
    When the person shows the item i1
    Then the backlog service returns the label l1
    And the backlog service returns the label l2
    And the backlog service does not return the label l3

  @g2 @r2
  Scenario: A label an item is tagged with is kept
    Given an item i1
    And a label l1
    When the person tags the item i1 with the label l1
    Then the backlog service keeps the label l1
