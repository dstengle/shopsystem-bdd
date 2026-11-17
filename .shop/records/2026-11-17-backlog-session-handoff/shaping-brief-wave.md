# The shared brief for shaping one backlog item (a wave after the 2026-11-16 triage)

Repository: /home/vscode/shopsystem-bdd (plugin 0.35.1). Read its CLAUDE.md first. Then invoke the skill `shopsystem-bdd:shaping-items` with the Skill tool and follow it for your one item, with the exceptions below. Use `python3 scripts/<tool>` from the repository root; the skill's `<scripts>` is this repository's `scripts/`.

## Ground rules

- Touch only your own item, `.shop/backlog/b<n>.md`, and only through `work` commands (`work shape`, `work line`, `work rate`, `work ready`), each of which commits only that file, or by editing its `## Requirements` bullets or `## Notes` and committing that one file. An item already `shaped` cannot take `work shape --note`: add to `## Notes` by hand. Never edit `spec/`, `features/`, code, or another item. Other agents shape their own items in this same checkout at the same time: if a git command fails on `index.lock`, wait a few seconds and run it again.
- Do not push (ignore `not pushed: ...`; the session pushes). Do not start a batch (skip the skill's step 6). Do not ask the person anything; decide, and report the decision. Never use Claude Code's memory.
- Use the main checkout as the only reference. Never read leftover worktrees, other branches or other repositories.
- Run each command with a timeout of a few minutes; `work ready` and a first `model parse` may take up to 10 minutes while grammar 4 compiles. Write every term bullet (and relation row) your item needs before you check any line, then run `work ready` once, and again after each rewording.
- For a fault, reproduce it first on a throwaway copy of `spec/` in your own scratch directory (`model --root <copy> parse --form`, `model --root <copy> logic`, `features generate --root <copy>`) or with the command it names, and say in your reply what you ran and what it printed.

## Background

Read your item (`python3 scripts/work show b<n>`) and the triage record `.shop/records/2026-11-16-backlog-triage.md`: your item's notes end with the triage's evidence and, for some, the person's decision with its quote id (quote-37 to quote-42; `python3 scripts/work show quote-<n>`). Cite those quotes in your note. An item whose notes the triage narrowed is shaped as narrowed.

## How lines read

Requirement lines are what the rest of the system stands on. Each line says one checkable behaviour of this plugin, in the capability that owns it (`spec/capabilities/*.md`); a reader of the line alone can tell what a test of it does. Prefer a few sharp lines to many vague ones. A changed delivered line is a new line with `--retires`. Read the existing lines near yours for the words available (`python3 scripts/model lexicon`), and add a term with `work line --term` where a word is missing, never a near synonym. The note (by hand under `## Notes`, or `work shape --note` on an idea) says, in prose, which modules change (CLAUDE.md's module map), what the scenario does, what is left out, and dependencies. Keep the rating the triage gave unless shaping shows it wrong; say why if you change it.

If your item turns out to have no behaviour a scenario can check, do not force lines: say so in the reply, with the files it would change and the check that would show it done (b316 will let such an item be readied).

## Reply

Your item's id and status (ready, or the refusal `work ready` gave last), each line verbatim with its id and capability, each term added, the note in one paragraph, its rating, the reproduction, and every decision the person may want to revisit. Be terse.
