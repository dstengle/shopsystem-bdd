/home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-9-integrate/.shop/scratch/9-integrate/drafts/round-9/spec/capabilities/spec-integration.md
/home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-9-integrate/.shop/scratch/9-integrate/drafts/round-9/spec/index.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | spec-integration | r60 | The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines. | q26 "request line 1; answer: every such session" |
| added | spec-integration | r61 | **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts. | q26 "line 3; answer: a general failure line is not a finding" |
| added | spec-integration | r62 | **When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/` other than a capability's general failure line, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions. | "answer Q1 A of 2026-10-30, and the 2026-10-28 answer that the finding is given in the result and the gate's questions" |
| added | spec-integration | r63 | **When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it. | q26 "line 4; answer: replaces the glossary line, only lines drafted from now on" |
| added | spec-integration | r64 | **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking. | q26 "line 5; r35 unchanged" |
| added | spec-integration | r65 | **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading. | q26 "line 6" |
| added | spec-integration | r66 | The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id. | q26 "line 7" |
| added | spec-integration | r67 | **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id. | q26 "line 7; answer: retire r13" |
| removed | spec-integration | r13 | **When** a line is changed, `integrating-a-proposal` shall keep its id. | "answer: retire r13" |

| change | term | entry | source |
|---|---|---|---|
| added | term/catch-all-trigger | - **catch-all trigger**: a trigger or condition of a line that holds for every event or every condition of its system, such as any failure at all, rather than for one event or condition it names. | the earlier drafts' index.md (round 3), for q26 line 3 |
| added | term/conflicting-responses | - **conflicting responses**: the responses of two lines with overlapping triggers that cannot both be given, such as two statuses for one node, or a refusal and a write of one file. | the earlier drafts' index.md (round 3), for q26 line 3 |
| added | term/convention | - **convention**: a rule of how the spec is written that `docs/capability-format.md` or a decision under `spec/decisions/` states. | the earlier drafts' index.md (round 3), for q26 line 5 |
| added | term/general-failure-line | - **general failure line**: a capability's one line whose trigger is that its system cannot do what it was asked, and whose response is to stop, say why and change nothing. | the earlier drafts' index.md (round 3); answer "a general failure line is not a finding" |
| added | term/implementation-detail | - **implementation detail**: what a line says of how its system gives a response rather than what the narrator observes: the words of a message, an exit or status code, a field name, a table or a column. | the earlier drafts' index.md (round 3) |
| added | term/overlapping-triggers | - **overlapping triggers**: the triggers or conditions of two lines of one system that can both hold at once, so that both lines respond. | the earlier drafts' index.md (round 3), for q26 line 3 |

Notes on placement: r67 sits where r13 was; r64 follows r35 (the gate lines); r61-r63 and r65 follow r44 (the integrate lines); r60 and r66 precede r33, which stays last. Frontmatter: r13 appended to `retired`. Each of the six entries is in the form `- **<term>**: <one-sentence definition>.` with no `Not:` part, and each term is letters and hyphens only. No decision drafted.

## Questions

None.

## Cut sentences

None.
