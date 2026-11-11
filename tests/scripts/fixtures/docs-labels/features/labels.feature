# generated from spec/capabilities/labels.md by features generate; do not edit
Feature: Labels
  Narrator: a person grouping items

  @g1 @r1
  Scenario: `work show` prints the labels of an item
    Given an item i1
    And a label l1
    And the item i1 has the label l1
    And a label l2
    And the item i1 has the label l2
    When the person runs `work show` on the item i1
    Then `work` prints the label l1
    And `work` prints the label l2
