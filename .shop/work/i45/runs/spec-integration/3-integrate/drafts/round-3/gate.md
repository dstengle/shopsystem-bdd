# Gate: q26, round 3 (spec-integration, redrafted from the answers)

Drafts: `.shop/scratch/3-integrate/drafts/round-3/spec/`. No decision is drafted (answer: reading B, no decision).

## spec-integration (adds r58–r65, removes r13; r13 goes to `retired`)

Added:
- [r58] The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines. (line 1; answer: every such session)
- [r59] **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts. (line 3; answer: a general failure line is not a finding)
- [r60] **When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions. (answer: finding in result and gate's questions)
- [r61] **When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it. (line 4; answer: replaces the glossary line, lines drafted from now on)
- [r62] **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking. (line 5; r35 unchanged)
- [r63] **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading. (line 6)
- [r64] The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id. (line 7)
- [r65] **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id. (line 7; answer: retire r13)

Removed:
- [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id.

## Glossary (adds; none has a `Not:`)
- `term/implementation-detail`: - **implementation detail**: what a line says of how its system gives a response rather than what the narrator observes: the words of a message, an exit or status code, a field name, a table or a column.
- `term/overlapping-triggers`: - **overlapping triggers**: the triggers or conditions of two lines of one system that can both hold at once, so that both lines respond.
- `term/conflicting-responses`: - **conflicting responses**: the responses of two lines with overlapping triggers that cannot both be given, such as two statuses for one node, or a refusal and a write of one file.
- `term/catch-all-trigger`: - **catch-all trigger**: a trigger or condition of a line that holds for every event or every condition of its system, such as any failure at all, rather than for one event or condition it names.
- `term/convention`: - **convention**: a rule of how the spec is written that `docs/capability-format.md` or a decision under `spec/decisions/` states.
- `term/general-failure-line`: - **general failure line**: a capability's one line whose trigger is that its system cannot do what it was asked, and whose response is to stop, say why and change nothing.

## Decisions
None drafted.

## Questions
1. r59 against r60: r59 leaves a capability's general failure line out of the check, but r60's trigger ("whose trigger catches all of a line of `spec/`") does not. A (recommended): replace r60 by "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/` other than a capability's general failure line, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions." B: r60 as drafted, read as giving only what r59's check finds.
2. r64 and r65 against `docs/capability-format.md`, which still says "A changed line keeps its id" until r64 is delivered. A (recommended): no line; r64's work-item changes the format. B: a Not yet entry: "Rounds follow r65 over `docs/capability-format.md`'s Requirement ids — trigger: r64 delivered."
3. The answers carried labels from an earlier gate (the answer under Q2 reads "Q4, r47's session"); this round matched each by its words. A (recommended): the mapping stands. B: an answer that belongs elsewhere is drafted again.

## Cut sentences
None.
