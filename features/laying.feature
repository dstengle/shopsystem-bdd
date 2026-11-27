# generated from spec/capabilities/laying.md by features generate; do not edit
Feature: Laying
  Narrator: the batches service

  @g2 @r2
  Scenario: An item lifted is no longer held by the workspace
    Given a requirement r1
    And an item i1
    And the item i1 has the requirement r1
    And a workspace w1
    And the workspace w1 holds the requirement r1
    When the batches service lifts the item i1 from the workspace w1
    Then the laying service keeps the workspace w2
    And the workspace w2 does not hold the requirement r1

  @g5 @r5
  Scenario: A lift of an item keeps out a requirement of the same group that another requirement in the workspace retires
    Given a requirement r2
    And a requirement group r3
    And the requirement group r3 has the requirement r2
    And a requirement id r4
    And the requirement r2 has the requirement id r4
    And a requirement r1
    And the requirement r1 retires the requirement id r4
    And an item i1
    And the item i1 holds the requirement r1
    And a requirement r6
    And the requirement group r3 has the requirement r6
    And a requirement id r7
    And the requirement r6 has the requirement id r7
    And a requirement r5
    And the requirement r5 retires the requirement id r7
    And a workspace w1
    And the workspace w1 holds the requirement r5
    When the batches service lifts the item i1 from the workspace w1
    Then the laying service keeps the workspace w2
    And the workspace w2 does not hold the requirement r6

  @g6 @r6
  Scenario: A workspace prepared for a batch holds a scenario of each requirement of its items
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a requirement r1
    And the item i1 holds the requirement r1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the requirement r1 has the requirement id r2
    And the laying service keeps the scenario s1
    And the scenario s1 refers to the requirement id r2

  @g9 @r9
  Scenario: A workspace prepared for a batch keeps the logical form of each requirement of its items in the corpus
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a requirement r1
    And the item i1 has the requirement r1
    And a logical form l1
    And the requirement r1 has the logical form l1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then this corpus holds the logical form l1
    And the laying service keeps the logical form l1

  @g10 @r10
  Scenario: A workspace prepared for a batch keeps no corpus block of a requirement id its items retire
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a requirement r2
    And this corpus holds the requirement r2
    And the requirement r2 has the requirement id r1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service keeps the corpus c1
    And the corpus c1 does not hold the requirement r2

  @g11 @r11
  Scenario: A workspace prepared for a batch keeps the catalogue entry of a rule its items use
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a requirement r1
    And the item i1 has the requirement r1
    And a rule r2
    And the requirement r1 uses the rule r2
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service keeps the catalogue entry c1
    And the rule r2 has the catalogue entry c1

  @g12 @r12
  Scenario: A workspace prepared for a batch keeps the construct catalogue when its items use a construct
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a requirement r1
    And the item i1 has the requirement r1
    And a construct c1
    And the requirement r1 uses the construct c1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service keeps this construct catalogue

  @g13 @r13
  Scenario: A workspace prepared for a batch whose items use no construct keeps no construct catalogue
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And no requirement of an item in the batch b1 uses a construct
    And no construct catalogue exists
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service does not keep a construct catalogue

  @g14 @r14
  Scenario: A workspace prepared for a batch keeps an index file of the index form
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service keeps the index file i2
    And the index file i2 conforms to the index form

  @g15 @r15
  Scenario: A workspace prepared for a batch keeps a capability with no requirement out of the index file
    Given a capability c1
    And the capability c1 has no requirement
    And an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service keeps the index file i2
    And the index file i2 does not hold the capability c1

  @g16 @r16
  Scenario: A workspace prepared for a batch keeps a capability with a requirement in the index file
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service keeps the index file i2
    And the index file i2 holds the capability c1

  @g17 @r17
  Scenario: A workspace prepared for a batch generates the feature of a capability whose operation its items' model lines specify
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a model line m1
    And an operation o1
    And the model line m1 specifies the operation o1
    And the item i1 holds the model line m1
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 governs the operation o1
    And the item i1 holds no requirement id in the capability c1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then the laying service generates the feature f1
    And the capability c1 has the feature f1
    And this corpus holds the requirement r1
    And the laying service keeps the logical form l1
    And the requirement r1 has the logical form l1

  @g18 @r18
  Scenario: A workspace prepared for a batch keeps in the corpus the logical form of a requirement that uses a verb its items give a sense
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a sense s1
    And a verb v1
    And the verb v1 has the sense s1
    And the item i1 holds the verb v1
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses the verb v1
    And the item i1 holds no requirement id in the capability c1
    And a workspace w1
    When the batches service prepares the workspace w1 for the batch b1
    Then this corpus holds the requirement r1
    And the laying service keeps the logical form l1
    And the requirement r1 has the logical form l1

  @g43 @r43
  Scenario: A lift of an item whose model line restates an operation keeps the operation in the domain model
    Given a model line m1
    And an operation o1
    And the model line m1 restates the operation o1
    And an item i1
    And the item i1 holds the model line m1
    And this domain model holds the model line m1
    And a workspace w1
    When the batches service lifts the item i1 from the workspace w1
    Then the laying service keeps the domain model d1
    And the domain model d1 holds the operation o1

  @g44 @r44
  Scenario: A lift of an item restating an element keeps another item's member line of the element
    Given a member line m2
    And a model line m1
    And the model line m1 holds the member line m2
    And an item i1
    And the item i1 holds the model line m1
    And a model line m3
    And an element e1
    And the model line m3 restates the element e1
    And an item i2
    And the item i2 holds the model line m3
    And the element e1 does not hold the member line m2
    And a workspace w1
    When the batches service lifts the item i2 from the workspace w1
    Then this domain model holds the member line m2
    And the laying service keeps the member line m2
    And the laying service keeps the domain model d1
    And the domain model d1 does not hold the model line m3

  @g45 @r45
  Scenario: A lift of another item keeps a port area holding a capability of an item and importing a supporting area
    Given an area a1
    And the kind of the area a1 is `port`
    And a capability c1
    And an item i1
    And the item i1 holds the capability c1
    And the area a1 holds the capability c1
    And an area a2
    And the kind of the area a2 is `supporting`
    And the area a1 imports the area a2
    And an item i2
    And a workspace w1
    When the batches service lifts the item i2 from the workspace w1
    Then the laying service keeps the area a2

  @g46 @r46
  Scenario: A lift of an item that holds a capability of a port area takes out the import its lay added
    Given the kind of `registry` is `port`
    And a capability c1
    And the `registry` area holds the capability c1
    And an item i1
    And the item i1 holds the capability c1
    And the `registry` area imports `tracking`
    And a workspace w1
    When the batches service lifts the item i1 from the workspace w1
    Then the laying service keeps `registry`
    And the laying service keeps the area a1
    And the area a1 does not import `tracking`

  @g47 @r47
  Scenario: A lift that puts back a group leaves out the Relied on by of a line another requirement in the workspace retires
    Given a requirement r2
    And a requirement group r3
    And the requirement group r3 has the requirement r2
    And a requirement id r4
    And the requirement r2 has the requirement id r4
    And a requirement r1
    And the requirement r1 retires the requirement id r4
    And an item i1
    And the item i1 holds the requirement r1
    And a requirement r6
    And the requirement group r3 has the requirement r6
    And a requirement id r7
    And the requirement r6 has the requirement id r7
    And a requirement r5
    And the requirement r5 retires the requirement id r7
    And a workspace w1
    And the workspace w1 holds the requirement r5
    And a requirement id r8
    And the requirement r6 supports the requirement id r8
    When the batches service lifts the item i1 from the workspace w1
    Then the laying service keeps the requirement r9
    And the requirement group r3 has the requirement r9
    And the requirement r9 does not support the requirement id r8
