# generated from spec/capabilities/charging.md by features generate; do not edit
Feature: Charging a card
  Narrator: a merchant

  @g1 @r1
  Scenario: A card authorised is granted
    Given a card c1
    When the merchant authorises the card c1 with an amount and a currency and a reference
    Then the payments service keeps the authorisation a1
    And the authorisation a1 is on the card c1

  @g2 @r2
  Scenario: A blocked card is declined
    Given a card c1
    And the standing of the card c1 is `blocked`
    When the merchant authorises the card c1
    Then the payments service refuses this request
    And the payments service names the card c1

  @g3 @r3
  Scenario: An amount over the limit is refused
    Given a card c1
    When the merchant authorises the card c1 with the amount `10000`
    Then the payments service refuses this request
    And the payments service names the amount

  @g4 @r4
  Scenario: An authorisation captured is captured
    Given an authorisation a1
    And the status of the authorisation a1 is `granted`
    When the merchant captures the authorisation a1
    Then the payments service sets the status of the authorisation a1 to `captured`

  @g5 @r5
  Scenario: A voided authorisation is not captured
    Given an authorisation a1
    And the status of the authorisation a1 is `voided`
    When the merchant captures the authorisation a1
    Then the payments service refuses this request
    And the payments service names the authorisation a1

  @g6 @r6
  Scenario: An authorisation voided is voided
    Given an authorisation a1
    And the status of the authorisation a1 is `granted`
    When the merchant voids the authorisation a1
    Then the payments service sets the status of the authorisation a1 to `voided`

  @g7 @r7
  Scenario: A captured authorisation is not voided
    Given an authorisation a1
    And the status of the authorisation a1 is `captured`
    When the merchant voids the authorisation a1
    Then the payments service refuses this request
    And the payments service names the authorisation a1

  @g8 @r8
  Scenario: A capture settled tells the merchant
    Given an authorisation a1
    And the status of the authorisation a1 is `captured`
    When the network settles the authorisation a1
    Then the payments service sets the status of the authorisation a1 to `settled`
    And the payments service notifies the merchant of the authorisation a1

  @g9 @r9
  Scenario: A capture reversed tells the merchant
    Given an authorisation a1
    And the status of the authorisation a1 is `captured`
    When the network reverses the authorisation a1
    Then the payments service sets the status of the authorisation a1 to `reversed`
    And the payments service notifies the merchant of the authorisation a1
