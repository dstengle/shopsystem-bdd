# generated from spec/capabilities/notebook.md by features generate; do not edit
Feature: Notebook
  Narrator: a person keeping notes

  @g1 @r1
  Scenario: A note added is filed
    Given a note n1
    When the person adds the note n1
    Then the notes service files the note n1

  @g2 @r2
  Scenario: A note that carries a tag is archived when it is filed
    Given a note n1
    And a tag t1
    And the note n1 carries the tag t1
    When the person files the note n1
    Then the notes service archives the note n1
