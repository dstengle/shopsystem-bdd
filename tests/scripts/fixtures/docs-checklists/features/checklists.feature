# generated from spec/capabilities/checklists.md by features generate; do not edit
Feature: Checklists
  Narrator: a person keeping checklists

  @g1 @r1
  Scenario: A checklist listed returns its notes
    Given a checklist c1
    And a note n1
    And the checklist c1 holds the note n1
    And a note n2
    And the checklist c1 holds the note n2
    And a note n3
    And the checklist c1 does not hold the note n3
    When the person lists the checklist c1
    Then the checklists service returns the note n1
    And the checklists service returns the note n2
    And the checklists service does not return the note n3

  @g2 @r2
  Scenario: The checklists listed are returned
    Given a checklist c1
    And a checklist c2
    When the person lists the checklists
    Then the checklists service returns the checklist c1
    And the checklists service returns the checklist c2

  @g3 @r3
  Scenario: A note's characters listed are returned
    Given a note n1
    And a character c1
    And the note n1 has the character c1
    And a character c2
    And the note n1 has the character c2
    And a character c3
    And the note n1 does not have the character c3
    When the person lists the characters of the note n1
    Then the checklists service returns the character c1
    And the checklists service returns the character c2
    And the checklists service does not return the character c3

  @g4 @r4
  Scenario: A note's length shown returns the note
    Given a note n1
    When the person shows the length of the note n1
    Then the checklists service returns the note n1

  @g5 @r5
  Scenario: A note shown is returned
    Given a note n1
    When the person shows the note n1
    Then the checklists service returns the note n1
