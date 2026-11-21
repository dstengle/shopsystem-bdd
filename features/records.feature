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

  @g3 @r3
  Scenario: `work record` keeps a record about an item or a batch
    Given a text t1
    And an item i1
    And the text t1 denotes the item i1
    And a record r1
    When the person files the record r1 with the text t1
    Then the record r1 concerns the item i1
    And the records service keeps the record r1

  @g4 @r5
  Scenario: `work record` refuses an `--about` that denotes no node, item or batch
    Given a text t1
    And the text t1 denotes no node
    And the text t1 denotes no item
    And the text t1 denotes no batch
    And a record r1
    When the person files the record r1 with the record r1
    Then the records service refuses this request
    And the records service names the record r1

  @g5 @r6
  Scenario: `work record` keeps a record about a batch
    Given a text t1
    And a batch b1
    And the text t1 denotes the batch b1
    And a record r1
    When the person files the record r1 with the text t1
    Then the record r1 concerns the batch b1
    And the records service keeps the record r1
