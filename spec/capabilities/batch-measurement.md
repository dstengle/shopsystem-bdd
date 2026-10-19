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
- [r1] **When** `measure batch <archive file>` is run, `measure` writes one facts file for the batch running from the commit that added the archive file before it to the commit that added its own.
- [r2] **Where** no archive file is given, `measure batch` measures the open batch, from the last archive commit to now, reading the living plan.
- [r3] **Where** `--from` or `--to` is given, as a commit or an ISO time, `measure batch` uses it in place of that end of the batch.
- [r4] **Where** no `--out` is given, `measure batch` writes the facts to `docs/superpowers/measurements/<archive file's name without .md>.json`.
- [r5] **If** the archive file was not added by any commit, `measure batch` refuses, naming the file.
- [r6] **If** a transcript's shape is not known, `measure batch` refuses, naming the file and what was missing, and writes no facts file.
- [r7] **If** the facts file exists and `--replace` is not given, `measure batch` refuses and leaves the file as it was.
- [r8] **If** no dispatch is found inside the batch, `measure batch` refuses, naming the window it searched, and writes nothing.
- [r9] A subagent transcript that starts inside the batch is counted as a dispatch, and one that starts outside it is not.
- [r10] A request's usage is counted once in the facts, however many transcript rows it appears in, and its reasoning tokens are a part of its output tokens: the facts report reasoning as "of which" the output figure and never add it to that figure.
- [r11] The facts count a session's own requests inside the batch as the controller's when that session dispatched there.
- [r12] The facts attribute a dispatch to a slice or batch work by its description, failing that by the task or slice its prompt names, and otherwise count it as unattributed.
- [r13] The facts count a reviewer's findings as it wrote them: its lines beginning Critical or Important, and its stated count of Minor.
- [r14] The facts give each commit to the implementer running when it was made, and count the files it touched as production, test or other.
- [r15] The facts give each slice its Lands line from the archive file, or the living plan for the open batch, the numbers of production and test files it says it will land, beside the numbers of production, test and other files its dispatches touched.
- [r16] The facts give the tasks the batch plan had when it was added and the tasks it had at the batch's end, the plan's hand-back entries and its suite record.
- [r17] The facts hold no prompt, reply or tool content.
- [r18] **When** `measure show <file>` is run, `measure` prints the facts file as tables.
- [r19] **When** `measure compare <a> <b>` is run, `measure` prints the two facts files side by side.
- [r20] **If** `measure show` is given a file that is not a facts file `measure` wrote, `measure` refuses, naming the file.
- [r21] **If** no archive file is given, no `--plan` is given and the repository holds no `docs/superpowers/plans/*-slices.md` or several, `measure batch` refuses, saying to name the living plan with `--plan`.
- [r22] **If** no archive file was added before the batch's end and no `--from` is given, `measure batch` refuses, saying to give the batch's start with `--from`.
- [r23] **If** `--from` or `--to` is neither a commit nor an ISO time, `measure batch` refuses, naming what it was given.
- [r24] **If** `--repo`, default the current directory, is not inside a git repository, or a git command `measure batch` runs fails, `measure` refuses with git's error.
- [r25] **Where** no archive file is given, `measure batch` names the batch `--name`, default `open`, and without `--out` writes the facts to `docs/superpowers/measurements/<name>.json`.
- [r26] **Where** no archive file is given, the open batch starts at the last commit that added a file under `--archive-dir`, default `docs/superpowers/plans/archive`.
- [r27] The facts hold the archive file's slices and every other slice a dispatch is attributed to, and for the open batch only the slices a dispatch is attributed to.
- [r28] The facts count, as ambiguous, the commits made while more than one implementer was running.
- [r29] **If** no dispatch names a ledger and no `--tasks` is given, or the batch plan is in no commit, the facts leave tasks uncounted and hold a note saying why, and `measure batch` writes the note on stderr.
- [r30] **When** `measure batch` has written the facts, it prints one line naming the file, the number of dispatches and slices, and the window.
- [r31] The facts give each dispatch the closing status its reply states, and count replies that close BLOCKED, PARTIAL or NEEDS_CONTEXT as not done.
- [r32] The facts record the plugin and harness versions the transcripts name, and the batch's window as times and, where known, commits.
- [r33] **Where** the batch starts at a commit, the facts give the files and lines changed from it to the batch's end commit, or to HEAD when the end is not a commit.
- [r34] The facts count the dispatches given more than one prompt as resumed; they give the share of building time from the first branch review on, where building time is the dispatches' own durations summed and not wall-clock time, and a scout's dispatches are left out of both that time and the part of it from the first branch review on; and they give the mean and summed starting context of the dispatches.
- [r35] **When** `measure show` is run, `measure` prints the repository, batch, window, plugin and harness versions and suite record, then the summary, roles and slices tables, the dispatches not done or not attributed, each hand-back and each note.
- [r36] **When** `measure compare` is run, `measure` prints each summary figure and the output, new input, cache read and agent minutes per slice (each summary figure divided by the file's slices) of both files, each file headed by its batch and plugin versions, with the ratio of the second to the first.
- [r37] **If** `measure compare` is given a file that is not a facts file `measure` wrote, or `measure show` or `measure compare` a file it cannot read as JSON, `measure` refuses, naming the file.
- [r38] **If** `measure` refuses, it says why on stderr and exits 1.

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
