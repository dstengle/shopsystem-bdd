---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-i13-ears-round1-capabilities
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# 0.21.0 EARS restructure (i13), round 1: capability drafts

Round 1 of initiative i13-ears (release 0.21.0, .shop/work/i13-ears/): each of the 17 capability files with its Behaviour lines restructured into EARS patterns under brief.md, splitting lines so that each has one trigger, one shall and one response (438 lines became 732). Superseded: the person found them far too detailed, and round 2 (brief-2.md) compacted the built capabilities while the unbuilt ones became walking skeletons (brief-skeleton.md); the approved result is commit a844763. Ids above each capability's published highest were never published.

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/ears/round1/capabilities/analysis-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: an agent researching or reviewing a project's code
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs]
retired: []
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and a lint check. It is not a test runner for the fast suite and edits no dependency
file; it reports what the tools found and names a tool that is missing rather than skipping it.

## Behaviour
- [r1] **When** `tools` needs an interpreter, `tools` shall use the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script.
- [r36] **When** `tools probe` is run without `--log`, `tools` shall print the interpreter's path and whether it came from `--python`, from the project's virtualenv (`.venv`, `venv` or `$VIRTUAL_ENV` alike), or from neither.
- [r2] **If** `tools probe`, `tools install` or `tools check` is run in a project that is not a Python project, then `tools` shall say in one line that no analysis tools are known for its language and exit 1.
- [r3] **When** `tools probe` is run, `tools` shall print one line per tool, `<name> <version>` for an installed tool and `<name> missing: <what it is for>` for a missing one, then the interpreter.
- [r37] **If** a tool is missing when `tools probe` is run, then `tools` shall exit 1.
- [r4] **When** `tools probe --log` is run, `tools` shall print one line, `Probe: tools -> ...`, giving each tool with its version or `missing`, for a researcher's notes.
- [r5] **When** `tools install` is run, `tools` shall install each missing tool into the interpreter with pip and edit no dependency file.
- [r6] **If** `tools install` is run with an interpreter that is not a virtualenv, then `tools` shall refuse to install into it and say so.
- [r7] **If** a tool is still missing after `tools install`, then `tools` shall print the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, and exit 1.
- [r8] **When** `tools map` is run, `tools` shall run the suite once under coverage with a context per test.
- [r38] **Where** arguments are given after `--`, **when** `tools map` is run, `tools` shall pass them to pytest.
- [r39] **When** `tools map` is run, `tools` shall keep the map in `.shop/scratch/tools/coverage`.
- [r9] **When** `tools tests-of <file>[:<function, Class.method or line range>]` is run, `tools` shall print each test that executed it in the last map, one a line, and how many of the map's tests that is, with the commit the map was made at.
- [r10] **Where** `--by-file` is given, **when** `tools tests-of` is run, `tools` shall print a count for each test file instead of each test.
- [r11] **If** no test in the map executed the target of `tools tests-of`, then `tools` shall exit 1.
- [r40] **If** the file `tools tests-of` is given has no function by the name it is given, then `tools` shall exit 1.
- [r12] **If** `tools tests-of` is run when no map has been made, then `tools` shall refuse and say to make one with `tools map`.
- [r13] **When** `tools untested <file>...` is run, `tools` shall print each function in the files that no test in the last map executed.
- [r14] **When** `tools refs <name>` is run, `tools` shall print every reference to that function, class or name defined in the project as `path:line`, including uses through an import or an alias, then one summary line with the number of references, the number of production files that contain them and, as a separate number, the number of test files that contain them, and where the name is defined.
- [r15] **If** `tools refs` is given a name that nothing in the project is defined as, then `tools` shall exit 1.
- [r16] **When** `tools check` is run, `tools` shall run ruff and vulture over the paths given or the Python files changed since `--base`, each under its own heading.
- [r41] **Where** the project has import contracts, **when** `tools check` is run, `tools` shall run import-linter over the project under its own heading.
- [r42] **If** a tool `tools check` runs reports, then `tools check` shall exit 1.
- [r17] **If** a tool `tools check` would run is missing, then `tools` shall name it as missing under its heading instead of skipping it.
- [r18] **While** the interpreter is not a virtualenv, **if** a tool is missing when `tools install` is run, then `tools` shall install nothing, print for each missing tool the tool, what it is for, what the workflow does without it and that the interpreter is not a virtualenv, and exit 1.
- [r19] **When** `tools install` finds every tool present, `tools` shall say so and exit 0, whether or not the interpreter is a virtualenv.
- [r20] **When** `tools install` installs a tool, `tools` shall print that the tool is installed.
- [r21] **If** the interpreter does not run when `tools probe`, `tools install` or `tools check` is run, then `tools` shall refuse, naming the interpreter and the end of its error.
- [r22] **When** `tools probe --log` is run, `tools` shall name every tool in its line with its version or `missing`.
- [r23] **When** `tools map` is run, `tools` shall replace any earlier map.
- [r43] **When** `tools map` is run, `tools` shall print pytest's last line, where the map is and the commit it was made at, and exit 0 whether or not the tests passed.
- [r24] **If** `tools map` makes no map, then `tools` shall refuse, naming the command it ran and the end of its output.
- [r25] **When** `tools untested` is run, `tools` shall print each function as `<path>:<line> <name>`, then how many functions no test executed and the commit the map was made at, and exit 0 however many there are.
- [r26] **If** `tools untested` is run when no map has been made, then `tools` shall refuse and say to make one with `tools map`.
- [r27] **If** coverage is missing from the interpreter when `tools tests-of` or `tools untested` is run, then `tools` shall refuse, saying to run `tools install`.
- [r28] **If** jedi is missing from the interpreter when `tools refs` is run, then `tools` shall refuse, saying to run `tools install`.
- [r29] **If** the file `tools tests-of` is given does not exist, then `tools` shall refuse, naming it.
- [r30] **When** `tools refs` is run on a name the project defines, `tools` shall count no definition as a reference.
- [r44] **When** `tools refs` is run on a name the project defines, `tools` shall name where it is defined and exit 0 however many references there are.
- [r31] **Where** `--base` is given, **when** `tools check` is run, `tools` shall check the Python files changed since it and not deleted, in place of any paths given.
- [r32] **If** git cannot compare the working tree with `--base`, then `tools check` shall refuse with git's error.
- [r33] **When** `tools check` has no file to check, `tools check` shall say under the ruff and vulture headings that there is nothing to check, and not exit 1 for those two.
- [r34] **Where** the project states no import contracts, **when** `tools check` is run, `tools check` shall not run import-linter.
- [r47] **Where** the project states no import contracts, **when** `tools check` is run, `tools check` shall say so under the import-linter heading.
- [r35] **When** a tool `tools check` runs prints nothing, `tools check` shall say under its heading that it is clean.

## Implementation, may change
- The tools probed are coverage, pytest-cov, jedi, ast-grep, ruff, vulture, import-linter and hypothesis.
- A Python project is one with `pyproject.toml`, `setup.py`, `setup.cfg`, `pytest.ini`, `requirements.txt`,
  `tox.ini` or any `.py` file under the current directory.
- `install` runs `<interpreter> -m pip install <package>` per missing tool.
- `map` runs `pytest -q --cov=. --cov-context=test`, writes the commit it was made at beside the data, and is
  its own command, never part of the fast suite. Code on the path of every call is executed by most of the
  suite, so the map narrows a search only for code off that path; a test that ran and failed counts.
- When the interpreter is not the one running the script, the script re-runs itself under it.
- `refs` uses jedi, so it reads the code as the interpreter would and does not find a name built from a
  string. A test file is under a tests or test directory or named `test_*` or `*_test.*`.
- `check` treats `.importlinter` or a `[tool.importlinter` table in `pyproject.toml` as the project's import
  contracts, and says so under the import-linter heading when there are none; headings are `== <tool> ==`.
- Exit status: 0 success, 1 something is missing, refused or reported, 2 bad usage.

## Not yet
- Only Python projects are known; in any other, agents search by text and say that they did — trigger: a project in another language asks for its analysis tools.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/batch-measurement.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Batch measurement
narrator: a session measuring a closed batch
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/measure-refuses-unknown-shapes, design-decision/an-experiment-is-a-release]
retired: []
---

# Batch measurement

## Purpose
`scripts/measure` writes one facts file for a batch, from Claude Code's session transcripts, the plan and git:
dispatches, their tokens, time, attribution, findings and commits, the slices' Lands lines against the files
touched, tasks, hand-backs and the suite record. It also prints a facts file, or two side by side. It is not a
judgement of the batch and does not change the repository's code, plan or transcripts; it refuses rather than
guesses when its inputs are not what it knows.

## Behaviour
- [r1] **When** `measure batch <archive file>` is run, `measure` shall write one facts file for the batch running from the commit that added the archive file before it to the commit that added its own.
- [r2] **When** `measure batch` is run with no archive file, `measure batch` shall measure the open batch, from the last archive commit to now, reading the living plan.
- [r3] **Where** `--from` or `--to` is given, as a commit or an ISO time, `measure batch` shall use it in place of that end of the batch.
- [r4] **Where** no `--out` is given, `measure batch` shall write the facts to `docs/superpowers/measurements/<archive file's name without .md>.json`.
- [r5] **If** the archive file was not added by any commit, then `measure batch` shall refuse, naming the file.
- [r6] **If** a transcript's shape is not known, then `measure batch` shall refuse, naming the file and what was missing, and write no facts file.
- [r7] **If** the facts file exists and `--replace` is not given, then `measure batch` shall refuse, leaving the file as it was.
- [r8] **If** no dispatch is found inside the batch, then `measure batch` shall refuse, naming the window it searched, and write nothing.
- [r9] **When** a subagent transcript starts inside the batch, `measure batch` shall count it as a dispatch.
- [r42] **When** a subagent transcript starts outside the batch, `measure batch` shall not count it as a dispatch.
- [r10] **When** a request appears in several transcript rows, `measure batch` shall count its usage once in the facts.
- [r43] `measure batch` shall report a request's reasoning tokens in the facts as "of which" its output tokens.
- [r44] `measure batch` shall not add a request's reasoning tokens to its output figure.
- [r11] **When** a session dispatched inside the batch, `measure batch` shall count that session's own requests inside the batch as the controller's.
- [r12] **When** a dispatch's description names a slice or batch work, `measure batch` shall attribute the dispatch to it.
- [r45] **When** a dispatch's description attributes it to nothing, `measure batch` shall attribute the dispatch by the task or slice its prompt names.
- [r46] **When** neither a dispatch's description nor its prompt attributes it, `measure batch` shall count the dispatch as unattributed.
- [r13] `measure batch` shall count a reviewer's findings as it wrote them: its lines beginning Critical or Important, and its stated count of Minor.
- [r14] **When** a commit is made inside the batch, `measure batch` shall give it to the implementer running when it was made.
- [r47] **When** a commit is made inside the batch, `measure batch` shall count the files it touched as production, test or other.
- [r15] `measure batch` shall give each slice in the facts its Lands line, with the numbers of production and test files it says it will land, beside the numbers of production, test and other files its dispatches touched.
- [r48] **When** `measure batch` is run with an archive file, `measure batch` shall read each slice's Lands line from the archive file.
- [r49] **When** `measure batch` measures the open batch, `measure batch` shall read each slice's Lands line from the living plan.
- [r16] `measure batch` shall give in the facts the tasks the batch plan had when it was added and the tasks it had at the batch's end, the plan's hand-back entries and its suite record.
- [r17] `measure batch` shall write no prompt, reply or tool content into the facts.
- [r18] **When** `measure show <file>` is run, `measure` shall print the facts file as tables.
- [r19] **When** `measure compare <a> <b>` is run, `measure` shall print the two facts files side by side.
- [r20] **If** `measure show` is given a file that is not a facts file `measure` wrote, then `measure` shall refuse, naming the file.
- [r21] **If** no archive file is given, no `--plan` is given and the repository holds no `docs/superpowers/plans/*-slices.md`, then `measure batch` shall refuse, saying to name the living plan with `--plan`.
- [r50] **If** no archive file is given, no `--plan` is given and the repository holds several `docs/superpowers/plans/*-slices.md`, then `measure batch` shall refuse, saying to name the living plan with `--plan`.
- [r22] **If** no archive file was added before the batch's end and no `--from` is given, then `measure batch` shall refuse, saying to give the batch's start with `--from`.
- [r23] **If** `--from` or `--to` is neither a commit nor an ISO time, then `measure batch` shall refuse, naming what it was given.
- [r24] **If** `--repo`, default the current directory, is not inside a git repository, then `measure` shall refuse with git's error.
- [r51] **If** a git command `measure batch` runs fails, then `measure` shall refuse with git's error.
- [r25] **When** `measure batch` is run with no archive file, `measure batch` shall name the batch `--name`, default `open`.
- [r52] **Where** no `--out` is given, **when** `measure batch` is run with no archive file, `measure batch` shall write the facts to `docs/superpowers/measurements/<name>.json`.
- [r26] **When** `measure batch` is run with no archive file, `measure batch` shall start the open batch at the last commit that added a file under `--archive-dir`, default `docs/superpowers/plans/archive`.
- [r27] **When** `measure batch` is run with an archive file, `measure batch` shall hold in the facts the archive file's slices and every other slice a dispatch is attributed to.
- [r53] **When** `measure batch` measures the open batch, `measure batch` shall hold in the facts only the slices a dispatch is attributed to.
- [r28] **When** a commit is made while more than one implementer was running, `measure batch` shall count it as ambiguous.
- [r29] **If** no dispatch names a ledger and no `--tasks` is given, then `measure batch` shall leave tasks uncounted.
- [r54] **If** the batch plan is in no commit, then `measure batch` shall leave tasks uncounted.
- [r55] **When** `measure batch` leaves tasks uncounted, `measure batch` shall hold in the facts a note saying why.
- [r56] **When** `measure batch` leaves tasks uncounted, `measure batch` shall write the note on stderr.
- [r30] **When** `measure batch` has written the facts, `measure batch` shall print one line naming the file, the number of dispatches and slices, and the window.
- [r31] `measure batch` shall give each dispatch in the facts the closing status its reply states.
- [r57] **When** a dispatch's reply closes BLOCKED, PARTIAL or NEEDS_CONTEXT, `measure batch` shall count the dispatch as not done.
- [r32] `measure batch` shall record in the facts the plugin and harness versions the transcripts name.
- [r58] `measure batch` shall record in the facts the batch's window as times.
- [r59] **When** an end of the batch's window is a known commit, `measure batch` shall record that commit in the facts.
- [r33] **When** the batch starts at a commit and ends at a commit, `measure batch` shall give in the facts the files and lines changed from its start commit to its end commit.
- [r60] **When** the batch starts at a commit and its end is not a commit, `measure batch` shall give in the facts the files and lines changed from its start commit to HEAD.
- [r34] **When** a dispatch was given more than one prompt, `measure batch` shall count it as resumed.
- [r61] `measure batch` shall give in the facts the share of building time from the first branch review on.
- [r62] `measure batch` shall count building time as the dispatches' own durations summed, not wall-clock time.
- [r63] `measure batch` shall leave a scout's dispatches out of building time and out of the part of it from the first branch review on.
- [r64] `measure batch` shall give in the facts the mean and summed starting context of the dispatches.
- [r35] **When** `measure show` is run, `measure` shall print the repository, batch, window, plugin and harness versions and suite record, then the summary, roles and slices tables, the dispatches not done or not attributed, each hand-back and each note.
- [r36] **When** `measure compare` is run, `measure` shall print each summary figure and the output, new input, cache read and agent minutes per slice (each summary figure divided by the file's slices) of both files, each file headed by its batch and plugin versions, with the ratio of the second to the first.
- [r37] **If** `measure compare` is given a file that is not a facts file `measure` wrote, then `measure` shall refuse, naming the file.
- [r65] **If** `measure show` or `measure compare` is given a file it cannot read as JSON, then `measure` shall refuse, naming the file.
- [r38] **If** `measure` refuses, then `measure` shall say why on stderr and exit 1.

## Implementation, may change
- Sessions are read from `~/.claude/projects` (or `--projects`), in the directory named after each worktree of
  the repository; `--sessions` names directories outright. Subagents are the `subagents/*.jsonl` beside a
  session, with a `.meta.json` carrying `agentType` and description.
- Tokens are output, new input (input and cache writes) and cache read; context is the whole input of one
  request; a dispatch's effort is the setting most of its requests ran at.
- Description attribution recognises 'slice <n>', 'step <k>', 'task <n>', 'batch' and 'slices', and a leading
  'spec'; the prompt is searched for a ledger's task brief. A dispatch's kind follows its role and the words
  fix, re-review and probe.
- With two implementers running at a commit, it goes to the later-started one and is counted as ambiguous.
  A test file is under a tests or test directory or named `test_*` or `*_test.*`; `docs/`, `features/`,
  `spec/`, `.superpowers/` and Markdown are other; the rest is production.
- The batch plan is the one the dispatches' ledger names, or `--tasks`; when it cannot be read, tasks are not
  counted and a note says so on stderr.
- The facts file is JSON with a version number; `show` refuses a file of another version.
- Transcripts are removed by the harness after some weeks and found only on the machine and paths the batch
  ran in, which is why a facts file is never written over without `--replace`.
- Exit status: 0 success, 1 refused, 2 bad usage.

## Not yet
None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/code-research.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/code-research
title: Code research
narrator: the supervisor that started the researcher
group: service
rests_on: [design-decision/scout-on-haiku-at-low-effort, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
formulated_as: features/code-research.feature
retired: [r2]
---

# Code research

## Purpose
Reads the code and runs the system for one drafted work-item, so that its planner does not have to: why each
accepted scenario is red today, what the system answers today, the tests the change would break, and the file set
that becomes the work-item's claim. It is `code-scout`, started by `work run` on a `drafted` work-item. It builds
nothing and changes nothing in the checkout.

## Behaviour
- [r1] **When** research ends, the researcher shall have its notes in the notes file the brief names.
- [r13] **When** research ends, the researcher shall have given the file set in the result file the brief names.
- [r14] **When** research ends, the researcher shall have left the checkout unchanged.
- [r3] **When** a requirement the work-item accepts changes one that existing code relies on, the researcher shall list in the notes every place that still makes the old assumption, with the tests that execute it.
- [r15] **When** a requirement the work-item accepts replaces one that existing code relies on, the researcher shall list in the notes every place that still makes the old assumption, with the tests that execute it.
- [r4] **When** a work-item is researched, the researcher shall say in the notes why each scenario it accepts is red today from a run of it.
- [r16] **When** a work-item is researched, the researcher shall give in the notes each probe of today's behaviour with its command and what came back, marked `run`.
- [r17] **When** a work-item is researched, the researcher shall mark `read` in the notes what was concluded from reading.
- [r5] **When** a work-item is researched, the researcher shall list in the notes the existing tests its accepted requirements make impossible to keep, starting from the tests that execute the code those requirements change.
- [r6] **When** a work-item adds a path that skips a stage, the researcher shall list in the notes every refusal and effect only that stage produces.
- [r7] The researcher shall say of each count in the notes whether it came from `refs`, `tests-of` or a text search.
- [r8] **When** a probe finds a defect in today's behaviour, the researcher shall report it in the notes with its reproduction.
- [r9] The researcher shall run probes in a scratch directory.
- [r18] The researcher shall not run a probe on the checkout's data.
- [r10] The researcher shall name in the result's file set every production and test file the work-item must change for its scenarios to pass and for everything that passes today to keep passing, each one a search or a read showed.
- [r11] The researcher shall give in the notes each module on the change's path with its line count and its room under the size limit `CLAUDE.md` states.
- [r12] The researcher shall give the result a status that is `DONE` or `NEEDS_CONTEXT`.
- [r19] The researcher shall keep the result's summary under fifteen lines.

## Implementation, may change
- Haiku at low effort; the notes are `notes.md` in the stage's run directory; probe files under `.shop/scratch/<run>/`.
- `tools refs`, `tests-of` and `untested` first, a text search for what is not a name.

## Not yet
- None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/delivery.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/delivery
title: Delivery
narrator: the person delivering an initiative
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/review-of-work-items]
formulated_as: features/delivery.feature
retired: []
---

# Delivery

## Purpose
Turns an initiative's formulated capability-proposals into drafted work-items and has `work run` deliver them,
with the person asked only what nobody else may decide. It is `delivering-an-initiative`, run by the session the
person talks to. The session drafts from the spec and the feature files, never the code; it starts `work run`
and reads what it ends with, never what its workers write. It does not change a Behaviour line or a scenario: a
question about one goes to integration or formulation.

## Behaviour
- [r1] **When** the person asks to deliver an initiative, `delivering-an-initiative` shall draft work-items for each of its capability-proposals that is `formulated`.
- [r18] **When** the person asks to deliver an initiative, `delivering-an-initiative` shall name each of its capability-proposals it leaves out, with its status.
- [r2] **When** `delivering-an-initiative` drafts work-items, `delivering-an-initiative` shall have each requirement that a formulated proposal adds or changes, and that has a scenario, accepted by exactly one of them.
- [r19] **When** `delivering-an-initiative` drafts work-items, `delivering-an-initiative` shall have every requirement one scenario names accepted by the same work-item.
- [r3] **When** a proposal changes or removes a requirement whose old scenario is deprecated, `delivering-an-initiative` shall list that scenario under Retires in one drafted work-item: the one that accepts its replacement, or the one that removes what it tests.
- [r4] **When** `delivering-an-initiative` drafts a work-item, `delivering-an-initiative` shall have the work-item accept requirements of one capability or have a check.
- [r20] **When** `delivering-an-initiative` drafts a work-item, `delivering-an-initiative` shall give the work-item one observable sentence.
- [r21] **When** `delivering-an-initiative` drafts a work-item, `delivering-an-initiative` shall give the work-item one unknown or none.
- [r5] **When** `delivering-an-initiative` drafts a work-item, `delivering-an-initiative` shall give the work-item the risk `contract`, `concurrency`, `data` or `none`.
- [r22] `delivering-an-initiative` shall give the risk `contract`, `concurrency` or `data` only to a work-item that is to be reviewed alone.
- [r6] **If** a drafted work-item's scenarios can pass without another work-item's work, then `delivering-an-initiative` shall not make it `blocked_by` that work-item.
- [r7] **Where** a capability is guarantees, `delivering-an-initiative` shall give its work-items a check against the requirement's bound in place of scenarios.
- [r8] `delivering-an-initiative` shall draft from `spec/`, `features/` and `.shop/work/` alone.
- [r23] `delivering-an-initiative` shall read no code.
- [r9] **If** drafting finds a requirement that admits two readings, then `delivering-an-initiative` shall draft no work-item for it.
- [r24] **If** drafting finds a requirement that admits two readings, then `delivering-an-initiative` shall show the person the question with its readings, to be answered through `integrating-a-proposal`.
- [r10] **When** the work-items are drafted, `delivering-an-initiative` shall commit them alone.
- [r25] **When** the work-items are drafted, `delivering-an-initiative` shall show the person one table of them (name, accepts, blocked by, risk).
- [r26] **When** the work-items are drafted, `delivering-an-initiative` shall start `work run` without waiting for approval.
- [r11] **If** the working tree has changes, then `delivering-an-initiative` shall stop before drafting, saying so.
- [r27] **If** the branch is the repository's default branch, then `delivering-an-initiative` shall stop before drafting, saying so.
- [r12] **While** `work run` runs, `delivering-an-initiative` shall read nothing its workers write.
- [r28] **While** `work run` runs, `delivering-an-initiative` shall wait for it to exit.
- [r13] **When** `work run` exits with questions, `delivering-an-initiative` shall show the person each question with its readings, as `work run` printed them.
- [r29] **When** `work run` exits with questions, `delivering-an-initiative` shall ask the person nothing else.
- [r14] **When** the person answers, `delivering-an-initiative` shall record each answer with `work rule` in the person's words.
- [r30] **When** the person's answers are recorded, `delivering-an-initiative` shall start `work run` again.
- [r15] **When** `work run` exits with every work-item green or withdrawn, `delivering-an-initiative` shall tell the person, naming the initiative's capability-proposals.
- [r31] **When** `work run` exits with every work-item green or withdrawn, `delivering-an-initiative` shall say that closing the initiative is the owner's.
- [r16] **When** `work run` exits on a budget, `delivering-an-initiative` shall tell the person what was spent.
- [r32] **When** `work run` exits on a budget, `delivering-an-initiative` shall ask the person whether to raise the budget.
- [r33] **While** the person has not answered whether to raise the budget, `delivering-an-initiative` shall change nothing.
- [r17] **When** a question says a scenario the implementer was given is wrong, `delivering-an-initiative` shall show it as a formulation question.
- [r34] **When** the person answers a formulation question, `delivering-an-initiative` shall take the answer through `formulating-features` or `integrating-a-proposal` before recording it with `work rule`.

## Implementation, may change
- `skills/delivering-an-initiative/SKILL.md`. Drafting uses `work add`; the session runs `work run` as a
  background command and is woken when it exits; it reads `work run`'s last lines and `work questions`.
- Thin, by one unknown: a work-item with an unknown is usually one scenario; scenarios with none that share step
  definitions go together. A refactor a review asks for is an enabling work-item `for:` the one it unblocks.

## Not yet
- Drafting work-items for a cross-context-request's upstream proposal — trigger: a request between two bounded contexts on design model v3 is accepted.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/design-model-check.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or agent checking a repository against the design model
group: service
rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/a-scenario-may-name-several-requirements, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items]
retired: [r42, r45]
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records, in the
final layout and no other — as the facts of `docs/design-model/grammar.md`, and reports what the grammar
refuses, each rule by its code and its plain label. It also writes the generated decisions index, lists the
rules, and traces a requirement to why it exists. It does not edit the spec, the work or the records, and it
checks one bounded context: product-level artifacts are read only where the files contain them.

## Behaviour
- [r1] **When** `model check` finds no violation, unresolved reference or file problem, `model check` shall say so with the counts and exit 0.
- [r2] **If** `model check` finds violations, then `model check` shall print each violated relation by its grammar.md name and its plain label, with its rows, and exit 1.
- [r3] **If** a requirement bullet in a capability's Behaviour has no `[r<n>]`, then `model check` shall report it under v15a, a requirement has no id.
- [r4] **If** two requirements of one capability have the same id, then `model check` shall report them under v15b, two requirements share an id.
- [r5] **If** a capability uses an id it lists as retired, then `model check` shall report it under v15c, a retired id is used again.
- [r6] **If** a capability-proposal that is `drafted` or `approved` changes a requirement no capability has, then `model check` shall report it under v15e, a proposal changes a requirement no capability has.
- [r7] **If** a `formulated` capability-proposal adds or changes a requirement that has no scenario, of a capability that is not guarantees, then `model check` shall report it under v15f, a formulated proposal leaves a requirement without a scenario.
- [r8] **If** a requirement of a capability that is not guarantees has no scenario naming it, then `model check` shall report it under v_s3, a requirement has no scenario.
- [r9] **If** a scenario names a requirement its capability does not have, then `model check` shall report the unresolved reference and exit 1.
- [r68] **If** a capability rests on a decision that does not exist, then `model check` shall report the unresolved reference and exit 1.
- [r10] **If** a part's `part_of` chain does not reach an initiative, then `model check` shall report it under v9c, a part reaches no initiative.
- [r69] **If** a part has no `part_of`, then `model check` shall report it under v9a, a part has no part_of.
- [r11] **When** `model check` finds warnings, `model check` shall print each warning relation with its plain label and its count, leaving its exit status as its other findings set it.
- [r12] **If** the clingo package is missing, then `model check` shall say so with the command that installs it and exit 2.
- [r13] **When** `model facts` is run, `model facts` shall print the facts read, one a line in clingo's syntax.
- [r71] `model facts` shall run with only the standard library.
- [r14] **When** `model decisions` is run, `model decisions` shall write `spec/decisions/index.md` listing every decision in `spec/decisions/` with its summary, status, what it supersedes and when to revisit it, each linked to its file.
- [r15] **If** `model decisions --check` finds that `spec/decisions/index.md` is not what `model decisions` would write, then `model decisions` shall say so and exit 1, writing nothing.
- [r16] **When** `model why <capability>#r<n>` is run, `model why` shall print the requirement, each capability-proposal that adds or changes it, the `part_of` chain to its initiative and the initiative's sources.
- [r17] **If** no capability-proposal adds or changes the requirement, then `model why` shall say so and exit 1.
- [r18] `model` shall read `<capability>#r<a>-r<b>` in a proposal's or work-item's list as every id from a to b.
- [r19] `model` shall read, under `--root` (default the current directory), only `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, every `spec/decisions/*.md` but `index.md`, `.shop/work/<initiative>/*.md`, `.shop/records/observations.md` and any other Markdown under `.shop/records/` whose frontmatter has an `id`.
- [r20] `model` shall read each `@r<n>` tag of a scenario in `features/<capability name>.feature`, its own or its feature's, as a requirement of that capability the scenario names.
- [r21] `model` shall read a reference written `<name>#r<n>` or `capability/<name>#r<n>` as a requirement of the capability `capability/<context path>/<name>` in the bounded context, the field fixing the kind where it is written `<name>`.
- [r22] **If** a list names a reference that is not `<capability>#r<n>`, with the capability written `capability/<context path>/<name>`, `capability/<name>` or `<name>`, then `model check` shall report it as unresolved.
- [r73] **If** a list names a range `#r<a>-r<b>` with a greater than b, then `model check` shall report it as unresolved.
- [r23] **If** a capability-proposal adds or removes an id its capability neither has nor lists as retired, then `model check` shall report it as unresolved.
- [r74] **If** a capability-proposal that is not `merged`, `formulated` or `withdrawn` adds an id its capability lists as retired, then `model check` shall report it under v15c and not as unresolved.
- [r75] **If** a capability-proposal that is not `merged`, `formulated` or `withdrawn` removes an id its capability lists as retired, then `model check` shall report it as unresolved.
- [r76] **While** a capability-proposal is `merged`, `formulated` or `withdrawn`, `model check` shall report nothing for an id its capability lists as retired that its `adds`, `changes` or `removes` names.
- [r77] **While** a capability-proposal is `merged`, `formulated` or `withdrawn`, `model` shall read an id its capability lists as retired that its `removes` names as that requirement.
- [r24] **If** a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by`, `depends_on`, `fixes` or `findings` names nothing in the repository, then `model check` shall report it as unresolved.
- [r78] **If** one of those fields names a node of the wrong kind, `supersedes` needing a design-decision, `under` and `depends_on` a capability, `for`, `blocked_by` and `fixes` a work-item, and `findings` a review-finding, then `model check` shall report it as unresolved.
- [r25] **If** `spec/index.md` is missing, then `model check` shall report a file problem naming the file.
- [r79] **If** `spec/index.md` has no `id`, then `model check` shall report a file problem naming the file.
- [r80] **If** a capability's `id` is not `capability/<context path>/<file name>`, then `model check` shall report a file problem naming the file.
- [r81] **If** a capability has no `## Behaviour` section, then `model check` shall report a file problem naming the file.
- [r82] **If** a capability's `retired` lists an entry that is neither `r<n>` nor a number, then `model check` shall report a file problem naming the file.
- [r26] **If** a feature file is not `features/<name>.feature` for a capability `<name>`, then `model check` shall report a file problem naming the file.
- [r83] **If** two scenarios of a feature file that are not tagged `@deprecated` share a title, then `model check` shall report a file problem naming the file.
- [r27] **If** a work directory has no `initiative.md`, then `model check` shall report a file problem naming the directory, not the missing file.
- [r84] **If** an initiative or a part has no `id`, then `model check` shall report a file problem naming the file.
- [r85] **If** a part's kind is not a part kind, then `model check` shall report a file problem naming the file.
- [r86] **If** an initiative's or a part's status is missing or not in its kind's lifecycle, then `model check` shall report a file problem naming the file.
- [r87] **If** an initiative's priority is not a number, then `model check` shall report a file problem naming the file.
- [r88] **If** an initiative's date is not `YYYY-MM-DD`, then `model check` shall report a file problem naming the file.
- [r28] **If** a work-item accepts a requirement no scenario names yet, then `model check` shall report a file problem naming the work-item's file.
- [r29] **If** a decision has no `id`, then `model check` shall report a file problem.
- [r89] **If** a record with an `id` has a kind that is not a record kind, then `model check` shall report a file problem.
- [r90] **If** a frontmatter value is written as a folded or literal block, then `model check` shall report a file problem.
- [r91] **If** one id names nodes of two kinds, then `model check` shall report a file problem.
- [r30] **If** `model check` finds a file problem, then `model check` shall print each and exit 1.
- [r31] **When** `model check` ends without `--json`, `model check` shall print the counts of violations, warnings, unresolved references and file problems.
- [r32] **Where** `--limit <n>` is given, default 10, `model check` shall print at most n rows of each violated relation and how many more there are.
- [r33] **Where** `--json` is given, `model check` shall print the violations, warnings, unresolved references and file problems as one JSON object, with each code printed mapped to its plain label, and exit with the same status.
- [r34] **If** an initiative that is not a capability-change has more than one part directly under it, then `model check` shall report it under v_k5, an initiative has more than one first part.
- [r92] `model check` shall not report under v_k5 a capability-change initiative with several capability-proposals directly under it.
- [r35] **If** a capability-proposal argues more than one capability, then `model check` shall report it under v_k6, a capability-proposal argues more than one capability.
- [r36] **When** `model check` decides whether an initiative may be done, `model check` shall count a `formulated` capability-proposal as closed.
- [r37] **When** `model decisions --check` finds that `spec/decisions/index.md` is what `model decisions` would write, `model decisions` shall say the file is current and exit 0.
- [r38] **When** `model decisions` is run, `model decisions` shall print the file it wrote.
- [r93] **If** a decision file has no `id`, then `model decisions` shall leave it out of the index.
- [r39] **If** `model why` is given an argument that is not a requirement reference, then `model why` shall say why and exit 2.
- [r40] **If** no capability has the requirement `model why` names, then `model why` shall say so in place of the requirement's text.
- [r94] **If** no capability has the requirement `model why` names, then `model why` shall still list the proposals that name it.
- [r41] **When** `model why` is run, `model why` shall list each capability-proposal that adds, changes or removes the requirement, in date order with its status and date.
- [r95] **If** every capability-proposal that names the requirement only removes it, then `model why` shall exit 1.
- [r96] **When** one capability-proposal or more adds or changes the requirement, `model why` shall exit 0.
- [r43] `model` shall read a node written `<kind>/<context path>/<name>`, or in short `<kind>/<name>`, as that node, the context path being `<owner>/<product>/<context name>` and the bounded context `bounded-context/<context path>`.
- [r97] `model` shall read a bare `<name>` in a field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`), or in the capability part of a `#r<n>` reference, as a node of that kind.
- [r98] **If** a `part_of`, `for`, `blocked_by`, `fixes` or `findings` names a bare `<name>`, not `<kind>/<name>`, then `model check` shall report it as unresolved.
- [r44] `model` shall not read a scenario tagged `@deprecated` as an acceptance-scenario, whatever `@r<n>` tags it has.
- [r46] **If** a node's `id` is not `<kind>/<context path>/<name>` with its own kind, then `model check` shall report a file problem naming the file.
- [r99] **If** `spec/index.md`'s `id` is not `bounded-context/<context path>`, then `model check` shall report a file problem naming the file.
- [r47] **If** a reference is written `<context name>/<name>`, `decision/<name>` or `obs/<name>`, then `model check` shall report it as unresolved.
- [r48] `model` shall read each bullet of `spec/index.md`'s `## Glossary` written `- **<term>**: <one-sentence definition>. Not: <word>, <word>.`, the `Not:` part optional, as a term of the bounded context with the id `term/<context path>/<term>`, the term lowercased with spaces as hyphens.
- [r49] **If** a bullet in `spec/index.md`'s `## Glossary` is not of the form r48 gives, then `model check` shall report a file problem naming the file.
- [r50] **When** `model facts` is run, `model facts` shall print for each glossary entry a `node` fact of kind `term`, a `term_of` fact naming the bounded context, and an `avoid` fact for each word after its `Not:`.
- [r51] **When** `model facts` is run, `model facts` shall print a `mentions` fact for each requirement and each scenario and each term or avoided word it contains, matching a whole word, whatever its case, with a plural "s" allowed, outside code spans, double-quoted strings and `@` tags, so that "restore" is no mention of "store" and a line naming the tag `@holding` is no mention of "holding".
- [r52] **If** a requirement or a scenario mentions a word that its context's glossary lists after `Not:`, then `model check` shall report it under v_t1, a word the glossary avoids, naming the requirement or scenario, the word and the term.
- [r53] **If** two glossary entries have one term, then `model check` shall report it under v_t2, a term has two entries.
- [r54] **If** a word one term lists after `Not:` is another term of the context, or the term itself, then `model check` shall report it under v_t3, an avoided word is a term.
- [r55] **If** `import clingo` fails, then `model check` shall run again under the first interpreter that has clingo, looking in this order: `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`, `/usr/local/bin/python3`, `/usr/bin/python3`.
- [r56] **If** `import clingo` fails in a `model check` that has already run again under another interpreter, then `model check` shall not run again.
- [r57] **If** no interpreter has clingo, then `model check` shall exit 2 with its message naming each interpreter it tried.
- [r58] **When** `model check` decides whether an initiative may be done, `model check` shall count a `withdrawn` part as closed.
- [r100] `model check` shall accept `withdrawn` as the status of a capability-proposal or a work-item.
- [r59] **If** an initiative is `abandoned` while a part of it, at any depth, is neither closed nor `withdrawn`, then `model check` shall report the initiative under v_d2, an abandoned initiative has a part open.
- [r60] **If** a capability's frontmatter has `formulated_as`, then `model check` shall report a file problem naming the file.
- [r61] **If** the repository has `spec/decisions.md`, or a `decisions/`, `work/` or `records/` directory at its root, then `model check` shall report a file problem for each, naming the path and `scripts/migrate`.
- [r62] **If** a scenario is tagged `@holding`, then `model check` shall report a file problem naming the file and the scenario's title.
- [r63] **If** a decision file has no `## Decision` section, then `model check` shall report a file problem naming the file.
- [r64] `model` shall read a decision's `source` as a list of ids, each resolved as r24 says for `source` and naming a node of any kind.
- [r101] `model` shall not read a decision's `by`.
- [r65] **When** `model rules` is run, `model rules` shall print each rule's code and plain label, one a line, the violations first and then the warnings, and exit 0.
- [r66] `model` shall read a `term/<term>` that a capability-proposal's `adds`, `changes` or `removes` names as that glossary term.
- [r102] **If** a capability-proposal's `adds`, `changes` or `removes` names a `term/<term>` the glossary does not have, other than a term that a `merged` or `formulated` proposal removes, then `model check` shall report it as unresolved.
- [r67] **If** a reference is written `<capability>#behaviour/r<n>`, then `model check` shall report it as unresolved, as it does any reference that is not a requirement's.
- [r103] **If** a Behaviour line is not in one of EARS's patterns (ubiquitous, event-driven, state-driven, unwanted behaviour, optional feature), or combines their clauses in an order other than Where, While, then When or If, or has an If clause with no then, then `model check` shall report it under v_e1.
- [r104] **If** a Behaviour line has more than one "shall" or more than one sentence, then `model check` shall report it under v_e2.

## Implementation, may change
- `scripts/model.lp` is grammar.md v3 sections 1, 3 and 4 in clingo, with FIX notes where grammar.md does not
  compile as written; facts use grammar.md's relation names.
- Each rule's plain label is a fact `label("<code>", "<label>")` beside the rule in `model.lp`, the one place it
  is written; `check` and `rules` read the labels from the solve. A unit test fails when a relation `model.lp`
  shows has no label or two.
- Output: `<code>  <label>  (<count>)` above a violated relation's rows; `warning <code>  <label>  (<count>)`;
  `rules` prints `<code>  <label>`. `--json` adds `"labels": {code: label}` for the codes it prints.
- Node ids: the bounded-context is spec/index.md's `id`; a requirement without an id is `<capability>#line<k>`;
  a scenario is `<feature path>:<title>`.
- The frontmatter reader is a YAML subset: scalars, `[a, b]` lists and `- x` block lists.
- A decision's `source` gives no `source` fact (grammar.md's `source` is an initiative's); its ids are only
  resolved.
- `model decisions` links each row to `<file name>`, relative to `spec/decisions/index.md`.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is checked together with this one.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/feature-file-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: an agent or session editing feature files
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/held-scenarios, design-decision/plugin-scenarios-run-as-pytest-bdd]
retired: [r8, r9, r30, r31, r32, r33, r34, r43, r44, r45, r47, r48, r49, r50]
---

# Feature file tools

## Purpose
`scripts/features` reads and edits Gherkin feature files without the test runner: it counts and lists
scenarios by tag or title, adds a requirement tag to a scenario, moves a scenario between files and verifies the
move, deprecates and retires scenarios kept while they still pass, checks that every scenario has exactly one
test binding it and rewrites the titles test modules bind. It is not a Gherkin runner and does not run any
test; it edits only the feature files, test modules and directory it is pointed at.

## Behaviour
- [r1] The `features` script shall read every `*.feature` under `--dir` (default `features`), recursively.
- [r60] The `features` script shall never take text inside a docstring as a scenario, keyword or tag.
- [r2] **If** a feature file contains a `Rule:` block, then `features` shall refuse, naming the file.
- [r3] **If** an edit would leave a file that `features` cannot read, then `features` shall refuse the edit and leave every file as it was.
- [r61] **If** the result of an edit contains a `Rule:` block outside a docstring, then `features` shall read that file as invalid.
- [r62] **When** `features` checks the result of an edit, `features` shall check it for nothing but a `Rule:` block outside a docstring.
- [r4] **When** `features count --by-tag` is run, `features` shall print the number of scenarios with each tag and a total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags.
- [r63] **When** `features count --by-tag` is run, `features` shall count every scenario in the total, those with no tag included.
- [r5] **When** `features list --tag <tag>` is run, `features` shall print the file and title of each scenario whose tags, its feature's and its Examples' included, include that tag.
- [r6] **When** `features list --title <text>` is run, `features` shall print the file and title of each scenario whose title contains the text.
- [r7] **If** `features list` matches no scenario, then `features` shall print nothing and exit 1.
- [r10] **If** `features tag` is given a title no file has, then `features` shall refuse and change no file.
- [r64] **If** `features tag` is given a title several files have, then `features` shall refuse, naming every file that has it, and change no file.
- [r11] **If** `features tag` is given a tag not written `r<n>`, then `features` shall exit 2 as bad usage and change no file.
- [r12] **When** `features move <title> --to <file>` is run, `features` shall move the scenario's block unchanged from its file to the end of the destination file.
- [r13] **Where** `--inline-background` is given, **when** `features move` is run, `features` shall put the source Background's steps before the moved scenario's first step.
- [r14] **Where** `--keep-feature-tags` is given, **when** `features move` is run, `features` shall put the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the moved scenario's `Scenario:` line, after any tag line the scenario already has, joined to none.
- [r15] **If** the destination of `features move` does not exist, then `features` shall refuse and change no file.
- [r16] **When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` shall print how many scenarios match and exit 0.
- [r17] **If** a scenario's effective tags, description or steps differ between the two trees, then `features verify-moved` shall name the scenario and which of them changed, and exit 1.
- [r18] **If** a title is used by more than one scenario in either tree, then `features verify-moved` shall name the title as a duplicate and exit 1.
- [r19] **When** `features deprecate <title>` is run with `--for <new title>` or `--for-removal`, `features` shall give the scenario the tag `@deprecated` and " (deprecated)" at the end of its title, and change nothing else in it but its `Deprecated for:` description line.
- [r65] **Where** `--for <new title>` is given, **when** `features deprecate` is run, `features` shall give the scenario a description line `Deprecated for: <new title>`, whether or not the replacement exists yet.
- [r66] **Where** `--for-removal` is given, **when** `features deprecate` is run, `features` shall give the scenario a description line `Deprecated for: removal`.
- [r20] **If** `features deprecate` is given a scenario already tagged `@deprecated`, then `features` shall refuse it.
- [r21] **When** `features deprecated` is run, `features` shall list each deprecated scenario with what it is deprecated for.
- [r67] **When** `features deprecated` lists a scenario deprecated for a replacement whose title a scenario has, `features` shall give the file and `@r<n>` tag of the scenario with that title.
- [r68] **If** no scenario has the title of a deprecated scenario's replacement, then `features deprecated` shall say that no scenario has the replacement's title.
- [r69] **When** `features deprecated` lists a scenario deprecated for removal, `features` shall say that the scenario is deprecated for removal.
- [r22] **While** no scenario is deprecated, **when** `features deprecated` is run, `features` shall say that none is deprecated.
- [r23] **When** `features retire <title>` is run on a scenario tagged `@deprecated`, `features` shall remove that scenario's block and leave the rest of the file as it was.
- [r24] **If** `features retire` is given a scenario not tagged `@deprecated`, then `features` shall refuse because it is not deprecated, and leave the file as it was.
- [r25] **If** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, then `features` shall report the module, line, title and feature of each, and exit 1.
- [r70] **If** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` whose title is not in the feature it names, then `features` shall report the module, line, title and feature of each, and exit 1.
- [r26] **When** `features bindings` finds that every binding names a scenario, `features` shall say so and exit 0.
- [r27] **If** a test module under `--tests` does not parse when `features bindings` or `features rebind` is run, then `features` shall refuse, naming the module.
- [r28] **When** `features rebind <old> <new>` is run, `features` shall rewrite `<old>` to `<new>` in each binding call that names it and change nothing else in the module.
- [r71] **When** `features rebind <old> <new>` is run, `features` shall print how many bindings it rebound, zero included.
- [r29] **If** `features rebind` is given a new title that is no scenario in a feature file, then `features` shall refuse and change no test module.
- [r35] **If** `features move`, `features deprecate` or `features retire` is given a title no file has, then `features` shall refuse and change no file.
- [r72] **If** `features move`, `features deprecate` or `features retire` is given, without `--file`, a title several files have, then `features` shall refuse, naming every file that has it, and change no file.
- [r36] **If** the destination of `features move` is the scenario's own file, then `features` shall refuse and change no file.
- [r37] **If** a title is in the `--from` tree and not the other, then `features verify-moved` shall name it as missing and exit 1.
- [r73] **If** a title is in the other tree and not the `--from` tree, then `features verify-moved` shall name it as added and exit 1.
- [r38] **When** `features list --tag` is run, `features` shall find the tag whether it is given with its leading `@` or without.
- [r39] **When** `features deprecate` has deprecated a scenario, `features` shall print its file and its new title.
- [r40] **If** `features deprecated` finds a deprecated scenario with no `Deprecated for:` line, then `features` shall say so on that scenario's line.
- [r74] **If** `features deprecated` finds a deprecated scenario whose replacement has no `@r<n>` tag, then `features` shall say so on that scenario's line.
- [r41] **If** `features rebind` is given a new title that several feature files have, then `features` shall refuse and change no test module.
- [r42] **If** a binding call names the old title of `features rebind` in a string written over several lines, then `features` shall refuse, naming the module and line, and change no test module.
- [r46] **If** `features` refuses a command or an edit, then `features` shall say why on stderr and exit 1.
- [r51] **When** `features tag <title> r<n>` is run on a title exactly one file has, `features` shall add `@r<n>` to the scenario's requirement tags and leave its other tags, its other `@r<m>` tags included, and every other line unchanged.
- [r52] **Where** `--file <path>` is given, the `features` script shall look for the scenario's title in that file only, whatever the command.
- [r53] **If** `--file` names a file that does not have the title, then `features` shall refuse, naming the file, and change no file.
- [r54] **If** `--file` names a file that has the title twice, then `features` shall refuse, naming the file, and change no file.
- [r55] **If** `--file` names a file outside `--dir`, then `features` shall refuse and change no file.
- [r56] **Where** `--file <feature path>` is given, **when** `features rebind` is run, `features` shall rewrite only the bindings whose feature argument names that file, the feature argument resolved against `--dir`.
- [r75] **When** `features rebind` is run without `--file`, `features` shall rewrite every binding of the old title.
- [r57] **When** `features bindings` reads a `scenarios(<path>, ...)` call under `--tests` whose path names a feature file, `features` shall take it as binding every scenario of that feature file.
- [r76] **When** `features bindings` reads a `scenarios(<path>, ...)` call under `--tests` whose path names a directory, `features` shall take it as binding every scenario of every feature file under that directory.
- [r58] **Where** `--unbound` is given with feature files named after it, **when** `features bindings` is run, `features` shall also report the file and title of each scenario in those feature files that no `scenario(...)` or `scenarios(...)` call binds.
- [r77] **Where** `--unbound` is given with no feature file named after it, **when** `features bindings` is run, `features` shall also report the file and title of each scenario in every feature file under `--dir` that no `scenario(...)` or `scenarios(...)` call binds.
- [r78] **Where** `--unbound` is given, **if** a scenario is bound by no call, then `features bindings` shall exit 1.
- [r59] **Where** `--unbound` is given, **if** a scenario is bound by more than one call, then `features bindings` shall report its file and title with the module and line of each call, and exit 1.

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next
  scenario's tag lines; `move` drops the block's trailing blank lines.
- `tag` adds the `@r<n>` tag to the scenario's last tag line; `deprecate` adds to the last
  tag line; a new tag line takes the scenario's indentation. Background steps inlined by `move` take the
  scenario's step indentation; kept feature tags take the `Scenario:` line's.
- `verify-moved` compares lines stripped of indentation, blank lines and comments, and also reports titles
  missing from or added to the second tree.
- `move` also refuses a destination that is the scenario's own file.
- `deprecate` writes the description line as `Deprecated for: <title>` or `Deprecated for: removal`, indented
  like the scenario's first following line.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up
  among the module's own top-level assignments. A `scenario` or `scenarios` path names a feature file by its
  base name, as it does today, or a directory by every feature file under it. `rebind` refuses a title written
  over several lines.
- Output lines: `list` prints `<path>: <title>`; `deprecated` prints
  `<path>: <title> | for: <what> | <replacement's path> @r<n>` or `none deprecated`; `bindings` prints
  `<path>:<line>: no scenario titled "<title>" in <feature>`, and with `--unbound`
  `<feature path>: <title> | bound by no test` or `<feature path>: <title> | bound by <module>:<line>, <module>:<line>`.
- Exit status: 0 success, 1 a check failed or an edit was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/formulation.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/formulation
title: Formulation
narrator: the person who approved the lines
group: service
rests_on: [design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/held-scenarios, design-decision/controller-per-spec-round]
retired: []
---

# Formulation

## Purpose
Writes the acceptance-scenarios for approved Behaviour lines, one feature file per capability, from the
narrator's side and without sight of the code. It is `formulating-features`, run in a `initiative-round` that
dispatches `feature-formulator`s. It decides nothing: a line with two readings comes back as a question.

## Behaviour
- [r1] **When** lines are approved, `formulating-features` shall write the scenarios of each added or changed line with one reading in its capability's feature file `features/<name>.feature`: one scenario or one outline, or one scenario per reason for a line every call must keep (r9).
- [r15] `formulating-features` shall commit no scenario that is not deprecated and formulates no line.
- [r2] `formulating-features` shall commit formulated scenarios without showing them to the person for approval.
- [r3] **If** a line admits two readings, then `formulating-features` shall show the person the question with its two readings instead of a scenario for the line.
- [r16] **If** a line admits two readings, then `formulating-features` shall formulate the rest of the capability.
- [r4] **When** a line whose old scenario passes today is changed or removed, `formulating-features` shall keep the old scenario in the suite tagged `@deprecated`, with " (deprecated)" at the end of its title and a `Deprecated for:` line naming what replaces it, until the work-item that turns its replacement green retires it.
- [r5] **When** a line whose old scenario does not pass today is changed or removed, `formulating-features` shall replace or remove the old scenario.
- [r6] **When** `formulating-features` commits feature files, `features bindings` shall report that every binding names a scenario.
- [r17] **When** `formulating-features` commits feature files, `formulating-features` shall commit only the feature files and the test files `features rebind` changed.
- [r7] **When** an existing feature file is changed, `formulating-features` shall keep every scenario not added, changed or removed byte for byte as it was, tags included.
- [r8] `formulating-features` shall begin a feature file with `# formulated from spec/capabilities/<name>.md`, then `Feature: <title>`, then `Narrator: <narrator>`.
- [r9] `formulating-features` shall formulate a line every call must keep as one scenario per reason the line gives, each with one representative call.
- [r10] **When** the person rules a scenario that a work-item's implementer handed back with evidence a formulation question, `formulating-features` shall rewrite the scenario to fit its line and the evidence, or show the person a question with two readings.
- [r11] `formulating-features` shall tag each scenario, on its tag line, `@r<n>` for each line it formulates, the lines all of one capability, whatever the scenario's title.
- [r12] **When** `formulating-features` tags a scenario `@deprecated`, `formulating-features` shall keep the `@r<n>` tags the scenario had.
- [r18] `formulating-features` shall count no scenario tagged `@deprecated` as formulating a line.
- [r13] **Where** `model check` can run, **when** feature files are committed, `model check` shall report no scenario that names no line or names lines of two capabilities.
- [r19] **Where** `model check` can run, **when** feature files are committed, `model check` shall report no added or changed line without a scenario.
- [r20] **Where** `model check` cannot run, the `initiative-round` that formulates shall say so.
- [r21] **Where** `model check` cannot run, the `initiative-round` that formulates shall check coverage by hand.
- [r14] **When** a scenario uses a word its context's glossary avoids, `formulating-features` shall reword the scenario to its line through the small-change path, without a further gate.

## Implementation, may change
- The workflow scenarios of this capability run as fixture sessions (design-decision/fixture-scenarios-under-pytest-bdd).
- The session dispatches `initiative-round` with the job `formulate`; the round dispatches one `feature-formulator`
  a capability with the brief in the skill, checks coverage one to one, runs each old scenario alone before
  replacing it, uses `features deprecate`, `features rebind` and `features bindings`, splices and commits.
- A scenario's title usually restates its lines' condition, though the `@r<n>` tags are what name the lines; Then lines name a refusal's reason, never message text.

## Not yet
None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/migration-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
title: Migration tools
narrator: a person or session migrating a repository to the final layout
group: service
rests_on: [design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/references-are-ids, design-decision/capability-ids-are-context-scoped, design-decision/plugin-takes-the-dependencies-it-needs]
retired: []
---

# Migration tools

## Purpose
`scripts/migrate` makes every mechanical change that takes a repository from the old system to the final
layout (design-decision/final-layout): requirement and node ids, the moves of the old directories with ids
for the records among them, the decision ledger split into decision files, `@holding` renamed to
`@deprecated`, and a living slice plan turned into work-items and observations. It is the only code in the
plugin that knows the old layout. It decides nothing that needs judgment: it refuses, naming what it cannot
place, and leaves the mapping of scenarios to lines, the context path and the gate to the session.

## Behaviour
- [r1] `migrate` shall read and change files only under `--root`, default the current directory.
- [r2] **When** `migrate status` is run, `migrate` shall print each thing of the old system the repository has, one a line: `spec/decisions.md`; a `decisions/`, `work/` or `records/` directory at the root; each file under `docs/superpowers/`; a living plan `*-slices.md`; each scenario tagged `@holding`; each capability with `formulated_as`, with an `id` not `capability/<context path>/<file name>`, or without `retired`; each capability with a Behaviour line that has no `[r<n>]`; and `spec/index.md` with no `id`.
- [r46] **When** `migrate status` finds any thing of the old system, `migrate` shall exit 1.
- [r3] **When** `migrate status` finds no thing of the old system, `migrate` shall say the repository is on the final layout and exit 0.
- [r4] **If** the root of `migrate run` or `migrate plan` is not a git working tree, then `migrate` shall refuse.
- [r5] **If** `migrate run` is given no `--context` and `spec/index.md` has no `id`, then `migrate` shall refuse, saying the context's id is needed, without changing any file.
- [r6] **If** the `--context` given to `migrate run` is not `bounded-context/<owner>/<product>/<context name>`, then `migrate` shall refuse without changing any file.
- [r48] **If** the `--context` given to `migrate run` is not the `id` `spec/index.md` already has, then `migrate` shall refuse without changing any file.
- [r7] **Where** `--dry-run` is given to `migrate run` or `migrate plan`, `migrate` shall print every change it would make without changing any file.
- [r8] **When** `migrate run` or `migrate plan` changes files, `migrate` shall print each change, one a line, under the name of its step, with the number of changes of each step.
- [r9] **If** any change of `migrate run` or `migrate plan` cannot be made, then `migrate` shall refuse before changing any file, naming each change it could not make.
- [r10] **When** `migrate run` is run on a repository on the final layout, `migrate` shall say there is nothing to migrate without changing any file.
- [r11] **When** `migrate run` finds `spec/index.md` with no `id`, `migrate` shall write the context's `id` into its frontmatter.
- [r12] **When** `migrate run` finds a Behaviour bullet with no `[r<n>]`, `migrate` shall give it one, numbered from one above the highest id its capability has used or retired in the order the bullets come, leaving its text unchanged.
- [r13] **When** `migrate run` finds a capability with no `retired`, `migrate` shall give it `retired: []`.
- [r49] **When** `migrate run` is run, `migrate` shall write each capability's `id` as `capability/<context path>/<file name>`.
- [r14] **When** `migrate run` finds a `decision/<name>` reference in frontmatter or a `## decision/<name>` heading, `migrate` shall rewrite it as `design-decision/<name>`.
- [r50] **When** `migrate run` finds an `obs/<x>` reference, `migrate` shall rewrite it as `observation/<x>`.
- [r51] **When** `migrate run` finds a `## obs/<x>` heading, `migrate` shall rewrite it as `## observation/<context path>/<x>`.
- [r52] **When** `migrate run` finds a frontmatter `id` under `spec/decisions/` or `.shop/`, `migrate` shall write it as `<kind>/<context path>/<name>`.
- [r53] **When** `migrate run` rewrites a reference, `migrate` shall change nothing else in it.
- [r15] **When** `migrate run` finds a capability whose `formulated_as` is `features/<its file name>.feature`, `migrate` shall remove its `formulated_as`.
- [r16] **If** `migrate run` finds a capability whose `formulated_as` names any other file, then `migrate` shall refuse, naming the capability and the file.
- [r17] **When** `migrate run` is run, `migrate` shall move with git: `decisions/*.md` to `spec/decisions/`; `work/` to `.shop/work/`; `records/` to `.shop/records/`; `docs/superpowers/specs/` to `.shop/records/archive/design-notes/`; `docs/superpowers/plans/`, with its `archive/`, to `.shop/records/archive/plans/`; `docs/superpowers/requests/` to `.shop/records/archive/requests/`; `docs/superpowers/measurements/` to `.shop/records/measurements/`; `docs/superpowers/reports/` to `.shop/records/archive/reports/`; any other file under `docs/superpowers/` to `.shop/records/archive/` under its path below `docs/superpowers/`; and each other directory a ledger entry's `source` names a file in, such as `adrs/`, to `.shop/records/decision-arguments/`.
- [r18] **If** `migrate run` would move a file onto a file that exists, then `migrate` shall refuse, naming both.
- [r19] **When** `migrate run` finds a Markdown file under `.shop/records/`, other than `observations.md` and `README.md`, with no frontmatter `id`, `migrate` shall give it `id`, `kind`, `about` and `date`: the id `<kind>/<context path>/<its file name without .md>`, lowercased with each run of other characters than letters, digits and hyphens as one hyphen; the kind by its directory (`decision-arguments/` and `archive/design-notes/` decision-argument, `measurements/` measurement, `review-findings/` review-finding, any other under `archive/` initiative-archive); `about` the bounded context; the date its name begins with, or else the date of the commit that added it.
- [r54] **When** `migrate run` gives a record an `id`, `migrate` shall keep any frontmatter the record had.
- [r20] **When** `migrate run` has moved files, `migrate` shall rewrite each moved path, written in full from the root, to its new path in every tracked text file outside `.shop/records/`.
- [r55] **When** `migrate run` rewrites a moved path in a file other than Markdown, `migrate` shall list the file with the line.
- [r21] **When** `migrate run` finds a `.superpowers/` line in `.gitignore`, `migrate` shall make it `.shop/scratch/`.
- [r56] **When** `migrate run` finds neither a `.superpowers/` nor a `.shop/scratch/` line in `.gitignore`, `migrate` shall add `.shop/scratch/` to it.
- [r22] **When** `migrate run` is run, `migrate` shall make each entry of `spec/decisions.md` the file `spec/decisions/<nnnn>-<name>.md`, `nnnn` its position in the ledger written in four digits, or `<name>.md` when the name already begins with those four digits and a hyphen.
- [r57] **When** `migrate run` has written the decision files, `migrate` shall remove `spec/decisions.md`.
- [r23] **When** `migrate run` makes a decision file from a ledger entry, `migrate` shall give it the frontmatter `id` `design-decision/<context path>/<name>`, `summary` the entry's text up to its first blank line or property line with its lines joined by a space, `date`, `status: accepted`, and the entry's `supersedes` and `revisit_when` where it has them.
- [r58] **When** `migrate run` makes a decision file from a ledger entry, `migrate` shall write as its body `# <nnnn>. <name with hyphens as spaces>` and a `## Decision` section of the entry's text.
- [r24] **If** a ledger entry `migrate run` reads has a property line other than `date:`, `revisit_when:`, `supersedes:` or `source:`, then `migrate` shall refuse, naming the entry.
- [r59] **If** a ledger entry `migrate run` reads has no `date:`, then `migrate` shall refuse, naming the entry.
- [r25] **When** `migrate run` writes a decision's `source`, from a ledger entry or a decision file's own `source`, `migrate` shall write each part of it, split at `;`, that begins with the path of a file the run moved, old or new, as that file's record id.
- [r60] **When** `migrate run` writes a decision's `source`, `migrate` shall keep as it is each part of it that is an id of a node kind.
- [r61] **When** `migrate run` writes a decision's `source`, `migrate` shall write in `by`, joined with "; ", the rest of each part that begins with a moved file's path and every other part.
- [r26] **When** `migrate run` has written the decision files, `migrate` shall write `spec/decisions/index.md` as `model decisions` writes it.
- [r27] **When** `migrate run` finds a scenario tagged `@holding`, `migrate` shall tag it `@deprecated`, make " (held)" at the end of its title " (deprecated)" and its `Held for:` line `Deprecated for:`, changing nothing else in it.
- [r28] **When** `migrate run` retitles a scenario, `migrate` shall rewrite to the new title each `scenario(<feature>, "<old title>")` binding call under `--tests`, default `tests`, that names it, changing nothing else in the module.
- [r29] **If** a test module `migrate run` reads under `--tests` does not parse, then `migrate` shall refuse, naming the module.
- [r62] **If** a test module `migrate run` reads under `--tests` names an old title in a string written over several lines, then `migrate` shall refuse, naming the module.
- [r30] **When** `migrate plan` is run with no `--plan`, `migrate` shall read as the living plan the one `*-slices.md` directly in `.shop/records/archive/plans/`.
- [r63] **Where** `--plan` is given to `migrate plan`, `migrate` shall read as the living plan the file it names.
- [r31] **If** `migrate plan` finds no living plan, then `migrate` shall refuse, saying so.
- [r64] **If** `migrate plan` finds several living plans, then `migrate` shall refuse, naming those it found.
- [r32] **If** a slice of the plan `migrate plan` reads is `in progress`, then `migrate` shall refuse, naming it.
- [r33] **When** `migrate plan` finds a slice whose status is not green and that `--drop` does not name, `migrate` shall write it as a `planned` work-item `.shop/work/migrated-plan/slice-<n>.md`, `n` the slice's number with its dots as hyphens, with the id `work-item/<context path>/slice-<n>`, `wkind` capability for a capability slice and enabling for an enabling or stack slice, and as its body the slice's heading, its `Observable:`, `Unknown:`, `Needs:`, `Lands:` and `Status:` lines, and its place in the plan.
- [r34] **When** `migrate plan` writes a capability slice's work-item, `migrate` shall make it `under` the capability of its first `Scenarios:` entry's feature, `part_of` `capability-proposal/<context path>/migrated-<that capability>`, and `accepts` `<capability>#r<n>` for each `@r<n>` tag of the scenario of each `<feature> / <title>` entry's title in `features/<feature>.feature`.
- [r35] **If** a `Scenarios:` entry of the plan `migrate plan` reads names a title no scenario of its feature file has, then `migrate` shall refuse, naming the slice and the entry.
- [r65] **If** a `Scenarios:` entry of the plan `migrate plan` reads names a scenario with no `@r<n>` tag, then `migrate` shall refuse, naming the slice and the entry.
- [r36] **When** `migrate plan` writes an enabling or stack slice's work-item, `migrate` shall make its `check` the slice's `Check:` text, make it `for` the work-item of the first capability slice after it in the plan that becomes a work-item, and make it `part_of` that work-item's capability-proposal.
- [r37] **When** `migrate plan` finds an enabling or stack slice after which no capability slice becomes a work-item, `migrate` shall write that slice as an observation in place of a work-item.
- [r38] **When** `migrate plan` is run, `migrate` shall append to `.shop/records/observations.md` each entry of the plan's Backlog, and each Log entry that begins `QUESTION FOR THE SPEC:`, `REQUEST` or `RE-FORMULATE` with its continuation lines, that `--leave` does not name, as `## observation/<context path>/<date>-backlog-<k>` or `<date>-log-<k>`, `k` counting that section's entries of that date from 1, with `about:` the bounded context, `by:` the plan's backlog or log, `date:`, and the entry's text as it was.
- [r39] **When** `migrate plan` writes any work-item, `migrate` shall also write `.shop/work/migrated-plan/initiative.md`, the initiative `initiative/<context path>/migrated-plan`, kind capability-change, status started, priority 1, dated today, its source the observation `<today>-migrated-plan`.
- [r66] **When** `migrate plan` writes the initiative, `migrate` shall append the observation `<today>-migrated-plan`, naming the plan and how many slices it migrated.
- [r67] **When** `migrate plan` writes a work-item under a capability, `migrate` shall write for that capability `migrated-<capability>.md`, a capability-proposal `part_of` the initiative, `argues` the capability, status formulated, dated today.
- [r40] **If** `migrate plan` finds that `.shop/work/migrated-plan/` exists, then `migrate` shall refuse without changing any file.
- [r41] **When** `migrate plan` finds no slice to migrate, `migrate` shall say so, writing no initiative, proposal or work-item.
- [r68] **When** `migrate plan` finds no slice to migrate, `migrate` shall still write the observations.
- [r42] **When** `migrate plan` writes files, `migrate` shall write them so that `model check` reports no violation, unresolved reference or file problem in them.
- [r43] **Where** `--dry-run` is given to `migrate plan`, `migrate` shall list each slice it would migrate or drop and each entry it would make an observation, by the name `--drop` and `--leave` take.
- [r44] **If** the `--drop` given to `migrate plan` names a slice the plan does not have, then `migrate` shall refuse, naming it.
- [r69] **If** the `--leave` given to `migrate plan` names an entry the plan does not have, then `migrate` shall refuse, naming it.
- [r45] **If** `migrate` refuses, then `migrate` shall say why on stderr and exit 1 without changing any file.
- [r71] **If** `migrate` is used badly, then `migrate` shall exit 2.

## Implementation, may change
- Python 3 with the standard library; moves are `git mv`, the commit date is `git log --diff-filter=A
  --format=%as -- <path>`. It does not commit.
- `run`'s steps, in order: ids, layout, decisions, deprecated. Every change is computed first, then written;
  a refusal in any step writes nothing.
- The ledger is read by `## (design-)?decision/<name>` headings; an entry ends at the next heading. Property
  lines are `<name>: <value>`, one a line.
- `plan` parses the old plan format (`## Slice <n>: <name>`, `- Kind:`, `- Scenarios: <feature> / <title>;
  …`, `- Check:`, `- Status:`, sections `Backlog` and `Log` of `- <date> <text>` entries); it does not use
  `scripts/plan`. `--drop` takes slice numbers, `--leave` observation names, both comma-separated.
- A slice's `Scenarios:` entry is split at `; ` between entries and at the first ` / ` within one.
- The help text (`--help`) is the contract.
- Exit status: 0 done, 1 refused or something left to migrate (`status`), 2 bad usage.

## Not yet
- Product-level repositories (jobs, a context-map) — trigger: shopsystem-knowledge is migrated.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/planning.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/planning
title: Planning
narrator: the supervisor that started the planner
group: service
rests_on: [design-decision/plans-carry-intent-not-code, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
formulated_as: features/planning.feature
retired: []
---

# Planning

## Purpose
Turns one researched work-item into a plan an implementer can follow alone: the decisions the spec leaves open,
the tests those decisions break and what becomes of each, the final file set, what to reuse and how to verify. It
is `bdd-planner`, started by `work run` on a `researched` work-item. It plans from the researcher's notes and
gives intent, never code. A decision a client would observe that nothing settles is a question, not a plan.

## Behaviour
- [r1] **When** planning ends, the planner shall have written the plan to the plan file the brief names.
- [r15] **When** planning ends, the planner shall have given in the result file the final file set, the capabilities the work depends on and the questions.
- [r16] **When** planning ends, the planner shall have left the checkout unchanged.
- [r2] **When** the planner writes the plan, the planner shall say in it, for each scenario the work-item accepts or for its check, why it is red today from the researcher's notes.
- [r17] **When** the plan gives a reason that the researcher's notes mark `read`, the planner shall mark that reason as unverified.
- [r3] **When** the planner writes the plan, the planner shall state in it each decision the capability's Behaviour leaves open, with the requirement or design-decision it rests on.
- [r4] **When** the planner writes the plan, the planner shall list in it, under Tests the decisions break, every test the researcher's notes name and every test in the file set that a decision of the plan changes, each with what becomes of it: rewritten, and to assert what, or a question.
- [r18] **When** the plan's list under Tests the decisions break is empty, the planner shall say there what was checked.
- [r5] **When** the planner writes the plan, the planner shall name in it the step definitions and fixtures to reuse, the commands that verify the work with the number of scenarios each runs, and the deprecated scenarios the work-item retires.
- [r6] **When** the planner writes the plan, the planner shall put in it no code block, file contents, diff or step-definition body.
- [r7] **If** a decision would change what the capability's narrator observes and no requirement or design-decision settles it, then the planner shall give the result `QUESTION`, with the question, its readings and what the plan becomes under each.
- [r8] **If** what becomes of a broken test would change what a client observes, then the planner shall give it as a question, not a rewrite.
- [r9] **When** the planner gives the final file set, the planner shall give the researcher's, with each file the plan's decisions add, each named.
- [r10] **When** the researcher's notes report a defect a probe found that is a wrong answer or lost data on the work-item's path, the planner shall plan its fix in this work-item.
- [r19] **When** the researcher's notes report a defect a probe found that is neither a wrong answer nor lost data on the work-item's path, the planner shall give it in the result as an observation with its reproduction.
- [r11] **When** the researcher's notes list refusals and effects that only a skipped stage produces, the planner shall say in the plan's decisions, for each, what the new path does about it.
- [r12] **Where** the system has a dry run and a real run of an operation the work-item touches, the planner shall name in the plan the randomized test that they agree.
- [r20] **Where** the system has a dry run and a real run of an operation the work-item touches, **when** no randomized test that they agree exists, the planner shall make writing it part of the work-item's plan.
- [r13] **While** planning, the planner shall read the work-item, the researcher's notes, `spec/`, `features/`, `CLAUDE.md` and the files of the file set, and no other code.
- [r14] **When** planning ends, the planner shall have given the result the status `DONE`, `QUESTION` or `NEEDS_CONTEXT`.
- [r21] **When** planning ends, the planner shall have kept the result's summary under fifteen lines.

## Implementation, may change
- `agents/bdd-planner.md`: tools Read, Glob, Grep, Write; Opus. The plan is `plan.md` in the stage's run directory.
- A ruled work-item is not planned again: the ruling is under its `## Rulings`, for the implementer.

## Not yet
- None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/red-green.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/red-green
title: Red-green
narrator: the supervisor that started the implementer
group: service
rests_on: [design-decision/feature-files-read-only-in-red-green, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/work-item-lifecycle-as-run]
formulated_as: features/red-green.feature
retired: []
---

# Red-green

## Purpose
Implements one ready work-item, one scenario at a time, under `bdd-red-green`, by the `bdd-implementer` that
`work run` starts in the work-item's worktree; or continues one, or does one fix work-item. The scenarios are
the contract; the implementer satisfies them and stops when one cannot be satisfied honestly. It never decides what
a scenario should have said, and it never moves a work-item: `work run` reads its result.

## Behaviour
- [r1] **When** the implementer reports a work-item done, the implementer shall have every scenario the work-item accepts passing.
- [r20] **When** the implementer reports a work-item done, the implementer shall have everything that passed in the suite record its brief gives still passing.
- [r2] The implementer shall not commit a change to a `.feature` file, except removing, with `features retire`, a deprecated scenario the work-item lists under Retires.
- [r3] **If** a scenario the work-item accepts passes before any code is written for it, then the implementer shall hand back.
- [r21] **If** the work-item's check passes before any work is done, then the implementer shall hand back.
- [r22] **If** a scenario of a work-item not yet claimed passes, then the implementer shall hand back.
- [r4] **If** a Then line can only pass through code that contradicts it, then the implementer shall hand back.
- [r23] **If** a scenario can only fail on setup, then the implementer shall hand back.
- [r5] **If** an existing test could stay green only by being removed, loosened, skipped or rewritten to assert something else, and the work-item's plan does not list it, then the implementer shall stop `BLOCKED` naming the test.
- [r6] **When** the implementer changes a test's setup without touching what it asserts, the implementer shall name the test in its report.
- [r24] **When** the implementer rewrites a test first committed after the initiative's base, the implementer shall name the test in its report.
- [r7] **When** the implementer hands back, the implementer shall return the result `HAND-BACK` with the stop condition, the evidence verbatim and which scenarios are green and which are red.
- [r25] **When** the implementer hands back, the implementer shall commit the work so far on the work-item's branch.
- [r8] **When** a work-item's scenarios are green, the implementer shall say in its report what someone can now do, what was surprising and the open questions.
- [r26] **When** a work-item's scenarios are green, the implementer shall give the commits in its result.
- [r27] **If** the work needs more than 15 files touched, then the implementer shall name in its report, before any edit, the files this worker will touch.
- [r28] **If** the work needs more than 15 files touched, then the implementer shall touch only the files its report names.
- [r9] **If** the work needs more than 15 files touched, then the implementer shall stop at a green commit with the result `PARTIAL`.
- [r29] **If** the work needs more than 15 files touched, then the implementer shall leave a report from which a new implementer can continue.
- [r10] **When** the scenarios are silent about a case, the implementer shall not have the code choose the case's behaviour.
- [r30] **When** the scenarios are silent about a case, the implementer shall name the case in its report as an open question.
- [r11] **When** the plan contains code, the implementer shall not paste it.
- [r31] **When** the plan contains code, the implementer shall say in its report that it did not paste it.
- [r12] **If** going green needs work that no scenario of the work-item describes and its plan does not name, beyond a trivial helper, then the implementer shall hand back.
- [r13] **If** a previously green scenario breaks and fixing it would change what a step means, then the implementer shall stop `BLOCKED`.
- [r14] **If** the work needs a decision the plan, its rulings and the capability's Behaviour leave open, then the implementer shall stop `BLOCKED` with the specifics.
- [r32] **If** a file would cross the repository's size limit with no rule in `CLAUDE.md` saying where the code goes, then the implementer shall stop `BLOCKED` with the specifics.
- [r15] **If** the brief names no scripts directory, then the implementer shall stop `NEEDS_CONTEXT`.
- [r33] **If** the brief names no result file, then the implementer shall stop `NEEDS_CONTEXT`.
- [r34] **If** `bdd-red-green` is not in the implementer's context, then the implementer shall stop `NEEDS_CONTEXT`.
- [r16] The implementer shall give every result a status that is one of `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `NEEDS_CONTEXT`.
- [r35] The implementer shall keep every result's summary under fifteen lines.
- [r17] **If** the work needs a file outside the work-item's file set, then the implementer shall claim it with `work claim` before editing it.
- [r36] **If** the implementer's claim of a file is refused, then the implementer shall commit what is green.
- [r37] **If** the implementer's claim of a file is refused, then the implementer shall stop `BLOCKED`, naming the file and the work-item whose claim has it.
- [r18] The implementer shall work only in the worktree and on the branch its brief names.
- [r38] The implementer shall not push, merge, rebase or reset.
- [r19] The implementer shall not commit a change to a file under `.shop/work/`.

## Implementation, may change
- The cycle: run one scenario red, write the step definitions it needs, the least code, run the work-item's
  scenarios (`--work-item <name>` where `work_expectations.py` is registered) and the scenario's module, refactor,
  commit; the whole suite once before the last commit, its record in the report.
- The implementer has no Skill tool; `bdd-red-green` is loaded through its `skills` field. Sonnet by default.
- A continuation reads the report first and takes the next part it names; a fix work-item reads its findings and
  fixes those and nothing else.

## Not yet
- None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/review.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review
title: Review
narrator: the supervisor closing a work-item or an initiative
group: service
rests_on: [design-decision/review-of-work-items, design-decision/the-v3-agents, design-decision/worker-results-are-files]
formulated_as: features/review.feature
retired: []
---

# Review

## Purpose
Finds defects in one work-item's commits or in an initiative's whole branch, against the work-item's plan, the
spec and the repository's rules, and triages them. The reviewers are `bdd-task-reviewer` and `bdd-branch-reviewer`,
started by `work run`, and, when the person asks, `architecture-reviewer`. A reviewer changes nothing: what is to be
fixed now becomes a fix work-item, and the rest an observation.

## Behaviour
- [r1] **When** a review ends, the reviewer shall have its findings in the findings file and the result file the brief names.
- [r15] **When** a review ends, the reviewer shall have left the working tree, index, HEAD and branches as they were.
- [r2] **When** a task or branch review ends, the reviewer shall have graded every finding Critical, Important or Minor.
- [r16] **When** a task or branch review ends, the reviewer shall have given in every finding its file and line, what is wrong, why it matters and the fix.
- [r3] **When** a test was removed or weakened in the commits reviewed, the reviewer shall list it.
- [r17] **If** a test removed or weakened in the commits reviewed is one the work-item's plan did not list, then the reviewer shall grade it Important.
- [r4] **When** the implementer reported a setup-only change, the reviewer shall check each such change against the commits.
- [r18] **When** the implementer reported a rewrite of a test this initiative wrote, the reviewer shall check each such rewrite against the commits.
- [r5] **If** the commits reviewed show behaviour that contradicts a Behaviour line or a capability's Purpose, then the reviewer shall grade it Important, whether or not a scenario covers it.
- [r6] **If** the branch reviewer cannot verify a check a work-item states, then the branch reviewer shall fail the review.
- [r19] **If** a task reviewer cannot verify something from the commits, then the task reviewer shall list it separately.
- [r7] **When** a branch review ends, the branch reviewer shall report the suite's wall time.
- [r20] **When** a branch review ends, the branch reviewer shall have checked the code's shape against `CLAUDE.md`.
- [r21] **When** a branch review ends, the branch reviewer shall have checked the code's coupling to the projects it depends on.
- [r8] **When** the re-review of a fix work-item finds something other than data left invalid, the system's own fault on input, or a write that lands where a refusal belongs, the reviewer shall triage it as an observation.
- [r9] **Where** the system reviewed has a dry run and a real run of one operation, the branch reviewer shall run the randomized test that they agree.
- [r10] **If** the commits reviewed change anything under `features/` other than removing a deprecated scenario the work-item lists under Retires, then the reviewer shall grade it Critical.
- [r11] **When** a branch review ends, the branch reviewer shall report each deprecated scenario whose replacement's work-item is green, each scenario removed that was not deprecated, and each binding that names no scenario.
- [r22] The reviewer shall name in each finding the work-item whose commits contain it.
- [r12] The reviewer shall name in each finding its triage, one of fix now, observation or drop.
- [r23] **When** the reviewer finds a wrong answer, a crash where a refusal belongs or lost data, the reviewer shall triage the finding fix now.
- [r24] **When** the reviewer finds something to harden, the reviewer shall triage the finding as an observation, with its reproduction.
- [r25] **When** the reviewer finds polish that is not cheap, the reviewer shall triage the finding drop.
- [r13] The task reviewer shall read the commits of one work-item and its plan.
- [r26] The branch reviewer shall read the initiative branch from its base and every work-item of the initiative.
- [r14] **When** the architecture reviewer finds a refactor to call for, the architecture reviewer shall give it as an observation with a check that would show it done.
- [r27] **When** the architecture reviewer finds a refactor that would unblock a work-item, the architecture reviewer shall name that work-item.

## Implementation, may change
- Opus; a work-item's commits over 8 production or 4 test files are reviewed by area, one reviewer each, in parallel.
- Probes go in the scratch directory the brief names; another revision is checked out as a worktree there.
- `tools check` runs the lint, dead-code and import-contract tools.

## Not yet
- None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/role-boundaries.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries
title: Role boundaries
narrator: the person running the workflow
group: guarantees
rests_on: [design-decision/the-v3-agents, design-decision/spec-writers-blind-to-code]
formulated_as: features/role-boundaries.feature
retired: []
---

# Role boundaries

## Purpose
What the plugin's agent definitions guarantee about each role, whatever a brief asks. Each is checked by reading
the definitions under `agents/`, not by a scenario. Tool lists bound what an agent can do directly: an agent with
Bash can still write files through the shell, which is why `work run` checks the files a worker leaves.

## Behaviour
- [r1] The plugin's agent definitions shall let only `initiative-round` start another agent.
- [r2] The plugin's agent definitions shall give no reviewer, no scout and no planner the Edit tool.
- [r3] The plugin's agent definitions shall give the `capability-writer` and the `feature-formulator` no edit and no shell tool.
- [r4] The plugin's agent definitions shall give the implementer only the skills its definition lists under `skills:`.
- [r7] The plugin's agent definitions shall list `bdd-red-green` among the implementer's `skills:`.
- [r8] The plugin's agent definitions shall give the implementer no Skill tool.
- [r9] The plugin's agent definitions shall keep the listing of every installed skill out of the implementer's context.
- [r5] The plugin's agent definitions shall name each agent's model.
- [r10] The plugin's agent definitions shall name Opus as the model of the spec writers, the planner and the reviewers.
- [r11] The plugin's agent definitions shall name Sonnet as the model of the implementer and `initiative-round`.
- [r12] The plugin's agent definitions shall name Haiku as the model of the scout.
- [r6] The plugin's agent definitions shall give the `bdd-planner` no shell tool.

## Implementation, may change
- Tool lists and `model:` in `agents/*.md`; `skills:` preloads a skill. `tests/scripts/test_agents.py` reads the
  definitions and checks each line.
- What a tool list cannot enforce (no push, one write path) is asked, or `permissions.deny` in the consuming
  repository's settings.

## Not yet
- None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/spec-consistency.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
title: Spec consistency
narrator: the person keeping a spec
group: service
rests_on: [design-decision/glossary-terms-are-standing, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code]
formulated_as: features/spec-consistency.feature
retired: []
---

# Spec consistency

## Purpose
Checks a bounded context's spec against itself: that one word means one thing, that one thing has one word,
that a line has one reading and that a scenario says what its line says. It is `checking-spec-consistency`,
run on demand by the session the person talks to, with a blind `spec-checker` agent for each judgment of
meaning. It reads nothing but `spec/` and `features/`, and it is not run by integration or formulation.

## Behaviour
- [r1] **When** the person asks for a consistency check, `checking-spec-consistency` shall run `model check` before anything else.
- [r12] **When** `model check` has run in a consistency check, `checking-spec-consistency` shall report its `v_t1`, `v_t2` and `v_t3` rows as findings.
- [r2] **When** the check starts, `checking-spec-consistency` shall state how many `spec-checker` dispatches it will make, one for each capability and one for the whole context, before it dispatches any.
- [r3] **When** a `spec-checker` is dispatched, the `spec-checker` shall read only `spec/` and `features/`, never the source.
- [r13] **When** a `spec-checker` is dispatched, the `spec-checker` shall write its findings to a file under the drafts path.
- [r14] **When** a `spec-checker` has written its findings, the `spec-checker` shall reply with a short summary.
- [r4] **Where** the check runs in report mode, **when** the check ends, `checking-spec-consistency` shall write one findings file grouped by term cluster, then lines with two readings, then other drift, each finding naming its ids.
- [r15] **Where** the check runs in report mode, `checking-spec-consistency` shall change nothing but its findings file.
- [r5] **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words.
- [r16] **Where** fix mode is asked for, **when** the person says yes to a proposed glossary entry, `checking-spec-consistency` shall put the entry and the line changes that apply it, ids kept, through one gate pass for the term.
- [r6] **Where** fix mode is asked for, **when** the terms are settled, `checking-spec-consistency` shall have a scenario that uses an avoided word reworded to its line through formulation's small-change path, with no further approval.
- [r7] **Where** fix mode is asked for, **when** a line has two readings, `checking-spec-consistency` shall ask the person one question with its readings.
- [r17] **Where** fix mode is asked for, **when** the person answers a question about a line's readings, `checking-spec-consistency` shall have the answer integrated through the question path of `integrating-a-proposal`.
- [r8] **Where** fix mode is asked for, **when** a finding is drift other than a term or a line with two readings, `checking-spec-consistency` shall ask the person which side is right, one finding at a time.
- [r9] **Where** fix mode is asked for, **when** a step is done, `checking-spec-consistency` shall run `model check` before the next step.
- [r18] **Where** fix mode is asked for, **when** a step is done, `checking-spec-consistency` shall report what `model check` found before the next step.
- [r10] **When** every finding is applied, rejected or recorded as an observation, `checking-spec-consistency` shall end fix mode.
- [r19] **When** every finding is applied, rejected or recorded as an observation, `model check` shall report no `v_t1`, `v_t2` or `v_t3` row.
- [r11] **While** an integration or formulation round runs, the `initiative-round` running it shall not run the consistency check.
- [r20] `checking-spec-consistency` shall run only when the person asks for it.

## Implementation, may change
- The skill is `skills/checking-spec-consistency/SKILL.md`; the agent is `agents/spec-checker.md`
  (tools Read, Glob, Grep, Write; model sonnet).
- One dispatch for each capability judges its lines against its scenarios; one for the context judges every
  Behaviour line and the glossary, with no scenarios.

## Not yet
- The check runs in integration and formulation rounds — trigger: a measured initiative shows drift the on-demand check would have caught.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/spec-integration.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids]
retired: []
---

# Spec integration

## Purpose
Merges an approved brainstorming note, or a question's answer, into the bounded context's one spec,
and stops at the one human gate: the Behaviour lines. It is `integrating-a-proposal`, run by the session
the person talks to, with each round handed to a fresh `initiative-round` that dispatches the
`capability-writer`. It is not formulation and not planning; it writes nothing a client can run.

## Behaviour
- [r1] **When** an approved note is integrated, `integrating-a-proposal` shall show the person every added, changed and removed Behaviour line, each with its id.
- [r23] **When** an approved note is integrated, `integrating-a-proposal` shall show the person every question the note left open, each question with the lines its answers would give.
- [r2] **If** a line drafted from a note quotes no sentence of the note, then `integrating-a-proposal` shall show it to the person as a question, not as a line.
- [r3] **While** the person has not said yes to the lines and answered every question, `integrating-a-proposal` shall not change anything under `spec/`.
- [r4] **When** the person answers a question, `integrating-a-proposal` shall draft the answer as a further round.
- [r24] **When** an answer has been drafted as a further round, `integrating-a-proposal` shall show the changed lines again before anything is written.
- [r5] **If** the person rejects a line, then `integrating-a-proposal` shall not write that line to `spec/`.
- [r6] **When** the person says yes, `integrating-a-proposal` shall apply the approved drafts to `spec/`, with the Behaviour lines exactly as approved.
- [r25] **When** the approved drafts are applied, `integrating-a-proposal` shall commit them alone, with the approval and its date in the commit message.
- [r7] **If** a note would start a second spec in a context that has one, then `integrating-a-proposal` shall integrate it into the existing `spec/` instead.
- [r8] **When** a change adds or changes at most two Behaviour lines in existing capabilities, changes no published contract and leaves nothing unknown, `integrating-a-proposal` shall write the lines itself from `spec/` alone.
- [r26] **When** `integrating-a-proposal` has written a change's lines itself, `integrating-a-proposal` shall stop at the gate before writing them to `spec/`.
- [r9] **Where** the person has delegated decisions to the session's recommendations, **when** the approved drafts are committed, `integrating-a-proposal` shall say in the commit message that the lines were approved under that delegation.
- [r27] **Where** the person has delegated decisions to the session's recommendations, **when** the change is a decision, `integrating-a-proposal` shall say in the decision's `by` that it was approved under that delegation.
- [r10] **When** an integration is started in the session that brainstormed the note, `integrating-a-proposal` shall recommend a new session for the integration before starting it, saying that this session brainstormed the note.
- [r11] **When** integration is applied, `integrating-a-proposal` shall hand the changed capabilities to formulation.
- [r12] **When** a line is added to a capability, `integrating-a-proposal` shall give it the id one above every id the capability has used or retired, wherever the line sits in the section.
- [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id.
- [r14] **When** a line is removed, `integrating-a-proposal` shall add its id to the capability's `retired` list.
- [r28] `integrating-a-proposal` shall not give a retired id to any later line.
- [r15] **When** the approved drafts are committed, `integrating-a-proposal` shall name each id added, changed and removed in the commit message.
- [r16] **Where** `model check` can run, **if** applying the approved drafts makes it report a new problem other than an added line with no scenario yet, a removed line's scenario that now names no line, or a scenario that uses a word the new glossary entry avoids, then `integrating-a-proposal` shall not commit them.
- [r29] **Where** `model check` can run, **when** applied drafts leave an added line with no scenario yet, a removed line's scenario that now names no line, or a scenario that uses a word the new glossary entry avoids, `formulating-features` shall clear it.
- [r17] **Where** a repository keeps `.shop/work/`, **when** a glossary term is changed, `integrating-a-proposal` shall put the change with the capability-proposal that needs it, listing the term in its `adds`, `changes` or `removes`.
- [r18] **When** the approved drafts are committed, `integrating-a-proposal` shall name each term added, changed and removed in the commit message.
- [r19] **Where** a repository has no `.shop/work/`, **when** a glossary change is drafted, `integrating-a-proposal` shall show it to the person like a Behaviour line.
- [r30] **Where** a repository has no `.shop/work/`, **while** the person has not said yes to a drafted glossary change, `integrating-a-proposal` shall not write anything to `spec/`.
- [r20] **When** a change makes a decision, `integrating-a-proposal` shall show it to the person as one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in `spec/decisions/`, with a one-sentence summary and a Decision section.
- [r31] **If** a drafted decision weighed no options, then `integrating-a-proposal` shall give it no Context and no Alternatives section.
- [r21] **When** a drafted decision names what it came from, `integrating-a-proposal` shall list in its `source` the records, initiatives or decisions it came from, by id.
- [r32] **When** a drafted decision came from the person, a date, a delegation or anything outside the repository, `integrating-a-proposal` shall write that in the decision's `by`.
- [r22] **When** the approved drafts are committed with a decision, `integrating-a-proposal` shall commit in the same commit the `spec/decisions/index.md` that `model decisions` writes.

## Implementation, may change
- The session dispatches `initiative-round` with the job `integrate` or `apply`, the note's path, a drafts path
  `.shop/scratch/drafts/<date>-<note>/` and the round number; the round dispatches `capability-writer`,
  which writes only under `<drafts>/round-<n>/` and replies with the change list, questions, cut sentences
  and paths, last of all to a reply file.
- The round checks `git status --porcelain` against the state before dispatch and sends back an agent that
  wrote outside its drafts path; it checks the change list in both directions.
- The writer drafts a decision as a whole file under `<drafts>/round-<n>/spec/decisions/`; applying it copies the
  file and runs `model decisions`.
- The format the writer follows is `docs/capability-format.md`.

## Not yet
- The gate approves requirement ids listed by a capability-proposal (`adds`, `changes`, `removes`) under `.shop/work/` rather than lines shown as text; until then the gate shows each line with its id — trigger: a consuming repository keeps `.shop/work/` and asks for it.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/spec-migration.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout]
retired: []
---

# Spec migration

## Purpose
Moves a repository onto the final layout of design model v3 (design-decision/final-layout) in one pass,
whatever it has of the old system: design notes and approved feature files with no `spec/`, capability files
without ids, a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`, a living
slice plan, `@holding` scenarios. It is `migrating-to-capabilities`: the first integration where there is no
`spec/`, re-pairing the existing scenarios, and `scripts/migrate` for every mechanical change, with one gate.
It changes the meaning of no approved scenario.

## Behaviour
- [r1] **If** the working tree is not clean, then `migrating-to-capabilities` shall stop before any change and say that the working tree is not clean.
- [r24] **If** a work-item is `claimed`, then `migrating-to-capabilities` shall stop before any change and say that a work-item is claimed.
- [r25] **If** the suite does not run cleanly, then `migrating-to-capabilities` shall stop before any change and say that the suite does not run cleanly.
- [r2] **When** migration drafts the spec, `migrating-to-capabilities` shall show the person the capabilities, which old features' scenarios each receives, every line no scenario backs, and every question.
- [r26] **While** the person has not said yes to the drafted spec, `migrating-to-capabilities` shall change nothing under `spec/`.
- [r3] **If** two scenarios with one title would land in one capability, then `migrating-to-capabilities` shall ask the person at the gate to retitle one.
- [r4] **When** migration is done, `migrating-to-capabilities` shall have given each capability one feature file named for it, with the scenarios mapped to it.
- [r27] **When** migration is done, `migrating-to-capabilities` shall have left each scenario's effective tags, title, description and tables, and its Background steps followed by its own steps, as they were, the new `@r<n>` tags aside.
- [r5] **When** migration is done, `migrating-to-capabilities` shall have left the suite's summary, its passing scenarios by title and its count of scenarios per tag equal to those before it, retitles approved at the gate and the new `@r<n>` tags aside.
- [r6] **If** the suite's summary, its passing scenarios by title or its count of scenarios per tag differ from those before migration beyond what r5 sets aside, then `migrating-to-capabilities` shall stop and report the difference without editing a scenario.
- [r7] The `migrating-to-capabilities` skill shall change no step definition's body in a migration.
- [r8] **When** migration is done, `migrating-to-capabilities` shall have headed each note as a proposal integrated into `spec/` on its date.
- [r9] **Where** a repository has capability files whose Behaviour lines have no ids, **when** it is migrated to ids, `migrating-to-capabilities` shall give each line `[r<n>]` in its order from r1, with its text unchanged.
- [r28] **Where** a repository has capability files whose Behaviour lines have no ids, **when** it is migrated to ids, `migrating-to-capabilities` shall give each capability `retired: []`.
- [r29] **Where** a repository has capability files whose Behaviour lines have no ids, **when** it is migrated to ids, `migrating-to-capabilities` shall make each capability's id `capability/<context path>/<name>`.
- [r10] **When** a repository is migrated to ids, `migrating-to-capabilities` shall make its context's id `bounded-context/<context path>`, the context path being the owner's domain, product and context name.
- [r30] **When** a repository whose `spec/index.md` does not name its owner's domain, product and context name is migrated to ids, `migrating-to-capabilities` shall take them for the context path from what the person gives at the gate.
- [r11] **When** a repository is migrated onto `spec/` or to ids, `migrating-to-capabilities` shall give each scenario that is not deprecated the `@r<n>` tag of each line it formulates, and change nothing else in a scenario but the deprecations the gate led to and the renaming of r18.
- [r12] **If** a scenario formulates no line, then `migrating-to-capabilities` shall show it to the person at the gate as a question.
- [r31] **While** the person has not answered the question about a scenario that formulates no line, `migrating-to-capabilities` shall tag nothing.
- [r13] **When** migration onto `spec/` or to ids is done, `migrating-to-capabilities` shall have left the suite's summary, its passing scenarios by title and its count of scenarios per tag equal to those before it, the new `@r<n>` tags, the deprecations the gate led to, and the " (deprecated)" titles of those and of r18's renaming aside.
- [r14] **When** a repository is migrated to ids, `migrating-to-capabilities` shall make its `decision/<name>` references `design-decision/<name>` and change nothing else in a reference.
- [r32] **When** a repository is migrated to ids, `migrating-to-capabilities` shall write every frontmatter `id` under `spec/decisions/` and `.shop/` in full.
- [r33] **When** a repository is migrated to ids, `migrating-to-capabilities` shall make its observation headings `## obs/<x>` into `## observation/<context path>/<x>`.
- [r15] **When** a repository is migrated, `migrating-to-capabilities` shall leave it on the final layout: decisions one file each in `spec/decisions/` with the generated `index.md`, work and records under `.shop/`, nothing of the plugin under `docs/superpowers/` or `.superpowers/`, and `migrate status` saying there is nothing left to migrate.
- [r16] **When** migration stops at the gate, `migrating-to-capabilities` shall show the person, besides r12's questions, each glossary bullet not in the glossary's form, each open slice of the living plan, and each backlog and log entry that would become an observation.
- [r34] **While** the person has not answered at the gate, `migrating-to-capabilities` shall commit nothing after the mechanical move.
- [r17] **When** migration is done, `migrating-to-capabilities` shall have made each open slice the person kept a work-item accepting the requirements its scenarios are tagged with.
- [r35] **When** migration is done, `migrating-to-capabilities` shall have left each slice the person dropped only in the archived plan.
- [r36] **When** migration is done, `migrating-to-capabilities` shall have made each entry the person did not leave out an observation.
- [r37] **When** migration is done, `migrating-to-capabilities` shall have made the plan and its archives records under `.shop/records/archive/plans/`.
- [r18] **When** migration is done, `migrating-to-capabilities` shall have tagged each scenario that was tagged `@holding` `@deprecated`, with " (deprecated)" for " (held)" on its title and `Deprecated for:` for `Held for:`.
- [r38] **When** migration is done, `migrating-to-capabilities` shall have left each scenario that was tagged `@holding` bound by its test.
- [r19] **When** migration is done, `migrating-to-capabilities` shall have made each decision of the ledger a decision file with the entry's text as its summary and Decision.
- [r39] **When** migration is done, `migrating-to-capabilities` shall have made each decision file's `source` name by id the records the files its entry named became.
- [r20] **When** migration is done, `migrating-to-capabilities` shall have left the repository with no violation, unresolved reference, file problem or `v_s3` (a requirement has no scenario) for `model check` to report, but a `v_s3` for a line that had no scenario before.
- [r21] **When** migration is done, `migrating-to-capabilities` shall have put each glossary bullet in the glossary's form, in the words the person gave at the gate.
- [r22] **When** migration is done, `migrating-to-capabilities` shall have made the mechanical move one commit, before the gate, in which no Behaviour line's text and no scenario but its renaming of r18 changes.
- [r40] **When** migration is done, `migrating-to-capabilities` shall have committed the tags, work-items and observations the gate allowed in the commit after the mechanical move.
- [r23] **When** migration is done, `migrating-to-capabilities` shall show the person each file other than Markdown in which the migration rewrote a path it moved, with the line.

## Implementation, may change
- A baseline under `.shop/scratch/migration/`: the summary line, the passing tests (`-q -rA`), a copy of
  `features/`, and `features count --by-tag`.
- `scripts/migrate status`, `run` and `plan` (capability/migration-tools) make the mechanical changes; the
  session asks the context path before `run` when `spec/index.md` lacks it, maps scenarios to lines with
  `feature-formulator`, tags with `features tag`, then runs `plan` with the gate's `--drop` and `--leave`.
- `capability-writer` drafts with the migration brief; `features move` (with `--keep-feature-tags`,
  `--inline-background`) moves scenarios; `features verify-moved` compares them.
- Bindings follow step definitions: `scenarios(...)` per capability where every step has one body, otherwise
  `@scenario(<file>, <title>)` from the old modules.

## Not yet
None.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/supervision.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
title: Supervision
narrator: the person who started work run
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents]
formulated_as: features/supervision.feature
retired: []
---

# Supervision

## Purpose
`work run <initiative>` delivers an initiative's work-items: it pulls each through its stages, starting a fresh
`claude -p` worker for each stage, reads each worker's result file, checks the guards, writes the status, merges
the implementers' work, runs the reviews, and logs every worker and every move for measurement. It is a script and
takes no judgment: what a worker decides comes back in its result, and what nobody may decide goes to the person as
a question. It never changes an initiative's or a capability-proposal's status.

## Behaviour
- [r1] **When** `work run <initiative>` is started, `work run` shall pull the initiative's work-items through their stages until none can move.
- [r36] **When** a work-item of the initiative is `drafted`, `work run` shall pass it to a `code-scout` worker.
- [r37] **When** a work-item of the initiative is `researched`, `work run` shall pass it to a `bdd-planner` worker.
- [r38] **When** a work-item of the initiative is `ready`, `work run` shall pass it to a `bdd-implementer` worker.
- [r39] **When** a work-item of the initiative is `done` with a named risk, `work run` shall pass it to a `bdd-task-reviewer` worker.
- [r40] **When** every work-item of the initiative is `done`, `green` or `withdrawn`, `work run` shall pass the initiative's branch to a `bdd-branch-reviewer` worker.
- [r2] **When** `work run` starts a worker, `work run` shall start it as a new `claude -p` session of its stage's agent, given one brief file that names the work-item, the stage, the files to read, the run directory to write in and the result file.
- [r41] `work run` shall resume no worker.
- [r3] `work run` shall take a worker's outcome only from its result file.
- [r42] **If** a worker ends without a result file, then `work run` shall fail the stage.
- [r43] **If** a worker ends with a result file not in its stage's form, then `work run` shall fail the stage.
- [r4] **If** a stage fails, then `work run` shall start a new worker for it once more.
- [r44] **If** the new worker for a failed stage fails too, then `work run` shall move the work-item to `awaiting-ruling` with the failure as its question.
- [r5] **If** a worker changes a file under `.shop/work/` outside its run directory, then `work run` shall put the file back as it was.
- [r45] **If** a worker changes a file under `.shop/work/` outside its run directory, then `work run` shall fail the stage.
- [r46] **If** a worker changes a file under `.shop/work/` outside its run directory, then `work run` shall log the file.
- [r6] **When** a researcher's result is `DONE` with a file set, `work run` shall write the file set and the notes' path into the work-item.
- [r47] **When** a researcher's result is `DONE` with a file set, `work run` shall move the work-item to `researched`.
- [r48] **If** a researcher's result is `DONE` with an empty file set, then `work run` shall fail the stage.
- [r7] **When** a planner's result is `DONE`, `work run` shall write the plan's path, the final file set and the capabilities the work depends on into the work-item.
- [r49] **When** a planner's result is `DONE`, `work run` shall move the work-item to `planned`.
- [r50] **When** a planner's result is `QUESTION`, `work run` shall move the work-item to `planned` and then to `awaiting-ruling`, with each question and its readings.
- [r8] **When** the queue's guard allows a `planned` work-item to move, `work run` shall move it to `ready`.
- [r51] **When** an implementer's place is free, `work run` shall claim a `ready` work-item as it starts its implementer.
- [r9] **When** `work run` starts an implementer, `work run` shall give it its own git worktree under `.shop/worktrees/<work-item>/`, on a branch made from the initiative branch's head.
- [r52] `work run` shall run no more implementers at once than `delivery.toml` allows, 2 when it says nothing.
- [r10] **When** an implementer's result is `DONE` or `DONE_WITH_CONCERNS`, `work run` shall rebase its branch onto the initiative branch.
- [r53] **When** `work run` has rebased an implementer's branch, `work run` shall run the work-item's accepted scenarios, or its check, and the whole suite in its worktree.
- [r54] **When** the work-item's accepted scenarios, or its check, and the whole suite pass in its worktree, `work run` shall merge its branch fast-forward.
- [r55] **If** anything that passed in the last suite record fails in the worktree, then `work run` shall not merge the branch.
- [r56] **When** `work run` merges an implementer's branch, `work run` shall move the work-item to `done`.
- [r11] **If** the work-item's commits change a file outside its file set, then `work run` shall move the work-item to `awaiting-ruling` naming the files, without merging the commits.
- [r12] **If** the rebase of an implementer's branch conflicts, then `work run` shall move the work-item to `awaiting-ruling` with the conflict, leaving the initiative branch as it was.
- [r57] **If** the work-item's scenarios or the suite fail in its worktree, then `work run` shall move the work-item to `awaiting-ruling` with the failing tests, leaving the initiative branch as it was.
- [r13] **When** an implementer's result is `PARTIAL` for the first, second or third time in a row, `work run` shall start a new implementer on the same worktree and report as a continuation.
- [r58] **If** an implementer's result is `PARTIAL` for the fourth time in a row, then `work run` shall move the work-item to `awaiting-ruling`.
- [r14] **When** an implementer's result is `BLOCKED`, `HAND-BACK` or `NEEDS_CONTEXT`, `work run` shall move the work-item to `awaiting-ruling` with the result's questions and evidence, keeping its worktree and branch.
- [r59] **When** an implementer's result is `BLOCKED`, `HAND-BACK` or `NEEDS_CONTEXT`, `work run` shall release the work-item's claim.
- [r15] **When** an implementer stops because `work claim` refused a path, `work run` shall move its work-item back to `ready`.
- [r60] **While** the work-item whose claim has the refused path is `claimed`, `work run` shall keep the work-item that was refused it at `ready`.
- [r61] **When** `work run` starts the next implementer of a work-item moved back to `ready` for a refused path, `work run` shall have it continue on the same branch.
- [r16] **While** a work-item is `awaiting-ruling`, `work run` shall go on with every work-item that is not blocked by it.
- [r17] **When** no work-item can move and no worker is running, `work run` shall exit, printing the number of work-items in each status, and each open question with its readings and the `work rule` command that answers it.
- [r18] **When** `work run` stops with every work-item `green` or `withdrawn`, `work run` shall exit 0.
- [r63] **When** `work run` stops with a work-item `awaiting-ruling`, `work run` shall exit 3.
- [r64] **If** a budget stops `work run`, then `work run` shall exit 4.
- [r65] **If** `work run` stops for any other reason, then `work run` shall exit 1.
- [r19] `work run` shall run each worker within the time and the spending `delivery.toml` gives its role.
- [r66] **If** a worker reaches the time `delivery.toml` gives its role, then `work run` shall end it.
- [r67] **If** a worker reaches the spending `delivery.toml` gives its role, then `work run` shall end it.
- [r68] **If** `work run` ends a worker at its role's time or spending, then `work run` shall fail the stage.
- [r20] **If** the spending of the workers `work run` has started reaches the run's budget in `delivery.toml`, then `work run` shall start no further worker.
- [r69] **If** the spending of the workers reaches the run's budget, then `work run` shall wait for the running workers.
- [r70] **If** `work run` has waited for its running workers after reaching the run's budget, then `work run` shall exit, saying what was spent.
- [r21] **When** a work-item whose risk is `contract`, `concurrency` or `data` is `done`, `work run` shall start a task review of its commits.
- [r71] **When** a task review of a work-item finds nothing to fix now, `work run` shall move the work-item to `green` once its accepted scenarios pass at the initiative branch's head.
- [r22] **When** a review triages findings as fix now, `work run` shall add for each work-item they name a fix work-item at `planned`, with `fixes:` naming that work-item, `findings:` naming the review-finding, the files the findings name as its file set, and the requirements that work-item accepts.
- [r72] **While** a work-item has a fix work-item that is not `green`, `work run` shall not move the work-item to `green`.
- [r23] **When** a review of a work-item ends, `work run` shall write its findings as a review-finding record under `.shop/records/review-findings/`, about the reviewed work-item's capability.
- [r73] **When** a branch review ends, `work run` shall write its findings as a review-finding record under `.shop/records/review-findings/`, about the bounded context.
- [r24] **When** a review triages a finding as an observation, `work run` shall append it to `.shop/records/observations.md`, about the work-item's capability, with its reproduction and the review-finding it came from.
- [r25] **When** every work-item of the initiative is `done`, `green` or `withdrawn`, none is `awaiting-ruling`, and the initiative branch has commits since its last branch review, `work run` shall start a branch review from the initiative's base.
- [r74] **When** a branch review finds nothing to fix now, `work run` shall move each `done` work-item whose scenarios pass to `green`.
- [r26] **When** a fix work-item is `done`, `work run` shall start a scoped re-review of its commits.
- [r75] **When** a scoped re-review finds data left invalid, the system's own fault on input, or a write that lands where a refusal belongs, `work run` shall add a further fix work-item for the finding.
- [r76] **When** a scoped re-review finds any other finding, `work run` shall make it an observation.
- [r77] **When** a scoped re-review finds nothing that gets a further fix work-item, `work run` shall move the fix work-item to `green`.
- [r27] **When** `work run` starts a worker, `work run` shall append a line to `log.jsonl` with the time, the work-item, the stage, the attempt, the agent, the model and the session id.
- [r78] **When** a worker ends, `work run` shall append a line to `log.jsonl` with the time, the work-item, the stage, the attempt, the agent, the model, the session id, the result's status, the exit, and the duration, cost and token counts the session reported.
- [r28] **When** `work run` has run the whole suite, `work run` shall append a suite record to `log.jsonl` (passed, failed, expected, the commit, the seconds).
- [r79] **When** `work run` writes an implementer's brief, `work run` shall give in it the last suite record.
- [r29] **When** `work run` moves a work-item, `work run` shall commit the work-item's file, its run directory and `log.jsonl` on the initiative branch, and nothing else, with the message `work: <work-item> <before> -> <after>`.
- [r30] **If** another `work run` is running in the repository, then `work run` shall refuse, naming its process id.
- [r31] **If** `work run` is started on the repository's default branch, then `work run` shall refuse before starting any worker, saying so.
- [r80] **If** `work run` is started with changes in the working tree outside `.shop/`, then `work run` shall refuse before starting any worker, saying so.
- [r32] **When** `work run` is interrupted, `work run` shall end its running workers.
- [r81] **When** `work run` is interrupted, `work run` shall log each running worker as interrupted.
- [r82] **When** `work run` is started after an interrupted one, `work run` shall continue each `claimed` work-item from its worktree and report as a continuation.
- [r33] **When** every work-item of the initiative is `green` or `withdrawn` and the last branch review found nothing to fix now, `work run` shall say the initiative's work-items are done, changing no initiative's or capability-proposal's status.
- [r34] **When** `work step <work-item>` is run, `work` shall run that work-item's next stage alone, under the rules of `work run`.
- [r83] **When** the stage `work step` runs ends, `work` shall exit.
- [r35] **When** `work run` starts a worker, `work run` shall print one line naming the work-item, the stage and the agent.
- [r84] **When** a worker ends, `work run` shall print one line with its result's status.
- [r85] `work run` shall print nothing a worker wrote.

## Implementation, may change
- A worker is `claude -p "<the brief's path and the result file>" --agent shopsystem-bdd:<agent> --session-id <uuid>
  --output-format json --max-budget-usd <n> --permission-mode <delivery.toml, default acceptEdits>`, with `--model`
  only where `delivery.toml` overrides the agent definition's. The executable is `$SHOPSYSTEM_WORK_CLAUDE`, else
  `claude`; the plugin's tests set it to a stub that follows a script.
- Run directory `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`: `brief.md`, `result.json`, `session.json`
  (claude's JSON output), and the worker's `notes.md`, `plan.md`, `report.md` or `findings.md`.
- `.shop/delivery.toml`: `[tests] scenarios` (default `python3 -m pytest -q --work-item {item}`) and `suite`
  (default `python3 -m pytest -q`); `[workers] implementers = 2`, `researchers = 3`; `[limits]` minutes and dollars
  per role (scout 10/1, planner 20/3, implementer 45/8, task reviewer 20/3, branch reviewer 45/8) and `run_dollars`
  (default 60); `[worktree] setup`; `[models]` overrides.
- The initiative's base is the merge-base of the initiative branch with the default branch when `work run` first
  starts; it is the first line of `log.jsonl`. `.shop/worktrees/` and `.shop/scratch/` are git-ignored.
- One process, a lock file `.shop/work/.lock` with its pid; workers run as child processes polled for exit.

## Not yet
- Re-planning after a ruling (the planner run again on the ruled work-item) — trigger: a ruled work-item's implementer stops on what the ruling changed.
- Workers in a sandbox the supervisor starts (a container per worker) — trigger: a consuming repository asks to run `work run` with bypassed permissions.
~~~~~~

## `.shop/scratch/ears/round1/capabilities/work-queue.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, agent or script reading or moving work-items
group: service
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs]
formulated_as: features/work-queue.feature
retired: []
---

# Work queue

## Purpose
`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them and
what can move, moves them through their lifecycle checking each transition's guard, takes claims and rulings, and
logs every move. It is the only writer of a work-item's status. It also writes `work_expectations.py`, the pytest
plugin that expects the scenarios of work-items not yet claimed to fail. `work run`, the supervisor, is the
supervision capability; this one is the queue it runs on. It judges nothing and starts no worker.

## Behaviour
- [r1] `work` shall read the work-items of every initiative under `.shop/work/`, each `.shop/work/<initiative>/<name>.md` whose frontmatter `kind` is `work-item`, and the scenarios under `features/`.
- [r25] `work` shall need nothing beyond the standard library.
- [r2] **When** `work add <initiative> <name>` is run with `--part-of`, `--under` and either `--accepts` or `--check`, `work` shall write `.shop/work/<initiative>/<name>.md` with the status `drafted`, the fields given, and the sections Observable, Unknown and Risk from `--observable`, `--unknown` and `--risk`.
- [r26] **When** `work add` writes a work-item, `work` shall print the work-item's id.
- [r3] **If** `work add` names an initiative with no `initiative.md`, then `work` shall refuse, naming it, without writing anything.
- [r27] **If** `work add` names a `--part-of` that is not a capability-proposal of that initiative, then `work` shall refuse, naming it, without writing anything.
- [r28] **If** `work add` names a `--blocked-by` that is no work-item, then `work` shall refuse, naming it, without writing anything.
- [r29] **If** `work add` names a `--risk` other than `contract`, `concurrency`, `data` or `none`, then `work` shall refuse, naming it, without writing anything.
- [r30] **If** `work add` names a requirement in `--accepts` that no scenario names, then `work` shall refuse, naming it, without writing anything.
- [r4] **If** the work-item's file already exists, then `work` shall refuse, leaving the file as it was.
- [r5] **When** `work show` is run, `work` shall print each work-item, one a line, with its status, its capability, what it waits on and the number of paths in its file set, grouped by initiative.
- [r31] **Where** `--status <status>` is given, **when** `work show` is run, `work` shall print only the work-items with that status.
- [r6] **When** `work next` is run, `work` shall print each move that can be made now, as the work-item, its status before and after and the worker that would make it, without changing anything.
- [r7] **When** `work` moves a work-item, `work` shall write the new status into the work-item's file.
- [r32] **When** `work` moves a work-item, `work` shall append one line to `.shop/work/<initiative>/log.jsonl` giving the time, the work-item, the status before and after, who moved it (a worker's session id, `person` or `work`) and why.
- [r8] **If** a work-item's status in its file is not the last status `log.jsonl` gives it, then `work` shall refuse to move it, naming the file and both statuses.
- [r9] **If** a `planned` work-item is `blocked_by` a work-item that is not `green`, then `work` shall not move it to `ready`.
- [r33] **If** a `claimed` work-item's file set has a path in a `planned` work-item's file set, then `work` shall not move the `planned` one to `ready`.
- [r10] **While** two `ready` work-items' file sets share a path, `work` shall let at most one of them be claimed.
- [r11] **When** `work claim <work-item> <path>...` is run on a `claimed` work-item, `work` shall add each path to its file set.
- [r34] **When** `work claim` adds paths to a work-item's file set, `work` shall print them.
- [r35] **If** another `claimed` work-item's file set has one of the paths `work claim` names, then `work` shall refuse, naming that work-item and the path, without adding any path.
- [r12] **If** `work claim` names a work-item that is not `claimed`, then `work` shall refuse without changing anything.
- [r13] **When** `work questions` is run, `work` shall print each `awaiting-ruling` work-item with each open question, numbered, its readings, and the `work rule` command that answers it.
- [r14] **When** `work rule <work-item> <n> "<answer>"` is run on an `awaiting-ruling` work-item, `work` shall write the answer, its date and the question it answers under the work-item's `## Rulings`.
- [r36] **When** every open question of an `awaiting-ruling` work-item has an answer, `work` shall move the work-item to `planned`.
- [r15] **If** `work rule` names a work-item that is not `awaiting-ruling`, then `work` shall refuse without changing anything.
- [r37] **If** `work rule` names a question the work-item does not have, then `work` shall refuse without changing anything.
- [r16] **When** `work withdraw <work-item> "<why>"` is run, `work` shall move the work-item to `withdrawn` with the reason.
- [r38] **If** `work withdraw` names a work-item that is `claimed` or `green`, then `work` shall refuse.
- [r17] **When** `work log <work-item>` is run, `work` shall print the work-item's lines of `log.jsonl` in order.
- [r18] **If** `work` refuses a command, then `work` shall say why on stderr and exit 1.
- [r40] **If** a command is given wrongly, then `work` shall exit 2.
- [r19] **When** `work plugin <directory>` is run, `work` shall write `work_expectations.py` into the directory, over any there.
- [r41] **When** `work plugin <directory>` is run, `work` shall print the line that registers `work_expectations.py` in the `conftest.py` beside it.
- [r42] **Where** the directory has an `__init__.py`, **when** `work plugin <directory>` is run, `work` shall print a registering line that imports `work_expectations.py` relative to the package.
- [r43] **If** the path `work plugin` is given is not a directory, then `work` shall refuse without writing anything.
- [r20] `work` and `work_expectations.py` shall count a scenario as accepted by a work-item when the scenario is in the feature file of the work-item's capability and one of its `@r<n>` tags is a requirement the work-item `accepts`.
- [r21] **Where** `work_expectations.py` is registered, **while** a scenario is accepted by some work-item and none of the work-items that accept it has reached `claimed`, **when** the scenario fails, `work_expectations.py` shall report its failure as expected.
- [r44] **Where** `work_expectations.py` is registered, **while** a scenario is accepted by some work-item and none of the work-items that accept it has reached `claimed`, **when** the scenario passes, `work_expectations.py` shall fail the run.
- [r22] **Where** `work_expectations.py` is registered, **while** a `claimed`, `done` or `green` work-item accepts a scenario, `work_expectations.py` shall run the scenario as it is.
- [r45] **Where** `work_expectations.py` is registered, **while** no work-item accepts a scenario, `work_expectations.py` shall run the scenario as it is.
- [r23] **Where** `--work-item <name>` is given to pytest, `work_expectations.py` shall run only the scenarios that work-item accepts, each as it is.
- [r46] **Where** `--work-item <name>` is given to pytest, **if** that work-item accepts no scenario, then `work_expectations.py` shall fail the run.
- [r24] **Where** `work_expectations.py` is registered, `work_expectations.py` shall name in the run's header the `.shop/work` directory it read.
- [r47] **Where** `work_expectations.py` is registered, **if** no `.shop/work` directory is found, then `work_expectations.py` shall say in the run's header that none was found and nothing is expected to fail.
- [r48] **Where** `work_expectations.py` is registered, `work_expectations.py` shall say in the run's summary how many scenarios of which work-items were expected to fail.

## Implementation, may change
- `scripts/work` with its library `scripts/workqueue.py`; the frontmatter subset `scripts/model` reads. A work-item's
  fields are `design-decision/work-file-forms`', plus `risk`, `plan`, `notes`, `fixes` and `findings`; its body
  sections are Observable, Unknown, Risk, Retires, Rulings, and the paths of its notes, plan, report and findings.
- `work_expectations.py` reads pytest-bdd's scenario object for the feature file and the tags, and marks a waiting
  scenario `xfail(strict=True)`.
- `log.jsonl` is one JSON object a line; a move and its file are written together, the log line last.

## Not yet
- A work-queue across bounded contexts (an upstream's items for a cross-context-request) — trigger: a second bounded context is delivered by `work run`.
~~~~~~
