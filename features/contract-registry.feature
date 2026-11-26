# generated from spec/capabilities/contract-registry.md by features generate; do not edit
Feature: Contract registry
  Narrator: the specification service

  @g1 @r1
  Scenario: A contract deposited is kept by the registry
    Given a contract c1
    When the specification service deposits the contract c1
    Then the contract registry service completes this request

  @g2 @r2
  Scenario: A contract retrieved is returned by the registry
    Given a contract c1
    When the specification service retrieves the contract c1
    Then the contract registry service returns the contract c1

  @g3 @r3
  Scenario: A contract retrieved at a version never deposited is refused by the registry
    Given a version v1
    And no contract has the version v1
    And a contract c1
    When the specification service retrieves the contract c1 with the version v1
    Then the contract registry service refuses this request
    And the contract registry service names the version v1

  @g4 @r4
  Scenario: A contract registered for an adapter spec is kept by the registry
    Given a contract c1
    And an adapter spec a1
    When the specification service registers the contract c1 for the adapter spec a1
    Then the contract registry service completes this request

  @g5 @r5
  Scenario: A contract deregistered for an adapter spec is no longer kept by the registry
    Given a contract c1
    And an adapter spec a1
    When the specification service deregisters the contract c1 for the adapter spec a1
    Then the contract registry service completes this request
