# Requirement ids: test log (0.19.0)

Branch `0.19.0-requirement-ids`, commits `9038634` to the release commit. Scripts: 307 tests, OK.

**The headless runs were not made.** The permission classifier denied the nested
`claude -p ... --dangerously-skip-permissions` sessions, both Task 7's self-run of the new formulation text on
this repository and all of Task 9's fixture runs. Nothing tried to get around it. They wait on the person. This
log therefore holds no scorer table and no A/B cost table: the skills' new text for ids (integration, formulation,
migration) has been reviewed against the lines it implements, but not run by a model.

## What changed

- Design model v3 in use: every Behaviour line `[r<n>]`, every scenario tagged `@r<n>`, retired ids in the
  capability's frontmatter, capability ids as IRIs under the context id.
- `scripts/model`: held scenarios are no acceptance-scenarios; a decisions ledger is read; `features tag` takes
  `r<n>`.
- `docs/capability-format.md`, `integrating-a-proposal`, `formulating-features`, `migrating-to-capabilities`
  (including "Adding Ids" for a repository already on capability files), the `capability-writer` and
  `feature-formulator` briefs.
- Five script capabilities formulated and bound: `analysis-tools`, `batch-measurement`, `slice-plan-tool`,
  `design-model-check`, `feature-file-tools`.
- Version 0.19.0, README, `spec/index.md`, initiative i3, observation
  `obs/2026-10-16-release-0.19.0-defects`.

## Formulating this repository's script capabilities in-session

Five `feature-formulator` agents were dispatched with the new brief, one per capability, drafts under
`.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/`. The brief was formulating-features' new text,
written out as the skill gives it. This exercises the brief and the agents, not the skill's end-to-end run:
`spec-round`, `model check` inside the round and the commit step were done by an implementer by hand.

- Requirement lines per capability, each with a scenario tagged to it (from the capability files and the feature files' distinct `@r<n>` tags): analysis-tools 35, batch-measurement 38, slice-plan-tool 38, design-model-check 45, feature-file-tools 51; 207 in all.
- The formulators returned 14 questions between them (analysis-tools r1, r14; batch-measurement r10, r34;
  slice-plan-tool r8, r10, r23; design-model-check r23, r26, r27, r41; feature-file-tools r3, r4, r14). The lines
  were drafted from the 0.18.0 code and admitted two readings.
- The questions were answered from the code, not by the person: each line was reworded to state what the code does
  (14 rewordings, commit `d4090e3`), then a second round formulated them (14 of 14, no questions). Four lines
  changed meaning against the draft, because the code did not do what the draft said: r1, r3, r26 and r41.
- After review, four scenarios were fixed where they asserted more than the code does, only the affected steps,
  and one line (analysis-tools r16, import-linter run over no paths) was reworded at binding. These rewordings are
  listed for the gate: the person sees them there, and may reject any.
- One formulator, analysis-tools, could not write its `.reply.md`: the harness refused ("subagents may not write
  report files"). The drafts were written. `spec-round` waits in one shell command for every reply file, so a
  harness that blocks them stalls the round. Recorded as a risk in the observation, not changed.
- Untagged scenarios: none. Coverage after formulation was checked by `model check`.

## Binding

Each scenario is bound to the unittest test whose docstring is its title; scenarios are tagged `@r<n>`, titles are
free. 307 tests. A mutation check per subtask: each new test passed on its first run (the code already did it) and
was then failed by a scratch mutation of the script, restored afterwards.

| subtask | script | mutation checks |
|---|---|---|
| 8a | `scripts/model`, `model.lp` | each new test failed by a mutation; r41 first survived (dates in id order) and its data was changed |
| 8b | `scripts/features`, `slice_expectations.py` | 21 mutations caught |
| 8c | `scripts/plan` | 34 mutations caught; two survive (porcelain-only, the title check has no scenario) |
| 8d | `scripts/measure` | in the subtask report |
| 8e | `scripts/tools` | about 35 caught; two redundant map mechanisms (old-map removal, `--cov-append`) mask each other and survive |

Code defects found and fixed:

- `features tag slice-1.2.3` was accepted, though feature-file-tools r11 allows `slice-<n>` or `slice-<n>.<m>`.
- `scripts/plan` reported a slice that has a Check as "has Scenarios, not Check": the message was reversed.

Open defects are in `obs/2026-10-16-release-0.19.0-defects`.

## The fixture harness

Built and self-tested in `/home/vscode/scratch/shopsystem-bdd/ids/` (`make_ids.py`, `score.py`, `run.sh`,
`run-all.sh`, `selftest.sh`, `selftest.out`). Five cases: `integrate` (to the gate), `apply` (approved drafts
applied and committed alone), `formulate` (with clingo), `noclingo` (clingo hidden by a `PYTHONPATH` directory;
the run must say model check did not run), `migrate` (adding ids to a repository on capability files).
`run-all.sh` runs three B runs per case (the branch) and two A runs of integrate and formulate (0.18.0, cost only).

The self-test needs no model. Fresh fixtures fail every check a run has to achieve; a hand-made correct result
passes every check (ok lines in selftest.out: integrate 7, apply 7, formulate 8, noclingo 7, migrate 12); mutation cases (a renumbered
line, an apply message that names the wrong lines, an unformulated lend-items, a v_s3 left, the index id not
changed, spec and features in two commits) each fail the check meant for them (some fail others too: the stale index id also fails `model check` and the one-commit check). Two rounds of review
of the harness fixed: a correct same-line gate misread, the missing index id and one-commit checks, and prompts
that hinted the checks.

Command: `/home/vscode/scratch/shopsystem-bdd/ids/run-all.sh`. **Its results are not in this log.**

## What the reviews caught

- **Commit-then-check order** (integrating-a-proposal step 4): the plan committed `spec/` and then ran
  `model check`; spec-integration r16 says check first. The order is apply, check, commit.
- **`model check` given paths**: the skills passed paths; the script reads the whole repository and takes none.
- **Failures not scoped to the round**: in a repository not yet on ids every scenario is `v_s1` and every line
  `v15a`, so a literal follower could never pass. Both skills now judge what the round added.
- **A removal deadlock**: a scenario placed under no line could never clear `v_s1`; an answer now leads to a new
  line or to holding it for removal.
- **A missing id in `spec/index.md`**: Adding Ids never wrote the context id there, so `model check` reported a
  file problem. Found by the harness; fixed in `4afdeda`.
- **First migration untagged**: spec-migration's lines and the skill did not tag scenarios on a first migration;
  r4, r5, r6 and r11 now allow the new `@r<n>` tags, and r11 says "nothing else in a scenario changes".
- **Hold without rebind**: a hold changes the title, so its test needs `features rebind`; the skill now says so.

## Not tested

- All the headless runs: Task 7's self-run of the formulation text and Task 9's five cases, A and B, with the
  scorer tables and the cost comparison.
- A real batch in a consuming repository, kb or shopsystem-knowledge, measured with `scripts/measure`.
- A question round-trip after ids: a formulation question going back to integration and returning as a round.
- The skills run end to end on this repository: `spec-round` with `model check` inside the round.
- Decisions as files in consuming repositories, which is not in this release.
- A harness that blocks subagents from writing reply files.

## Fix note

Corrected after review: the harness's ok counts are taken from selftest.out; "exactly" dropped from the mutation sentence; the unsupported "186 lines" replaced by counts of requirement lines per capability.
