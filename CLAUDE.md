# CLAUDE.md

## Working rules

- A request's lines only propose. Write accepted lines in this context's own terms, and keep how a request is kept
  or exchanged out of every line (design-decision/requests-only-propose).
- A requirement is never edited in place. A changed one gets a new id and the old id goes to `retired:`
  (design-decision/requirements-retired-never-edited).
- A short-term direction the person gives a session is written with `work directive "<their words>"`, shown to every
  session while live, and reviewed with `work promote` or `work drop`; nothing is kept in Claude Code's memory.
- A stated intention goes into the backlog in the same turn: `work idea` for this context's own, `work request` for
  an upstream's. It is never kept only in a session's memory or in a record's findings.
- Every report a session or an agent writes (an analysis, an investigation, research with recommendations) is kept
  as `.shop/records/<date>-<topic>.md`, supporting files in a folder of the same name, indexed in
  `.shop/records/README.md` and committed. `work record "<title>" --kind analysis --summary "<the index row>" --body
  <file>` writes the record file and its index row and commits them; `work record "<title>" --design --summary "<row>"
  --body <file>` a design's folder (below) and `work record "<title>" --plan --design <design> --body <file>` a plan in
  it; other supporting files are still written by hand. A committed record is never edited.
- A design-decision is written by `work decision "<title>" --summary "<one sentence>" --tier <tier> --decision
  "<text>"`, never by hand. `spec forms` names the command that writes each other file form; copy no existing file
  to learn a form.
- A design is reported as a record, under `.shop/records/<date>-<topic>/design.md`, in place of a skill's default
  `docs/superpowers/` path: nothing writes under `docs/superpowers/` (design-decision/final-layout). Its decisions are
  written as design-decisions, model changes and item lines. A plan is a batch's tasks; a plan file
  (`plan-*.md` beside the design) is a report.
- No artifact of the system cites a record: an item's provenance cites quotes, requests and decisions, and a
  conclusion something stands on is restated as a design-decision (design-decision/records-are-kept-never-cited).
- A plan is carried out by one fresh agent that implements every task in order, then one fresh reviewer of the whole
  branch; not an implementer and a reviewer per task, and not inside a long main session.
  A batch likewise: the session that runs `work batch start` dispatches one fresh agent with the batch brief it
  printed as its whole prompt, and that agent runs the batch to `awaiting-merge`.
- Requirement lines are what the rest of the system stands on: when work touches spec lines or requests, weigh
  their clarity and checkability first.
- Never read another repository on this machine (another bounded context's, the product's) unless the person asks
  for it; this repository's `main` is the only reference, never a leftover worktree of earlier work.
- A short-term direction of the person is a directive (`work directive`), never Claude Code's memory; the live ones
  are shown at SessionStart and passed on in every brief to an agent.

## Size limit

Code and test files, every tracked Python file, stay at 300 lines or fewer. `python3 scripts/tools size --limit 300` prints each one over it with its line count and exits 1 when there is any. A change does not push a file over the limit; a file that is over it already is split by the work that names it.

## Module map

The module map, each module of `scripts/` and `tests/` with its concern, is [docs/reference/modules.md](docs/reference/modules.md).
Read it when placing or reviewing a module. A new concern gets a new module and a row there.
