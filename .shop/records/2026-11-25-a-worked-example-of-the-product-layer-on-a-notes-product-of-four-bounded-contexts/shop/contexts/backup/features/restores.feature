# generated from spec/capabilities/restores.md by features generate; do not edit
Feature: Restores
  Narrator: the person

  @g1 @r1
  Scenario: Restoring a snapshot fetches it
    Given a snapshot s1
    When the person restores the snapshot s1
    Then the backup service fetches the snapshot s1

  @g2 @r2
  Scenario: A snapshot fetched is imported
    Given a snapshot s1
    When the storage service returns the snapshot s1
    Then the backup service imports the bundle b1
    And the snapshot s1 has the bundle b1

  @g3 @r3
  Scenario: A lost snapshot is not restored
    Given a snapshot s1
    And the status of the snapshot s1 is `lost`
    When the person restores the snapshot s1
    Then the backup service refuses this request
    And the backup service names the snapshot s1
