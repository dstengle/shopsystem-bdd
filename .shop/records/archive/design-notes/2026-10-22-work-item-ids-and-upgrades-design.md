# Work-item ids and plugin upgrades (0.24.0)

Source: observation/2026-10-22-release-gate-0-23-0 (the person: "Why wouldn't we use Ids instead of names and get all
of the uniqueness we need?"), measurement/2026-10-22-research-at-the-limit (item 2: work-item names repeat across
initiatives, and `--work-item` takes the first initiative's work-item of a name). The person, 2026-10-22: "Please create
a more general purpose migration capability. When a user installs the new plugin, it should detect version and present
the user with an upgrade option exactly like we'll need to do with the work ids. Now skip questions and get the release
done." The drafting decisions are delegated to the coordinator; every reading below is the coordinator's.

## work-queue: a work-item is named by an id

- `work add <initiative> <title>` with `--part-of`, `--under` and `--accepts` drafts a work-item whose id is `w<n>`:
  it writes `.shop/work/<initiative>/w<n>.md`, its frontmatter `id` `work-item/<context path>/w<n>`, and its title as
  the file's `# ` heading, and prints the id.
- `<n>` is one above the highest `<n>` of any work-item under `.shop/work/`, in any initiative and any status: a
  work-item id is the bounded context's, never repeated, as a requirement id is its capability's.
- Every command that names a work-item names it by its id: `work retry <work-item>`, `work withdraw <work-item>`,
  pytest's `--work-item <work-item>`, `work run`'s work-item branch `work/<work-item>` and its stage directories
  `runs/<work-item>/`. Nothing changes in these commands but what they are given.

## design-model-check: ids are checked

- `model check` prints a work-item whose file name is not `w<n>`, and two work-items with the same id.

## migration-tools: upgrades between plugin versions

`migrate run` takes a repository from the old system to the final layout. An upgrade takes a repository on the final
layout from one plugin release to the next, and is the general means for every later change to a repository's files
that a release makes (work-item ids are the first).

- A repository records the plugin version it is on in `.shop/plugin-version`, one line holding the version. A
  repository with `.shop/` and no record is on 0.23.1, the last release without one.
- The plugin holds a list of upgrade steps, each with the version that introduced it and a one-line description.
  A step is pending for a repository when its version is above the repository's and at or below the plugin's.
- `migrate status` prints the repository's version, the plugin's, and each pending step with its version and
  description. It exits successfully whatever it finds.
- `migrate upgrade` applies each pending step, oldest first, writes the plugin's version into `.shop/plugin-version`,
  and commits all of it in one commit that names each step. It refuses, changing nothing, when the repository has
  uncommitted changes, and, as `migrate run` does, makes every change or none.
- When a session starts in a repository with `.shop/`, the plugin's SessionStart hook runs `migrate status`, and when
  a step is pending tells the session to offer the person the upgrade: the versions, each pending step, and that it
  runs `migrate upgrade` only on the person's yes. When the repository's version is above the plugin's, the hook tells
  the session to tell the person to update the plugin. Otherwise it says nothing.
- The upgrade step of 0.24.0, "work-items named by ids": every work-item under `.shop/work/` gets the id `w<n>`,
  numbered from 1 in initiative order (by the initiative's number) and, within one, by its file name. For each, the
  step renames with git its file to `w<n>.md` and its `runs/<name>/` to `runs/w<n>/`, writes its `id`, keeps its old
  name as its `# ` heading, and rewrites its old name to its id in its initiative's `log.jsonl` `work-item` fields and
  in the `blocked_by` and `depends_on` of its initiative's work-items. Free text in records is history and is left.

## Not in this release

- Steps for releases before 0.24.0: a repository before 0.24.0 is taken as 0.23.1; earlier upgrades were by hand.
- Round trips in `measure` and analysis-tools' `--json` lines (approved for 0.24.0 at the 0.23.0 gate) move to the
  release after this one, so that this one ships the ids.

## Delivery

This repository is the first target: `migrate upgrade` runs on it before the release, and its work-items become
`w<n>`. The plugin's skills that run `work add` (delivering-an-initiative) follow the new arguments.
