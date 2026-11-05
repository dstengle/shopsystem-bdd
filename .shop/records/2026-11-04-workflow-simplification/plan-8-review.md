# Plan 8 of the workflow simplification: end-of-branch review

This is the review of plan 8 (conversation and names), range `eebf9bfd..c044abc0` on `workflow-simplification`. One
fresh reviewer did it on 2026-11-05 and read:
- `plan-8-conversation.md`: its Review Focus, Global Constraints and D1-D16;
- `plan-8-implementation.md`, with its 11 deviations;
- `design.md` goals 9 and 10, and the rulings of plans 1-7;
- `CLAUDE.md`, `hooks/hooks.json`, the five `conversation_*` modules, `scripts/work`'s change,
  `skills/shaping-items/SKILL.md`, the conversation tests and the helper `transcript_testing.py`.

The reviewer changed nothing in the repository except this file, which is not committed. The probes ran in
`/home/vscode/.claude/jobs/7e9ba079/tmp/review8/`, on synthetic transcripts written by `probe/mk.py`. No real
transcript content is copied here. The real store was read only for counts of row shapes: row types, the tag a
person-row's text starts with, and `origin.kind`.

## Verdict

**Approve, after one blocking fix (B1) and two should-fix changes (S1, S2).**

Every verification figure in the report reproduces. The quote file round-trips through `render`/`parse` for every
tricky text tried. Both hooks exit 0 and stay silent in every failure case the plan lists. Both run well under 1 s.
`work show quote-<n>` and `work names` do what D7 and D8 say.

The gaps are all in what D2 counts as "the person's message". Each one is a shape of row the plan did not list, so
the implementer followed the plan. Real transcripts carry these shapes often enough to matter:
- **`<task-notification>` rows** are background-task and subagent completion notices, injected as `user` rows. The
  person's real store holds 1,102 of them, against 629 prompts the person typed. They are read as the person's
  messages, so a quote can commit a background command's or subagent's output (B1).
- **`!` bash-mode rows** (`<bash-input>` / `<bash-stdout>`) and the `[Request interrupted by user…]` marker are read as
  the person's messages too (S1, M1).

Separately, the two new hook commands run all of `scripts/work`. Its imports pull in `pytest` and `clingo`, so under a
`python3` without them each hook exits 1 with a traceback on every prompt and every session start. The `migrate`
hooks beside them have no such dependency (S2).

## Verification (the plan's exact invocations)

| Check | Report | Got |
|---|---|---|
| Task 8 Step 1 (unbuilt) | `{} 0 []` | `{} 0 []` |
| `python3 -m pytest -q \| tail -2` | 1553 passed, 1 skipped, 0 xfailed, 135 subtests (31.7 s); ceiling `test_e2e_codified` 13.3 s | 1553 passed, 1 skipped, 135 subtests passed (30.9 s); ceiling `test_e2e_codified` 12.9 s |
| `python3 -m pytest -m timing -n 0 -q` | 4 passed, 1554 deselected (6.8 s) | 4 passed, 1554 deselected (6.86 s) |
| `model check` | 53 / 16 / 19 / 0 | 53 violations, 16 warnings, 19 unresolved references, 0 file problems |
| `model logic` | 11 findings: 6 L5, 5 L6 | same |
| `model lexicon --check` | 401 terms, 0 problems | same |
| `model decisions --check` | 4 hold, 0 failing | same |
| `features generate --check` | exit 0 | exit 0 |
| `features vocab --check` | every step has one handler | same |
| `features bindings --unbound` | every binding names a scenario | same |
| `tools size --limit 300` | silent; `scripts/work` 219, `conversation_quote.py` 223 | silent, exit 0; 219 and 223 |
| `tools check <changed py>` | ruff, vulture clean; no contracts | same |
| Files the plan says not to change (`measure_read`, `measure_batch_read`, `migrate_session`, `migrate_prompt`, `scripts/migrate`, `backlog_*`, `batch_*`, `workqueue*`, the four scenario modules, `spec/index.md`) | unchanged | `git diff --name-only` over them is empty |
| Spec edits | only `unbuilt:`, r2 in place, Implementation sections, telemetry's price sentence | as reported; the r2 feature diff is g2 only |
| Hook medians (200 items, 20 batches) | prompt 0.11 s, names 0.14 s | quote --hook 0.12 s, names --hook 0.18 s (via `sh -c`); `migrate prompting` 0.06 s |

The smoke run on the real transcript was not repeated, because the record may not carry real content. The mutations
in the report's commit table were not re-run.

## Probes

| Probe | Result |
|---|---|
| Noise rows: thinking, tool_use, tool_result, image, meta, sidechain person and session, `summary`, `file-history-snapshot`, `system` compact_boundary, `isCompactSummary`, `attachment`, `<local-command-stdout>`, `<command-name>` echo, a system reminder inside the prompt | none reaches a message; one turn split over thinking, tool use, result and text is one message |
| `<bash-input>` and `<bash-stdout>` rows | **each a person's message** (S1); the stdout one reached `quote-1` as a message of the person |
| `[Request interrupted by user for tool use]` (a text block beside a tool_result) | **a person's message** (M1) |
| `<task-notification>` (shape from the store: `origin.kind: task-notification`, `promptSource: system`) | **a person's message** by D2's rules (B1) |
| A slash command `/x args` | dropped whole; the session's reply to it joins the session's previous turn (Q1) |
| Words wrapped and spaced differently | match |
| Words in markdown the person wrote (`**bold**`) quoted without the stars | refused, writing nothing (D4 as written) |
| Message text holding `## Messages`, a `### the person, …, cited` line, `---`, `> x`, a ```` ```text ```` fence, a run of 7 backticks, trailing blank lines, U+2028, form feed: written to the file and read back by `work show --json` | identical, **except** `\r\n` came back as `\n` (M2) |
| Two sessions in one checkout | the pointer is the last prompt's; words only in the other session are refused, naming the session searched and `--session` |
| Pointer missing, corrupt JSON, or a directory | refused: "no session is known…" (M3: misleading for a corrupt pointer) |
| Prompt hook: stdin empty, `junk`, `[]`, `3`, `null`, a non-string id, a missing key, invalid UTF-8 bytes, `LC_ALL=C`; in a non-git dir, a repo with no `.shop/`, the scratch repo | exit 0, nothing printed in every case; pointer written only in the repo with `.shop/` |
| Prompt hook when the rename fails (`prompt.json` is a directory) | exit 0, but `.prompt.json.<pid>` is left in the git dir (M4) |
| Names hook: no items; garbage item file; non-UTF-8 item file; malformed `.shop/batches/1/plan.md`; non-git dir; no `.shop/` | exit 0; silent, or `work names: <why>` for a refusal (D8) |
| Names hook output, 200 items and 20 batches | 223 lines, 8,037 bytes (about 2.5k tokens) at every SessionStart (Q2) |
| The hooks.json lines from the install layout: `${CLAUDE_PLUGIN_ROOT}` is the plugin root (`~/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/<version>/`, holding `scripts/` and `hooks/`), quoted, run through `sh -c` | resolve and run under `/usr/local/bin/python3` (3.11, the first on PATH). Under `/usr/bin/python3` (3.13, no site packages) or `python3 -S`, **both exit 1 with a traceback** (`No module named 'pytest'`, then `'clingo'`), while `migrate status --hook` and `migrate prompting` exit 0 (S2) |

## Findings

### B1. blocking: background-task notifications are quoted as the person's words

`scripts/conversation_read.py:35-40` (`_persons`), with the skip rule at `:63`.

**Evidence.** Claude Code writes a finished background task or subagent as a `user` row. Its text is
`<task-notification>…</task-notification>`, its `origin` is `{"kind": "task-notification", …}` and its
`promptSource` is `system`. It is not `isMeta`. D2's rules take any non-meta, non-sidechain `user` text, so each
notification becomes a message of the person.

In this machine's store there are 1,102 such rows, against 629 prompts typed or queued by the person (`origin.kind:
human`). There is also one `auto-continuation` row of the same kind. A notification carries the task's result: a
subagent's summary, or a background command's output.

Within two messages of a cited prompt, a notification is therefore committed into `.shop/quotes/<n>.md` as "the
person". The words can also match inside a notification, which then gets cited. This breaks the Global Constraint "A
quote keeps no tool output … It keeps the words of the person and of the session only", in the person's own workflow,
which dispatches many agents. The smoke run's transcript happened to have none near the quote.

**Fix.**
- In `_persons`, return `""` for a row whose `origin` is a dict with a `kind` other than `human`, and for text starting
  with `<task-notification>`. Keep both rules: older rows have no `origin`.
- Add the `task notification` case (`origin` and the tag) and an `auto-continuation` case to `NOISE` in
  `tests/scripts/test_conversation_read.py`.
- Add the rule to D2's Implementation bullet in `conversation.md` ("…without tool uses, tool results, thinking,
  reminders or notifications").

### S1. should fix: `!` bash-mode input and output are the person's messages

`scripts/conversation_read.py:14` (`COMMAND`).

**Evidence.** A probe row `<bash-stdout>…</bash-stdout><bash-stderr></bash-stderr>` reached `quote-1` as `### the
person`. The store has 5 `<bash-input>` and 5 `<bash-stdout>` rows. The stdout is a command's output, which is tool
output in all but name.

**Fix.**
- Add `"<bash-"` to `COMMAND`, which covers `<bash-input>`, `<bash-stdout>` and `<bash-stderr>`.
- Add both to `NOISE`.

### S2. should fix: the hooks need `pytest` and `clingo` in whatever `python3` the hook runs

`hooks/hooks.json:12,26` run `scripts/work`. `scripts/work:12-24` imports `batch_cli` and the rest at module level.
The chain runs `batch_cli → batch_close → batch_tasks → spec_unbuilt`, which has `import pytest` at
`scripts/spec_unbuilt.py:10`. It also runs `batch_review → … → readiness_bar → features_generate → spec_steps →
spec_steps_facts`, which has `import clingo` at `scripts/spec_steps_facts.py:9`.

**Evidence.** `env -i PATH=/usr/bin:/bin … /usr/bin/python3 "${CLAUDE_PLUGIN_ROOT}/scripts/work" quote --hook` gives
a traceback and exit 1, and so does `names --hook`. Under `python3 -S`, the same happens, with pytest stubbed and then
clingo. `migrate status --hook` and `migrate prompting` exit 0 under both.

The `try`/`except` in `conversation_prompt.keep` and `conversation_names.hook_text` cannot help, because the failure
is at import. A person whose `PATH` finds a bare `python3` first, for example a project venv that is not activated,
gets a hook error on every prompt and every session start. That breaks the Global Constraint "always exit 0". The full
`work` import also costs about 0.1 s of each prompt's 0.12 s.

**Fix.**
- Give the two hooks a slim entry point, for example `scripts/conversation_hook`. It puts its directory on `sys.path`,
  imports only `conversation_prompt` or `conversation_names`, and runs `keep`/`hook_text` inside one `try` that exits 0
  whatever happens.
- Point hooks.json's two commands at it, keeping the subcommand words so that `hook_command(event, sub)` still finds
  them: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conversation_hook" quote` and `… names`.
- Keep `work quote --hook` and `work names --hook` as aliases.
- Add a test that runs each hooks.json command with `python3 -S` (no site packages) and asserts exit 0 and empty
  stderr.

An import-guard alternative also works: make `spec_unbuilt` import `pytest` inside `mark()`. It still leaves `clingo`
on the path, and it is slower.

### Minor

- **M1. `[Request interrupted by user]` and `[Request interrupted by user for tool use]` are the person's messages.**
  Claude Code writes these, not the person (17 in the store), and each takes one of the 2+2 slots around a quote.
  Fix: in `_persons` (`conversation_read.py:40`), drop text that starts with `[Request interrupted by user`. Add a
  `NOISE` case.
- **M2. `\r` does not survive the file.** `render` writes `\r\n` from a message's text as is. `find` reads the file
  through `workqueue.read` (`path.read_text`, universal newlines; `conversation_quote.py:67`), so `\r\n` comes back as
  `\n`. D3's "whatever its text holds" holds in memory only: `test_a_quote_reads_back_whatever_its_text_holds` calls
  `parse(render(q))` and never goes through a file. Fix: normalise `\r\n` and `\r` to `\n` in `conversation_read` when
  a message is made, so that what is rendered is a fixed point. Add a `"a\r\nb"` case that writes and reads the file.
- **M3. A corrupt or unreadable pointer is refused as "no session is known".** `conversation_prompt.kept` returns
  None for it (`conversation_prompt.py:150-153`), the same as for no pointer at all
  (`conversation_quote.py:168-174`). Fix: have `kept` tell "none" from "unreadable", and refuse as `the pointer <path>
  the UserPromptSubmit hook keeps cannot be read; give --session <id>`.
- **M4. A failed rename leaves `.prompt.json.<pid>` in the git dir** (`conversation_prompt.py:138-143`). This happens
  when `prompt.json` is a directory (probed), on a full disk, or on a permission error. Fix: in the `except`, unlink
  `part` with `missing_ok=True`.
- **M5. `ident` falls back to `<absolute transcript path>:<line>`** (`conversation_read.py:70,74`). That would commit
  the person's home path in a quote's frontmatter. No real person-row lacks a `uuid` (0 of 2,452 typed or SDK
  prompts), so this is theory today. Fix, if wanted: use `<file name>:<line>`.
- **M6. The skill's refusal advice says "give `--session <id>` for an earlier session"**
  (`skills/shaping-items/SKILL.md:24`), but nothing tells the session how to find an earlier session's id. Fix: say
  "or give `--transcript <path>` of the session it was said in", or drop the clause.

## The implementer's 11 deviations

| # | Deviation | Judgment |
|---|---|---|
| 1 | A session message takes its ident and time from its first row with text | **Right.** D2's "its first row" would make the ident a tool row's uuid, which names no text. |
| 2 | Line numbers computed beside `json_rows` (two reads) | **Right**, given that `measure_read.py` may not change. `zip(strict=True)` holds because both skip the same blank lines. The second read costs nothing measurable at quote time. |
| 3 | Script tests use conftest's `backlog_repo` | **Right**: the same context, and less fixture code. |
| 4 | Refusals print `work quote:` / `work show:` | **Right**: D4 and D7 word them so. |
| 5 | Registry handlers where no other capability claims the key | **Right**: `features vocab --check` reads only the registry, so locals alone would leave steps unhandled. |
| 6 | `hook_command` and `crowded()` live in `transcript_testing.py` | **Right**: shared by the script tests and the scenario handlers. |
| 7 | The r2 scenario repository gets a committed `.shop/README.md` | **Right**: D5 keeps nothing without `.shop/`. |
| 8 | r4's batch is written with `batch_plan.render` | **Right**: `work names` reads only files. The batches world would build an origin and branches for nothing. |
| 9 | A conversation-local `ThenPrints item` chained over backlog's | **Right**: backlog's handler reads a `work backlog` row, whose shape differs. `backlog_handlers.py` stays unchanged, as the constraint asks. |
| 10 | The names timing test asserts 222 table lines | **Right**: header, separator and 220 rows is 222, so the plan miscounted. With `HOOK_LINE`, the hook prints 223 lines, as probed. |
| 11 | Added `test_hook_takes_no_words`, `test_a_batch_of_a_missing_item_names_it_missing`, and the `--transcript` not-a-file check | **Right**: each pins behaviour D5, D8 or the CLI states. |

D1-D16 are kept as the report says. The probes confirm D3-D5, D7, D8 and D10. D2 is kept to the letter, and B1, S1
and M1 are gaps in D2's list rather than departures from it.

## Questions for the person (the person is unavailable; rulings recommended)

- **Q1. Is a slash command with arguments the person's message?** Today a `/name args` row (`<command-name>` /
  `<command-args>`) is dropped whole (`conversation_read.py:40`). Two things follow:
  - the person's words in `args` cannot be quoted;
  - the session's reply to the command joins the session's previous turn, which misattributes it.

  **Recommended ruling: yes.** Read a row whose text holds `<command-name>` as the person's message
  `/<name> <args>`, from the two tags. Keep `<local-command-stdout>` and the meta skill expansion out. Add a test that
  `/brainstorm keep the turns` is quotable by "keep the turns", and that the reply starts a new session message.
- **Q2. Should the SessionStart table list every item, closed ones included?** r4 says "every item". At 200 items the
  hook injects about 8 KB (about 2.5k tokens) at each start, resume, clear and compaction. That is a cost goal 10's
  "rather than wasting tokens" may not intend. **Recommended ruling: keep r4 as built for plan 8.** Have plan 9 measure
  the table on this repository's real backlog. If it passes about 50 rows, retire r4 for a line that names the items
  not `delivered` or `withdrawn` and the batches not `merged` or `abandoned`. `work names` without `--hook` keeps the
  full table.
- **Q3. Two sessions in one checkout.** The pointer is the last prompt's (D5, an open problem in the report). A
  `claude -p` session started in the main checkout also moves it. That includes any `promptSource: sdk` session, of
  which the store holds 1,822 prompts. **Recommended ruling: accept for now.** The refusal names the session searched
  and `--session`, so a wrong pointer never writes a wrong quote unless the words are in both transcripts. Have the
  hook ignore stdin whose `cwd` (given in the hook's JSON) is not inside the top level, at no extra cost.

## Files

- Reviewed: `scripts/conversation_read.py`, `conversation_quote.py`, `conversation_cli.py`, `conversation_prompt.py`,
  `conversation_names.py`, `scripts/work`, `scripts/measure_cost.py`, `hooks/hooks.json`, `CLAUDE.md`, `README.md`,
  `skills/shaping-items/SKILL.md`, `spec/capabilities/conversation.md`, `brainstorming.md`, `telemetry.md`,
  `tests/scripts/test_conversation_*.py`, `transcript_testing.py`, `test_skill_shaping_items.py`,
  `test_measure_cost.py`.
- Probes: `/home/vscode/.claude/jobs/7e9ba079/tmp/review8/` (`probe/mk.py`, `repo/`, `crowd/`, `store/`, `nogit/`,
  `noshop/`). These are left in place, including the leftover `.prompt.json.<pid>` of M4 in `repo/.git/shopsystem/`.
