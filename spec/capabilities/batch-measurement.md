---
id: shopsystem-bdd/batch-measurement
title: Batch measurement
narrator: a session measuring a closed batch
group: service
rests_on: [decision/scripts-stdlib-only, decision/measure-refuses-unknown-shapes, decision/an-experiment-is-a-release]
formulated_as: features/batch-measurement.feature
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
- [r4] **Where** no `--out` is given, `measure batch` writes the facts to `docs/superpowers/measurements/<archive file's name>.json`.
- [r5] **If** the archive file was not added by any commit, `measure batch` refuses, naming the file.
- [r6] **If** a transcript's shape is not known, `measure batch` refuses, naming the file and what was missing, and writes no facts file.
- [r7] **If** the facts file exists and `--replace` is not given, `measure batch` refuses and leaves the file as it was.
- [r8] **If** no dispatch is found inside the batch, `measure batch` refuses, naming the window it searched, and writes nothing.
- [r9] A subagent transcript that starts inside the batch is counted as a dispatch, and one that starts outside it is not.
- [r10] A request's usage is counted once in the facts, however many transcript rows carry it, and its reasoning is counted inside its output, not beside it.
- [r11] The facts count a session's own requests inside the batch as the controller's when that session dispatched there.
- [r12] The facts attribute a dispatch to a slice or batch work by its description, failing that by the task or slice its prompt names, and otherwise count it as unattributed.
- [r13] The facts count a reviewer's findings as it wrote them: its lines beginning Critical or Important, and its stated count of Minor.
- [r14] The facts give each commit to the implementer running when it was made, and count the files it touched as production, test or other.
- [r15] The facts give each slice its Lands line from the archive file, or the living plan for the open batch, beside the files its dispatches touched.
- [r16] The facts give the tasks the batch plan held when it was added and the tasks it held at the batch's end, the plan's hand-back entries and its suite record.
- [r17] The facts hold no prompt, reply or tool content.
- [r18] **When** `measure show <file>` is run, `measure` prints the facts file as tables.
- [r19] **When** `measure compare <a> <b>` is run, `measure` prints the two facts files side by side.
- [r20] **If** `measure show` is given a file that is not a facts file `measure` wrote, `measure` refuses, naming the file.

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
