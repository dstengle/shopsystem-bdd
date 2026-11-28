# generated from spec/capabilities/applying.md by features generate; do not edit
Feature: Applying
  Narrator: the batches service

  @g2 @r2
  Scenario: An item applied that holds a universal condition where none exists keeps universal in the new language
    Given `universal` does not exist
    And a universal condition u1
    And an item i1
    And the item i1 holds the universal condition u1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps `universal`
    And the specification service sets the language of `universal` to `codified-2`

  @g3 @r3
  Scenario: An item applied that holds a capability keeps the capability of the capability form
    Given a capability c1
    And an item i1
    And the item i1 holds the capability c1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the capability c1 conforms to the capability form
    And the specification service keeps the capability c1

  @g4 @r4
  Scenario: An item applied that holds a requirement group serving a job keeps the group serving the job
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And an item i1
    And the item i1 holds the requirement group r1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the requirement group r2 serves the job j1
    And the specification service keeps the capability c1
    And the capability c1 has the requirement group r2

  @g5 @r5
  Scenario: An item applied that holds a capability in an area keeps the capability in the area
    Given a capability c1
    And an item i1
    And the item i1 holds the capability c1
    And an area a1
    And the area a1 holds the capability c1
    And the item i1 holds the area a1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the area a1 holds the capability c1
    And the specification service keeps the capability c1

  @g6 @r6
  Scenario: An item applied that holds a capability in a driven port keeps the capability in the driven port
    Given a capability c1
    And an item i1
    And the item i1 holds the capability c1
    And a driven port d1
    And the driven port d1 holds the capability c1
    And the item i1 holds the driven port d1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the driven port d1 holds the capability c1
    And the specification service keeps the driven port d1

  @g7 @r7
  Scenario: An item applied that holds a term of a pack keeps the pack with the term and imports it
    Given a term t1
    And a pack p1
    And the pack p1 has the term t1
    And an item i1
    And the item i1 holds the term t1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the pack p1 has the term t1
    And the specification service keeps the pack p1
    And this bounded context imports the pack p1

  @g8 @r8
  Scenario: An item applied that holds a term of a pack beside its requirements keeps the pack with the term
    Given a term t1
    And a pack p1
    And the pack p1 has the term t1
    And an item i1
    And the item i1 holds the term t1
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a capability c1
    And the capability c1 holds the requirement id r1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the pack p1 has the term t1
    And the specification service keeps the pack p1

  @g9 @r9
  Scenario: An item applied that imports a pack keeps the pack imported
    Given an item i1
    And a pack p1
    And the item i1 imports the pack p1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then this bounded context imports the pack p1
    And the specification service keeps the pack p1

  @g10 @r10
  Scenario: An item applied that holds an operation table keeps it in the adapter contract
    Given an operation table o1
    And an item i1
    And the item i1 holds the operation table o1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the adapter contract a1
    And the adapter contract a1 holds the operation table o1

  @g11 @r11
  Scenario: An item applied that holds an operation keeps no operation table of it
    Given an operation o1
    And an item i1
    And the item i1 holds the operation o1
    And a specification s1
    And an operation table o2
    And the operation o1 has the operation table o2
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the adapter contract a1
    And the specification service does not keep the operation table o2

  @g12 @r12
  Scenario: An item applied whose model line specifies a new operation with no table keeps a table of it
    Given a model line m1
    And an item i1
    And the item i1 holds the model line m1
    And an operation o1
    And the model line m1 specifies the operation o1
    And this domain model does not hold the operation o1
    And the item i1 holds no operation table of the operation o1
    And a specification s1
    And an operation table o2
    And an adapter contract a1
    When the batches service applies the item i1 to the specification s1
    Then the operation o1 has the operation table o2
    And the specification service keeps the adapter contract a1
    And the adapter contract a1 holds the operation table o2

  @g13 @r13
  Scenario: An item applied that holds an operation table beside its requirements keeps it in the adapter contract
    Given an operation table o1
    And an item i1
    And the item i1 holds the operation table o1
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a capability c1
    And the capability c1 holds the requirement id r1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the adapter contract a1
    And the adapter contract a1 holds the operation table o1

  @g14 @r14
  Scenario: An item applied whose model line restates an operation keeps the model line in place of the operation
    Given a model line m1
    And an operation o1
    And the model line m1 restates the operation o1
    And an item i1
    And the item i1 holds the model line m1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then this domain model holds the model line m1
    And the specification service keeps the model line m1
    And the specification service keeps the domain model d1
    And the domain model d1 does not hold the operation o1

  @g15 @r15
  Scenario: An item applied whose model line restates an element keeps the model line in place of the element
    Given a model line m1
    And an element e1
    And the model line m1 restates the element e1
    And an item i1
    And the item i1 holds the model line m1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then this domain model holds the model line m1
    And the specification service keeps the model line m1
    And the specification service keeps the domain model d1
    And the domain model d1 does not hold the element e1

  @g16 @r16
  Scenario: An item applied whose model line restates an event keeps the model line in place of the event
    Given a model line m1
    And an event e1
    And the model line m1 restates the event e1
    And an item i1
    And the item i1 holds the model line m1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then this domain model holds the model line m1
    And the specification service keeps the model line m1
    And the specification service keeps the domain model d1
    And the domain model d1 does not hold the event e1

  @g17 @r17
  Scenario: An item applied whose model line restates an actor keeps the model line in place of the actor
    Given a model line m1
    And an actor a1
    And the model line m1 restates the actor a1
    And an item i1
    And the item i1 holds the model line m1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then this domain model holds the model line m1
    And the specification service keeps the model line m1
    And the specification service keeps the domain model d1
    And the domain model d1 does not hold the actor a1

  @g18 @r18
  Scenario: An item applied whose model line moves to an area keeps the area holding the model line
    Given a model line m1
    And an area a1
    And the model line m1 moves to the area a1
    And an item i1
    And the item i1 holds the model line m1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the area a1 holds the model line m1
    And the specification service keeps the area a1

  @g19 @r19
  Scenario: An item applied that moves a term keeps the term in the area of its element
    Given a term t1
    And an element e1
    And the term t1 means the element e1
    And an item i1
    And the item i1 moves the term t1
    And an area a1
    And the area a1 holds the element e1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the area a1 holds the term t1
    And the specification service keeps the area a1

  @g20 @r20
  Scenario: An item applied that moves a term beside its requirements keeps the term in the area of its element
    Given a term t1
    And an element e1
    And the term t1 means the element e1
    And an item i1
    And the item i1 moves the term t1
    And an area a1
    And the area a1 holds the element e1
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a capability c1
    And the capability c1 holds the requirement id r1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the area a1 holds the term t1
    And the specification service keeps the area a1

  @g21 @r21
  Scenario: An item applied that retires a model line keeps an area without it
    Given an item i1
    And a model line m1
    And the item i1 retires the model line m1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the area a1
    And the area a1 does not hold the model line m1

  @g22 @r22
  Scenario: An item applied that retires a term keeps an area without it
    Given an item i1
    And a term t1
    And the item i1 retires the term t1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the area a1
    And the area a1 does not hold the term t1

  @g23 @r23
  Scenario: An item applied that retires an element and a term meaning it keeps an area without the term
    Given a model line m1
    And an element e1
    And the model line m1 restates the element e1
    And an item i1
    And the item i1 retires the model line m1
    And a term t1
    And the term t1 means the element e1
    And the item i1 retires the term t1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the area a1
    And the area a1 does not hold the term t1

  @g24 @r24
  Scenario: An item applied that makes two areas imports into one the other whose term its requirement uses
    Given an item i1
    And the item i1 holds `watering`
    And the item i1 holds `plots`
    And a term t1
    And the `plots` area holds the term t1
    And a capability c1
    And the `watering` area holds the capability c1
    And a requirement r1
    And the capability c1 has the requirement r1
    And the requirement r1 uses the term t1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps `watering`
    And the specification service keeps the area a1
    And the area a1 imports `plots`

  @g25 @r25
  Scenario: An item applied that holds a capability keeps the capability specifying the service its area holds
    Given a capability c1
    And an item i1
    And the item i1 holds the capability c1
    And an area a1
    And the area a1 holds the capability c1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the area a1 has the service s2
    And the capability c1 specifies the service s2
    And the specification service keeps the capability c1

  @g37 @r37
  Scenario: Applying an item prepares the specification: scenarios, corpus, catalogues and index
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification s1 holds the requirement r1
    And the specification service keeps the specification s1
    And the requirement r1 has the requirement id r2
    And the specification service keeps the scenario s2
    And the scenario s2 refers to the requirement id r2

  @g38 @r38
  Scenario: An item applied keeps the logical form of each of its requirements in the corpus
    Given a requirement r1
    And an item i1
    And the item i1 has the requirement r1
    And a logical form l1
    And the requirement r1 has the logical form l1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then this corpus holds the logical form l1
    And the specification service keeps the logical form l1

  @g39 @r39
  Scenario: An item applied keeps no corpus block of a requirement id it retires
    Given a requirement id r1
    And an item i1
    And the item i1 holds the requirement id r1
    And a requirement r2
    And this corpus holds the requirement r2
    And the requirement r2 has the requirement id r1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the corpus c1
    And the corpus c1 does not hold the requirement r2

  @g40 @r40
  Scenario: An item applied keeps the catalogue entry of a rule its requirements use
    Given a requirement r1
    And an item i1
    And the item i1 has the requirement r1
    And a rule r2
    And the requirement r1 uses the rule r2
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the catalogue entry c1
    And the rule r2 has the catalogue entry c1

  @g41 @r41
  Scenario: An item applied keeps the construct catalogue when its requirements use a construct
    Given a requirement r1
    And a construct c1
    And the requirement r1 uses the construct c1
    And an item i1
    And the item i1 holds the requirement r1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps this construct catalogue

  @g42 @r42
  Scenario: An item applied whose requirements use no construct keeps no construct catalogue
    Given an item i1
    And no requirement in the item i1 uses a construct
    And no construct catalogue exists
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service does not keep a construct catalogue

  @g43 @r43
  Scenario: An item applied keeps an index file of the index form
    Given an item i1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the index file i2
    And the index file i2 conforms to the index form

  @g44 @r44
  Scenario: An item applied keeps a capability with no requirement out of the index file
    Given a capability c1
    And the capability c1 has no requirement
    And an item i1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the index file i2
    And the index file i2 does not hold the capability c1

  @g45 @r45
  Scenario: An item applied keeps a capability with a requirement in the index file
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And an item i1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the index file i2
    And the index file i2 holds the capability c1

  @g46 @r46
  Scenario: An item applied generates the feature of a capability whose operation its model lines specify
    Given a model line m1
    And an operation o1
    And the model line m1 specifies the operation o1
    And an item i1
    And the item i1 holds the model line m1
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 governs the operation o1
    And the item i1 holds no requirement id in the capability c1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service generates the feature f1
    And the capability c1 has the feature f1
    And this corpus holds the requirement r1
    And the specification service keeps the logical form l1
    And the requirement r1 has the logical form l1

  @g47 @r47
  Scenario: An item applied keeps in the corpus the logical form of a requirement that uses a verb it gives a sense
    Given a sense s1
    And a verb v1
    And the verb v1 has the sense s1
    And an item i1
    And the item i1 holds the verb v1
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses the verb v1
    And the item i1 holds no requirement id in the capability c1
    And a specification s2
    When the batches service applies the item i1 to the specification s2
    Then this corpus holds the requirement r1
    And the specification service keeps the logical form l1
    And the requirement r1 has the logical form l1

  @g48 @r48
  Scenario: An item applied that retires an area keeps a domain model without it
    Given an item i1
    And an area a1
    And the item i1 retires the area a1
    And a specification s1
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the domain model d1
    And the domain model d1 does not hold the area a1

  @g49 @r49
  Scenario: An item applied that retires an area keeps no area importing it
    Given an area a1
    And an area a2
    And the area a1 imports the area a2
    And an item i1
    And the item i1 retires the area a2
    And a specification s1
    And an area a3
    And the area a3 imports the area a2
    When the batches service applies the item i1 to the specification s1
    Then the specification service keeps the domain model d1
    And the domain model d1 does not hold the area a3

  @g50 @r50
  Scenario: An item applied that retires an area keeps its capabilities in no area
    Given an item i1
    And an area a1
    And the item i1 retires the area a1
    And a capability c1
    And the area a1 holds the capability c1
    And a specification s1
    And a capability c2
    And the area a1 holds the capability c2
    When the batches service applies the item i1 to the specification s1
    Then the specification s1 holds the capability c1
    And the specification service keeps the capability c1
    And the specification service does not keep the capability c2

  @g51 @r51
  Scenario: An item applied that retires an area keeps in no area a capability with the stem of the area
    Given an item i1
    And an area a1
    And the item i1 retires the area a1
    And a stem s1
    And the area a1 has the stem s1
    And a capability c1
    And the capability c1 has the stem s1
    And a specification s2
    And a capability c2
    And the area a1 holds the capability c2
    When the batches service applies the item i1 to the specification s2
    Then the specification s2 holds the capability c1
    And the specification service keeps the capability c1
    And the specification service does not keep the capability c2
