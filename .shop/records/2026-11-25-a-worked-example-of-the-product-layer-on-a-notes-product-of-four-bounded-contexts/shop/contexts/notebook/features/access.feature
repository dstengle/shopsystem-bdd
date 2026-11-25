# generated from spec/capabilities/access.md by features generate; do not edit
Feature: Access
  Narrator: a client

  @g1 @r1
  Scenario: A note opened to a reader has the reader
    Given a note n1
    And a reader r1
    When a client opens the note n1 to the reader r1
    Then the notes service keeps the note n2
    And the note n2 has the reader r1

  @g2 @r2
  Scenario: A removed note is not opened
    Given a note n1
    And the status of the note n1 is `removed`
    And a reader r1
    When a client opens the note n1 to the reader r1
    Then the notes service refuses this request
    And the notes service names the note n1

  @g3 @r3
  Scenario: A note closed to its reader completes
    Given a reader r1
    And a note n1
    And the note n1 has the reader r1
    When a client closes the note n1 to the reader r1
    Then the notes service completes this request
