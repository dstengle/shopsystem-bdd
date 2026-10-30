# Gate: q26, round 9 (spec-integration, redrafted over spec r59)

Drafts: `.shop/scratch/9-integrate/drafts/round-9/spec/`. No decision is drafted (answer: reading B, no decision). The earlier drafts' ids r58-r65 collided with spec r59 (added since), so the lines are renumbered r60-r67, and r60 of the earlier drafts is replaced as the answer Q1 A of 2026-10-30 says.

## spec-integration (adds r60-r67, removes r13; r13 goes to `retired`)

Added:
- [r60] The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines. (line 1; answer: every such session)
- [r61] **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts. (line 3; answer: a general failure line is not a finding)
- [r62] **When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/` other than a capability's general failure line, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions. (answer Q1 A, 2026-10-30; replaces the earlier r60)
- [r63] **When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it. (line 4; answer: replaces the glossary line, lines drafted from now on)
- [r64] **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking. (line 5; r35 unchanged)
- [r65] **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading. (line 6)
- [r66] The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id. (line 7)
- [r67] **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id. (line 7; answer: retire r13)

Removed:
- [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id.

## Glossary (adds; none has a `Not:`)
- `term/catch-all-trigger`: - **catch-all trigger**: a trigger or condition of a line that holds for every event or every condition of its system, such as any failure at all, rather than for one event or condition it names.
- `term/conflicting-responses`: - **conflicting responses**: the responses of two lines with overlapping triggers that cannot both be given, such as two statuses for one node, or a refusal and a write of one file.
- `term/convention`: - **convention**: a rule of how the spec is written that `docs/capability-format.md` or a decision under `spec/decisions/` states.
- `term/general-failure-line`: - **general failure line**: a capability's one line whose trigger is that its system cannot do what it was asked, and whose response is to stop, say why and change nothing.
- `term/implementation-detail`: - **implementation detail**: what a line says of how its system gives a response rather than what the narrator observes: the words of a message, an exit or status code, a field name, a table or a column.
- `term/overlapping-triggers`: - **overlapping triggers**: the triggers or conditions of two lines of one system that can both hold at once, so that both lines respond.

## Decisions
None drafted.

## Findings of the check against `spec/` (r61)
None: r64 gates a different kind than r35's every-question line (r35 unchanged by the answer); r67 contradicts only r13, which is removed; r62 and r61 are the check's own lines and agree.

## Questions
None. Every earlier question is answered (the answers of 2026-10-30 are held: Q1 A in r62, Q2 A with no further line, Q3 A the mapping stands).

## Cut sentences
None.
