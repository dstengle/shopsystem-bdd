# generated from spec/capabilities/storage-port.md by features generate; do not edit
Feature: Storage port
  Narrator: the backup service

  @g1 @r1
  Scenario: A snapshot stored completes
    Given a snapshot s1
    When the backup service stores the snapshot s1
    Then the storage service completes this request

  @g2 @r2
  Scenario: A snapshot fetched is returned
    Given a snapshot s1
    When the backup service fetches the snapshot s1
    Then the storage service returns the snapshot s1
