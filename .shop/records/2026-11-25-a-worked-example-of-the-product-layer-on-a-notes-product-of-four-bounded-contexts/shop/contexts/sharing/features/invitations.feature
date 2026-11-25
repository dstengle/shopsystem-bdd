# generated from spec/capabilities/invitations.md by features generate; do not edit
Feature: Invitations
  Narrator: the owner

  @g1 @r1
  Scenario: A note shared with an address is kept as an invitation
    Given a note n1
    When the owner shares the note n1 with an address
    Then the sharing service keeps the invitation i1
    And the invitation i1 has the note n1

  @g2 @r2
  Scenario: A note shared without an address is refused
    Given a note n1
    When the owner shares the note n1 without an address
    Then the sharing service refuses this request
    And the sharing service names the address

  @g3 @r9
  Scenario: An invitation accepted is accepted and its note shown
    Given an invitation i1
    When the colleague accepts the invitation i1
    Then the sharing service sets the status of the invitation i1 to `accepted`
    And the sharing service shows the note n1
    And the invitation i1 has the note n1

  @g4 @r5
  Scenario: A withdrawn invitation is not accepted
    Given an invitation i1
    And the status of the invitation i1 is `withdrawn`
    When the colleague accepts the invitation i1
    Then the sharing service refuses this request
    And the sharing service names the invitation i1

  @g5 @r6
  Scenario: An invitation declined is declined
    Given an invitation i1
    When the colleague declines the invitation i1
    Then the sharing service sets the status of the invitation i1 to `declined`

  @g6 @r7
  Scenario: An invitation withdrawn is withdrawn
    Given an invitation i1
    When the owner withdraws the invitation i1
    Then the sharing service sets the status of the invitation i1 to `withdrawn`

  @g8 @r8
  Scenario: An accepted invitation withdrawn has its note hidden
    Given an invitation i1
    And the status of the invitation i1 is `accepted`
    When the owner withdraws the invitation i1
    Then the sharing service hides the note n1
    And the invitation i1 has the note n1
