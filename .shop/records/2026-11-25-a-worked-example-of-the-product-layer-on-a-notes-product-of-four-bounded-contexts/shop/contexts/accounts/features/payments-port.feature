# generated from spec/capabilities/payments-port.md by features generate; do not edit
Feature: Payments port
  Narrator: the accounts service

  @g1 @r1
  Scenario: A subscription charged completes
    Given a subscription s1
    When the accounts service charges the subscription s1
    Then the payments service completes this request

  @g2 @r2
  Scenario: A subscription refunded completes
    Given a subscription s1
    When the accounts service refunds the subscription s1
    Then the payments service completes this request
