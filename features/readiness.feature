# generated from spec/capabilities/readiness.md by features generate; do not edit
Feature: Readiness
  Narrator: a person or session readying an item

  @g1 @r1
  Scenario: `work ready` readies a passing item
    Given an item i1 that is `shaped`
    And the item i1 is passing
    When the person runs `work ready` on the item i1
    Then the item i1 is `ready`

  @g2 @r2
  Scenario: `work ready` refuses an item that is not passing
    Given an item i1 that is `shaped`
    And the item i1 is not passing
    When the person runs `work ready` on the item i1
    Then `work` exits with an error naming the reason r1
    And `work` changes nothing

  @g3 @r3
  Scenario: `work ready` refuses an item that is not shaped
    Given an item i1
    And the item i1 is not `shaped`
    When the person runs `work ready` on the item i1
    Then `work` exits with an error naming the status of the item i1
    And `work` changes nothing

  @g4 @r4
  Scenario: `work ready` asks no question
    When the person runs `work ready` on the item i1
    Then `work` does not ask the question q1

  @g5 @r5
  Scenario: `work line --relation` writes a relation row onto an item
    Given `--relation` is given
    When the person runs `work line` on the item i1
    Then `work` writes the relation row r1
    And `work` commits the item i1

  @g6 @r6
  Scenario: `work line --relation` refuses a malformed relation row
    Given `--relation` is given
    And a relation row r1
    And the relation row r1 is malformed
    When the person runs `work line` on the relation row r1
    Then `work` exits with an error naming the relation row r1
    And `work` changes nothing

  @g7 @r7
  Scenario: `work line --universal` writes a universal condition onto an item
    Given `--universal` is given
    When the person runs `work line` on the item i1
    Then `work` writes the universal condition u1
    And `work` commits the item i1

  @g8 @r8
  Scenario: `work line --upstream` writes an upstream entry onto an item
    Given `--upstream` is given
    When the person runs `work line` on the item i1
    Then `work` writes the upstream entry u1
    And `work` commits the item i1

  @g9 @r9
  Scenario: `work line --upstream` refuses a malformed upstream entry
    Given `--upstream` is given
    And an upstream entry u1
    And the upstream entry u1 is malformed
    When the person runs `work line` on the upstream entry u1
    Then `work` exits with an error naming the upstream entry u1
    And `work` changes nothing

  @g10 @r10
  Scenario: `work line --given` writes a given block onto an item
    Given `--given` is given
    When the person runs `work line` on the item i1
    Then `work` writes the given block g1
    And `work` commits the item i1

  @g11 @r11
  Scenario: `work line --given` refuses a malformed given block
    Given `--given` is given
    And a given block g1
    And the given block g1 is malformed
    When the person runs `work line` on the given block g1
    Then `work` exits with an error naming the given block g1
    And `work` changes nothing

  @g12 @r12
  Scenario: `work ready` refuses an item with an unworded step
    Given an item i1 that is `shaped`
    And the item i1 is unworded
    When the person runs `work ready` on the item i1
    Then `work` exits with an error naming the step s1

  @g13 @r13
  Scenario: A line that retires another
    Given `--retires` is given
    When the person runs `work line` on the item i1
    Then `work` writes the requirement r1
    And `work` commits the item i1

  @g14 @r14
  Scenario: A retired id that no capability holds
    Given `--retires` is given
    And a requirement r1
    And the requirement r1 is nonexistent
    When the person runs `work line` on the requirement r1
    Then `work` exits with an error naming the requirement r1
    And `work` changes nothing
