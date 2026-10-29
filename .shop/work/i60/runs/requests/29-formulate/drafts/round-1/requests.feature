# formulated from spec/capabilities/requests.md
Feature: Requests
  Narrator: a context taking in or raising a request

  # formulates [r72] of spec/capabilities/requests.md
  # [r72] **When** the person gives a session a delegation for a request outside `work request`, the session shall, in the same reply, write the delegation in the request by giving `work delegate` the delegation as the person's words with the date.
  @r72
  Scenario: a session the person gives a delegation for a request writes it, in the same reply, through delegate as the person's words with the date
    Pins that a delegation the person gives in a session is in the request when the session's reply ends, kept as the person's words and the day they were given, and written by delegate.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    And q1 holds no delegation
    When the person tells a session, on 2026-10-29, that for q1 it may "answer any question on line 1"
    Then in its reply to that message the session runs `work delegate`, giving q1 and the delegation 'The person, 2026-10-29: "answer any question on line 1"'
    And when that reply ends, q1's delegation is 'The person, 2026-10-29: "answer any question on line 1"'
