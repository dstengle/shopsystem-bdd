# History

This folder keeps documents as they were when they were written. **Nothing here is current.** Each one describes
the plugin at an earlier release, in the words of its day, and some of what it teaches the plugin now refuses.

It's for anyone who follows an old link, meets an old citation in a decision or a record, or wants to know why
the plugin is shaped the way it is. If you want to know how things work today, start at the
[docs home](../index.md) instead.

## What happens if you follow an old document today

Design model v5 teaches a capability file that says `language: codified-1`. Write one today and the plugin
stops you. This is a scratch copy of this repository, with one capability's frontmatter set back to the old
language:

```console
$ features generate backlog
features: spec/capabilities/backlog.md says `language: codified-1`: run `migrate upgrade`
$ model check
v_p0  a spec file is not codified (no `language: codified-2`, or a capability in `codified-1`): run `migrate upgrade`  (1)
    spec/capabilities/backlog.md
...
```

`features generate` exits 2, and `model check` names the file under `v_p0`. That's why these documents live here,
with a banner on top, rather than beside the pages you learn from.

## What's here

| document | written | for | retired | read instead |
|---|---|---|---|---|
| [`design-model-v5/`](design-model-v5/README.md) | 2026-11-03 | plugin 1.x and `codified-1` | its workflow in 2.0.0, its language in 4.0.0 | [the design model](../reference/design-model.md), [concepts](../concepts.md) |

### `design-model-v5/`: design model v5

The model the plugin was built on through 1.x: the standing artifacts of a context and the edges between them,
the requirement language of `codified-1`, and a workflow of initiatives, parts and a pull-based work-queue. It has
five files:

- [`README.md`](design-model-v5/README.md): the model in one paragraph, and the order to read the rest in.
- [`how-we-got-here.md`](design-model-v5/how-we-got-here.md): the conversations of September and October 2026
  that produced it, condensed. Read this one first if you read any.
- [`design-model.md`](design-model-v5/design-model.md): the reference of version 5.
- [`grammar.md`](design-model-v5/grammar.md): the same model stated formally, as edges, constraints and lifecycles.
- [`ecommerce-example.md`](design-model-v5/ecommerce-example.md): a small shop written in the model.

Two of its ideas are still live, in a different shape: the graph of standing artifacts that `model check` holds,
and records that are dated and never edited. Both are described as they are now in
[the design model reference](../reference/design-model.md). The rest changed:

| in design model v5 | today | changed in |
|---|---|---|
| an initiative, realised by a tree of parts and work-items | an item in `.shop/backlog/` | [2.0.0](../../CHANGELOG.md#200-the-workflow-simplified) |
| the work-queue, pulled from by `work run` | a batch of ready items (`work batch start`), reviewed once at its pull request | [2.0.0](../../CHANGELOG.md#200-the-workflow-simplified) |
| a capability-proposal | requirement lines on an item (`work line`) | [2.0.0](../../CHANGELOG.md#200-the-workflow-simplified) |
| `language: codified-1`, EARS lines in the 1.x grammar | `language: codified-2`, lines in grammar 4 | [4.0.0](../../CHANGELOG.md#400-the-controlled-language-4) |
| the temporal check, written for telingo | `model logic`: one clingo solve over each line's facts | [1.0.0](../../CHANGELOG.md#100-codified-requirements) |

The [changelog](../../CHANGELOG.md) has the full story of each release.

## Old citations still land here

Older decisions and records cite these documents by their first path, `docs/design-model/`. For example,
`spec/decisions/0023-scenario-names-requirement-by-tag.md` says it was decided by
"docs/design-model/design-model.md v3 section 2". Those files are records, so they are never edited to follow a
move. Read `docs/design-model/<file>` in a citation as `docs/history/design-model-v5/<file>`.

A citation that names an older version, such as v3, means the document as it stood then. Git keeps every version,
and the history follows the move, because the folder was moved with `git mv`:

```console
$ git log --oneline --follow -- docs/history/design-model-v5/design-model.md
...
3ce6d5c0a The plugin's first spec in the design model's layout; scripts/model checks it
```

Pick a commit from that list and `git show <commit>:docs/design-model/design-model.md` prints the file as it was.

## The rules of this folder

- **Documents are kept whole.** Each one is moved here with `git mv` and not edited, apart from a banner at the
  top of its first page that says what it was, when it stopped being current, and what to read instead.
- **The docs test skips this folder.** The examples, commands and links under `docs/` are checked against the
  plugin as it is; the ones here are checked against nothing, because they describe the plugin as it was.
- **A document comes here when its release has passed.** When a page under `docs/` stops being true and is
  replaced, the old one moves here whole, gets its banner, and gets a row in the table above.

Next: [the design model](../reference/design-model.md), [concepts](../concepts.md), or the
[changelog](../../CHANGELOG.md).
