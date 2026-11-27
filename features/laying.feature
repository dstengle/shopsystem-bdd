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
