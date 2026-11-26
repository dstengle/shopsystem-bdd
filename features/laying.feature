# generated from spec/capabilities/laying.md by features generate; do not edit
Feature: Laying
  Narrator: the batches service

  @g1 @r1
  Scenario: An item laid is held by the workspace
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a workspace w1
    When the batches service lays the item i1 in the workspace w1
    Then the workspace w1 holds the requirement r1
    And the laying service keeps the workspace w1
    And the requirement r1 has the requirement id r2
    And the laying service keeps the scenario s1
    And the scenario s1 refers to the requirement id r2

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

  @g3 @r3
  Scenario: A check of an item that violates a rule of severity error fails naming the rule
    Given a requirement r1
    And an item i1
    And the item i1 has the requirement r1
    And a rule r2
    And the severity of the rule r2 is `error`
    And the requirement r1 violates the rule r2
    And a workspace w1
    When the batches service checks the item i1 in the workspace w1
    Then the laying service fails this request
    And the laying service names the rule r2

  @g4 @r4
  Scenario: A check of an item that violates no rule of severity error completes
    Given an item i1
    And no requirement in the item i1 violates a rule whose severity is `error`
    And a workspace w1
    When the batches service checks the item i1 in the workspace w1
    Then the laying service completes this request

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
