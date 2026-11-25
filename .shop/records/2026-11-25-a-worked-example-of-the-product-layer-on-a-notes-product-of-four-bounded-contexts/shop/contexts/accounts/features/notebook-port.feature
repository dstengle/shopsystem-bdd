# generated from spec/capabilities/notebook-port.md by features generate; do not edit
Feature: Notebook port
  Narrator: the accounts service

  @g1 @r1
  Scenario: A subscription entitled completes
    Given a subscription s1
    When the accounts service entitles the subscription s1
    Then the notebook service completes this request
