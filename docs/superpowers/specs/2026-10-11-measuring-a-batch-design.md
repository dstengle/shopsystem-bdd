# Measuring a Batch Design

Date: 2026-10-11
Status: Approved (the design in conversation; the person went offline and asked for the release to be carried
through, so this file was not read by them before the work)
Release: 0.12.0
Request: `docs/superpowers/requests/2026-10-11-predictable-batches-and-analysis-tools.md`

## Purpose

The request proposes some twenty changes, and its evidence was summed by hand from one session. Asked to choose
between two of them, the person said they had no way to judge, and asked for the plugin to carry its own
diagnostics: release, run a batch in a real repository, analyze, pick a change, release again, compare.

So 0.12.0 changes no rule. It makes a finished batch measurable from what the run leaves on disk, and gives the
measurement a fixed report. Every proposal of the request becomes a candidate that a later release tries on a real
batch and keeps or drops by what the measurement shows.

The request is split into three later groups, in this order, each with its own spec: the rule adjustments (its
section E), the suite kept green across re-formulation (C), and the analysis tools with the consequence sweep and
invariants (A, B, D).

## Evidence

A forty-line trial over kb's session of 2026-10-10 (69 subagent transcripts), with no agent involved:

| role | dispatches | output | new input | cache read | context at first turn | minutes |
|---|---|---|---|---|---|---|
| implementer | 38 | 650k | 3.2M | 52M | 29k | 154 |
| task reviewer | 18 | 262k | 1.3M | 9.4M | 15k | 50 |
| branch reviewer | 3 | 124k | 527k | 12M | 15k | 25 |
| scout | 10 | 493k | 1.4M | 12.9M | 14k | 40 |

- Each subagent transcript has a metadata file with the agent type, the model and the controller's description of
  the dispatch; 61 of 69 descriptions name a slice, a task or a batch.
- Each request in a transcript carries its usage: output, input, cache writes and cache reads. Cache reads, and
  the context a dispatch starts with, are things no agent can report about itself.
- kb's history bounds every batch by the commit that adds its archive file (`plan archive`), and the archive holds
  the batch's slices with their `Lands:` lines and its log with every `HAND-BACK`.
- Implementer prompts name the ledger directory `.superpowers/sdd/<batch plan's name>/`, which names the batch plan.
- Skill and script paths in the transcripts carry the plugin's version (`shopsystem-bdd/0.11.0/`).

## Changes

### 1. `scripts/measure`

New `scripts/measure`, `tests/scripts/test_measure.py`. Python standard library, `--help` as its contract, like
`plan` and `features`.

- **`measure batch [<archive file>]`** writes one facts file for one batch.
  - A batch runs from the commit that added the archive before it to the commit that added its own. With no
    archive file named, the batch is the open one: from the last archive commit to now. `--from` and `--to` take a
    commit or a time and replace either end.
  - Sessions are found under `~/.claude/projects/`, in the directory of each worktree of the repository
    (`git worktree list`); `--projects` names another root and `--sessions` names directories outright.
  - A subagent transcript that starts inside the batch is a dispatch. A session's own requests inside the batch
    are the controller's.
  - The file goes to `docs/superpowers/measurements/<archive file's name>.json`, or `--out`. It holds counts, times,
    commit hashes, file counts and the controller's descriptions. It holds no prompt, reply or tool content.
- **`measure show <file>`** prints the batch's summary, the roles and the slices as tables.
- **`measure compare <a> <b>`** prints two batches' summaries side by side with the ratio.

**Per dispatch:** role, model, description, slice, step, task, kind (implement, fix, review, re-review, branch
review, research, probe), how it was attributed (description, prompt, or not), start, end, requests, tool calls,
prompts received (more than one means it was resumed), tokens (output, new input, cache read), context at the
first request and at its peak, closing status, findings as replied (Critical, Important, Minor), and the commits
made while it ran with the production, test and other files they touched.

**Derived, per role and per slice:** dispatches, tokens, agent-minutes, the mean starting context, and for a slice
its `Lands:` as planned against the files its implementers touched.

**Derived, per batch:** the diff's size; tasks in the batch plan when it was added against tasks at the batch's
end; hand-backs, quoted from the log; statuses other than done; reviews by kind with how many came back with no
Critical or Important finding; the share of dispatch time after the first branch review started; the plugin and
harness versions seen in the transcripts; and what could not be attributed.

**Rules of the script:**

- The transcript files are Claude Code's and are not a published format. A transcript whose shape the script does
  not know is refused by name, with what was missing. A number is never guessed.
- A request's usage is counted once, however many rows carry it.
- A commit belongs to the implementer dispatch running when it was made. Where two were running, it goes to the
  later-started one and the facts say how many commits were ambiguous.
- A test file is one under a `tests` or `test` directory or named `test_*` or `*_test.*`; `docs/`, `features/`,
  `spec/` and Markdown are other; the rest is production.
- Findings are counted from the reviewer's reply as it wrote it, and the facts say so. Judging them is the
  report's.

### 2. Two lines in the plan's Global Constraints

`skills/slicing-into-increments`, the execution rules.

- **Descriptions say what a dispatch is.** Every dispatch's description starts `slice <n>[ step <k>]: ` and one of
  `implement`, `fix`, `review`, `re-review`, `research`, `probe`; work that belongs to no slice starts
  `batch <name>: `. `measure` attributes by it.
- **Measure at the close.** After `plan archive`, the controller runs `measure batch <the archive file>` and commits
  the facts file with the archive. Transcripts are removed by the harness after some weeks; the facts are kept.

These are the only changes to how a batch runs.

### 3. Skill `analyzing-a-batch`

New `skills/analyzing-a-batch/SKILL.md`. Used in the repository that ran the batch, when the person asks what a
batch cost or what to change in the workflow.

- It runs `measure batch` when the facts file is missing, and reads the facts with `measure show`. It never reads
  a transcript: every number in the report is the script's.
- The session does the judging itself, with no agent: the facts, the archive's log and the findings files are
  small. It judges only what counting cannot:
  - each hand-back's cause: a listing omission (the test was not in "Tests the decisions break"), a decision
    missing from the plan, a scenario that is wrong, or other;
  - each Critical or Important finding: the stage that found it (task review, branch review, after the batch
    closed) and the earliest stage that could have, with why;
  - each task added after the batch plan was written: what caused it.
- It writes `docs/superpowers/reports/<date>-<batch>-analysis.md` in a fixed shape: what ran (repository, batch,
  plugin version, slices); the tables as `measure show` prints them; the comparison with one earlier measurement,
  named, from `measure compare`; the three judgements, each row citing a log entry or a findings file by
  `path:line`; observations; candidates.
- An observation cites a row of the facts or a `path:line`. A candidate is something to try in the plugin, with the
  observation it rests on and the number that would show it worked. The report words no rule: that is the
  shopsystem-bdd session's, which receives the report as a request.

### 4. Release

- `.claude-plugin/plugin.json` to 0.12.0.
- README: a section "Measuring a batch (0.12.0)" with the loop (release, run, measure, analyze, compare); the
  skill in the skills list; `measure` beside `plan` and `features`.

## Experiments are releases

A variant is a plugin version. A release changes one rule or one small group, a batch runs on it, and
`measure compare` sets it against the baseline. There are no switches inside a version: the facts record the
version, and that is the variant's name.

## Not yet

- **Every proposal of the request**: E's ten rule adjustments, C, A, B and D. Each is a candidate with the
  request as its evidence, tried against the baseline in the order the person chose.
- **Cost in money.** Tokens by model are recorded; prices change and are not the script's to hold.
- **Other harnesses.** Only Claude Code's transcripts are read.
- **A hook that records each agent as it stops.** It would not depend on the transcript format, and it would not
  measure runs already made. Promoted if the format changes often.
- **An analyst agent.** The session's own judging is enough while a batch's log and findings are small. Promoted
  if a report's judgements are wrong in a way a narrower reader would not be.
- **Switches for rules inside one version.**

## Verification

- **The script:** tests over a generated repository with dated commits and generated transcripts: the batch's
  bounds from archive commits; a request's usage counted once; attribution by description, by prompt, and none;
  commits and their files by dispatch; `Lands:` against touched; tasks planned against run; hand-backs; a resumed
  agent; a transcript of unknown shape refused; `show` and `compare`.
- **The baseline:** `measure batch` on kb's batches 32, 33 and 34 and on the open batch 35, written under
  `docs/superpowers/testing/` in this repository (nothing is written to kb), and checked against the request's
  hand-summed figures, each difference explained in the test log.
- **The skill:** as this repository's skills are tested: headless on a fixture, before and after, logged under
  `docs/superpowers/testing/`.
