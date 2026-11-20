---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-20-ux-trial-2-a-checklist-app-from-prompts-on-0-40-0
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-20
---

# UX trial 2: a checklist app from prompts on 0.40.0

The second user-experience trial: a new user's empty git repository driven to a built, tested checklists CLI with
only short prompts, in real headless Claude Code sessions (`claude -p -c --plugin-dir <this repository>
--dangerously-skip-permissions`, Claude Code 2.1.327) with the plugin loaded from main at 0.40.0 (7daf0d652), later
main with this trial's fixes. The trial repository had a bare local `origin` beside it and no GitHub repository: from
session 3 on, `$SHOPSYSTEM_WORK_GH` pointed at tests/scripts/stub_gh.py as a stand-in for gh, and the person's merge
on GitHub was played by merging `batch-<n>` into the remote's `main` and setting the stand-in's pull request
`MERGED` with that merge commit. The trial repository's key files are kept in the folder beside this record, each
with a `.txt` suffix.

**How far it got:** all the way, twice. From an empty folder to item b1 delivered (eleven lines, a `checklists.py`
with create, add, check and list, `spec/adapters/cli.toml`, step bindings, 11 scenarios passing, `spec check` 0
violations, `features generate --check` clean), then a second item b2 (browse every checklist with its open count)
shaped, built, reviewed and delivered from one more prompt. No spec file was written by hand. The first trial
(0.39.0) stopped at `work batch start` with hand-written model and vocabulary files.

## The prompts and what each did

1. "Set up this repository for the plugin." (README, getting-started step 3): a `.venv` with pytest 9.1.1 and
   pytest-bdd 8.1.0, `tools install` and `tools probe` (b388's fix: the grammar block printed in a folder with no
   Python file), then it asked for the context id, the remote and what to build. Good.
2. "Use bounded-context/example.org/checklists/checklists-cli. Keep the local origin for now. I want a small CLI
   that keeps checklists: create one, add items, check items off, list them." (the brief's own words; the docs
   give the id step but no combined prompt): `migrate init` refused by git (`Author identity unknown`); the session
   set `user.name dave` and an email it took from the account, without asking. Then `work idea`, `work quote`
   (refused: no session known, see b417; it found its transcript and passed `--transcript`), `work shape`, `work
   line --capability`, `--model`, thirteen `--term` entries, eleven lines, `work rate`, `work ready` (four parse
   refusals and v15k/v15l on the first try; reworded; it removed every line, which took the new capability's block
   with the last one, and `--into checklists` was then refused with no word of `--capability`, see b414),
   `work batch start`, and the driver agent from the brief. The task agent wrote the program, the contract and the
   bindings from getting-started and docs/reference/adapters.md, red to green line by line; `work batch done`
   passed. `work batch review` stopped at `gh pr create` (no GitHub remote); the session had said beforehand it
   would, and asked for a repository.
3. "Keep it local: in this setup SHOPSYSTEM_WORK_GH points at a stand-in for gh that plays GitHub for the local
   origin. Carry on with the batch.": review 1 (pr-reviewer) found f1 (the feature differed from what `features
   generate` writes: this trial's b413 fix had landed on main meanwhile) and f2 (ruff in the new files); one fix
   agent, review 2 clean, `awaiting-merge`.
4. "The pull request is merged." (getting-started step 7): it pulled the merge commit into the local main (`work
   batch merged` needs it there), `work batch merged`, `measure batch` (19 min 43 s wall, cost 4.07), committed.
5. "Yes: I also want to list all my checklists, with how many items each has left to check.": b2 shaped (a new
   operation `browse` on the existing service, two lines), ready, batch-2 built and reviewed clean.
6. "The pull request is merged.": b2 delivered (5 min 32 s, cost 1.13).

The CLI, run by hand on main: `create --title Groceries`, two `add`s, `check 1`, `list Groceries` prints
`1 [x] milk / 2 [ ] eggs`; a second `check 1` is refused (`the item 1 is checked already`, exit 1).

## Fixed on ux2-fixes, merged to main (8a642b0ec)

- b413 (169d8bbe2): `features generate` wrote `And the title of the checklist c1 is [t_title_2_v_groceries]`, GF's
  placeholder, for a text attribute's value; spec_steps4 now says a value no entry lists with `_IsCodeOf` and its
  code. Test in tests/scripts/test_spec_steps4_request.py.
- b414 (699212783): `work line --into <name>` for a capability no file holds now names `work line <item>
  --capability <name>`.
- b415 (2d5a26c8a): `migrate init` checks git's identity before it writes and refuses saying to ask the person and
  set `git config user.name` / `user.email`. Test tests/scripts/test_migrate_init_identity.py.

Suite: 2435 passed, 1 skipped; `tools size --limit 300` clean; `spec check` 0 violations.

## Items left

Ready: b416, a response's thing that a trigger's thing has ("return the items of the checklist") brought in by a
Given before the When (scenarios#r33). The generated r10 scenario named an item i1 no Given introduced, and its row
was a Then; the task agent's binding made the item itself. It does not block the goal, but every first app with a
"list the Ks of X" line meets it.

Ideas filed: b417 (the prompt hook keeps no session in the turn that founds the context), b418 (a value in use,
such as a duplicate title, can only be said with example data), b419 (plain pytest warns of an unknown mark per
@g/@r tag; `-p work_items` needs the plugin's scripts on PYTHONPATH), b420 (a verb names one operation, so "list all
my checklists" became the coined verb `browse` and a `browse` command).

Known and seen again: b394 (a batch needs a GitHub remote and gh; the session said so before the review, which is
the one hard stop for a user without GitHub).

## What went well

Every step from setup to a delivered second item came from the skills and the briefs with no hand-editing: the
domain model and vocabulary on the item (b387, b354), the lay in 0.38's form (b391), no construct catalogue written
for a backticked value (b390), the batch brief and building-a-batch saying how to make the program, contract and
bindings (b389). The sessions explained each step to the person in plain words and asked only for the context id,
the remote, and the merge.
