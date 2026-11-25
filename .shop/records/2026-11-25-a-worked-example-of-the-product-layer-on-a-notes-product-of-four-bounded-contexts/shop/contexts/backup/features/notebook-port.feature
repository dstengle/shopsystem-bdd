# generated from spec/capabilities/notebook-port.md by features generate; do not edit
Feature: Notebook port
  Narrator: the backup service

  @g1 @r1
  Scenario: Exporting returns a bundle
    When the backup service exports the notes
    Then the notebook service returns the bundle b1

  @g2 @r2
  Scenario: A bundle imported completes
    Given a bundle b1
    When the backup service imports the bundle b1
    Then the notebook service completes this request
