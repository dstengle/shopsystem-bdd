---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-i13-ears-briefs
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# 0.21.0 EARS restructure (i13): the three briefs

The briefs given to the agents of initiative i13-ears (release 0.21.0), in order: brief.md (round 1, restructure each Behaviour line into EARS, meaning exactly kept), brief-2.md (round 2, compact after the person found the drafts too detailed and decision 0051 changed), brief-skeleton.md (walking skeletons for the capabilities not yet built: supervision, work-queue, delivery, planning, migration-tools).

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/ears/brief.md`

~~~~~~
# Brief: restructure Behaviour lines into EARS (initiative i13)

Repository /home/vscode/shopsystem-bdd, branch release-0.21.0. Change NOTHING in the repository except
files under .shop/scratch/ears/ (git-ignored). Do not commit.

Read: decisions/0051-behaviour-lines-are-ears.md and decisions/0052-a-scenario-may-name-several-requirements.md
(binding), work/i13-ears/initiative.md, docs/capability-format.md (its Behaviour section is being replaced by
0051; its other rules stand: the response is observable by the narrator; ids [r<n>], never reused),
spec/index.md's Glossary (use its terms; avoid its Not: words).

The patterns (the person's words):
- Ubiquitous: The system shall <action>.
- Event-Driven: When <trigger>, the system shall <action>.
- State-Driven: While <state>, the system shall <action>.
- Unwanted Behavior: If <condition>, then the system shall <action>.
- Optional: Where <feature enabled>, the system shall <action>.
Complex lines combine clauses in the order Where, While, When or If … then. "the system" is the named
system: a script (`model check`, `features`, `tools`, `measure`, `work`, `migrate`), an agent, or a skill.

The person rejected "simplistic additions of shall": restructure each line by what starts the behaviour.
A command, input or event → When, with the trigger in the When clause. A refusal or fault → If … then. A
period → While. An option → Where. Only what holds with no trigger → ubiquitous. One trigger or condition,
one "shall", one response and one sentence per line. Bold the keyword as now (`**When**`, `**If**`, `then`
unbolded is fine). Approved example of the restructure (red-green r3, three conditions):
  - [r3] **If** a scenario the work-item accepts passes before any code is written for it, then the implementer shall hand back.
  - [rNEW] **If** the work-item's check passes before any work is done, then the implementer shall hand back.
  - [rNEW] **If** a scenario of a work-item not yet claimed passes, then the implementer shall hand back.

Rules:
- Meaning exactly kept: nothing added, nothing dropped. If restructuring forces a meaning choice, keep the
  closest reading and list it under Questions.
- Ids: a line whose meaning is unchanged keeps its id. A split keeps the old id on the part that is the
  line's core, and new ids, continuing above the highest id the capability has ever used (Behaviour ids AND
  `retired:` in frontmatter), for the rest. No id reused.
- Scenarios do not multiply (0052): the scenario that named the old id names each new id too. Lines that
  already state one-tag-per-scenario (e.g. formulation r11, design-model-check r20, feature-file-tools r51
  `features tag`, work-queue r20, spec-migration r11, delivery r2) change to 0052's rule; say so in the map.
- Purpose, Implementation-may-change and Not-yet sections: leave as they are, except words that would now
  contradict the restructured lines.

Write, per capability <name>:
1. `.shop/scratch/ears/capabilities/<name>.md`: the whole capability file as it would read, frontmatter
   unchanged except `retired:` if needed.
2. `.shop/scratch/ears/map/<name>.md`: a table `old id | new ids | pattern(s) | note`, then "Scenario tags":
   for each feature-file scenario (by title, in features/<name>.feature) that gains tags, the tags it gains;
   then "Questions" (meaning choices, each with your choice).
Reply in at most 6 lines: capabilities done, lines before → after, number of questions.
~~~~~~

## `.shop/scratch/ears/brief-2.md`

~~~~~~
# Brief 2: compact the EARS drafts (initiative i13, round 2)

Same setting as .shop/scratch/ears/brief.md (read it; change nothing outside .shop/scratch/ears/, commit
nothing). Re-read decisions/0051-behaviour-lines-are-ears.md: its rule changed (commit 26e0dd2). The person
found the drafts far too detailed: "a huge amount of coverage for failures that may not happen … dangerous
to specify so much without proving".

Apply to YOUR capabilities only (named in your dispatch), editing .shop/scratch/ears/capabilities/<name>.md
and .shop/scratch/ears/map/<name>.md in place:
- Conditions with the same response join in one line: `If A or B, then …`; triggers likewise where natural.
- An `If` line stays only when it is the capability's purpose (a check reporting problems), protects the
  person's files from loss or silent damage, or answers a failure that has been seen (a hand-back that came
  from a real batch counts; the decision records and decisions/ files say where one came from). Every other
  failure goes under ONE general line per script or agent: "If <system> cannot do what it was asked, then
  <system> shall exit non-zero, say why, and change nothing" (wording to fit an agent: "hand back, saying why").
- A check's rules may become a table in Behaviour whose rows carry ids `[r<n>]` and count as lines (e.g.
  design-model-check's reports: code, what is reported).
- Message wording, output formats and minor refusals move to "Implementation, may change".
- Ids: the original ids (in spec/capabilities/<name>.md today) are published. An original id merged into
  another line, or dropped, goes into `retired:` and its scenario (if any) gains the surviving line's tag
  instead — scenarios are never removed (decision 0052). New ids made in round 1 that disappear are simply
  unused (never published). Never reuse an id.
- Map: rewrite the table as `original id | now | note` (now = surviving id, "retired → rN", or "dropped:
  general line rN"), keep "Scenario tags" exact against features/<name>.feature, and trim Questions to those
  still open.
- Aim: built capabilities near or below their original line count, clearer than before.
Reply in at most 5 lines: lines original → round 1 → now, per capability.
~~~~~~

## `.shop/scratch/ears/brief-skeleton.md`

~~~~~~
# Brief: walking skeletons for the capabilities not yet built (i13 with i10, i8)

Same setting as .shop/scratch/ears/brief.md and brief-2.md (read both; change nothing outside
.shop/scratch/ears/, commit nothing). Capabilities: supervision, work-queue, delivery, planning (i10's) and
migration-tools (i8's). None exists yet; their round-1 drafts (.shop/scratch/ears/capabilities/) run to
21-84 lines each. The person: "dangerous to specify so much without proving". Decision 0051 now says a
capability not yet built is a walking skeleton, a handful of lines, grown from what running it shows.

For each, rewrite .shop/scratch/ears/capabilities/<name>.md as a skeleton: the fewest EARS lines (aim 4-10)
for the smallest thing that proves the idea end to end, with one general failure line. Together the i10
skeleton must let one person-approved, formulated work-item on a fixture repository go through research,
plan, implement (bdd-red-green) and review by `claude -p` workers started by `work run`, with only the
supervisor writing status, and end green or awaiting a ruling. The i8 skeleton: `migrate` takes a fresh
clone of a repository on the old system to the final layout (spec/decisions/, .shop/work, .shop/records,
@deprecated) in one run, and `model check` passes on the result. Ids: these were never published; number
from r1. Purpose and Not yet sections short; Not yet names what the skeleton leaves out.

Then write .shop/scratch/ears/skeleton-notes.md: for each capability, the round-1 lines you cut, grouped as
"ideas to test once the skeleton runs" (one line each, plain words), so nothing is lost — these become the
initiative's notes, not requirements. Also list which of i10's and i8's drafted work-items (work/i10-*/,
work/i8-*/ and work/i1-first-spec/spec-integration-*.md on the branch) the skeleton still needs (rewritten
to the skeleton's lines) and which are dropped or deferred.
Reply in at most 6 lines.
~~~~~~
