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

  @g6 @r9
  Scenario: `work observe` files an observation
    Given an observation o1
    When the person files the observation o1
    Then the records service keeps the observation o1

  @g7 @r7
  Scenario: `work record --design` files a design in its folder
    Given a design d1
    When the person files the design d1
    Then the records service keeps the design d1

  @g8 @r4
  Scenario: `work record --plan` files a plan in the folder of its design
    Given a plan p1
    And a design d1
    When the person files the plan p1 with the design d1
    Then the records service keeps the plan p1
    And the design d1 holds the plan p1
    And the records service keeps the design d1

  @g9 @r8
  Scenario: `work record --plan` refuses a design that does not exist
    Given a design d1
    And the design d1 does not exist
    And a plan p1
    When the person files the plan p1 with the design d1
    Then the records service refuses this request
    And the records service names the design d1
