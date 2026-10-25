  # [r22] **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.
  @r22
  Scenario: request with an empty delegation is refused, and nothing changes
    Pins that a request is not taken in with a delegation that names no question a session may answer in the person's place.
    Given an upstream that keeps no request
    And a file lines.md with two lines in strict EARS
    When the asker runs `work request "Show the queue" --from ctx-a --lines lines.md --source o1 --delegation ""`
    Then the command is refused because the delegation is empty
    And it exits with an error
    And the upstream keeps no request
