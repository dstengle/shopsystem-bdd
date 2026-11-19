# generated from spec/capabilities/checklists.md by features generate; do not edit
Feature: Checklists
  Narrator: the person

  @g1 @r1
  Scenario: Create checklists, add items, check items off and list them
    Given a checklist c1
    When the person creates the checklist c1 with a title
    Then the checklists service keeps the checklist c1

  @g2 @r2
  Scenario: A checklist created without a title is refused
    Given a checklist c1
    When the person creates the checklist c1 without a title
    Then the checklists service refuses this request
    And the checklists service names the title

  @g3 @r3
  Scenario: An item added with a text is kept in the checklist
    Given an item i1
    And a checklist c1
    When the person adds the item i1 to the checklist c1 with a text
    Then the checklist c1 holds the item i1
    And the checklists service keeps the item i1

  @g4 @r4
  Scenario: An item added without a text is refused
    Given an item i1
    And a checklist c1
    When the person adds the item i1 to the checklist c1 without a text
    Then the checklists service refuses this request
    And the checklists service names the text

  @g5 @r5
  Scenario: Checking an item sets its status to done
    Given an item i1
    When the person checks the item i1
    Then the checklists service sets the status of the item i1 to `done`

  @g6 @r6
  Scenario: Listing a checklist returns every item in it
    Given a checklist c1
    And an item i1
    And the checklist c1 holds the item i1
    And an item i2
    And the checklist c1 holds the item i2
    And an item i3
    And the checklist c1 does not hold the item i3
    When the person lists the checklist c1
    Then the checklists service returns the item i1
    And the checklists service returns the item i2
    And the checklists service does not return the item i3
