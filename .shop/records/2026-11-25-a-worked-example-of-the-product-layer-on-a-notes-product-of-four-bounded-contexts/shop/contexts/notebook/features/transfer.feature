# generated from spec/capabilities/transfer.md by features generate; do not edit
Feature: Transfer
  Narrator: a client

  @g1 @r1
  Scenario: Exporting returns a bundle of the kept notes
    Given a note n1
    And the status of the note n1 is `kept`
    And a note n2
    And the status of the note n2 is `kept`
    And a note n3
    And the status of the note n3 is `removed`
    When a client exports the notes
    Then the notes service returns the bundle b1
    And the bundle b1 holds the note n1
    And the bundle b1 holds the note n2
    And the bundle b1 does not hold the note n3

  @g2 @r2
  Scenario: A bundle imported is kept
    Given a bundle b1
    And a note n1
    And the bundle b1 holds the note n1
    And a note n2
    And the bundle b1 holds the note n2
    And a note n3
    And the bundle b1 does not hold the note n3
    When a client imports the bundle b1
    Then the notes service keeps the note n1
    And the notes service keeps the note n2
    And the notes service does not keep the note n3

  @g3 @r3
  Scenario: A bundle imported past the allowance is refused
    Given a bundle b1
    When a client imports the bundle b1
    Then the notes service refuses this request
    And the notes service names the allowance a1
