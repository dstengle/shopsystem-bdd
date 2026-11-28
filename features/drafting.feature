# generated from spec/capabilities/drafting.md by features generate; do not edit
Feature: Drafting
  Narrator: the person

  @g1 @r1
  Scenario: A relation row drafted into an item is kept
    Given an item i1
    And a relation row r1
    When the person drafts the item i1 with the relation row r1
    Then the item i1 holds the relation row r1
    And the drafting service keeps the relation row r1

  @g2 @r2
  Scenario: A relation row that does not conform to its form is refused
    Given a relation row r1
    And the relation row r1 does not conform to the relation-row form
    And an item i1
    When the person drafts the item i1 with the relation row r1
    Then the drafting service refuses this request
    And the drafting service names the relation row r1

  @g3 @r3
  Scenario: A universal condition drafted into an item is kept
    Given an item i1
    And a universal condition u1
    When the person drafts the item i1 with the universal condition u1
    Then the item i1 holds the universal condition u1
    And the drafting service keeps the universal condition u1

  @g4 @r4
  Scenario: An upstream entry drafted into an item is kept
    Given an item i1
    And an upstream entry u1
    When the person drafts the item i1 with the upstream entry u1
    Then the item i1 holds the upstream entry u1
    And the drafting service keeps the upstream entry u1

  @g5 @r5
  Scenario: An upstream entry that does not conform to its form is refused
    Given an upstream entry u1
    And the upstream entry u1 does not conform to the upstream-entry form
    And an item i1
    When the person drafts the item i1 with the upstream entry u1
    Then the drafting service refuses this request
    And the drafting service names the upstream entry u1

  @g6 @r6
  Scenario: A given block drafted into an item is kept
    Given an item i1
    And a given block g1
    When the person drafts the item i1 with the given block g1
    Then the item i1 holds the given block g1
    And the drafting service keeps the given block g1

  @g7 @r7
  Scenario: A given block that does not conform to the example-data form is refused
    Given a given block g1
    And the given block g1 does not conform to the example-data form
    And an item i1
    When the person drafts the item i1 with the given block g1
    Then the drafting service refuses this request
    And the drafting service names the given block g1

  @g8 @r8
  Scenario: A line that retires a requirement is kept in the item
    Given an item i1
    And a requirement id r1
    When the person drafts the item i1 with the requirement id r1
    Then the drafting service keeps the requirement r2
    And the item i1 holds the requirement r2

  @g9 @r9
  Scenario: Retiring a requirement id that no requirement has is refused
    Given a requirement id r1
    And no requirement has the requirement id r1
    And an item i1
    When the person drafts the item i1 with the requirement id r1
    Then the drafting service refuses this request
    And the drafting service names the requirement id r1

  @g10 @r10
  Scenario: Recodifying a capability in an item sets its language
    Given a capability c1
    And an item i1
    When the person recodifies the capability c1 in the item i1
    Then the item i1 holds the capability c1
    And the drafting service sets the language of the capability c1 to `codified-2`
    And the drafting service keeps the item i1

  @g11 @r11
  Scenario: Recodifying the universal conditions in an item sets their language
    Given an item i1
    When the person recodifies `universal` in the item i1
    Then the item i1 holds `universal`
    And the drafting service sets the language of `universal` to `codified-2`
    And the drafting service keeps the item i1

  @g12 @r12
  Scenario: A universal condition that retires another is kept in the item
    Given an item i1
    And a universal condition id u1
    When the person drafts the item i1 with the universal condition id u1
    Then the drafting service keeps the universal condition u2
    And the item i1 holds the universal condition u2

  @g13 @r13
  Scenario: Retiring a universal condition id that no universal condition has is refused
    Given a universal condition id u1
    And no universal condition has the universal condition id u1
    And an item i1
    When the person drafts the item i1 with the universal condition id u1
    Then the drafting service refuses this request
    And the drafting service names the universal condition id u1

  @g15 @r15
  Scenario: Rewording a requirement of a capability is refused
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    When the person rewords the requirement r1
    Then the drafting service refuses this request
    And the drafting service names the requirement r1

  @g16 @r16
  Scenario: Removing a requirement of a capability is refused
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    When the person removes the requirement r1
    Then the drafting service refuses this request
    And the drafting service names the requirement r1

  @g17 @r17
  Scenario: Retiring a requirement with no line replacing it keeps only the requirement id
    Given an item i1
    And a requirement id r1
    And a requirement r2
    And the item i1 holds the requirement r2
    When the person drafts the item i1 with the requirement id r1 and without a requirement
    Then the item i1 holds the requirement id r1
    And the drafting service keeps the requirement id r1
    And the drafting service does not keep the requirement r2

  @g18 @r18
  Scenario: Retiring with no line a requirement id that no requirement has is refused
    Given a requirement id r1
    And no requirement has the requirement id r1
    And an item i1
    When the person drafts the item i1 with the requirement id r1 and without a requirement
    Then the drafting service refuses this request
    And the drafting service names the requirement id r1

  @g19 @r19
  Scenario: A chore assigned to an item is kept
    Given a chore c1
    And an item i1
    When the person assigns the chore c1 to the item i1
    Then the item i1 holds the chore c1
    And the drafting service keeps the chore c1

  @g20 @r20
  Scenario: A chore is not assigned to an item that holds a requirement
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a chore c1
    When the person assigns the chore c1 to the item i1
    Then the drafting service refuses this request
    And the drafting service names the requirement r1

  @g21 @r21
  Scenario: An item that holds a chore is not drafted
    Given a chore c1
    And an item i1
    And the item i1 holds the chore c1
    When the person drafts the item i1
    Then the drafting service refuses this request
    And the drafting service names the chore c1

  @g22 @r22
  Scenario: A new capability drafted into an item is kept
    Given an item i1
    And a capability c1
    When the person drafts the item i1 with the capability c1
    Then the item i1 holds the capability c1
    And the drafting service keeps the capability c1

  @g23 @r23
  Scenario: Drafting a capability that exists is refused
    Given a capability c1
    And the capability c1 exists
    And an item i1
    When the person drafts the item i1 with the capability c1
    Then the drafting service refuses this request
    And the drafting service names the capability c1

  @g24 @r24
  Scenario: Removing a requirement of an item keeps the requirement ids it does not retire
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a requirement id r2
    And the item i1 holds the requirement id r2
    And the requirement r1 does not retire the requirement id r2
    And a requirement id r3
    And the item i1 holds the requirement id r3
    And the requirement r1 does not retire the requirement id r3
    And a requirement id r4
    And the requirement r1 does not retire the requirement id r4
    And the item i1 does not hold the requirement id r4
    When the person removes the requirement r1
    Then the drafting service keeps the requirement id r2
    And the drafting service keeps the requirement id r3
    And the drafting service does not keep the requirement id r4

  @g25 @r25
  Scenario: A term written for a new capability of an item is kept
    Given a capability c1
    And the capability c1 does not exist
    And an item i1
    And the item i1 holds the capability c1
    And a term t1
    When the person writes the term t1 into the item i1
    Then the item i1 holds the term t1
    And the drafting service keeps the term t1

  @g26 @r26
  Scenario: A model line declared for a new capability of an item is kept
    Given a capability c1
    And the capability c1 does not exist
    And an item i1
    And the item i1 holds the capability c1
    And a model line m1
    When the person declares the model line m1 in the item i1
    Then the item i1 holds the model line m1
    And the drafting service keeps the model line m1

  @g27 @r27
  Scenario: Removing the last requirement of a new capability of an item keeps the capability
    Given a capability c1
    And the capability c1 does not exist
    And an item i1
    And the item i1 holds the capability c1
    And a requirement r1
    And the capability c1 has the requirement r1
    When the person removes the requirement r1
    Then the item i1 holds the capability c1
    And the drafting service keeps the capability c1

  @g28 @r28
  Scenario: `work line --retires` names the decisions the retired requirement enforces
    Given a requirement r2
    And a design-decision d1
    And the requirement r2 enforces the design-decision d1
    And a requirement id r1
    And the requirement r2 has the requirement id r1
    And an item i1
    When the person drafts the item i1 with the requirement id r1
    Then the drafting service keeps the requirement r3
    And the item i1 holds the requirement r3
    And the drafting service names the design-decision d1

  @g29 @r29
  Scenario: A retirement list applied to an item keeps every requirement it holds
    Given a retirement list r1
    And an item i1
    And a requirement r2
    And the retirement list r1 holds the requirement r2
    And a requirement r3
    And the retirement list r1 holds the requirement r3
    And a requirement r4
    And the retirement list r1 does not hold the requirement r4
    When the person applies the retirement list r1 to the item i1
    Then the drafting service keeps the item i1
    And the drafting service keeps the requirement r2
    And the drafting service keeps the requirement r3
    And the drafting service does not keep the requirement r4

  @g30 @r30
  Scenario: A retirement list that names a requirement id no requirement has is refused whole
    Given a requirement id r2
    And no requirement has the requirement id r2
    And a retirement list r1
    And the retirement list r1 holds the requirement id r2
    And an item i1
    When the person applies the retirement list r1 to the item i1
    Then the drafting service refuses this request
    And the drafting service names the requirement id r2
    And the drafting service does not keep the item i1

  @g31 @r31
  Scenario: An operation table exposed in an item is kept
    Given an operation table o1
    And an item i1
    When the person exposes the operation table o1 in the item i1
    Then the item i1 holds the operation table o1
    And the drafting service keeps the operation table o1

  @g32 @r32
  Scenario: An operation table of an operation that does not exist is refused
    Given an operation o1
    And the operation o1 does not exist
    And an operation table o2
    And the operation o1 has the operation table o2
    And an item i1
    When the person exposes the operation table o2 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the operation table o2

  @g33 @r33
  Scenario: An operation exposed again keeps only its new operation table
    Given an operation table o1
    And an operation o2
    And the operation o2 has the operation table o1
    And an item i1
    And the item i1 holds the operation table o1
    And an operation table o3
    And the operation o2 has the operation table o3
    And an operation table o4
    And the item i1 holds the operation o2
    And the operation o2 does not have the operation table o4
    When the person exposes the operation table o3 in the item i1
    Then the drafting service does not keep the operation table o4

  @g34 @r34
  Scenario: An operation withheld in an item is kept
    Given an operation o1
    And an item i1
    When the person withholds the operation o1 in the item i1
    Then the item i1 holds the operation o1
    And the drafting service keeps the operation o1

  @g35 @r35
  Scenario: Removing a capability from an item takes it and its model lines out
    Given a capability c1
    And an item i1
    And the item i1 holds the capability c1
    And a model line m1
    And the item i1 holds the model line m1
    When the person removes the capability c1 from the item i1
    Then the item i1 does not hold the capability c1
    And the drafting service does not keep the capability c1
    And the item i1 does not hold the model line m1
    And the drafting service does not keep the model line m1

  @g36 @r36
  Scenario: Drafting a new capability that another item holds is refused naming that item
    Given a capability c1
    And the capability c1 does not exist
    And an item i1
    And the item i1 holds the capability c1
    And an item i2
    And an item i3
    When the person drafts the item i2 with the capability c1
    Then the drafting service refuses this request
    And the drafting service names the item i3
    And the item i3 holds the capability c1

  @g37 @r37
  Scenario: Drafting into a new capability an in-batch item holds is refused naming the item and its batch
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a capability c1
    And the capability c1 does not exist
    And the item i1 holds the capability c1
    And a requirement r1
    And the capability c1 has the requirement r1
    And an item i2
    And an item i3
    When the person drafts the item i2 with the requirement r1
    Then the drafting service refuses this request
    And the drafting service names the batch b1
    And the drafting service names the item i3
    And the item i3 holds the capability c1

  @g38 @r38
  Scenario: A requirement of an in-batch item is reworded
    Given an item i1
    And the status of the item i1 is `in-batch`
    And a requirement r1
    And the item i1 holds the requirement r1
    And a requirement r2
    When the person rewords the requirement r1
    Then the drafting service keeps the requirement r2
    And the item i1 holds the requirement r2

  @g39 @r39
  Scenario: A requirement drafted into an in-batch item is kept
    Given an item i1
    And the status of the item i1 is `in-batch`
    And a requirement r1
    When the person drafts the item i1 with the requirement r1
    Then the item i1 holds the requirement r1
    And the drafting service keeps the requirement r1

  @g40 @r40
  Scenario: A requirement removed from an in-batch item is not kept
    Given an item i1
    And the status of the item i1 is `in-batch`
    And a requirement r1
    And the item i1 holds the requirement r1
    When the person removes the requirement r1
    Then the item i1 does not hold the requirement r1
    And the drafting service does not keep the requirement r1

  @g41 @r41
  Scenario: A model line that restates an operation is kept in the item
    Given a model line m1
    And an operation o1
    And the model line m1 restates the operation o1
    And an item i1
    When the person declares the model line m1 in the item i1
    Then the item i1 holds the model line m1
    And the drafting service keeps the model line m1

  @g42 @r42
  Scenario: An operation exposed in an item without a table given gets its table from the domain model
    Given an operation table o2
    And an operation o1
    And the operation o1 has the operation table o2
    And an item i1
    When the person exposes the operation table o2 in the item i1
    Then the operation table o2 conforms to the operation-table form
    And the drafting service keeps the operation table o2
    And the item i1 holds the operation table o2

  @g43 @r43
  Scenario: A model line removed from an item leaves it
    Given a model line m1
    And an item i1
    When the person removes the model line m1 from the item i1
    Then the item i1 does not hold the model line m1
    And the drafting service does not keep the model line m1

  @g44 @r44
  Scenario: Removing a model line that an item does not hold is refused
    Given a model line m1
    And an item i1
    And the item i1 does not hold the model line m1
    When the person removes the model line m1 from the item i1
    Then the drafting service refuses this request
    And the drafting service names the model line m1

  @g45 @r45
  Scenario: Rewording a model line of an item keeps the new model line
    Given a model line m1
    And an item i1
    And a model line m2
    When the person rewords the model line m1 in the item i1
    Then the drafting service keeps the model line m2
    And the item i1 holds the model line m2

  @g46 @r46
  Scenario: Rewording a model line that an item does not hold is refused
    Given a model line m1
    And an item i1
    And the item i1 does not hold the model line m1
    When the person rewords the model line m1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the model line m1

  @g47 @r47
  Scenario: A term removed from an item leaves it
    Given a term t1
    And an item i1
    When the person removes the term t1 from the item i1
    Then the item i1 does not hold the term t1
    And the drafting service does not keep the term t1

  @g48 @r48
  Scenario: Removing a term that an item does not hold is refused
    Given a term t1
    And an item i1
    And the item i1 does not hold the term t1
    When the person removes the term t1 from the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g50 @r50
  Scenario: Rewording a term that an item does not hold is refused
    Given a term t1
    And an item i1
    And the item i1 does not hold the term t1
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g51 @r51
  Scenario: A term written into a pack for an item is kept
    Given a term t1
    And a pack p1
    And an item i1
    When the person writes the term t1 into the pack p1 with the item i1
    Then the item i1 holds the term t1
    And the drafting service keeps the term t1

  @g52 @r52
  Scenario: A term that its pack has already is refused
    Given a term t1
    And a pack p1
    And the pack p1 has the term t1
    And an item i1
    When the person writes the term t1 into the pack p1 with the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g53 @r53
  Scenario: A universal condition removed from an item is no longer kept
    Given a universal condition u1
    And an item i1
    When the person removes the universal condition u1 from the item i1
    Then the item i1 does not hold the universal condition u1
    And the drafting service does not keep the universal condition u1

  @g54 @r54
  Scenario: An upstream entry removed from an item is no longer kept
    Given an upstream entry u1
    And an item i1
    When the person removes the upstream entry u1 from the item i1
    Then the item i1 does not hold the upstream entry u1
    And the drafting service does not keep the upstream entry u1

  @g55 @r55
  Scenario: A given block removed from an item is no longer kept
    Given a given block g1
    And an item i1
    When the person removes the given block g1 from the item i1
    Then the item i1 does not hold the given block g1
    And the drafting service does not keep the given block g1

  @g56 @r56
  Scenario: Removing a universal condition that the item does not hold is refused
    Given a universal condition u1
    And an item i1
    And the item i1 does not hold the universal condition u1
    When the person removes the universal condition u1 from the item i1
    Then the drafting service refuses this request
    And the drafting service names the universal condition u1

  @g57 @r57
  Scenario: Removing an upstream entry that the item does not hold is refused
    Given an upstream entry u1
    And an item i1
    And the item i1 does not hold the upstream entry u1
    When the person removes the upstream entry u1 from the item i1
    Then the drafting service refuses this request
    And the drafting service names the upstream entry u1

  @g58 @r58
  Scenario: Removing a given block that the item does not hold is refused
    Given a given block g1
    And an item i1
    And the item i1 does not hold the given block g1
    When the person removes the given block g1 from the item i1
    Then the drafting service refuses this request
    And the drafting service names the given block g1

  @g59 @r59
  Scenario: A universal condition replaced in an item keeps the new one
    Given a universal condition u1
    And an item i1
    And a universal condition u2
    When the person replaces the universal condition u1 in the item i1
    Then the drafting service keeps the universal condition u2
    And the item i1 holds the universal condition u2

  @g60 @r60
  Scenario: An upstream entry replaced in an item keeps the new one
    Given an upstream entry u1
    And an item i1
    And an upstream entry u2
    When the person replaces the upstream entry u1 in the item i1
    Then the drafting service keeps the upstream entry u2
    And the item i1 holds the upstream entry u2

  @g61 @r61
  Scenario: A given block replaced in an item keeps the new one
    Given a given block g1
    And an item i1
    And a given block g2
    When the person replaces the given block g1 in the item i1
    Then the drafting service keeps the given block g2
    And the item i1 holds the given block g2

  @g62 @r62
  Scenario: Replacing a universal condition that the item does not hold is refused
    Given a universal condition u1
    And an item i1
    And the item i1 does not hold the universal condition u1
    When the person replaces the universal condition u1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the universal condition u1

  @g63 @r63
  Scenario: Replacing an upstream entry that the item does not hold is refused
    Given an upstream entry u1
    And an item i1
    And the item i1 does not hold the upstream entry u1
    When the person replaces the upstream entry u1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the upstream entry u1

  @g64 @r64
  Scenario: Replacing a given block that the item does not hold is refused
    Given a given block g1
    And an item i1
    And the item i1 does not hold the given block g1
    When the person replaces the given block g1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the given block g1

  @g65 @r65
  Scenario: A requirement drafted into an item joins its group of the same group title
    Given a requirement group r1
    And a capability c1
    And the capability c1 has the requirement group r1
    And an item i1
    And the item i1 holds the requirement group r1
    And a group title g1
    And the requirement group r1 has the group title g1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a requirement group r3
    And the requirement group r3 does not have the group title g1
    When the person drafts the item i1 with the requirement r2
    Then the drafting service does not keep the requirement group r3

  @g66 @r66
  Scenario: A model line moved in an item is kept
    Given a model line m1
    And an item i1
    When the person moves the model line m1 in the item i1
    Then the item i1 holds the model line m1
    And the drafting service keeps the model line m1

  @g67 @r67
  Scenario: Moving a model line that the domain model does not hold is refused
    Given a model line m1
    And this domain model does not hold the model line m1
    And an item i1
    When the person moves the model line m1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the model line m1

  @g68 @r68
  Scenario: A term moved in an item is kept
    Given a term t1
    And an item i1
    When the person moves the term t1 in the item i1
    Then the item i1 holds the term t1
    And the drafting service keeps the term t1

  @g69 @r69
  Scenario: Moving a term that no area holds is refused
    Given a term t1
    And no area holds the term t1
    And an item i1
    When the person moves the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g70 @r70
  Scenario: A restatement that leaves out a member line of its element names the member line
    Given a model line m1
    And an element e1
    And the model line m1 restates the element e1
    And a member line m2
    And the model line m1 does not hold the member line m2
    And the element e1 holds the member line m2
    And an item i1
    When the person declares the model line m1 in the item i1
    Then the item i1 holds the model line m1
    And the drafting service keeps the model line m1
    And the drafting service names the member line m2

  @g71 @r71
  Scenario: A requirement group dedicated to a job serves the job in the item
    Given a requirement group r1
    And a job j1
    And an item i1
    When the person dedicates the requirement group r1 to the job j1 with the item i1
    Then the requirement group r1 serves the job j1
    And the item i1 holds the requirement group r1
    And the drafting service keeps the item i1

  @g72 @r72
  Scenario: A new capability drafted with an area is kept in that area
    Given an item i1
    And a capability c1
    And an area a1
    When the person drafts the item i1 with the capability c1 and the area a1
    Then the item i1 holds the capability c1
    And the drafting service keeps the capability c1
    And the area a1 holds the capability c1
    And the drafting service keeps the area a1

  @g73 @r73
  Scenario: A plugin pack imported into an item is kept
    Given a pack p1
    And an item i1
    When the person imports the pack p1 into the item i1
    Then the item i1 imports the pack p1
    And the drafting service keeps the item i1

  @g74 @r74
  Scenario: Importing a pack that does not exist is refused
    Given a pack p1
    And the pack p1 does not exist
    And an item i1
    When the person imports the pack p1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the pack p1

  @g75 @r75
  Scenario: A model line retired in an item is kept
    Given a model line m1
    And an item i1
    When the person retires the model line m1 in the item i1
    Then the item i1 holds the model line m1
    And the drafting service keeps the model line m1

  @g76 @r76
  Scenario: Retiring a model line that the domain model does not hold is refused
    Given a model line m1
    And this domain model does not hold the model line m1
    And an item i1
    When the person retires the model line m1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the model line m1

  @g77 @r77
  Scenario: A term retired in an item is kept
    Given a term t1
    And an item i1
    When the person retires the term t1 in the item i1
    Then the item i1 holds the term t1
    And the drafting service keeps the term t1

  @g78 @r78
  Scenario: Retiring a term that no area holds is refused
    Given a term t1
    And no area holds the term t1
    And an item i1
    When the person retires the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g79 @r79
  Scenario: A model line reinstated in an item is no longer retired
    Given a model line m1
    And an item i1
    When the person reinstates the model line m1 in the item i1
    Then the drafting service keeps the item i2
    And the item i2 does not retire the model line m1

  @g80 @r80
  Scenario: Reinstating a model line that the item does not retire is refused
    Given an item i1
    And a model line m1
    And the item i1 does not retire the model line m1
    When the person reinstates the model line m1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the model line m1

  @g81 @r81
  Scenario: A term reinstated in an item is no longer retired
    Given a term t1
    And an item i1
    When the person reinstates the term t1 in the item i1
    Then the drafting service keeps the item i2
    And the item i2 does not retire the term t1

  @g82 @r82
  Scenario: Reinstating a term that the item does not retire is refused
    Given an item i1
    And a term t1
    And the item i1 does not retire the term t1
    When the person reinstates the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g83 @r83
  Scenario: A pack import removed from an item is no longer imported
    Given a pack p1
    And an item i1
    When the person removes the pack p1 from the item i1
    Then the drafting service keeps the item i2
    And the item i2 does not import the pack p1

  @g84 @r84
  Scenario: Removing a pack that the item does not import is refused
    Given an item i1
    And a pack p1
    And the item i1 does not import the pack p1
    When the person removes the pack p1 from the item i1
    Then the drafting service refuses this request
    And the drafting service names the pack p1

  @g85 @r85
  Scenario: A capability drafted with a driven port keeps the port in the item
    Given an item i1
    And a capability c1
    And a driven port d1
    When the person drafts the item i1 with the capability c1 and the driven port d1
    Then the item i1 holds the capability c1
    And the drafting service keeps the capability c1
    And the driven port d1 holds the capability c1
    And the drafting service keeps the driven port d1

  @g86 @r86
  Scenario: A port line drafted with the core lines it supports is kept in the item
    Given a requirement r1
    And a requirement id r2
    And the requirement r1 supports the requirement id r2
    And an item i1
    When the person drafts the item i1 with the requirement r1
    Then the item i1 holds the requirement r1
    And the drafting service keeps the requirement r1

  @g87 @r87
  Scenario: A port line drafted as supporting a requirement id no requirement has is refused
    Given a requirement id r2
    And no requirement has the requirement id r2
    And a requirement r1
    And the requirement r1 supports the requirement id r2
    And an item i1
    When the person drafts the item i1 with the requirement r1
    Then the drafting service refuses this request
    And the drafting service names the requirement id r2

  @g88 @r88
  Scenario: A port line drafted with the core lines it supports keeps the requirement id it retires
    Given a requirement r1
    And a requirement id r2
    And the requirement r1 supports the requirement id r2
    And an item i1
    And a requirement id r3
    When the person drafts the item i1 with the requirement r1 and the requirement id r3
    Then the item i1 holds the requirement r1
    And the drafting service keeps the requirement r1
    And the item i1 holds the requirement id r3
    And the drafting service keeps the requirement id r3

  @g89 @r89
  Scenario: Reinstating a requirement id that the item does not retire is refused
    Given a requirement id r1
    And an item i1
    And the item i1 does not hold the requirement id r1
    When the person reinstates the requirement id r1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the requirement id r1

  @g90 @r90
  Scenario: A requirement id reinstated in an item is no longer retired by it
    Given a requirement id r1
    And an item i1
    When the person reinstates the requirement id r1 in the item i1
    Then the drafting service keeps the item i2
    And the item i2 does not hold the requirement id r1

  @g91 @r91
  Scenario: Reinstating a requirement id takes the retirement of the item's own requirement out
    Given a requirement r2
    And a requirement id r1
    And the requirement r2 retires the requirement id r1
    And an item i1
    And the item i1 holds the requirement r2
    And a requirement r3
    And the requirement r3 retires the requirement id r1
    When the person reinstates the requirement id r1 in the item i1
    Then the drafting service keeps the item i2
    And the item i2 does not hold the requirement r3

  @g92 @r92
  Scenario: Dedicating a requirement group to a job the product does not hold is refused
    Given this product exists
    And a job j1
    And this product does not hold the job j1
    And a requirement group r1
    And an item i1
    When the person dedicates the requirement group r1 to the job j1 with the item i1
    Then the drafting service refuses this request
    And the drafting service names the job j1

  @g93 @r93
  Scenario: A requirement drafted for a job is named with the job
    Given a requirement group r1
    And a job j1
    And an item i1
    And a requirement r2
    When the person dedicates the requirement group r1 to the job j1 with the item i1 and the requirement r2
    Then the item i1 holds the requirement r2
    And the drafting service keeps the requirement r2
    And the drafting service names the requirement r2
    And the drafting service names the requirement group r1
    And the drafting service names the job j1

  @g94 @r94
  Scenario: A term that violates v_t6 is kept and the rule named
    Given a term t1
    And the term t1 violates `v_t6`
    And an item i1
    When the person writes the term t1 into the item i1
    Then the item i1 holds the term t1
    And the drafting service keeps the term t1
    And the drafting service names `v_t6`
    And the drafting service completes this request

  @g95 @r95
  Scenario: Rewording a term of an item in a capability keeps the new term
    Given a term t1
    And an item i1
    And a capability c1
    And a term t2
    When the person rewords the term t1 in the item i1 with the capability c1
    Then the drafting service keeps the term t2
    And the item i1 holds the term t2

  @g96 @r96
  Scenario: A requirement group dedicated to a job of a product not of the product form is kept and the product named
    Given this product does not conform to the product form
    And a requirement group r1
    And a job j1
    And an item i1
    When the person dedicates the requirement group r1 to the job j1 with the item i1
    Then the requirement group r1 serves the job j1
    And the item i1 holds the requirement group r1
    And the drafting service keeps the item i1
    And the drafting service names this product

  @g97 @r97
  Scenario: A requirement group dedicated to a job the product holds, given by the job's id, is kept
    Given a job j1
    And this product holds the job j1
    And an id i1
    And the job j1 has the id i1
    And a requirement group r1
    And an item i2
    When the person dedicates the requirement group r1 to the job j1 with the item i2
    Then the requirement group r1 serves the job j1
    And the item i2 holds the requirement group r1
    And the drafting service keeps the item i2

  @g98 @r98
  Scenario: A requirement drafted into an item is returned with its id
    Given an item i1
    And a requirement r1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    When the person drafts the item i1 with the requirement r1
    Then the drafting service returns the requirement id r2
    And the drafting service returns the requirement r1

  @g101 @r101
  Scenario: work line --term refuses a verb with no aspect, no Frame: or a Frame: that does not read (case 1)
    Given a term t1
    And the term t1 violates `v_t4`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g101 @r101
  Scenario: work line --term refuses a verb with no aspect, no Frame: or a Frame: that does not read (case 2)
    Given a term t1
    And the term t1 violates `v_t7`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g101 @r101
  Scenario: work line --term refuses a verb with no aspect, no Frame: or a Frame: that does not read (case 3)
    Given a term t1
    And the term t1 violates `v_t11`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g101 @r101
  Scenario: work line --term refuses a verb with no aspect, no Frame: or a Frame: that does not read (case 4)
    Given a term t1
    And the term t1 violates `v_t13`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g101 @r101
  Scenario: work line --term refuses a verb with no aspect, no Frame: or a Frame: that does not read (case 5)
    Given a term t1
    And the term t1 violates `v_t14`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g101 @r101
  Scenario: work line --term refuses a verb with no aspect, no Frame: or a Frame: that does not read (case 6)
    Given a term t1
    And the term t1 violates `v_t19`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g102 @r102
  Scenario: Rewording a term into one that breaks a lexicon rule is refused naming each rule (case 1)
    Given a term t1
    And the term t1 violates `v_t4`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g102 @r102
  Scenario: Rewording a term into one that breaks a lexicon rule is refused naming each rule (case 2)
    Given a term t1
    And the term t1 violates `v_t7`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g102 @r102
  Scenario: Rewording a term into one that breaks a lexicon rule is refused naming each rule (case 3)
    Given a term t1
    And the term t1 violates `v_t11`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g102 @r102
  Scenario: Rewording a term into one that breaks a lexicon rule is refused naming each rule (case 4)
    Given a term t1
    And the term t1 violates `v_t13`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g102 @r102
  Scenario: Rewording a term into one that breaks a lexicon rule is refused naming each rule (case 5)
    Given a term t1
    And the term t1 violates `v_t14`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g102 @r102
  Scenario: Rewording a term into one that breaks a lexicon rule is refused naming each rule (case 6)
    Given a term t1
    And the term t1 violates `v_t19`
    And an item i1
    And a rule r1
    And the term t1 violates the rule r1
    And a rule r2
    And the term t1 violates the rule r2
    And a rule r3
    And the term t1 does not violate the rule r3
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1
    And the drafting service names the rule r1
    And the drafting service names the rule r2
    And the drafting service does not name the rule r3

  @g103 @r103
  Scenario: A term written into an item is returned
    Given a term t1
    And an item i1
    When the person writes the term t1 into the item i1
    Then the drafting service returns the term t1

  @g105 @r105
  Scenario: A reworded term is kept, returned and the request completed
    Given a term t1
    And an item i1
    And a term t2
    When the person rewords the term t1 in the item i1
    Then the drafting service keeps the term t2
    And the item i1 holds the term t2
    And the drafting service returns the term t2
    And the drafting service completes this request

  @g106 @r106
  Scenario: A reworded requirement is kept and returned with its id
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a requirement r2
    And a requirement id r3
    When the person rewords the requirement r1
    Then the drafting service keeps the requirement r2
    And the item i1 holds the requirement r2
    And the drafting service returns the requirement id r3
    And the requirement r2 has the requirement id r3
    And the drafting service returns the requirement r2

  @g107 @r107
  Scenario: Rewording a requirement to the text the item holds changes nothing
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    When the person rewords the requirement r1 with the requirement r1
    Then the drafting service changes nothing
    And the drafting service names the requirement r1

  @g108 @r108
  Scenario: A term whose part of speech does not fit the element it means is refused
    Given a term t1
    And an element e1
    And the term t1 does not fit the element e1
    And the term t1 means the element e1
    And an item i1
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g109 @r109
  Scenario: Rewording a term into one whose part of speech does not fit the element it means is refused
    Given a term t1
    And an element e1
    And the term t1 does not fit the element e1
    And the term t1 means the element e1
    And an item i1
    When the person rewords the term t1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g110 @r110
  Scenario: work line --term refuses a frame that text other than a frame follows in its entry, naming the frame
    Given a frame f1
    And a term t1
    And the frame f1 does not end the term t1
    And the term t1 has the frame f1
    And an item i1
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the frame f1

  @g111 @r111
  Scenario: work line --term refuses a slot of a frame that names no kind, no actor and no parameter, naming the slot
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a slot s1
    And the frame f1 has the slot s1
    And the slot s1 refers to no term
    And the slot s1 refers to no parameter
    And an item i1
    When the person writes the term t1 into the item i1
    Then the drafting service refuses this request
    And the drafting service names the slot s1

  @g112 @r112
  Scenario: spec check --item reports the item's lexicon problems as work ready does, and --reword-term warns as --term does
    Given a term t1
    And the term t1 violates `v_t6`
    And an item i1
    When the person rewords the term t1 in the item i1
    Then the item i1 holds the term t1
    And the drafting service keeps the term t1
    And the drafting service names `v_t6`
    And the drafting service completes this request

  @g113 @r113
  Scenario: A line drafted into one capability that retires a requirement of another is kept in the item
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    And an item i1
    And a capability c2
    And a requirement r3
    And an item i2
    When the person drafts the item i1 with the requirement id r2 and the capability c2
    Then the capability c2 has the requirement r3
    And the requirement r3 retires the requirement id r2
    And the drafting service keeps the item i2
    And the item i2 holds the requirement r3

  @g114 @r114
  Scenario: An area retired in an item is kept
    Given an area a1
    And an item i1
    When the person retires the area a1 in the item i1
    Then the drafting service keeps the item i2
    And the item i2 retires the area a1

  @g115 @r115
  Scenario: Retiring an area that the domain model does not hold is refused
    Given an area a1
    And this domain model does not hold the area a1
    And an item i1
    When the person retires the area a1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the area a1

  @g116 @r116
  Scenario: Retiring an area that holds a model line is refused
    Given a model line m1
    And an area a1
    And the area a1 holds the model line m1
    And an item i1
    When the person retires the area a1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the model line m1

  @g117 @r117
  Scenario: Retiring an area that holds a term is refused
    Given a term t1
    And an area a1
    And the area a1 holds the term t1
    And an item i1
    When the person retires the area a1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the term t1

  @g118 @r118
  Scenario: Retiring an area that holds a capability with a requirement is refused
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And an area a1
    And the area a1 holds the capability c1
    And an item i1
    When the person retires the area a1 in the item i1
    Then the drafting service refuses this request
    And the drafting service names the requirement r1
