# generated from spec/capabilities/notebook-port.md by features generate; do not edit
Feature: Notebook port
  Narrator: the sharing service

  @g1 @r1
  Scenario: A note shown is shown
    Given a note n1
    When the sharing service shows the note n1
    Then the notebook service completes this request

  @g2 @r2
  Scenario: A note hidden is hidden
    Given a note n1
    When the sharing service hides the note n1
    Then the notebook service completes this request
