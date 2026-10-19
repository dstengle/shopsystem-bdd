---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r2-r7, supervision#r27, supervision#r34, supervision#r35]
blocked_by: [work-item/work-queue-2, work-item/work-queue-3]
risk: data
---

# supervision-1

## Observable
`work step <item>` runs a drafted item's researcher or a researched item's planner as a fresh worker, reads its
result file, and moves the item, retries, or puts it to awaiting-ruling, with every start and end logged.

## Unknown
What `claude -p --agent shopsystem-bdd:<agent> --output-format json` gives for a plugin agent's session (session id,
cost, usage), and whether `--agent` loads the agent's `skills:` and `effort:` (a probe against the installed claude,
recorded in the notes).

## What goes green
supervision#r2-r7, r27, r34, r35: the brief file, the run directory `runs/<item>/<k>-<stage>/`, the result's form per
stage (design-decision/worker-results-are-files), a failed stage and its one retry, the restore of a work file a
worker changed, writing the file set, notes, plan and depends_on into the item, QUESTION to awaiting-ruling, the
log lines with the session's figures, and the two printed lines.

## Files, roughly
`scripts/work` (`step`), new `scripts/supervise.py` (stages, briefs, result schemas, the worker process), new
`tests/scripts/stub_claude.py` (a stand-in `claude` that reads its brief and writes the result a script tells it to,
with a `session.json` like claude's), step definitions for `features/supervision.feature`.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
