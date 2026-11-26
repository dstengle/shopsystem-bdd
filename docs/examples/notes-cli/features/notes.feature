# generated from spec/capabilities/notes.md by features generate; do not edit
Feature: Notes
  Narrator: the person

  @g1 @r1
  Scenario: A note added with a title and a tag is kept
    Given a tag t1
    When the person adds a note n1 with a title and the tag t1
    Then the note n1 is under the tag t1
    And the notes service keeps the note n1

  @g2 @r2
  Scenario: A note added without a title is refused
    When the person adds a note n1 without a title
    Then the notes service refuses this request
    And the notes service names the title

  @g3 @r3
  Scenario: Listing the notes returns every note
    Given a note n1
    And a note n2
    When the person lists the notes
    Then the notes service returns the note n1
    And the notes service returns the note n2

  @g4 @r4
  Scenario: Removing a note sets its status to removed
    Given a note n1
    When the person removes the note n1
    Then the notes service sets the status of the note n1 to `removed`

  @g5 @r5
  Scenario: A removed note is not removed again
    Given a note n1
    And the status of the note n1 is `removed`
    When the person removes the note n1
    Then the notes service refuses this request
