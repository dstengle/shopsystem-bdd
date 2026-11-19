# generated from spec/capabilities/records.md by features generate; do not edit
Feature: Records
  Narrator: the person

  @g1 @r1
  Scenario: `work record` writes and commits a record
    Given a record r1
    When the person files the record r1
    Then the records service keeps the record r1

  @g2 @r2
  Scenario: `work record` refuses an `--about` that identifies nothing
    Given a text t1
    And the text t1 does not conform to the node id form
    And a record r1
    When the person files the record r1 with the text t1
    Then the records service refuses this request
    And the records service names the text t1
