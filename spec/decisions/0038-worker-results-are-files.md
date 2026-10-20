---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/worker-results-are-files
summary: "A worker is a fresh session given one brief file, and its outcome is a JSON result file of its stage's form that work run reads; work run never parses a worker's prose and never resumes a worker."
date: 2026-10-19
status: proposed
supersedes: design-decision/fresh-agents-short-replies
source: [initiative/i10, design-decision/fresh-agents-short-replies, measurement/2026-10-12-spec-round-test-log]
by: "(reply files)"
---

# 0038. Worker results are files

## Decision

`work run` writes a brief file into the stage's run directory, `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`,
and starts the worker with a prompt that names it. The worker writes its notes, plan, report or findings there and,
last, `result.json`: `status` (DONE, DONE_WITH_CONCERNS, PARTIAL, BLOCKED, NEEDS_CONTEXT, HAND-BACK or QUESTION, as
its stage allows), `summary` (under fifteen lines), `questions` (each with its readings), and the stage's own fields
(the researcher's and planner's `fileset`, the planner's `depends_on` and `plan`, the implementer's `commits` and
`report`, a reviewer's `findings`). A missing or malformed result is a failed stage. `claude -p --output-format json`
is written beside it, so cost, turns and the session id are read from a file too. No worker is resumed: a
continuation, a fix or a re-review is a fresh worker given the files.
