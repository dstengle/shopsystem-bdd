# generated from spec/capabilities/readiness.md by features generate; do not edit
Feature: Readiness
  Narrator: a person or session readying an item

  @g4 @r4
  Scenario: `work ready` asks no question
    Given an item i1
    When the person runs `work ready` on the item i1
    Then `work` does not ask a question

  @g23 @r23
  Scenario: `work ready` readies a shaped item that passes the readiness bar
    Given an item i1
    And the status of the item i1 is `shaped`
    And the item i1 passes this readiness bar
    When the person runs `work ready` on the item i1
    Then `work` sets the status of the item i1 to `ready`

  @g24 @r24
  Scenario: `work ready` refuses an item that does not pass the readiness bar, naming each bar check it does not meet
    Given an item i1
    And the status of the item i1 is `shaped`
    And the item i1 does not pass this readiness bar
    And a bar check b1
    And this readiness bar has the bar check b1
    And the item i1 does not meet the bar check b1
    And a bar check b2
    And this readiness bar has the bar check b2
    And the item i1 does not meet the bar check b2
    And a bar check b3
    And the item i1 does not meet the bar check b3
    And this readiness bar does not have the bar check b3
    When the person runs `work ready` on the item i1
    Then `work` refuses `work ready`
    And `work` names the bar check b1
    And `work` names the bar check b2
    And `work` does not name the bar check b3

  @g25 @r25
  Scenario: `work ready` refuses an item that is not shaped
    Given an item i1
    And the status of the item i1 is not `shaped`
    When the person runs `work ready` on the item i1
    Then `work` refuses `work ready`
    And `work` names the status of the item i1

  @g26 @r26
  Scenario: `work line --relation` writes a relation row in an item
    Given a relation row r1
    And an item i1
    When the person runs `work line` with the `--relation` option set to the relation row r1 on the item i1
    Then the item i1 holds the relation row r1
    And `work` writes the relation row r1
    And `work` commits the item i1

  @g27 @r27
  Scenario: `work line --relation` refuses a relation row that does not conform to the relation-row form
    Given a relation row r1
    And the relation row r1 does not conform to the relation-row form
    When the person runs `work line` with the `--relation` option set to the relation row r1
    Then `work` refuses `work line`
    And `work` names the relation row r1

  @g28 @r28
  Scenario: `work line --universal` writes a universal condition in an item
    Given a universal condition u1
    And an item i1
    When the person runs `work line` with the `--universal` option set to the universal condition u1 on the item i1
    Then the item i1 holds the universal condition u1
    And `work` writes the universal condition u1
    And `work` commits the item i1

  @g29 @r29
  Scenario: `work line --upstream` writes an upstream entry in an item
    Given an upstream entry u1
    And an item i1
    When the person runs `work line` with the `--upstream` option set to the upstream entry u1 on the item i1
    Then the item i1 holds the upstream entry u1
    And `work` writes the upstream entry u1
    And `work` commits the item i1

  @g30 @r30
  Scenario: `work line --upstream` refuses an upstream entry that does not conform to the upstream-entry form
    Given an upstream entry u1
    And the upstream entry u1 does not conform to the upstream-entry form
    When the person runs `work line` with the `--upstream` option set to the upstream entry u1
    Then `work` refuses `work line`
    And `work` names the upstream entry u1

  @g31 @r31
  Scenario: `work line --given` writes a given block in an item
    Given a given block g1
    And an item i1
    When the person runs `work line` with the `--given` option set to the given block g1 on the item i1
    Then the item i1 holds the given block g1
    And `work` writes the given block g1
    And `work` commits the item i1

  @g32 @r32
  Scenario: `work line --given` refuses a given block that does not conform to the example-data form
    Given a given block g1
    And the given block g1 does not conform to the example-data form
    When the person runs `work line` with the `--given` option set to the given block g1
    Then `work` refuses `work line`
    And `work` names the given block g1

  @g34 @r34
  Scenario: `work line --retires` writes a requirement in an item
    Given an item i1
    When the person runs `work line` with the `--retires` option on the item i1
    Then `work` writes the requirement r1
    And the item i1 holds the requirement r1
    And `work` commits the item i1

  @g35 @r35
  Scenario: `work line --retires` refuses a requirement id that no requirement has
    Given a requirement id r1
    And no requirement has the requirement id r1
    When the person runs `work line` with the `--retires` option set to the requirement id r1
    Then `work` refuses `work line`
    And `work` names the requirement id r1

  @g36 @r36
  Scenario: `work ready` refuses an item a term of which violates a rule
    Given an item i1
    And the status of the item i1 is `shaped`
    And a term t1
    And the item i1 holds the term t1
    And a rule r1
    And the term t1 violates the rule r1
    When the person runs `work ready` on the item i1
    Then `work` refuses `work ready`
    And `work` names the term t1
    And `work` names the rule r1

  @g37 @r37
  Scenario: `work line --recodify` sets the language of a capability in an item
    Given a capability c1
    And an item i1
    When the person runs `work line` with the `--recodify` option set to the capability c1 on the item i1
    Then the item i1 holds the capability c1
    And `work` sets the language of the capability c1 to `codified-2`
    And `work` commits the item i1

  @g38 @r38
  Scenario: `work line --recodify universal` sets the language of the universal conditions in an item
    Given an item i1
    When the person runs `work line` with the `--recodify` option set to `universal` on the item i1
    Then the item i1 holds `universal`
    And `work` sets the language of `universal` to `codified-2`
    And `work` commits the item i1

  @g39 @r39
  Scenario: `work line --universal --retires` writes a universal condition in an item
    Given an item i1
    When the person runs `work line` with the `--universal` and `--retires` options on the item i1
    Then `work` writes the universal condition u1
    And the item i1 holds the universal condition u1
    And `work` commits the item i1

  @g40 @r40
  Scenario: `work line --universal --retires` refuses a universal condition id that no universal condition has
    Given a universal condition id u1
    And no universal condition has the universal condition id u1
    When the person runs `work line` with the `--universal` option and the `--retires` option set to the universal condition id u1
    Then `work` refuses `work line`
    And `work` names the universal condition id u1

  @g41 @r41
  Scenario: `work ready` refuses an item a requirement of which has no translation
    Given an item i1
    And the status of the item i1 is `shaped`
    And a requirement r1
    And the item i1 holds the requirement r1
    And the requirement r1 has no translation
    When the person runs `work ready` on the item i1
    Then `work` refuses `work ready`
    And `work` names the requirement r1

  @g42 @r42
  Scenario: `work line --reword` rewords a requirement of an item
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    When the person runs `work line` with the `--reword` option set to the requirement id r2 on the item i1
    Then `work` removes the requirement r1
    And `work` writes the requirement r3
    And the item i1 holds the requirement r3
    And `work` commits the item i1

  @g43 @r43
  Scenario: `work line --remove` removes a requirement of an item
    Given a requirement r1
    And an item i1
    And the item i1 holds the requirement r1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    When the person runs `work line` with the `--remove` option set to the requirement id r2 on the item i1
    Then `work` removes the requirement r1
    And `work` commits the item i1

  @g44 @r44
  Scenario: `work line --reword` refuses a requirement of a capability
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    And an item i1
    When the person runs `work line` with the `--reword` option set to the requirement id r2 on the item i1
    Then `work` refuses `work line`
    And `work` names the requirement id r2

  @g45 @r45
  Scenario: `work line --remove` refuses a requirement of a capability
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    And an item i1
    When the person runs `work line` with the `--remove` option set to the requirement id r2 on the item i1
    Then `work` refuses `work line`
    And `work` names the requirement id r2

  @g46 @r46
  Scenario: `work ready` refuses an item a universal condition of which has no translation when `spec/universal.md` does not exist
    Given `universal` does not exist
    And an item i1
    And the status of the item i1 is `shaped`
    And a universal condition u1
    And the item i1 holds the universal condition u1
    And the universal condition u1 has no translation
    When the person runs `work ready` on the item i1
    Then `work` refuses `work ready`
    And `work` names the universal condition u1

  @g47 @r47
  Scenario: `work line --retires --no-line` retires a requirement in an item with no line replacing it
    Given a requirement id r1
    And an item i1
    And a requirement r2
    And the item i1 holds the requirement r2
    When the person runs `work line` with the `--no-line` option and the `--retires` option set to the requirement id r1 on the item i1
    Then the item i1 holds the requirement id r1
    And `work` writes the requirement id r1
    And `work` does not write the requirement r2
    And `work` commits the item i1

  @g48 @r48
  Scenario: `work line --retires --no-line` refuses a requirement id that no requirement has
    Given a requirement id r1
    And no requirement has the requirement id r1
    When the person runs `work line` with the `--no-line` option and the `--retires` option set to the requirement id r1
    Then `work` refuses `work line`
    And `work` names the requirement id r1

  @g49 @r49
  Scenario: `work ready` refuses an item a requirement group of which shares its condition and trigger with another group (`v15n`)
    Given an item i1
    And the status of the item i1 is `shaped`
    And a requirement group r1
    And the item i1 holds the requirement group r1
    And the requirement group r1 violates `v15n`
    When the person runs `work ready` on the item i1
    Then `work` refuses `work ready`
    And `work` names the requirement group r1
    And `work` names `v15n`
