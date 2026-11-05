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
