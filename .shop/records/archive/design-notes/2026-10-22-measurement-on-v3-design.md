# Measurement on design model v3 (i12; 0.23.0, part 4)

Source: initiative i12 and observation/2026-10-19-final-state-only. The person approved this scope on 2026-10-22 and
delegated the drafting decisions to the coordinator's recommendations; each reading is listed on the release gate.
A walking skeleton (prove before specifying): it measures what `work run` already records, and grows from the
measurements of 0.21.0's, 0.22.0's and 0.23.0's deliveries.

## What is measured

`scripts/measure` measures one initiative's deliveries: its work-items, the stages `work run` ran for them, the
sessions of those stages and the commits that landed them. The old `measure batch` (a superpowers batch: a plan, an
archive file under `docs/superpowers/`, a ledger, slices, a suite record) is removed with every line of it; its
lines are retired and its scenarios deprecated for removal.

- `measure initiative <initiative>` writes one measurement record for the initiative under
  `.shop/records/measurements/<date>-<initiative>.md`, the date being the day it is run.
- For each stage `log.jsonl` gives a start and an end for (each worker), the record gives the work-item, the stage,
  the agent, the session id, how long the stage took, and, from the stage directory's `session.json`, the
  session's turns, output tokens, new input tokens (input and cache writes), cache-read tokens and cost.
- For each work-item, the record gives its transitions from `log.jsonl`, how many times it went to
  `awaiting-ruling` and to `failed`, and the commits merged into the initiative branch for it.
- The record gives the totals over the initiative: stages, sessions, tokens of each kind, cost, and the time from
  the first transition to the last.
- Where `--sessions <dir>` names a directory of transcripts (Claude Code's raw transcripts, or the slim export
  of dstengle/shopsystem-records), the record also gives each session found there inside the initiative's window,
  and each session it dispatched, with its tokens of each kind: the sessions that did the spec work around the
  delivery (the coordinator, its rounds and its direct dispatches).
- A measurement record is a record (frontmatter id of kind `measurement`); its figures are one JSON block in its
  body, so `measure show` and `measure compare` read them back.
- `measure show <record>` prints a record's figures as tables; `measure compare <a> <b>` prints two records'
  totals side by side with the ratio of the second to the first.
- `measure` refuses, writing nothing, when the initiative has no `log.jsonl`, when a `session.json` or a transcript
  is not of a shape it knows (naming the file), or when the record exists and `--replace` is not given.
- `measure` writes no prompt, reply or tool content into the record.

## Words

- **measurement**: a record under `.shop/records/measurements/` that `measure` writes for one initiative's
  deliveries, or that a trial writes. "Facts file" becomes "measurement file" everywhere it is used.
- The old system's glossary entries **batch**, **controller** and **suite record** ("old system, until i12") are
  removed.
- The capability keeps its file name `batch-measurement` (its ids are scoped by it); its title, narrator and
  Purpose become measurement of an initiative's deliveries.

## The skill

`analyzing-a-batch` follows it: it measures an initiative with `measure initiative`, compares two records with
`measure compare`, and names the figure a proposed workflow change should move (no line; a workflow skill).

## Two more glossary entries (from the session-keeps-the-gate round, i16)

- **ledger**: the file `.shop/scratch/run/ledger-<initiative>.md` of one initiative, one line an event, archived
  under `.shop/records/archive/` when the initiative's work ends.
- **trial**: one run by the `trial-runner` of a plugin tool or `work run` on a real target or a fixture repository,
  measuring what its input names.
