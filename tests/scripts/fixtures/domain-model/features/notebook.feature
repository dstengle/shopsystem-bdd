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

  @g3 @r3
  Scenario: A note added with a text and a priority is kept
    Given a note n1
    When the person adds the note n1 with a text and the priority `high`
    Then the notes service keeps the note n1

  @g4 @r4
  Scenario: A note added without a text is refused
    Given a note n1
    When the person adds the note n1 without a text and the reminder
    Then the notes service refuses this request
    And the notes service names the text

  @g5 @r5
  Scenario: A tag a note is labelled with is kept
    Given a note n1
    And a tag t1
    When the person labels the note n1 with the tag t1
    Then the notes service keeps the tag t1

  @g6 @r6
  Scenario: Listing the notes completes the request
    When the person lists the notes
    Then the notes service completes this request
