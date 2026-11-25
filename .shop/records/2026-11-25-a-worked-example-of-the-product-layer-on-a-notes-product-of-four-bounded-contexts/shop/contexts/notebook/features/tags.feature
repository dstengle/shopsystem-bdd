# generated from spec/capabilities/tags.md by features generate; do not edit
Feature: Tags
  Narrator: the person

  @g1 @r1
  Scenario: A tag renamed is kept
    Given a tag t1
    When the person renames the tag t1 with the spelling `work`
    Then the notes service keeps the tag t1
