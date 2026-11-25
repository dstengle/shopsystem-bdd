# generated from spec/capabilities/plans.md by features generate; do not edit
Feature: Plans
  Narrator: the person

  @g1 @r1
  Scenario: Subscribing to a plan charges a subscription
    Given a plan p1
    When the person subscribes to the plan p1
    Then the accounts service charges the subscription s1
    And the subscription s1 has the plan p1

  @g2 @r2
  Scenario: A charge completed makes the subscription charged and entitles it
    Given a subscription s1
    And the status of the subscription s1 is `requested`
    When the payments service completes this request
    Then the accounts service sets the status of the subscription s1 to `charged`
    And the accounts service entitles the subscription s1

  @g3 @r3
  Scenario: A charge refused is told to the person
    Given a subscription s1
    And the status of the subscription s1 is `requested`
    When the payments service refuses this request
    Then the accounts service notifies the person of the subscription s1

  @g4 @r4
  Scenario: An entitlement completed makes the subscription active
    Given a subscription s1
    And the status of the subscription s1 is `charged`
    When the notebook service completes this request
    Then the accounts service sets the status of the subscription s1 to `active`

  @g5 @r5
  Scenario: An entitlement refused refunds the charge
    Given a subscription s1
    And the status of the subscription s1 is `charged`
    When the notebook service refuses this request
    Then the accounts service refunds the subscription s1
    And the accounts service sets the status of the subscription s1 to `refunded`
