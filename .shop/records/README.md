# Records

Dated, never edited (design model v3, section 3a). Not design and not work. Paths are under `.shop/records/`.

| path | record | kind |
|---|---|---|
| `observations.md` | what was noticed, one `## <id>` each | origin: may be an initiative's `source` |
| `measurements/kb-baseline-2026-10-11/` | facts of shopsystem-kb batches 32-35 (`measurement/kb-batches-32-35`) | origin |
| `measurements/fixture-runs/` | test logs of each release's fixture runs | origin (not yet given ids) |
| `review-findings/` | reviews of the plugin, such as the 13 October assessment | origin |
| `2026-10-28-gate-question-wording.md` | the causes of 42 gate questions (i39-i43) against the wording of requests, spec lines, glossary and round instructions, with five recommendations | analysis |
| `2026-10-28-tools-skills-subagents.md`, `2026-10-28-tools-skills-subagents/` | tool friction, refused commands and the case for more tools, skills or subagents over 87 sessions of i37-i42, with its scripts | analysis |
| `2026-10-28-requirement-checking.md`, `2026-10-28-requirement-checking/` | whether clingo, English-structure NLP and a fast model judge can test a requirement line, with the parser, the clingo proof of concept, its outputs and a draft requirement-writing skill | analysis |
| `2026-11-02-domain-model/` | the domain model as a typed glossary (draft): kinds, values and lifecycles, relations, events, resources, universal conditions, for the codified requirement language; with the four extractions it rests on | design (draft) |
| `2026-11-02-work-run-efficiency.md` | cost and stops of `work run` across i42-i64 (10 initiatives): where the money goes, what stops work-items, three candidates | analysis |
| `2026-11-03-gf-conversion/cost-analysis.md` | length and cost of the overnight GF conversion (design and build workflows, live run, main session: $150.09 over 6 h 21 min, measured from transcripts) and an estimate of the same work through `work run` (≈ $292 / $524 / $1,682, with 100–1,180 person rulings) | analysis |
| `2026-10-30-backlog-board-design.md` | the board: items ranked by WSJF and prepared (Backlog, Discovered, Groomed) apart from their building (Doing, Done), from a discovery conversation held in place of i57's questions; replaces q31's backlog lines | design |
| `2026-11-04-workflow-simplification/design.md` | the workflow simplified: one kind of item in a backlog across sessions, a mechanical readiness bar in place of question gates, batches built superpowers-style as one PR with one adversarial review, decisions in three tiers, telemetry and tuning, quotes with their conversation, names for ids; builds on the board design | design (draft) |
| `2026-11-04-workflow-simplification/recon.md` | the figures behind that design: cost by stage, review yield, question-gate waits (i42-i64), the GF run, the decisions and the queue, quotes and ids, what superpowers 7.0.0 offers | analysis |
| `2026-11-04-workflow-simplification/roadmap.md`, `plan-1-spec.md`, `plan-2-backlog.md` | the design built as nine plans in order; plan 1: the new workflow's lexicon and nine capabilities codified, their requirements marked `unbuilt:` until built; plan 2: the backlog built (item files in `.shop/backlog/`, the item commands of `work`, `work backlog` by state in WSJF rank order, names beside ids), its 17 requirements leaving `unbuilt:`, with 18 decisions made by the planner (revisit) | design (draft) |
| `2026-11-04-workflow-simplification/plan-1-implementation.md`, `plan-1-review.md` | plan 1 executed (10 commits, every baseline held, 11 deviations) and its end-of-branch review: mechanics sound, 10 should-fix requirement lines and 11 questions for the person before merge | report |
| `2026-11-04-workflow-simplification/plan-1-rulings.md` | the review's questions ruled by the main session without the person (revisit): fixed in place before the merge, a strict unbuilt xfail, traceability, `work answer` and the park's question, settled lines in `passing`, old-process terms lifted into the glossary; and the gaps left for later plans (the generator's dropped preconditions, weak lines, frozen references) | analysis |
| `2026-11-04-workflow-simplification/plan-2-implementation.md`, `plan-2-review.md` | plan 2 executed: the backlog built (item files, the item commands of `work`, `work backlog` by state in rank order), its 17 requirements out of `unbuilt:`; and its end-of-branch review: ready to merge, two should-fix findings (bare ids in two lines, a negated Then fixing plan 4's exit code), ten minor, two questions | report |
| `2026-11-04-workflow-simplification/plan-2-rulings.md` | the review's two questions ruled by the main session without the person (revisit): a dependency on a refused or withdrawn item refused, dropping one left to plan 4; a negated Then requires only that the command exists; and what was done with each finding | analysis |
| `archive/design-notes/`, `archive/plans/`, `archive/requests/` | the design notes, plans and requests of releases 0.6.0-0.20.0, moved from `docs/superpowers/` | history: read to trace why, never a source |

A record file is a node for `scripts/model` only when its frontmatter has an `id`, a `kind` and `about`.
