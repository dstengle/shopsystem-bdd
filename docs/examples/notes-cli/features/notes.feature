# generated from spec/capabilities/notes.md by features generate; do not edit
Feature: Notes
  Narrator: the person

  @g1 @r1
  Scenario: `notes add` adds a note under a tag
    When the person runs `notes add` with the `--title` and `--tag` options
    Then the note n1 is under the tag t1
    And `notes` adds the note n1
    And `notes` exits successfully

  @g2 @r2
  Scenario: `notes add` refuses a note with no title
    When the person runs `notes add` without the `--title` option
    Then `notes` refuses `notes add`
    And `notes` names the `--title` option

  @g3 @r3
  Scenario: `notes list` prints every note
    Given the file `notes.json` holds:
      """
      [{"title": "Buy milk", "tags": ["home"]},
       {"title": "Call the bank", "tags": []}]
      """
    And a note n1
    And a note n2
    When the person runs `notes list`
    Then the note n1 has the title t1
    And `notes` prints the title t1
    And the note n2 has the title t2
    And `notes` prints the title t2

  @g4 @r4
  Scenario: `notes remove` deletes a note
    Given a note n1
    When the person runs `notes remove` on the note n1
    Then `notes` deletes the note n1
