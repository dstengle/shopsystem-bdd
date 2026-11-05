---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-8-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 8 of the workflow simplification: rulings on the review, and what was done with each finding

`plan-8-review.md` (committed in `bfb2755f`) asked the person three questions. The person was not available. Each
ruling below was **ruled by the main session without the person, 2026-11-05; revisit.** The fixes are on branch
`workflow-simplification`, from `22c6baa7` to this record's commit, not pushed. Every new test failed before its fix.
The tests use synthetic transcripts only.

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-05; revisit) | What was done |
|---|---|---|---|
| Q1 | Is a slash command with arguments the person's message? | Yes: `/<name> <args>` is the person's message, the command and its arguments, and the reply to it is a turn of its own. | `22c6baa7`: a row whose text starts `<command-name>` or `<command-message>` and names a command is read as `/<name> <args>` (`/clear` with no arguments). `<local-command-stdout>` and the meta skill expansion stay out. Test: `test_a_slash_command_is_the_persons_message` (`/brainstorm keep the turns` cited by "keep the turns", its reply its own message). |
| Q2 | Should the SessionStart table list every item, closed ones included? | Keep r4 as built. Plan 9: measure the table on this repository's real backlog, and past about 50 rows narrow the hook's table to the items not `delivered` or `withdrawn` and the batches not `merged` or `abandoned`. `work names` keeps the full table. | Nothing changed; a note for plan 9. |
| Q3 | Two sessions in one checkout | Accept one pointer per checkout. The hook ignores stdin whose `cwd` is outside the repository's top level. | `35d3c704`: `keep` writes nothing when the stdin's `cwd` has another top level than the hook's (one more `git rev-parse`, so a session in a worktree nested inside the checkout is told apart too). A stdin with no `cwd` is kept as before. Test: `test_a_prompt_from_outside_the_repository_is_ignored`. |

## The findings

| # | What was done |
|---|---|
| B1 | Fixed in `22c6baa7`. `_persons` returns nothing for a row whose `origin` is a dict of a kind other than `human` (task notifications, auto-continuations), and for text starting `<task-notification>` (older rows have no `origin`). `NOISE` gains `task notification` (origin and tag), `task notification tag` and `auto-continuation`; `test_a_prompt_the_person_typed_is_a_message` pins that `origin.kind: human` is kept. conversation.md's Implementation bullet says "notifications". |
| S1 | Fixed in `22c6baa7`. `"<bash-"` is in `COMMAND`. `NOISE` gains `bash input` and `bash output`. |
| S2 | Fixed in `df3b5d74` (and `1a0d7e01`, ruff). `scripts/conversation_hook quote|names` puts its directory on the path, imports only `conversation_prompt` or `conversation_names` (standard library and the conversation's modules), and catches everything, imports included, exiting 0. hooks.json runs it; `work quote --hook` and `work names --hook` stay as aliases; the `migrate` hooks are unchanged. Tests (`tests/scripts/test_hooks.py`): every hooks.json command under `python3 -S`, in a repository with `.shop/` and outside git, exits 0 with empty stderr (the two `work` commands failed first); under `-S` the prompt hook writes the pointer and the names hook prints the table; the hook copied alone, its modules missing, exits 0 silently. The hook medians on 200 items and 20 batches fell to 0.02 s (prompt) and 0.09 s (names). CLAUDE.md gains the module's row; README and the Implementation section name it. r2's line still says "the UserPromptSubmit hook runs `work quote --hook`": still true of the alias, left as written (requirements are retired, not edited); plan 9 may retire it for a line naming the hook. |
| M1 | Fixed in `22c6baa7`. Text starting `[Request interrupted by user` is not a message. `NOISE` gains `interrupted` and `interrupted for tool use` (a text block beside a tool result). |
| M2 | Fixed in `22c6baa7`. `_texts` writes `\r\n` and `\r` as `\n`, so a rendered quote reads back as it was. Tests: `test_carriage_returns_are_newlines`, and `test_a_carriage_return_reads_back_from_the_file` (written by `work quote`, read by `find`). |
| M3 | Fixed in `35d3c704`. `kept` returns None only when there is no pointer, and raises `Unreadable` when it is there but cannot be read or has the wrong shape; `work quote` refuses as "the pointer <path> the UserPromptSubmit hook keeps cannot be read; give --session <id>". Test: `test_an_unreadable_pointer_is_refused_naming_it` (corrupt JSON, a list). |
| M4 | Fixed in `35d3c704`. On any failure after the part file is named, `keep` unlinks it. Test: `test_a_failed_rename_leaves_nothing_behind` (`prompt.json` a directory). |
| M5 | Fixed in `22c6baa7`. A row with no `uuid` is named `<file name>:<line>`; the refusal of a row with no type still names the full path. Test: `test_a_row_with_no_uuid_is_named_by_its_file_and_line`. |
| M6 | Fixed in `874ff02a`, the cheapest way: shaping-items step 1 says an earlier session's id is the name of its transcript, `<id>.jsonl`, in the project's directory under `~/.claude/projects/` (newest last by `ls -tr`), or that file can be given with `--transcript <path>`. Test: `test_r3_the_skill_says_where_an_earlier_sessions_id_is`. |

## Verification after the fixes

| Check | Before (review) | After |
|---|---|---|
| unbuilt | `{} 0 []` | `{} 0 []` |
| `python3 -m pytest -q` | 1553 passed, 1 skipped, 135 subtests | 1582 passed, 1 skipped, 135 subtests (31.3 s); ceiling `test_e2e_codified` 11.9 s |
| `python3 -m pytest -m timing -n 0 -q` | 4 passed | 4 passed, 1583 deselected (6.3 s) |
| `model check` | 53 / 16 / 19 / 0 | 53 / 16 / 19 / 0 |
| `model logic` | 11 findings: 6 L5, 5 L6 | same |
| `model lexicon --check` | 401 terms, 0 problems | same |
| `model decisions --check` | 4 hold, 0 failing | same |
| `features generate --check`, `vocab --check`, `bindings --unbound` | exit 0; one handler each; every binding names a scenario | same |
| `tools size --limit 300` | silent | silent, exit 0 (`conversation_quote.py` 227) |
| `tools check` on the changed Python | clean | ruff and vulture clean; no import contracts |
