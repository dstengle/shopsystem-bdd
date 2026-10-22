# Rulings, round trips and the analysis tools' query output

Source: observation/2026-10-22-release-gate-0-23-0 (round trips in `measure`; analysis-tools' `--json` lines held),
observation/2026-10-22-release-0-24-0 (`work rule` missing: every ruling needed a direct implementer). The person,
2026-10-22: "yes, do 1-6", after "I'm not running these releases so we're just cutting them for no reason if we keep
pushing things off to another release". The drafting decisions stay delegated to the coordinator; every reading
below is the coordinator's.

## work-queue and supervision: `work rule`

Today a work-item that asks a question stops at `awaiting-ruling` and nothing takes it on: the person's answer had to
be carried to a hand-run implementer, and the work-item withdrawn from `work run`.

- `work rule <work-item> <ruling>` on an `awaiting-ruling` work-item writes the ruling, with the date, under the
  work-item's `## Rulings`, and transitions it back to the status the stage that asked started from: `drafted` for
  a researcher's question, `researched` for a planner's, `ready` for an implementer's, and `done` for a reviewer's.
  It commits the work-item's file and the `log.jsonl` line, as `work retry` and `work withdraw` do.
- `work rule` on a work-item that is not `awaiting-ruling` is a change `work` cannot make (r7).
- `work run` names a work-item's rulings in the brief of every worker it starts for that work-item, so the worker
  that asked reads the answer.
- When `work run` starts an implementer for a work-item whose work-item branch was kept (r26), the implementer's
  worktree is on that branch, so it goes on from the work it did before it asked.
- A reviewer's question ruled back to `done` runs the review again; a ruling that asks for a fix is drafted as a new
  work-item, as fixes are today.

This replaces decision 0039's row "awaiting-ruling → planned | the person, `work rule`": a ruling returns the
work-item to where its question was asked, not always to `planned`.

## batch-measurement: round trips

`measure initiative` gives each stage's turns from `session.json`'s `num_turns`, which is not the unit `--max-turns`
limits (measurement/2026-10-22-research-at-the-limit). It also gives each stage's round trips: the assistant
messages of the session's transcript with distinct request ids, the unit `--max-turns` limits. `measure show` and
`measure compare` print them beside the turns.

## analysis-tools, feature-file-tools, design-model-check, work-queue: query output

Decision 0058 (accepted in 0.23.0) and its lines for `features`, `model` and `work show` are in `spec/`. The
analysis-tools lines were held when the harness refused the writer's draft. They are, as the writer drafted them
in .shop/scratch/drafts/2026-10-22-structured-query-output/round-2/gate.md and the coordinator approved them then:

- r11 changed: when no test in the map executed the target of `tools tests-of`, `tools` prints that no test of the
  map executed it, with the commit the map was made at, and exits successfully.
- r57 added: if the file given to `tools tests-of` has no function by the name given, `tools` exits with an error,
  saying the target cannot be read.
- r53 to r56 added: where `--json` is given, `tools tests-of` (the tests, their count and the map's commit),
  `tools untested` (the functions, their count and the map's commit), `tools refs` (the references and the
  summary) and `tools map` (the map's commit and its test count) print their result as one JSON object.

## Answers, not rulings (the person, 2026-10-22)

The person: "rule is a dangerous term to use. We need either an alternative or a hyphenated compound to disambiguate
it", and, offered `work give-ruling`, `work answer`, or a rename throughout, chose "Rename to 'answer' throughout".
"Rule" is already `model check`'s word (`model rules`, its rules' codes).

- The glossary's **ruling** becomes **answer**: the person's answer to a work-item's question, written in the
  work-item in their words. Its `Not:` lists ruling and rule.
- The status `awaiting-ruling` becomes `awaiting-answer`, in every line, decision row still in force, and file form.
- The command is `work answer <work-item> <answer>`; it writes under the work-item's `## Answers`.
- Every line that says ruling, rulings, ruled or awaiting-ruling says answer, answers, answered or awaiting-answer.
- An upgrade step, for the plugin version after 0.24.0, renames the status `awaiting-ruling` to `awaiting-answer` in
  every work-item's file and every `log.jsonl` line, and a work-item's `## Rulings` to `## Answers`.
