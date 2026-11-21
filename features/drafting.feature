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

  @g14 @r14
  Scenario: Rewording a requirement of an item keeps the new requirement
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a requirement r2
    When the person rewords the requirement r1
    Then the drafting service keeps the requirement r2
    And the item i1 holds the requirement r2

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
