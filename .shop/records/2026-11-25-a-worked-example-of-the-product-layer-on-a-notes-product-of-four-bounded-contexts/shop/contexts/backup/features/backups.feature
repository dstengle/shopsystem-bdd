# generated from spec/capabilities/backups.md by features generate; do not edit
Feature: Backups
  Narrator: the person

  @g1 @r1
  Scenario: Saving the notes exports them and keeps a snapshot
    When the person saves the notes
    Then the backup service exports the notes
    And the backup service keeps the snapshot s1

  @g2 @r2
  Scenario: A bundle returned is stored as a snapshot
    Given a bundle b1
    When the notebook service returns the bundle b1
    Then the backup service stores the snapshot s1
    And the snapshot s1 has the bundle b1

  @g3 @r3
  Scenario: A refused store is kept
    When the storage service refuses this request
    Then the backup service keeps this request
