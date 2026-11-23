# generated from spec/capabilities/payouts.md by features generate; do not edit
Feature: Payouts and disputes
  Narrator: a merchant

  @g1 @r1
  Scenario: A payout disbursed is kept
    Given a payout p1
    When the merchant disburses the payout p1
    Then the payments service keeps the payout p1

  @g2 @r2
  Scenario: A payment contested opens a dispute and tells the merchant
    Given an authorisation a1
    When the cardholder contests the authorisation a1
    Then the payments service keeps the dispute d1
    And the dispute d1 is on the authorisation a1
    And the payments service notifies the merchant of the authorisation a1

  @g3 @r3
  Scenario: A dispute resolved completes the request
    Given a dispute d1
    When the merchant resolves the dispute d1
    Then the payments service completes this request
