# w142 research: delivery r15 (answers appended to the ledger with `work note`)

Tools: `tools tests-of` has no map (`tools map` runs the whole suite, not run); `tools refs workqueue_note` gave 0 (a module name, not a dotted name). Callers and tests found by search (`by search`). Probes run by pytest in `.shop/scratch/w142-1-research/` (nested git repos, `-n 0`).

## 1. Why each scenario is red today

No accepted scenario. `delivery#r15` has no scenario: the work-item says so, there is no `features/delivery.feature`, and the `@r15` tags in `features/` belong to other capabilities (`migration-tools`, `supervision`, `design-model-check`, `work-queue` x2, `requests`) (`by search`). Judged by review, not by a run.

## 2. What the system answers today

Probes (`run`). Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w142-1-research/probe_note.py` (8 tests), each `work --root <repo> note <initiative> <text>`:

- answer on initiative i1: rc 0; ledger gains `- 2026-10-25: answer: w1 ready`; one commit `work note: i1` holding only `.shop/work/i1/ledger.md`.
- text with LF: rc 1, `work: the note has a line break in it; a note is one line`; ledger and log unchanged.
- text with U+2028: same refusal.
- initiative `i9` with no directory: rc 1, `the initiative i9 does not exist (no .shop/work/i9)`; nothing written.
- initiative `../i1`: rc 1, `the initiative ../i1 is not a name`.
- initiative directory with no ledger yet: rc 0; ledger created with the one line; committed.
- empty text: rc 0; ledger gains `- 2026-10-25: ` and is committed (see Defects).
- answer while another file is staged: rc 0; commit holds only the ledger; `other.txt` stays staged.

Read: `scripts/workqueue_note.py:note` (line-break check, initiative check, append, `committed`); `scripts/work:112` and `cmd_note` (argument form). `work answer` (`scripts/workqueue_answer.py:24-53`) writes its answers to a `## Answers` section of the work-item file, not the ledger, and the delivery skill never calls it. So "the person gives an answer" has two readings, both for the plan to choose: (a) every answer, including `work answer`'s, also gets a `work note` line; (b) only answers the delivery skill relays get one.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `skills/delivering-an-initiative/SKILL.md:62` (Fixes, rulings and the ledger) | each ruling is one line appended to `.shop/scratch/run/ledger-<initiative>.md`; no command named | r15: an answer is one line via `work note` into `.shop/work/<initiative>/ledger.md`, committed | none | grep `ledger` |
| `skills/delivering-an-initiative/SKILL.md:63` | when all work-items are green or withdrawn, moves the ledger to `.shop/records/archive/` | not changed by r15; delivery r16 (archiving) is retired, and decision 0066 says the ledger is archived with the initiative: the skill conflicts with both (read; the work-item's "SKILL.md says so" can be read as the retirement's reason or as a defect) | none | grep `records/archive` |
| `skills/delivering-an-initiative/SKILL.md:37-63` (Drafting, Run, When it exits) | never runs `work answer` or `work note` | r15 adds a `work note` step; the skill reads only `spec/`, `features/`, `.shop/work/` | none | read |
| `agents/initiative-round.md:38` | every round appends a line to `.shop/scratch/run/ledger-<initiative>.md` by hand | same old form; spec-integration r40 and decision 0066 say `work note`; not in r15's file set | none | grep `ledger` |
| `spec/decisions/0059-the-session-keeps-the-gate.md:22` | an accepted decision (index.md:66) that names the scratch ledger path | conflicts with decision 0066 (accepted, index.md:73), which moves the ledger to `.shop/work/<initiative>/ledger.md` | none (a record) | grep `ledger-` |
| `skills/delivering-an-initiative/SKILL.md:59-63` ("ruling") vs `spec/capabilities/delivery.md` r15 ("answer") | the skill's word is ruling | the requirement's word is answer; `design-decision/answers-not-rulings` is in the rests_on lists of work-queue and migration-tools (read) | none | read |

## 4. Tests the requirement makes impossible to keep

None, by search. `tools tests-of` has no map. Searches over `tests/`: no test reads `SKILL.md` or `skills/` (`SKILL|skills/|delivering` no match); no test reads the scratch ledger path (`scratch/run|ledger-` no match); no test reads `agents/initiative-round.md`. Read, not run: `tests/scenarios/work_queue_note_steps.py` (the `work note` scenarios of work-queue r19-r21, asserting `.shop/work/i1/ledger.md` and the commit) stays sound; r15 changes no function.

## 5. A step the work-item skips

A plain line appended to the ledger (the skill's form today) skips `work note`'s steps. Each effect only `work note` gives, by probe (`run`) or `read`:

- refusal of a line break (LF, U+2028): probed `run`.
- refusal of an initiative that does not exist, or a name that is a path: probed `run`.
- the date stamp: probed `run` (the line carries today's date).
- a commit of the ledger alone, on the current branch: probed `run`; other staged files stay staged.
- a ledger created when absent: probed `run`.
- refusal when git cannot commit (`rev-parse` first, before any write): `read` (`workqueue.committed`, lines 264-275).
- a failed commit puts the file back as it was: `read` (`workqueue.committed` restore).
- a whole-or-nothing append: `read` (`workqueue.append`).

## 6. Defects

### Empty answer is written to the ledger

Reproduction (probe `test_empty_text_lands`): `python3 scripts/work --root <repo> note i1 ""` returns 0; the ledger gains `- 2026-10-25: ` as a committed line. The spec (work-queue r19-r21) does not say an empty note is refused, so this may be intended; the plan decides.

## 7. The file set

Files the change must touch (r15's skill edit, and the conflicts it exposes):

- `skills/delivering-an-initiative/SKILL.md`: the answer step (`work note <initiative> <line>`, path `.shop/work/<initiative>/ledger.md`) replaces the scratch ledger line at line 62; line 63 (archive) needs a decision (see Part 3). Found by grep `ledger` and read.
- `agents/initiative-round.md`: same scratch ledger path at line 38. Not r15's; a conflict for the plan to decide on.
- `spec/decisions/0059-the-session-keeps-the-gate.md`: the scratch ledger path at line 22; a conflict for the plan, not a code change.

Read-only on the path, not edited by r15:

- `scripts/work` (147 lines; room 153): the `note` subcommand, `cmd_note`.
- `scripts/workqueue_note.py` (21 lines; room 279): `note`.
- `scripts/workqueue.py` (286 lines; room 14): `committed`, `append`, `entry`. Near the limit: any change here must split first.
- `scripts/workqueue_answer.py` (53 lines; room 247): only if reading (a) is chosen, since it writes answers to work-items.
- `skills/delivering-an-initiative/SKILL.md` (72 lines; room 228, by the 300 default: CLAUDE.md gives no limit for markdown).

Room is 300 minus line count (CLAUDE.md limit, code and tests).

Scratch: `.shop/scratch/w142-1-research/` holds `probe_note.py` and its nested repos. `git status --porcelain` is empty; `.shop` is ignored.
