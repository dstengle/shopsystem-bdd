---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Batch measurement
narrator: a session measuring a closed batch
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/measure-refuses-unknown-shapes, design-decision/an-experiment-is-a-release]
retired: [r5, r8, r20, r21, r22, r23, r24, r25, r26, r27, r28, r30, r35, r36, r37]
---

# Batch measurement

## Purpose
`scripts/measure` writes one facts file for a batch, from Claude Code's session transcripts, the plan and git:
dispatches, their tokens, time, attribution, findings and commits, the slices' Lands lines against the files
touched, tasks, hand-backs and the suite record. It also prints a facts file, or two side by side. It is not a
judgement of the batch and does not change the repository's code, plan or transcripts; it refuses rather than
guesses when its inputs are not what it knows.

## Behaviour

### The batch
- [r1] **When** `measure batch <archive file>` is run, `measure` shall write one facts file for the batch running from the commit that added the archive file before it to the commit that added its own.
- [r2] **When** `measure batch` is run with no archive file, `measure batch` shall measure the open batch, named `--name` (default `open`), from the last commit that added a file under `--archive-dir` (default `docs/superpowers/plans/archive`) to now, reading the living plan.
- [r3] **Where** `--from` or `--to` is given, as a commit or an ISO time, `measure batch` shall use it in place of that end of the batch.
- [r4] **Where** no `--out` is given, `measure batch` shall write the facts to `docs/superpowers/measurements/<name>.json`, the name being the archive file's without `.md`, or the open batch's.
- [r6] **If** a transcript's shape is not known, or no dispatch is found inside the batch, then `measure batch` shall refuse, naming the file and what was missing, or the window it searched, and write no facts file.
- [r7] **If** the facts file exists and `--replace` is not given, then `measure batch` shall refuse, leaving the file as it was.
- [r38] **If** `measure` cannot do what it was asked, then `measure` shall exit non-zero, say why on stderr, and change nothing.

### What the facts hold
- [r9] `measure batch` shall count a subagent transcript as a dispatch when it starts inside the batch, and not when it starts outside it.
- [r10] `measure batch` shall count a request's usage once, however many transcript rows it appears in, reporting its reasoning tokens as "of which" its output tokens and never adding them to that figure.
- [r11] **When** a session dispatched inside the batch, `measure batch` shall count that session's own requests inside the batch as the controller's.
- [r12] `measure batch` shall attribute a dispatch to a slice or batch work by its description, failing that by the task or slice its prompt names, and otherwise count it as unattributed.
- [r13] `measure batch` shall count a reviewer's findings as it wrote them: its lines beginning Critical or Important, and its stated count of Minor.
- [r14] `measure batch` shall give each commit to the implementer running when it was made, counting as ambiguous a commit made while more than one ran, and count the files it touched as production, test or other.
- [r15] `measure batch` shall give each slice it holds (the archive file's and every other slice a dispatch is attributed to, or for the open batch only those) its Lands line from the archive file or the living plan, with the numbers of production and test files it says it will land, beside the numbers of production, test and other files its dispatches touched.
- [r16] `measure batch` shall give the tasks the batch plan had when it was added and the tasks it had at the batch's end, the plan's hand-back entries and its suite record.
- [r29] **If** no dispatch names a ledger and no `--tasks` is given, or the batch plan is in no commit, then `measure batch` shall leave tasks uncounted, with a note in the facts saying why.
- [r31] `measure batch` shall give each dispatch the closing status its reply states, counting replies that close BLOCKED, PARTIAL or NEEDS_CONTEXT as not done.
- [r32] `measure batch` shall record the plugin and harness versions the transcripts name, and the batch's window as times and, where known, commits.
- [r33] **Where** the batch starts at a commit, `measure batch` shall give the files and lines changed from it to the batch's end commit, or to HEAD when the end is not a commit.
- [r34] `measure batch` shall count the dispatches given more than one prompt as resumed; give the share of building time from the first branch review on, building time being the dispatches' own durations summed, not wall-clock time, with a scout's dispatches left out of both; and give the mean and summed starting context of the dispatches.
- [r17] `measure batch` shall write no prompt, reply or tool content into the facts.

### Reading facts
- [r18] **When** `measure show <file>` is run, `measure` shall print the facts file as tables.
- [r19] **When** `measure compare <a> <b>` is run, `measure` shall print the two facts files' figures side by side, in total and per slice, with the ratio of the second to the first.

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
  counted and the note is also written on stderr.
- Having written the facts, `measure batch` prints one line naming the file, the number of dispatches and slices,
  and the window.
- `show` prints the repository, batch, window, plugin and harness versions and suite record, then the summary,
  roles and slices tables, the dispatches not done or not attributed, each hand-back and each note. `compare`
  prints each summary figure and the output, new input, cache read and agent minutes per slice (each summary
  figure divided by the file's slices) of both files, each headed by its batch and plugin versions.
- Refusals under r38 include: an archive file no commit added (named); no archive file, no `--plan` and no or
  several `docs/superpowers/plans/*-slices.md` (saying to name the living plan with `--plan`); no archive file
  before the batch's end and no `--from` (saying to give the start with `--from`); a `--from` or `--to` that is
  neither a commit nor an ISO time (named); `--repo` (default the current directory) not in a git repository, or
  a git command that fails (git's error); `show` or `compare` given a file that is not a facts file `measure`
  wrote, or not JSON (named).
- The facts file is JSON with a version number; `show` refuses a file of another version.
- Transcripts are removed by the harness after some weeks and found only on the machine and paths the batch
  ran in, which is why a facts file is never written over without `--replace`.
- Exit status: 0 success, 1 refused, 2 bad usage.

## Not yet
- Measuring on the final layout: the lines above still name the living plan, `docs/superpowers/plans/archive` and
  `docs/superpowers/measurements/`, and `scripts/measure` follows them, so on a migrated repository its defaults
  find nothing. Initiative i12 (initiative/i12, proposed) measures an initiative's delivery under `.shop/` instead.
