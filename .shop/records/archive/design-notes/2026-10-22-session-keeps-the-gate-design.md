# The session keeps the gate (i16; 0.23.0, part 3)

Source: initiative i16 and observation/2026-10-21-session-keeps-the-gate. The person approved this scope on
2026-10-22 and delegated the drafting decisions to the coordinator's recommendations; each reading is listed on the
release gate. Walking skeletons only (decision 0051's skeleton form; prove before specifying): a handful of lines
each, grown from runs. These are workflow capabilities; their fixture scenarios are not written in this release.

## spec-integration: the gate job and the apply job

- `integrating-a-proposal` gives the gate to a round: the session dispatches `initiative-round` with the job `gate`,
  naming the rounds' drafts (and any reports) to show.
- The `gate` job writes the gate page's data as files under `<drafts path>/gate/`: one card a decision the person is
  asked for, each with the coordinator's recommendation marked, the lines in full under it. It replies in a few
  lines with the path.
- The session publishes the gate page from those files and reads only the person's verdicts, not the drafts.
- The `apply` job takes the verdicts file (or the person's approval in their words) and applies exactly the
  approved drafts, as step 4 does today.
- `initiative-round` appends one line to the piece of work's ledger for every round it runs: the job, the round,
  and its outcome or the verdicts it applied.

## A new capability `trials`: the trial-runner

- A new agent `trial-runner` runs one trial: a plugin tool or `work run` on a real target or a fixture repository,
  named in its input with what to measure.
- It reads only the target and the plugin's scripts; it changes nothing in this repository but the measurement
  record it writes.
- It writes one measurement record under `.shop/records/measurements/` with what it ran, on what, and what it
  measured.
- It replies in a few lines naming the record.
- role-boundaries: the trial-runner's model is Sonnet, and it may not dispatch.

## delivery: fixes go through `work run`

- A fix to code that a review or a trial finds is drafted as a work-item and delivered by `work run`; the session
  does not change code itself.
- When a fix needs a new scenario row, the row goes to the blind `feature-formulator` (through a `formulate`
  round), never written by the implementer. (This takes supervision's "Not yet" item of a fix work-item that sends
  rows to the blind formulator, as a rule of delivering-an-initiative, not of `work run`.)

## The session's rules (delivering-an-initiative and integrating-a-proposal teach them)

- An agent the session dispatches replies in a few lines and leaves the rest in files; the session reads a file
  only to decide.
- One ledger per piece of work, `.shop/scratch/run/ledger-<name>.md`, one line an event (rulings and verdicts),
  archived under `.shop/records/archive/` when the piece of work ends.

## After a release

- The installed plugin is updated after a release so the next session runs the new agents (a step of the release,
  in the README's release notes, no line).
