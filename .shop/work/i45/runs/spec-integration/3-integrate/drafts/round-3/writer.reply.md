/tmp/work-run-i45-7xftq6tl/spec-integration-3-integrate/.shop/scratch/3-integrate/drafts/round-3/spec/capabilities/spec-integration.md
/tmp/work-run-i45-7xftq6tl/spec-integration-3-integrate/.shop/scratch/3-integrate/drafts/round-3/spec/index.md

## Change list

| change | capability | id | line | from |
|---|---|---|---|---|
| added | spec-integration | r58 | The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines. | q26 line 1: "The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines."; answer: "every session that writes a request's lines" (the person's running `work request` and an integrate round giving lines into an upstream (r44) included) |
| added | spec-integration | r59 | **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts. | q26 line 3: "**When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts."; answer: "reading A, it is not a finding; r48 is replaced under a new id excluding a capability's general failure line" |
| added | spec-integration | r60 | **When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions. | answer: "reading A, the finding is given in the round's result and in the gate's questions, naming both lines' ids" |
| added | spec-integration | r61 | **When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it. | q26 line 4: "The glossary shall define each event and each condition that a line's trigger names."; answers: "reading A, r49 replaced by: an integrate round that drafts a line whose trigger names an event or condition the glossary does not define drafts a glossary entry for it" and "reading A, only lines drafted from now on" |
| added | spec-integration | r62 | **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking. | q26 line 5: "**When** a gate round finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking."; answer: "reading A, a rule docs/capability-format.md or a decision under spec/decisions/ states; a question r50 settles is not asked, so r35 is unchanged" |
| added | spec-integration | r63 | **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading. | q26 line 6: "**When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading." |
| added | spec-integration | r64 | The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id. | q26 line 7: "The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id." |
| added | spec-integration | r65 | **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id. | q26 line 7 (as above); answer: "reading A, retire r13 and add r52 and r53" |
| removed | spec-integration | r13 | **When** a line is changed, `integrating-a-proposal` shall keep its id. | q26 line 7 (as above); answer: "reading A, retire r13 and add r52 and r53" |

Frontmatter: r13 added to `retired`; `rests_on` unchanged. No decision file (answer: "reading B, no decision; r52 and r53 are the rule").

Change list as ids: spec-integration adds [spec-integration#r58, spec-integration#r59, spec-integration#r60, spec-integration#r61, spec-integration#r62, spec-integration#r63, spec-integration#r64, spec-integration#r65], changes [], removes [spec-integration#r13].

### Glossary

| change | term | entry | from |
|---|---|---|---|
| added | term/implementation-detail | - **implementation detail**: what a line says of how its system gives a response rather than what the narrator observes: the words of a message, an exit or status code, a field name, a table or a column. | q26 line 2: "...a line that names an implementation detail..."; round-1 gate Q3 reading A |
| added | term/overlapping-triggers | - **overlapping triggers**: the triggers or conditions of two lines of one system that can both hold at once, so that both lines respond. | q26 line 3: "...for overlapping triggers..." |
| added | term/conflicting-responses | - **conflicting responses**: the responses of two lines with overlapping triggers that cannot both be given, such as two statuses for one node, or a refusal and a write of one file. | q26 line 3: "...conflicting responses..." |
| added | term/catch-all-trigger | - **catch-all trigger**: a trigger or condition of a line that holds for every event or every condition of its system, such as any failure at all, rather than for one event or condition it names. | q26 line 3: "...and catch-all triggers..." |
| added | term/convention | - **convention**: a rule of how the spec is written that `docs/capability-format.md` or a decision under `spec/decisions/` states. | q26 line 5: "...a convention of the spec settles..."; answer: "a rule docs/capability-format.md or a decision under spec/decisions/ states" |
| added | term/general-failure-line | - **general failure line**: a capability's one line whose trigger is that its system cannot do what it was asked, and whose response is to stop, say why and change nothing. | answer: "it is not a finding; r48 is replaced under a new id excluding a capability's general failure line" |

None of the six was in the existing glossary; each is placed alphabetically. Glossary entry as ids: adds [term/implementation-detail, term/overlapping-triggers, term/conflicting-responses, term/catch-all-trigger, term/convention, term/general-failure-line], changes [], removes [].

## Questions

1. spec-integration r59 against r60: r59 leaves a capability's general failure line out of the check, but r60's trigger ("whose trigger catches all of a line of `spec/`") does not. A (recommended): r60 is retired before approval and replaced by "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/` other than a capability's general failure line, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions." B: r60 as drafted, read as giving only what r59's check finds.
2. spec-integration r64 and r65 against `docs/capability-format.md`: until r64 is delivered, the format still says "A changed line keeps its id", so a round following the format and one following r65 disagree. A (recommended): no line; r64's work-item changes the format. B: a Not yet entry under spec-integration: "Rounds follow r65 over `docs/capability-format.md`'s Requirement ids — trigger: r64 delivered."
3. The brief: the answers under Q1 to Q8 carry other labels from an earlier gate (for example, the answer under Q2 reads "Q4, r47's session"). This round followed the mapping in its input prompt, matching each answer by its own words. A (recommended): the mapping stands. B: if any answer belongs to a question other than the one its words name, the lines it gives are drafted again.

## Cut sentences

None.
