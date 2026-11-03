# generated from spec/capabilities/work-queue.md by features generate; do not edit
Feature: Work queue
  Narrator: the person

  @g1 @r1 @r2
  Scenario: `work start` starts a proposed initiative
    Given an initiative i1 that is `proposed`
    When the person runs `work start` on the initiative i1
    Then the initiative i1 is `started`
    And `work` exits successfully
