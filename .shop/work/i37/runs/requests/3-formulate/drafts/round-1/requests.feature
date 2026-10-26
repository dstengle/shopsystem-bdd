  # changed: [r7] **When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side.
  @r7
  Scenario Outline: turn on a request it does not set to accepted passes the request's turn from the <side> to the <other side>
    Pins that turn hands a request still under negotiation to the side that did not have it, whichever side that is.
    Given a request q1 from the asker ctx-a whose turn is the <side>'s, with one line whose line outcome is question
    When the <side> runs `work turn q1`
    Then q1's status is not accepted
    And q1's turn is the <other side>'s

    Examples:
      | side     | other side |
      | upstream | asker      |
      | asker    | upstream   |

  # added: [r23] **When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's.
  @r23
  Scenario: the upstream ending its turn on a request that turn sets to accepted keeps the request's turn the upstream's
    Pins that a request the upstream accepts stays with the upstream, which resolves it, rather than going back to the asker.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with three lines whose line outcomes are accepted, refused and withdrawn
    When the upstream runs `work turn q1`
    Then q1's status is accepted
    And q1's turn is the upstream's

  # added: [r24] **When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker.
  @r24
  Scenario: resolve setting a request's status to delivered passes the request's turn to its asker
    Pins that a delivered request goes back to the side that asked for it, from the upstream that resolved it.
    Given a request q1 from the asker ctx-a whose status is accepted and whose turn is the upstream's, with one line whose line outcome is accepted
    When the upstream runs `work resolve q1`, giving thing#r3 for line 1, found in the version 0.26.0
    Then q1's status is delivered
    And q1's turn is the asker's
