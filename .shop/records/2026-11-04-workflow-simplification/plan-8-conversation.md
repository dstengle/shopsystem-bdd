---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-8
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: draft
---

# Plan 8: Conversation and names — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `conversation` capability and brainstorming r3, so that no id is left in any `unbuilt:`. The
plan builds four things:
- `work quote "<the person's words>"` copies the person's message with the two messages before it and the two after
  it (the person's and the session's words, no tool output) into `.shop/quotes/<n>.md`, and commits it (r1).
- The UserPromptSubmit hook runs `work quote --hook`, which keeps the session and its transcript for `work quote`
  (r2, a line plan 1 left weak, strengthened in place).
- `work show quote-<n>` prints a quote's messages (r3).
- The SessionStart hook runs `work names --hook`, a table of every item and every batch with its name beside its id
  (r4).

The shaping-items skill then quotes with `work quote` (brainstorming r3).

The plan's first task makes two fixes left over from plan 7:
- `CLAUDE.md`'s row for `scripts/batch_findings.py` names the findings file as `pr-reviewer`'s reply, saved by the
  batch session (plan-7 rulings, "Not done here").
- `claude-sonnet-4` no longer prices every Sonnet 4 at Sonnet 4.6's rate. Only what the claude-api skill's table
  lists is priced (plan-7 M3's rule).

**Architecture:**
- **Messages are read from Claude Code's transcript on disk (D2).** `scripts/conversation_read.py` reads one session's
  `<session>.jsonl` through `measure_read.json_rows` and `moment`, so an unknown shape is refused naming the file
  and line (0018). It keeps only the person's prompts and the session's text. It drops tool uses, tool results,
  thinking, meta rows, system reminders, sidechain rows, compaction summaries and local-command rows. It never
  reads a subagent's transcript. The `measure_*` modules are not changed and still read no message text.
- **A quote is a committed file (D3, D4).** It lives at `.shop/quotes/<n>.md` and is named `quote-<n>`. Its
  frontmatter holds the session id and the cited message's id (its turn). The body holds the words, then the five
  messages, each in a fence longer than any backtick run in its text, so that `parse(render(q)) == q` whatever the
  text holds. `work quote` commits only that file, on the current branch (`workqueue.committed`).
- **The prompt hook keeps a pointer and prints nothing (D5).** `work quote --hook` reads the hook's stdin JSON
  (`session_id`, `transcript_path`) and writes `<git dir>/shopsystem/prompt.json`. The git dir is per worktree and
  never tracked. Nothing is committed, the session's context gets no tokens, and the hook always exits 0. `work quote`
  with no `--session` or `--transcript` reads that pointer.
- **The names table is the SessionStart hook's second command (D8).** `work names --hook` prints the table, with one
  line telling the session to name things by their names. It prints nothing when there is no item and no batch,
  and always exits 0.
- **New modules** (each ≤ 300 lines):
  - `scripts/conversation_read.py`, `conversation_quote.py`, `conversation_prompt.py`, `conversation_names.py`,
    `conversation_cli.py`;
  - `tests/scenarios/conversation_handlers.py`;
  - `tests/scripts/transcript_testing.py` and four test modules.
- **How each line is met:**

  | id | line (short) | met by | checked by |
  |---|---|---|---|
  | conversation r1 | a session runs `work quote` → a quote from the session citing a message, committed | `conversation_quote.write`, `conversation_cli.quote` | scenario @r1; Task 3 tests |
  | conversation r2 | the UserPromptSubmit hook runs `work quote --hook` → `work` keeps the session | `conversation_prompt.keep`, hooks.json | scenario @r2; Task 4 tests |
  | conversation r3 | `work show` on a quote → every message it cites printed | `conversation_cli.show` | scenario @r3; Task 5 tests |
  | conversation r4 | the SessionStart hook runs `work names` → every item, its title, every batch | `conversation_names.table`, hooks.json | scenario @r4; Task 6 tests |
  | brainstorming r3 | the brainstorming session writes a quote with `work quote` | `skills/shaping-items/SKILL.md` | `test_r3_…` in `test_skill_shaping_items.py`, Task 7 |

  `conversation` is a `service` capability with a generated feature. Each id leaves `unbuilt:` in the commit that
  makes its scenario pass, which the strict xfail enforces (plan-1 P6). `brainstorming` is `guarantees`, with no
  feature. Its r3 leaves `unbuilt:` in the commit that adds its test, and a trace test holds that rule (D14).

**Tech Stack:** Python 3.11, standard library only (`json`, `re`, `subprocess`, `dataclasses`, `datetime`), git,
pytest with xdist and pytest-bdd.

**Spec:**
- Read first: `spec/capabilities/conversation.md` (4 lines; the relation `message cited by quote`; the term "the
  UserPromptSubmit hook").
- The glossary of `spec/index.md`:
  - `quote` ("the person's words cited by a file, with its session, its message and the messages around it");
  - `message` ("one turn of the person or of a session in a transcript, without its tool uses");
  - `session`, `item`, `batch`;
  - the rows `quote from session` (one) and `quote cites message`.
- `spec/capabilities/backlog.md`: the `title` kind and its row `title of item`. `migration-tools.md`: "the SessionStart
  hook".
- `spec/capabilities/brainstorming.md` (r3 and its `## Not yet`).
- `design.md` goals 9 and 10. Its § "Decided by the person after the builder check" says that conversation turns are
  committed and that a quote keeps its session id and turn. § "Left to the builder" leaves how the conversation hook
  stores the session and turn of a quote to the builder.
- `recon.md` § "Quotes, transcripts, ids": `migrate_prompt.py` drops the hook's stdin, and nothing expands ids to
  names.
- Read beside them:
  - `plan-1-rulings.md`: P10 (lines never merged may be fixed in place), M3 (conversation r2's flags have no
    values), and the gap "conversation g4 uses an item it never sets up";
  - `plan-3-rulings.md` "For plan 4", last bullet, and `plan-3-review.md` ruling 12: the skill names `work quote`
    only in words;
  - `plan-7-rulings.md` M3 and "Not done here".

## Global Constraints

- **Branch:** `workflow-simplification`, from `a7aeb4c2` or later. Every plan is built on this one branch. No new
  branch, no push.
- **Shell rule (the person's):** never combine `cp` and `rm` in one command, since together they need the person's
  approval. Run them as separate commands, or leave scratch directories under
  `/home/vscode/.claude/jobs/7e9ba079/tmp`. Keep shell variables few.
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
  - `scripts/work` (213) may grow to at most 225: one import, the `quote-<n>` route in `cmd_show`, and
    `conversation_cli`'s parsers and `COMMANDS` merged in, as `backlog_cli`'s are.
  - These are not changed: `scripts/measure_read.py`, `measure_batch_read.py`, `migrate_session.py`,
    `migrate_prompt.py`, `scripts/migrate`, and every `backlog_*.py`, `batch_*.py` and `workqueue*.py`.
  - These scenario modules are not changed: `tests/scenarios/backlog_handlers.py`, `batches_handlers*.py`,
    `work_queue_handlers.py` and `world_nodes.py`. Conversation's steps that share a key with them go through
    `work_queue_world.local` (D13).
- **Module map:** each task that creates a module adds its `CLAUDE.md` row in the same commit (rows given per task).
  Task 4 rewrites the `hooks/hooks.json` row, and Task 6 rewrites it again. Task 3 adds `conversation` to the
  `tests/scenarios/<capability>_handlers*.py` row.
- **Spec:** these are the only spec edits:
  - `conversation.md`:
    - `unbuilt:`, ids taken out one per task;
    - r2's text, edited in place in Task 4. The file was written by plan 1 and has never been merged to `main`
      (plan-1 P10), and plan-1 M3 asks the plan that builds r2 to strengthen it;
    - its `## Implementation, may change`.
  - `brainstorming.md`: `unbuilt:` and its `## Not yet`, both in Task 7.
  - `telemetry.md`: the one Implementation sentence on prices, in Task 1.

  No other line, group, term or relation row is edited or added. A line found wrong is reported, not changed.
- **The glossary is not edited.**
- **The strict xfail:** a conversation id leaves `unbuilt:` in the same commit that makes its scenario pass, never
  before and never after.
- **Hooks never fail a session.** `work quote --hook` and `work names --hook` always exit 0. Neither writes a tracked
  file or makes a commit. Each prints nothing when the repository has no `.shop/`, is not a git repository, or has
  nothing to say. `work quote --hook` prints nothing at all. Each finishes in under 1 s on a repository of 200 items
  and 20 batches; the `timing` tests in Tasks 4 and 6 check this.
- **A quote keeps no tool output.** It keeps no tool use, tool result, thinking, system reminder, meta row or
  subagent row (D2). It keeps the words of the person and of the session only.
- **No network, no claude in the suite.** No test reaches a network, starts a session, or reads the person's
  `~/.claude`. Every test that reads a store sets `CLAUDE_CONFIG_DIR` to a directory of its own.
- **Names next to ids:** an item is printed with its label (`b1 "Abandon"`), a quote as `quote-<n> "<its words, cut
  at 60 characters>"` (design goal 10).
- **Old behaviour kept:** every test of plans 1-7 passes unchanged; Task 1 only adds price tests. That includes `migrate prompting` (requests r72) and `migrate status --hook`, which stay as the
  first command of their hooks until plan 9.
- **Commits** end with the attribution lines the session's harness gives.
- **Baselines** (measured at `a7aeb4c2` on this machine). Each task's expected figures are given in the task, and any
  change from these is planned there:
  - `python3 -m pytest -q`: `1481 passed, 1 skipped, 4 xfailed, 135 subtests passed` (30.2 s wall). The 4 xfailed
    are conversation r1-r4. The ceiling report lists `test_e2e_codified` (13.1 s) and `test_supervision`'s
    flaky-scenario test (11.5 s), as before.
  - `python3 -m pytest -m timing -n 0 -q`: `2 passed, 1486 deselected` (5.7 s).
  - Unbuilt ids (`spec_unbuilt.unbuilt`): 5, with no problems: brainstorming r3 and conversation r1-r4. At the end
    there are none.
  - `python3 scripts/model check | tail -1`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
  - `python3 scripts/model logic | tail -1`: `11 findings: 6 L5, 5 L6`.
  - `python3 scripts/model lexicon --check | tail -1`: `401 terms, 0 problems`.
  - `python3 scripts/model decisions --check | tail -1`: `4 check decisions: 4 hold, 0 failing`.
  - `python3 scripts/features generate --check`: exit 0.
  - `python3 scripts/features vocab --check | tail -1`: `every step has one handler`.
  - `python3 scripts/features bindings --unbound`: `every binding names a scenario`.
  - `python3 scripts/tools size --limit 300`: silent, exit 0.
  - `python3 scripts/tools check <the branch's changed Python>`: ruff and vulture clean. import-linter states no
    contracts.
  - Hook cost today: `python3 scripts/work --help` takes 0.16 s wall, `migrate status --hook` 0.37 s and `migrate
    prompting` 0.07 s.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-05;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Built and committed on `workflow-simplification`, as the main session ruled for every plan. |
| D2 | **What a message is** (`conversation_read.messages(path)`), read from one session's transcript in file order:<br>- **The person's message:** a row with `type` `user` that is not `isMeta`, `isSidechain` or `isCompactSummary`. Its text is `message.content` when it is a string, else its `text` blocks joined by a blank line. `tool_result`, `image` and other blocks are dropped. Every `<system-reminder>…</system-reminder>` span is removed, and the text is stripped. Empty text is not a message. Text that then starts with `<command-` or `<local-command-` (a slash command's echo or its output) is not a message either.<br>- **The session's message:** the `text` blocks of every `assistant` row that is not `isSidechain`, from one message of the person to the next, joined by a blank line. That is one turn. `thinking` and `tool_use` blocks are dropped, and a turn with no text is not a message.<br>- **Each message** has `ident` (the `uuid` of its first row, else `<file>:<line>`), `who` (`"person"` or `"session"`), `at` (its first row's `timestamp`, via `measure_read.moment`) and `text`.<br>- **Every other type** (`system`, `attachment`, `summary`, `queue-operation`, …) is skipped. A row with no `type` is refused naming the file and line (0018). |
| D3 | **The quote file.** `.shop/quotes/<n>.md`, named `quote-<n>`, n one more than the highest. Frontmatter: `id: quote/<context path>/quote-<n>` (`workqueue.context_path`), `kind: quote`, `session: <id>`, `message: <cited ident>`, `date: <the cited message's UTC date>`. Body: `# quote-<n>`, a blank line, the words as `> ` lines, then `## Messages`. Each message is `### <the person\|the session>, <ISO time>, <ident>`, with `, cited` added to the cited one, then its text in a fence of backticks one longer than the longest backtick run in it (at least 3), tagged `text`. `parse(render(q), rel) == q`, and any other shape is refused as `<rel>: <field> …`. |
| D4 | **Which messages.** The words are matched with whitespace collapsed to one space, case kept, against the person's messages only. The newest one that contains them is cited. With it come `AROUND = 2` messages before and 2 after, of either side, as many as exist. A message other than the cited one is cut at `LIMIT = 2000` characters with ` […]` appended. The cited message is kept whole.<br>**Refusals, each writing nothing:**<br>- empty or whitespace-only words: `work quote: the words are empty`;<br>- words in no message of the person: `work quote: the person wrote no message with "<the first 40 characters>" in the session <id>; quote their words as they wrote them, or give --session <id>`. |
| D5 | **The session and transcript.** `work quote --hook` reads the hook's stdin JSON and writes `{"session": <session_id>, "transcript": <transcript_path>, "at": <now, ISO>}` to `<git rev-parse --absolute-git-dir>/shopsystem/prompt.json`, by writing a temporary file and renaming it over. It does so only when the top level (`migrate_write.top_level(Path.cwd())`) has a `.shop/` directory. Anything else (stdin not JSON, a key missing or not a string, no git, no `.shop/`, an `OSError`) writes nothing. It prints nothing and exits 0.<br>`work quote "<words>"` finds the transcript in this order:<br>1. `--transcript <path>`, with the session `--session` or else the `sessionId` of its first row that has one;<br>2. `--session <id>` alone: the first of `sorted(store_dir()/"projects"/*/<id>.jsonl)`;<br>3. the pointer.<br>With none of them it is refused: `work quote: no session is known: the UserPromptSubmit hook keeps it (work quote --hook), or give --session <id>`. A transcript path that is not a file is refused, naming it. |
| D6 | **`work quote` prints** the quote's label, `quote-<n> "<its words, cut at 60 characters with …>"`, and commits `.shop/quotes/<n>.md` alone as `quote: quote-<n> from the session <first 8 characters of the id>`. It takes no item: the session cites `quote-<n>` in the item's note (Task 7). |
| D7 | **`work show quote-<n>`** prints the label, then `  session: <id>`, `  date: <date>`, then each message as `\n<the person\|the session>, <time>[, cited]:\n<text>`. With `--json` it prints `{"quote": {"name", "session", "message", "date", "words", "messages": [{"who", "at", "ident", "cited", "text"}]}}`. A quote with no file is refused: `there is no quote quote-9 in .shop/quotes/`. `scripts/work`'s `cmd_show` routes a target of the form `quote-<n>` to `conversation_cli.show`. |
| D8 | **`work names`** prints one table, items by number and then batches by number:<br>`\| id \| name \| status \|`<br>`\|---\|---\|---\|`<br>`\| b1 \| Fix the parser \| shaped \|`<br>`\| batch-1 \| b1 "Fix the parser", b2 "Exit" \| building \|`<br>A batch's name is the labels of its tasks' items. An item that is missing is shown as `b9 (missing)`. Cells are escaped with `backlog_view.cell`. With nothing to show, it prints `there is no item in .shop/backlog/ and no batch in .shop/batches/`.<br>**`--hook`** prints nothing when there is nothing to show. Otherwise it prints the line `The names of this repository's items and batches: tell the person each by its name beside its id (b3 "Fix the parser"), never by its id alone.`, then the table. A `Refused` (for example a malformed item file) prints `work names: <why>` and exits 0. Any other exception prints nothing and exits 0. It runs at the top level of the cwd's repository. |
| D9 | **The hooks.** `hooks/hooks.json` keeps its commands and gains two. `SessionStart`'s `hooks` list gets `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/work" names --hook` after `migrate status --hook`. `UserPromptSubmit`'s list gets `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/work" quote --hook` after `migrate prompting`. `migrate_prompt.py` and `migrate_session.py` are not changed: plan 9 retires their initiative and request text. |
| D10 | **r2 is reworded in place** (plan-1 P10 and M3). From `When the UserPromptSubmit hook runs \`work quote --session --transcript\`, \`work\` shall write a quote from a session.` to `When the UserPromptSubmit hook runs \`work quote --hook\`, \`work\` shall keep the session.` Its group title and the term "the UserPromptSubmit hook" are kept. The planner checked the line in a scratch copy: it parses, `features generate` changes only g2 (`When the UserPromptSubmit hook runs \`work quote --hook\`` / `Then \`work\` keeps the session s1`), `model logic` stays `11 findings: 6 L5, 5 L6`, and `model check` stays 53/16/19/0. The old r2 promised a quote on every prompt, and a commit on every prompt is not wanted. |
| D11 | **r4 keeps its text.** The hook runs `work names --hook`, which is `work names` with its hook flag. The scenario runs the command hooks.json gives (D13), so the line and the wiring cannot drift apart. |
| D12 | **The conversation's `## Implementation, may change`** is rewritten to say D3-D9 in one sentence each. The bullets are written by the tasks that build them. |
| D13 | **Scenario handlers** live in `tests/scenarios/conversation_handlers.py`, bound with `bind_all` (as `test_backlog.py` binds).<br>- The store is `CLAUDE_CONFIG_DIR=<the scenario's outside dir>/store`. Transcripts are written there by `tests/scripts/transcript_testing.py` (Task 2), under `measure_batch_read.project_dir(<repo>)`.<br>- The hook Whens run the command that `hooks/hooks.json` gives for their event and subcommand (`hook_command(event, sub)`). `${CLAUDE_PLUGIN_ROOT}` is replaced by the repository's root and the result `shlex.split`, then run in the scenario repository with the hook's stdin JSON.<br>- New registry keys: `WhenRuns` `` `work quote` ``, `` `work quote --hook` ``, `` `work names` ``; `GivenK` `message`, `quote`.<br>- Locals, each returning `False` unless `step.context.get("conversation")` (set by every conversation When and Given): `ThenDoes` `quote` (`write`, `commit`), `ThenR` `quote` (`from`, `cites`), `ThenDoes` `session` (`keep`), `GivenR` `message` (`cited by`), `WhenRuns` `quote` (`` `work show` ``), `ThenPrints` `message`, `ThenPrints` `batch`.<br>- r4's item and title Thens are backlog's own `ThenPrints item`, `ThenPrints title` and `ThenR title`: the `work names` When leaves `step.context["result"]` and `["items"]` as backlog's `work backlog` When does.<br>`features vocab --check` names any step left without exactly one handler. |
| D14 | **brainstorming r3's test.** `test_r3_a_quote_is_written_with_work_quote` reads the shaping-items skill. Step 1 names `` `work quote` `` before `work shape`, and its note cites `quote-<n>`. The words "Until `work` keeps quotes" are gone. `test_the_skills_name_only_commands_work_has` passes with `quote` now among `work`'s commands, so plan-3 ruling 12's exemption is not needed. A trace test, `test_each_built_brainstorming_line_has_its_test`, holds the strict-xfail rule for this guarantees capability: each brainstorming id out of `unbuilt:` has a `test_r<n>_…` in `test_skill_shaping_items.py`, and each id in it has none. |
| D15 | **Prices (Task 1).** `claude-sonnet-4` becomes `claude-sonnet-4-6` (3, 15, 0.30), and `claude-haiku-4` becomes `claude-haiku-4-5` (1, 5, 0.10). Those are the Sonnet 4 and Haiku 4 that the claude-api skill's table lists (`shared/models.md`, read 2026-11-05: Sonnet 4.6 at $3/$15, Haiku 4.5 at $1/$5). Any other Sonnet 4 (4.0, 4.5) or Haiku 4 is unpriced and named, never guessed, as plan-7 M3 did for Opus 4. `AS_OF` stays `2026-10-06`, since no price changed. |
| D16 | **No new decision file.** The person already decided that turns are committed (design § "Decided by the person"). Where they are kept is implementation, written in conversation's Implementation section. |

## Review Focus

These are the input classes the spec implies but no line's check exercises, most likely to bite first. Each has its
test in the task named.

1. **A real transcript's noise.** Tool results arrive as `user` rows, and an assistant turn is split over many rows
   of thinking, tool use and text. The transcript also holds system reminders inside the person's text, meta rows,
   a compaction summary, a slash command's output and subagent rows. None of these may reach a quote, and the
   session's text of one turn must be one message.
   Pinned in Task 2: `test_only_the_words_are_messages` (parametrised over each kind of row),
   `test_a_turn_split_over_rows_is_one_message`, `test_system_reminders_are_cut_from_the_persons_text`.
2. **Words that do not match cleanly.** Words that were wrapped or spaced differently, words that appear in two
   messages of the person, words that appear only in the session's message, and empty words. The first matches, the
   second cites the newest, and the third and fourth are refused, writing nothing.
   Pinned in Task 2: `test_whitespace_does_not_stop_a_match`, `test_the_newest_message_is_cited`,
   `test_the_sessions_words_are_not_the_persons`; Task 3: `test_a_quote_that_matches_nothing_writes_nothing`.
3. **A hook that fails or is slow.** Stdin that is not JSON or lacks a key, a cwd outside git, a repository with no
   `.shop/`, a malformed item file, an unwritable git dir. Each must exit 0 and change no tracked file, and each hook
   must finish in under 1 s on a large backlog.
   Pinned in Task 4: `test_the_prompt_hook_never_fails` (parametrised), `test_the_prompt_hook_is_fast` (timing);
   Task 6: `test_the_names_hook_never_fails` (parametrised), `test_the_names_hook_is_fast` (timing).
4. **Message text that looks like the file's own syntax.** A message holding `## Messages`, `### the person`, a
   ```` ``` ```` fence, `---` or `> ` lines must come back unchanged from the file.
   Pinned in Task 3: `test_a_quote_reads_back_whatever_its_text_holds` (parametrised).
5. **The wrong session.** Two sessions in one checkout leave the pointer at the last prompt's session. The words
   are then not in its transcript: the refusal names the session searched and `--session`, and `--session <id>`
   finds the other one. A pointer whose transcript is gone is refused, naming the path.
   Pinned in Task 4: `test_the_pointer_is_the_last_prompts_session`, `test_a_stale_pointer_is_refused_naming_its_path`;
   Task 3: `test_a_session_is_found_by_its_id_in_any_project`.

---

### Task 1: Two fixes left by plan 7

**Files:**
- Modify:
  - `CLAUDE.md`, the `scripts/batch_findings.py` row: "the findings file `pr-reviewer` writes" becomes "the findings
    file (`pr-reviewer`'s reply, saved by the batch session)";
  - `scripts/measure_cost.py` (D15) and its docstring ("an Opus 4 before 4.6, or a Sonnet 4 or Haiku 4 other than 4.6
    and 4.5, which the table does not state");
  - `spec/capabilities/telemetry.md`, its Implementation sentence: "(an Opus 4 before 4.6, a Sonnet 4 before 4.6
    and a Haiku 4 before 4.5 among them)".
- Test: `tests/scripts/test_measure_cost.py`

**Interfaces:**
- Produces: `measure_cost.PRICES` with the keys `claude-sonnet-4-6` and `claude-haiku-4-5` in place of
  `claude-sonnet-4` and `claude-haiku-4`.

- [x] **Step 1: Write the failing tests.**
  - `test_a_sonnet_4_the_table_states_no_price_for_is_unpriced`, parametrised over `claude-sonnet-4-20250514` and
    `claude-sonnet-4-5-20250929`: `cost(<request with 1,000,000 output tokens>, PRICES) is None`.
  - `test_sonnet_4_6_and_haiku_4_5_are_priced`: 1,000,000 output tokens of `claude-sonnet-4-6` cost 15.0, and of
    `claude-haiku-4-5-20251001` cost 5.0. 1,000,000 cache-read tokens of `claude-sonnet-4-6` cost 0.30.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_measure_cost.py -q | tail -3`
  Expected: the Sonnet 4.0 and 4.5 cases FAIL (`15.0 is not None`). `test_sonnet_4_6_and_haiku_4_5_are_priced`
  already passes.

- [x] **Step 3: Change the two keys, the docstring, the telemetry sentence and the CLAUDE.md row.**

- [x] **Step 4: Run the measure tests.**
  Run: `python3 -m pytest tests/scripts/test_measure_cost.py tests/scripts/test_measure_batch.py tests/scripts/test_measure_batch_show.py tests/scenarios/test_telemetry.py -q | tail -1`
  Expected: all pass. No fixture uses a Sonnet 4 or Haiku 4 id (`grep -rn "sonnet-4\|haiku-4" tests/` finds only
  the new tests).

- [x] **Step 5: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/tools check scripts/measure_cost.py tests/scripts/test_measure_cost.py`
  Expected: `1484 passed, 1 skipped, 4 xfailed`. Generate exits 0: an Implementation sentence changes no scenario.
  `check` is clean.

- [x] **Step 6: Commit.**
  ```bash
  git add CLAUDE.md scripts/measure_cost.py spec/capabilities/telemetry.md tests/scripts/test_measure_cost.py
  git commit -m "measure: only the Sonnet 4 and Haiku 4 the table lists are priced; CLAUDE.md: the findings file is pr-reviewer's reply (plan 7 left-overs)"
  ```

### Task 2: The messages of a transcript

**Files:**
- Create: `scripts/conversation_read.py`, `tests/scripts/transcript_testing.py`,
  `tests/scripts/test_conversation_read.py`
- Modify: `CLAUDE.md`, a row after `scripts/migrate_prompt.py`'s:
  - `scripts/conversation_read.py`: "the messages of a session's transcript: the person's prompts and the session's
    text of each turn, without tool uses, tool results, thinking, reminders, meta or subagent rows; the message a
    quote's words cite and the messages around it (conversation)".

**Interfaces:**
- Consumes: `measure_read.json_rows`, `moment`, `Refused`.
- Produces, in `conversation_read.py`:
  - `@dataclass(frozen=True) Message: ident: str, who: str, at: datetime, text: str` (`who` is `"person"` or
    `"session"`).
  - `messages(path) -> list[Message]` (D2), in file order.
  - `normal(text) -> str`: whitespace collapsed to one space, stripped.
  - `cited(found: list[Message], words: str) -> int | None`: the index of the newest person's message whose
    `normal(text)` contains `normal(words)` (D4).
  - `around(found, index, n=AROUND) -> list[Message]`: `found[index-n : index+n+1]`, clipped at both ends. `AROUND = 2`.
- Produces, in `transcript_testing.py` (test helpers, not a test module):
  - `person(text, uuid, at, session="s-1", **extra) -> dict` and `session_text(text, uuid, at, session="s-1",
    msg="m", **extra) -> dict`: Claude Code's raw rows. `extra` merges in `isMeta`, `isSidechain` and the like.
  - `thinking(…)`, `tool_use(…)`, `tool_result(…)`: rows of those blocks, of the same shape.
  - `write(project, session, rows) -> Path`: `<project>/<session>.jsonl`.
  - `CONVERSATION`: a list of rows giving 6 messages (person, session, person, session, person, session), with a tool
    use and its result inside the second session turn.

- [x] **Step 1: Write the failing tests** (`test_conversation_read.py`, on `tmp_path`).
  - `test_a_conversation_reads_as_its_messages`: `CONVERSATION` gives 6 messages alternating `person`/`session`,
    with `ident`s and texts as written.
  - `test_only_the_words_are_messages` (Review Focus 1), parametrised. Each row is added inside `CONVERSATION` and
    must not change the 6 messages or their texts. The rows are:
    - a `tool_result` user row;
    - a `thinking` and a `tool_use` assistant row;
    - an `isMeta` user row;
    - an `isSidechain` row of each type;
    - an `isCompactSummary` user row;
    - a user row `<local-command-stdout>ok</local-command-stdout>`;
    - a user row `<command-name>/clear</command-name>`;
    - `system`, `attachment` and `queue-operation` rows.
  - `test_a_turn_split_over_rows_is_one_message` (Review Focus 1): 3 assistant rows with the texts `a`, `b`, `c`,
    with a tool use between `b` and `c`, give one session message `a\n\nb\n\nc`.
  - `test_system_reminders_are_cut_from_the_persons_text` (Review Focus 1): the text `Keep this.
    <system-reminder>secret</system-reminder>` reads `Keep this.`. A text that is only a reminder is no message.
  - `test_text_blocks_of_the_person_are_joined`: content `[{"type":"text","text":"a"},{"type":"image"},
    {"type":"text","text":"b"}]` reads `a\n\nb`.
  - `test_a_row_with_no_type_is_refused`: `Refused` naming the file and `:2`.
  - `test_whitespace_does_not_stop_a_match` (Review Focus 2): the words `keep   the\nturns` cite the message `Please
    keep the turns.`
  - `test_the_newest_message_is_cited` (Review Focus 2): two person's messages with `same words`; `cited` gives the
    later index.
  - `test_the_sessions_words_are_not_the_persons` (Review Focus 2): words only in a session's message give `None`.
  - `test_around_is_clipped_at_both_ends`: on 6 messages, `around(m, 0)` has 3 messages, `around(m, 2)` has 5 and
    `around(m, 5)` has 3.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_conversation_read.py -q | tail -3`
  Expected: FAIL with `ModuleNotFoundError: No module named 'conversation_read'`.

- [x] **Step 3: Implement** `conversation_read.py` (D2, D4). It iterates `json_rows(path)` once. A person's message
  closes the open session turn.

- [x] **Step 4: Run them.**
  Run: `python3 -m pytest tests/scripts/test_conversation_read.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: Mutations, each reverted.** Each must turn its test red:
  - keeping `tool_result` text fails `test_only_the_words_are_messages`;
  - one message per assistant row fails `test_a_turn_split_over_rows_is_one_message`;
  - citing the first match fails `test_the_newest_message_is_cited`.

- [x] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/conversation_read.py tests/scripts/transcript_testing.py tests/scripts/test_conversation_read.py`
  Expected: `4 xfailed`, no failures; `size` silent; `check` clean.

- [x] **Step 7: Commit.**
  ```bash
  git add scripts/conversation_read.py tests/scripts/transcript_testing.py tests/scripts/test_conversation_read.py CLAUDE.md
  git commit -m "conversation: the messages of a session's transcript, without tool output, and the one a quote's words cite"
  ```

### Task 3: `work quote` writes and commits a quote (r1)

**Files:**
- Create: `scripts/conversation_quote.py`, `scripts/conversation_cli.py`, `tests/scripts/test_conversation_quote.py`,
  `tests/scenarios/conversation_handlers.py`
- Modify:
  - `scripts/work`: `import conversation_cli`, `conversation_cli.add_parsers(sub)`, `**conversation_cli.COMMANDS`, and
    the docstring's last sentence names `.shop/quotes/` (capability conversation);
  - `tests/scenarios/test_conversation.py`: binds with `bind_all`, like `test_backlog.py`;
  - `spec/capabilities/conversation.md`: `unbuilt: [r2, r3, r4]`, and the Implementation bullets for D3, D4 and D6;
  - `CLAUDE.md`:
    - `scripts/conversation_quote.py` with `scripts/conversation_cli.py`: "`work quote` and `work show quote-<n>`:
      their parsers and dispatch; the quote file `.shop/quotes/<n>.md` (`render`, `parse`), its
      words, session, cited message and the messages around it, written and committed (conversation)";
    - `conversation` added to the handlers row.

**Interfaces:**
- Consumes: Task 2's `messages`, `cited`, `around`, `normal`; `measure_read.store_dir`; `workqueue.context_path`,
  `committed`, `read`, `frontmatter`, `Refused`.
- Produces, in `conversation_quote.py`:
  - `QUOTES = Path(".shop") / "quotes"`, `LIMIT = 2000`.
  - `@dataclass Quote: name: str, ident: str, session: str, message: str, date: str, words: str, messages: list`
    (each entry a `conversation_read.Message`, the cited one the entry whose `ident == message`).
  - `is_quote(name) -> bool` (`quote-[1-9]\d*`), `rel_of(name) -> str`, `names(root)`, `next_name(root)`,
    `find(root, name) -> Quote`.
  - `render(quote) -> str`, `parse(text, rel) -> Quote` (D3).
  - `label(quote) -> str`: `quote-<n> "<words, cut at 60 with …>"`.
  - `transcript_of(root, session, transcript) -> tuple[str, Path]`: D5's order, steps 1 and 2. Task 4 adds step 3.
  - `write(root, words, session=None, transcript=None) -> Quote`: D4 and D6, committed.
- Produces, in `conversation_cli.py`: `add_parsers(sub)` (`quote` with `words` nargs `?`, `--session`,
  `--transcript`; Task 4 adds `--hook`, and Task 6 adds `names`), `quote(args) -> int`, and `COMMANDS = {"quote":
  quote}`.
- Produces, in `conversation_handlers.py`:
  - `store(step) -> Path`: `<outside>/store`; `env(step)` with `CLAUDE_CONFIG_DIR`;
  - `transcript(step, session) -> Path`: `CONVERSATION` written for `session` under
    `project_dir(step.repo)`, recording in `step.context["conversation"]` the session's id and the id of the person's
    message `m1` the words come from;
  - `WhenRuns` `` `work quote` ``: `work quote "<m1's words>" --session <s1's id>`, with `env`;
  - the locals `ThenDoes quote` (`write`: exit 0, a new `.shop/quotes/<n>.md`, bound to the name; `commit`:
    `B.in_commits`) and `ThenR quote` (`from`: frontmatter `session` is s1's id; `cites`: frontmatter `message` is
    m1's id, and its heading ends `, cited`).

- [x] **Step 1: Write the failing script tests** (`test_conversation_quote.py`). The repository is a `git init` with
  `spec/index.md` from `tests/scripts/fixtures/generate/repo`, giving the context `ex.com/prod/ctx`.
  `CLAUDE_CONFIG_DIR` is `tmp_path / "store"`.
  - `test_a_quote_keeps_its_turns`: words from the 3rd of 6 messages give `.shop/quotes/1.md`. It has
    `session: s-1`, the 3rd message's ident and 5 `### ` headings, the 3rd ending `, cited`, and no text of the tool
    use or its result. `work quote` prints `quote-1 "<words>"`, and `git log -1 --name-only` names only
    `.shop/quotes/1.md`.
  - `test_the_next_quote_is_numbered_on`: a second quote is `quote-2`.
  - `test_a_quote_reads_back_whatever_its_text_holds` (Review Focus 4), parametrised over texts holding `##
    Messages`, `### the person, x, y, cited`, ```` ```text ```` with a ```` ```` ```` run, `---`, `> quoted` and a
    trailing blank line: `parse(render(q), rel) == q`.
  - `test_a_long_message_around_the_quote_is_cut`: a 5,000-character session message is kept as its first 2,000
    characters with ` […]` appended. A 5,000-character cited message is kept whole.
  - `test_a_quote_that_matches_nothing_writes_nothing` (Review Focus 2): exit 1, and stderr names the session and the
    first 40 characters. Empty words exit 1 with `the words are empty`. Neither leaves `.shop/quotes/` or a new commit.
  - `test_a_session_is_found_by_its_id_in_any_project` (Review Focus 5): a transcript under
    `store/projects/-other-dir/` is found by `--session`.
  - `test_a_transcript_given_is_read_as_given`: `--transcript <path>` with no `--session` takes the rows' `sessionId`.
  - `test_a_malformed_quote_file_is_refused_naming_its_field`: `kind: note` gives `.shop/quotes/1.md: kind …`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_conversation_quote.py -q | tail -3`
  Expected: FAIL. There is no module `conversation_quote`, and `work` has no subcommand `quote` (exit 2).

- [x] **Step 3: Implement** `conversation_quote.py`, `conversation_cli.py` and the three lines of `scripts/work`.

- [x] **Step 4: Run them.**
  Run: `python3 -m pytest tests/scripts/test_conversation_quote.py tests/scripts/test_conversation_read.py tests/scripts/test_skill_shaping_items.py -q | tail -1`
  Expected: all pass. `test_the_skills_name_only_commands_work_has` still passes: `quote` is now one more choice.

- [x] **Step 5: The r1 handlers; take r1 out of `unbuilt:`.** Switch `test_conversation.py` to `bind_all`.
  Run: `python3 -m pytest tests/scenarios/test_conversation.py tests/scenarios/test_backlog.py tests/scenarios/test_supervision.py tests/scenarios/test_work_queue.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: conversation `1 passed, 3 xfailed`; the others pass as before, since the locals return `False` for
  them; `every step has one handler`.

- [x] **Step 6: Mutations, each reverted.** Each must turn its test red:
  - a fence of a fixed 3 backticks fails `test_a_quote_reads_back_whatever_its_text_holds`;
  - committing before the words are matched (the file written for a quote that matches nothing) fails
    `test_a_quote_that_matches_nothing_writes_nothing`;
  - writing the first message's ident as `message:` fails the r1 scenario's `cites`.

- [x] **Step 7: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/tools size --limit 300; wc -l scripts/work; python3 scripts/tools check scripts/conversation_quote.py scripts/conversation_cli.py scripts/work tests/scripts/test_conversation_quote.py tests/scenarios/conversation_handlers.py`
  Expected: `3 xfailed`, no failures; exit 0; silent; `scripts/work` ≤ 225; clean.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/conversation_quote.py scripts/conversation_cli.py scripts/work tests/scripts/test_conversation_quote.py \
    tests/scenarios/conversation_handlers.py tests/scenarios/test_conversation.py spec/capabilities/conversation.md CLAUDE.md
  git commit -m "work quote: the person's words with the two messages before and after, committed in .shop/quotes/ (conversation r1)"
  ```

### Task 4: The prompt hook keeps the session (r2)

**Files:**
- Create: `scripts/conversation_prompt.py`, `tests/scripts/test_conversation_prompt.py`
- Modify:
  - `spec/capabilities/conversation.md`: r2 reworded (D10), `unbuilt: [r3, r4]`, and the Implementation bullet for
    D5. The old bullet "`work quote --session <id> --transcript <path>` is how the UserPromptSubmit hook passes
    them" goes;
  - `features/conversation.feature`, regenerated (`python3 scripts/features generate`);
  - `hooks/hooks.json` (D9, UserPromptSubmit);
  - `scripts/conversation_cli.py` (`--hook`), `scripts/conversation_quote.py` (`transcript_of`'s step 3);
  - `tests/scenarios/conversation_handlers.py`;
  - `CLAUDE.md`:
    - a row `scripts/conversation_prompt.py`: "the UserPromptSubmit hook's `work quote --hook`: the session and its
      transcript kept in the git dir for `work quote`, never committed, never failing (conversation)";
    - the `hooks/hooks.json` row: "the plugin's hooks: SessionStart (`migrate status --hook`), UserPromptSubmit
      (`migrate prompting`, `work quote --hook`), PreCompact (`migrate compacting`)".

**Interfaces:**
- Consumes: `migrate_write.top_level`.
- Produces, in `conversation_prompt.py`:
  - `POINTER = Path("shopsystem") / "prompt.json"`.
  - `git_dir(root) -> Path | None`.
  - `keep(cwd, stdin_text) -> None` (D5, never raises).
  - `kept(root) -> tuple[str, str] | None`: (session, transcript) of the pointer, or None when there is none or it
    cannot be read.
- `conversation_cli.quote(args)` with `--hook` calls `keep(Path.cwd(), sys.stdin.read())` and returns 0. `--hook`
  given with words is refused: `work quote: --hook takes no words`.
- Produces, in `conversation_handlers.py`:
  - `hook_command(event, sub) -> list[str]` (D13);
  - `WhenRuns` `` `work quote --hook` ``: writes s1's transcript, then runs the hook command with stdin
    `{"session_id": <s1>, "transcript_path": <path>, "hook_event_name": "UserPromptSubmit", "prompt": "x"}`;
  - the local `ThenDoes session` (`keep`): exit 0, stdout empty, `kept(repo) == (s1, path)`, and `git status
    --porcelain` empty.

- [x] **Step 1: Write the failing tests** (`test_conversation_prompt.py`).
  - `test_the_hook_keeps_the_session_for_work_quote`: after `work quote --hook` with that stdin, `work quote
    "<words>"` with no flags writes `quote-1` from `s-1`.
  - `test_the_prompt_hook_never_fails` (Review Focus 3), parametrised over these cases, each exiting 0 with empty
    stdout and stderr, a clean `git status --porcelain` and no pointer:
    - stdin `not json`;
    - `{}`;
    - `{"session_id": 3, "transcript_path": "x"}`;
    - cwd a directory outside git;
    - a repository with no `.shop/`;
    - `<git dir>/shopsystem` a file, not a directory.
  - `test_the_pointer_is_the_last_prompts_session` (Review Focus 5):
    - the hook runs for `s-1` and then `s-2`, so `kept` gives `s-2`;
    - words only in `s-1` are refused, and stderr names `s-2` and `--session`;
    - with `--session s-1` they are quoted.
  - `test_a_stale_pointer_is_refused_naming_its_path` (Review Focus 5): the transcript file is removed, and `work
    quote "<words>"` exits 1 naming the path.
  - `test_no_session_known_is_refused`: with no pointer and no flags, exit 1 naming `work quote --hook` and
    `--session`.
  - `test_the_hook_is_wired`: hooks.json's UserPromptSubmit commands are `migrate" prompting` and `work" quote
    --hook`, in that order.
  - `test_the_prompt_hook_is_fast` (`@pytest.mark.timing`, Review Focus 3): the hook command, run 3 times in a
    repository of 200 item files and 20 batch plans (written with `backlog_items.render` and `batch_plan.render`, one
    commit), has a median under 1.0 s.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_conversation_prompt.py -q -m "timing or not timing" -n 0 | tail -3`
  Expected: FAIL. `work quote` has no `--hook` (exit 2), and there is no module `conversation_prompt`.

- [x] **Step 3: Implement** `conversation_prompt.py`, `--hook`, `transcript_of`'s step 3 and the hooks.json entry.
  The hook reads stdin only when `--hook` is given.

- [x] **Step 4: Reword r2 and regenerate.**
  Run: `python3 scripts/model parse "When the UserPromptSubmit hook runs \`work quote --hook\`, \`work\` shall keep the session."; python3 scripts/features generate && git diff --stat features/; python3 scripts/model logic | tail -1; python3 scripts/model check | tail -1`
  Expected: a tree (`… Do e_keep (k_session_toNP (k_session_The k_session)) …`); only `features/conversation.feature`
  changes, g2 reading `When the UserPromptSubmit hook runs \`work quote --hook\`` / `Then \`work\` keeps the session
  s1`; `11 findings: 6 L5, 5 L6`; `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.

- [x] **Step 5: The r2 handlers; take r2 out of `unbuilt:`.**
  Run: `python3 -m pytest tests/scenarios/test_conversation.py tests/scripts/test_conversation_prompt.py tests/scripts/test_conversation_quote.py -q | tail -1; python3 -m pytest -m timing -n 0 -q tests/scripts/test_conversation_prompt.py | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: conversation `2 passed, 2 xfailed`, the rest pass; `1 passed`, with the median printed under 1.0 s;
  `every step has one handler`.

- [x] **Step 6: Mutations, each reverted.** Each must turn its test red:
  - letting a `json.JSONDecodeError` escape fails `test_the_prompt_hook_never_fails`;
  - writing the pointer under the top level instead of the git dir fails the same test's `git status` check;
  - reading the pointer before `--session` fails `test_the_pointer_is_the_last_prompts_session`.

- [x] **Step 7: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/conversation_prompt.py scripts/conversation_cli.py scripts/conversation_quote.py tests/scripts/test_conversation_prompt.py tests/scenarios/conversation_handlers.py`
  Expected: `2 xfailed`, no failures; exit 0; silent; clean.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/conversation_prompt.py scripts/conversation_cli.py scripts/conversation_quote.py hooks/hooks.json \
    tests/scripts/test_conversation_prompt.py tests/scenarios/conversation_handlers.py \
    spec/capabilities/conversation.md features/conversation.feature CLAUDE.md
  git commit -m "work quote --hook: the UserPromptSubmit hook keeps the session and its transcript for work quote (conversation r2, reworded in place)"
  ```

### Task 5: `work show` on a quote prints its messages (r3)

**Files:**
- Modify:
  - `scripts/conversation_cli.py` (`show(args)`);
  - `scripts/work` (`cmd_show`: a target where `conversation_cli.is_quote` holds, re-exported from
    `conversation_quote`, goes to `conversation_cli.show`);
  - `tests/scripts/test_conversation_quote.py`, `tests/scenarios/conversation_handlers.py`;
  - `spec/capabilities/conversation.md`: `unbuilt: [r4]`, and the Implementation bullet for D7.

**Interfaces:**
- Consumes: Task 3's `find`, `label`, `render`.
- Produces: `conversation_cli.show(args) -> int` (D7).
- Produces, in `conversation_handlers.py`:
  - `GivenK message` and `GivenK quote`, recorded under `step.context["conversation"]`;
  - the local `GivenR message` (`cited by`), which writes the quote's file with `conversation_quote.render` (its
    cited message the given message, with one message around it) and commits it;
  - the local `WhenRuns quote` (`` `work show` ``), which runs `work show quote-<n>`;
  - the local `ThenPrints message`: exit 0, and the message's text and the word `cited` are in stdout.

- [ ] **Step 1: Write the failing tests** (in `test_conversation_quote.py`).
  - `test_show_prints_every_message_of_the_quote`: after a quote of the 3rd of 6 messages, `work show quote-1`
    prints its label first, `session: s-1`, the 5 texts in order, and `cited` on the 3rd message's line only.
  - `test_show_json_gives_the_quote`: `--json` gives `quote.name == "quote-1"`, 5 `messages`, and exactly one with
    `cited` true.
  - `test_show_of_no_quote_is_refused`: `work show quote-9` exits 1 with `there is no quote quote-9 in
    .shop/quotes/`.
  - `test_show_of_an_item_or_initiative_is_unchanged`: `work show b1` still prints the item's label, and `work show`
    with no target still lists work-items. This checks the routing.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_conversation_quote.py -q -k show | tail -3`
  Expected: FAIL. `work show quote-1` reaches the work-queue and is refused there.

- [ ] **Step 3: Implement** `show` and the route in `cmd_show`.

- [ ] **Step 4: The r3 handlers; take r3 out of `unbuilt:`.**
  Run: `python3 -m pytest tests/scenarios/test_conversation.py tests/scenarios/test_backlog.py tests/scenarios/test_work_queue.py tests/scripts/test_conversation_quote.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: conversation `3 passed, 1 xfailed`, the rest pass; `every step has one handler`.

- [ ] **Step 5: Mutation, reverted.** Printing only the cited message fails `test_show_prints_every_message_of_the_quote`.

- [ ] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/tools size --limit 300; wc -l scripts/work; python3 scripts/tools check scripts/conversation_cli.py scripts/work tests/scripts/test_conversation_quote.py tests/scenarios/conversation_handlers.py`
  Expected: `1 xfailed`, no failures; silent; ≤ 225; clean.

- [ ] **Step 7: Commit.**
  ```bash
  git add scripts/conversation_cli.py scripts/work tests/scripts/test_conversation_quote.py \
    tests/scenarios/conversation_handlers.py spec/capabilities/conversation.md
  git commit -m "work show quote-<n>: the quote's messages, the cited one marked (conversation r3)"
  ```

### Task 6: The names table at SessionStart (r4)

**Files:**
- Create: `scripts/conversation_names.py`, `tests/scripts/test_conversation_names.py`
- Modify:
  - `scripts/conversation_cli.py`: the `names` parser (`--hook`) and `COMMANDS["names"]`;
  - `hooks/hooks.json` (D9, SessionStart);
  - `tests/scenarios/conversation_handlers.py`;
  - `spec/capabilities/conversation.md`: `unbuilt: []`, and the Implementation bullet for D8, in place of "`work
    names` is the SessionStart hook's table…";
  - `CLAUDE.md`:
    - a row `scripts/conversation_names.py`: "`work names`: every item and batch with its name beside its id, and the
      SessionStart hook's `--hook`, silent with nothing to show and never failing (conversation)";
    - the `hooks/hooks.json` row also names `work names --hook` at SessionStart;
    - the `conversation_cli.py` row names `work names` beside `work quote` and `work show quote-<n>`.

**Interfaces:**
- Consumes: `backlog_items.items`, `label`, `find`; `batch_plan.batches`; `backlog_view.cell`;
  `migrate_write.top_level`.
- Produces, in `conversation_names.py`:
  - `rows(root) -> list[tuple[str, str, str]]`: (id, name, status), items then batches (D8);
  - `table(root) -> str`, with the empty-text line when there are no rows;
  - `HOOK_LINE`, and `hook_text(cwd) -> str` (D8's `--hook`, never raises).
- Produces, in `conversation_handlers.py`, `WhenRuns` `` `work names` ``:
  - it writes and commits one item per name in the scenario's item Thens (`i1`, title `Fix the parser`) through the
    backlog world;
  - it writes one batch through the batches world (`T.prepare`, `T.ensure_batch`), with a task for that item;
  - it runs hooks.json's SessionStart `names` command;
  - it leaves `step.context["result"]` and `["items"]` for backlog's `ThenPrints item`, `ThenPrints title` and
    `ThenR title`.

  The local `ThenPrints batch` checks that the batch's row is in stdout, holding the item's label.

- [ ] **Step 1: Write the failing tests** (`test_conversation_names.py`).
  - `test_the_table_names_every_item_and_batch`: items b1 (`shaped`) and b2 (`delivered`), and batch-1 of b1, give
    rows `| b1 | Fix the parser | shaped |`, `| b2 | Exit | delivered |` and `| batch-1 | b1 "Fix the parser" |
    building |`, in that order.
  - `test_a_title_with_a_bar_is_escaped`: a title `a | b` stays one cell.
  - `test_the_hook_says_why_before_the_table`: `work names --hook` prints `HOOK_LINE` and then the table.
  - `test_nothing_to_name_is_silent_in_the_hook`: with no `.shop/backlog/` and no `.shop/batches/`, `--hook`
    prints nothing and plain `work names` prints the empty-text line. Both exit 0.
  - `test_the_names_hook_never_fails` (Review Focus 3), parametrised. Each case exits 0, prints at most one line and
    leaves `git status --porcelain` unchanged:
    - a malformed item file prints `work names: .shop/backlog/b1.md: …`;
    - a cwd outside git and a repository with no `.shop/` print nothing;
    - a subdirectory cwd prints the top level's table.
  - `test_the_hook_is_wired`: hooks.json's SessionStart commands are `migrate" status --hook` and `work" names
    --hook`, in that order.
  - `test_the_names_hook_is_fast` (`@pytest.mark.timing`, Review Focus 3): 200 items and 20 batches, a median under
    1.0 s over 3 runs. The output has 221 table lines.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_conversation_names.py -q -m "timing or not timing" -n 0 | tail -3`
  Expected: FAIL. `work` has no subcommand `names` (exit 2).

- [ ] **Step 3: Implement** `conversation_names.py`, the parser and the hooks.json entry.

- [ ] **Step 4: The r4 handlers; take r4 out of `unbuilt:`.**
  Run: `python3 -m pytest tests/scenarios/test_conversation.py tests/scenarios/test_backlog.py tests/scenarios/test_batches.py tests/scripts/test_conversation_names.py -q | tail -1; python3 -m pytest -m timing -n 0 -q tests/scripts/test_conversation_names.py | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: conversation `4 passed`; backlog and batches as before; `1 passed`; `every step has one handler`.

- [ ] **Step 5: Mutations, each reverted.** Each must turn its test red:
  - leaving batches out fails `test_the_table_names_every_item_and_batch` and the r4 scenario;
  - letting `Refused` escape the hook fails `test_the_names_hook_never_fails`.

- [ ] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 -m pytest -m timing -n 0 -q | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/conversation_names.py scripts/conversation_cli.py tests/scripts/test_conversation_names.py tests/scenarios/conversation_handlers.py`
  Expected: no `xfailed` in the summary, no failures; timing `4 passed`; exit 0; silent; clean.

- [ ] **Step 7: Commit.**
  ```bash
  git add scripts/conversation_names.py scripts/conversation_cli.py hooks/hooks.json tests/scripts/test_conversation_names.py \
    tests/scenarios/conversation_handlers.py spec/capabilities/conversation.md CLAUDE.md
  git commit -m "work names: every item and batch with its name beside its id, the SessionStart hook's table (conversation r4)"
  ```

### Task 7: The brainstorming session quotes with `work quote` (brainstorming r3)

**Files:**
- Modify:
  - `skills/shaping-items/SKILL.md`: step 1 (below);
  - `tests/scripts/test_skill_shaping_items.py`;
  - `spec/capabilities/brainstorming.md`: `unbuilt: []`, and its `## Not yet` section removed;
  - `README.md`: under `scripts/work`, one bullet:

    > `work quote "<the person's words>"` copies the person's message with the two messages before and after it
    > (no tool output) into `.shop/quotes/` and commits it. `work show quote-<n>` prints it. `work names` is the table
    > of items and batches by name. The UserPromptSubmit hook keeps the session for `work quote` (`work quote
    > --hook`), and the SessionStart hook prints `work names --hook`.

**Interfaces:**
- Consumes: `work quote` (Tasks 3-4).

- [ ] **Step 1: Write the failing tests.**
  - `test_r3_a_quote_is_written_with_work_quote` (D14): in `process(SHAPING)`, step 1 names `work quote` in
    `commands(…, "work")`, before `shape`. The skill's text holds `quote-<n>`, and does not hold `Until \`work\`
    keeps quotes`.
  - `test_each_built_brainstorming_line_has_its_test` (D14): `ids` are the `- [r<n>] ` of `brainstorming.md`. Each id
    not in `spec_unbuilt.unbuilt(REPO).get("brainstorming", set())` has a function `test_r<n>_…` in this file, read
    with `ast`, and each listed id has none.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_skill_shaping_items.py -q | tail -3`
  Expected: `test_r3_…` FAILS, since the skill names quotes only in words. `test_each_built_…` FAILS, since r3 is
  still listed and has a test.

- [ ] **Step 3: Rewrite step 1 of the skill:**
  > 1. **Write the item.** `python3 <scripts>/work idea "<title>"`. For each thing the person said that the item rests
  > on, run `python3 <scripts>/work quote "<their words, exactly as they wrote them>"`. It prints `quote-<n> "…"`; on
  > a refusal, copy the words again from their message, or give `--session <id>` for an earlier session. Then
  > `python3 <scripts>/work shape <b> --note "<the context to work from>, the person's words in quote-<n>"`.

  Add one Red Flags row: `| The person's words pasted into a note with no quote | \`work quote\` keeps the turns
  around them; cite quote-<n> (step 1) |`. Take r3 out of `unbuilt:` and remove `## Not yet`.

- [ ] **Step 4: Run them, and the skill and spec checks.**
  Run: `python3 -m pytest tests/scripts/test_skill_shaping_items.py tests/scripts/test_spec_unbuilt.py -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1`
  Expected: all pass; `53 violations, 16 warnings, 19 unresolved references, 0 file problems`; `11 findings: 6 L5, 5
  L6`.

- [ ] **Step 5: Mutation, reverted.** Putting `r3` back in `unbuilt:` fails `test_each_built_brainstorming_line_has_its_test`.

- [ ] **Step 6: Commit.**
  ```bash
  git add skills/shaping-items/SKILL.md tests/scripts/test_skill_shaping_items.py spec/capabilities/brainstorming.md README.md
  git commit -m "shaping-items: the person's words are quoted with work quote (brainstorming r3); README: quotes and names"
  ```

### Task 8: Whole-plan verification, a smoke run on a real transcript, and records

**Files:**
- Create: `.shop/records/2026-11-04-workflow-simplification/plan-8-implementation.md`
- Modify: `.shop/records/README.md` (a row for the report); this plan (every box ticked)

- [ ] **Step 1: Every requirement is built.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print(d, sum(map(len,d.values())), u.problems(pathlib.Path('.')))"`
  Expected: `{} 0 []`. If any id is left, the report explains each one.

- [ ] **Step 2: The baselines, all at once.**
  Run: `python3 -m pytest -q | tail -2; python3 -m pytest -m timing -n 0 -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/model decisions --check | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound; python3 scripts/tools size --limit 300; python3 scripts/tools check $(git diff --name-only a7aeb4c2...HEAD -- '*.py' scripts/work)`
  Expected:
  - the suite: no `xfailed`, no failures. Passed = 1481 + 4 conversation scenarios + the new script tests, and the
    subtests stay 135;
  - timing: `4 passed`;
  - `model check`: 53/16/19/0;
  - `model logic`: `11 findings: 6 L5, 5 L6`;
  - the lexicon: `401 terms, 0 problems`;
  - `decisions --check`: `4 check decisions: 4 hold, 0 failing`;
  - generate: exit 0;
  - `vocab --check`: `every step has one handler`;
  - bindings: `every binding names a scenario`;
  - `size`: silent;
  - `check`: clean.

- [ ] **Step 3: The smoke run on a real transcript,** in a scratch repository under
  `/home/vscode/.claude/jobs/7e9ba079/tmp/smoke8/`. Each `cp` and each `rm` is its own command (the person's rule).
  The person's store is only read here, never written. Steps:
  1. **Build the repository:** `git init`, the fixture spec of `tests/scripts/fixtures/generate/repo`, two items
     (`work idea`, `work shape`) and a commit.
  2. **The prompt hook:** run hooks.json's UserPromptSubmit `work quote --hook` command from the scratch repository.
     Its stdin is `{"session_id": "<this session's id>", "transcript_path": "<this session's transcript>"}`, the
     newest `*.jsonl` of `measure_batch_read.project_dir(<this session's working directory>)`.
  3. **The quote:** `work quote "<a phrase from the prompt that started this session>"`, then `work show quote-1` and
     `work show quote-1 --json`.
  4. **The names hook:** run hooks.json's SessionStart `work names --hook` command, and time both hook commands with
     `bash -c 'time …'`.

  Expected:
  - the hook prints nothing and exits 0;
  - `quote-1` cites a person's message and holds at most 5 messages;
  - grepping `.shop/quotes/1.md` for `tool_use`, `tool_result`, `<system-reminder>`, a tool name such as `Bash(` and
    a path the session only read in a tool finds nothing;
  - the names table lists both items with their titles;
  - both hooks run in under 1 s;
  - `git status --porcelain` is empty.

  If no transcript can be found, record that in the report as not run, with why, and run the rest on
  `transcript_testing.CONVERSATION`.

- [ ] **Step 4: Write the implementation report** at `plan-8-implementation.md`, in `plan-7-implementation.md`'s form
  (no frontmatter):
  - Final state: each Step 2 figure as measured.
  - The smoke run: the quote's message count, the hooks' wall times, and what the grep found.
  - The commits: a table of each task's commit, what was done and its verification, the mutations included.
  - Deviations, each with its reason.
  - D1-D16, each kept or changed.
  - Open problems for plan 9. Among them:
    - `migrate prompting` and `migrate status --hook`'s initiative text go with `.shop/work/`;
    - the names table does not expand the old queue's `i<n>`, `w<n>` and `q<n>` (frozen history) or requirement ids
      `r<n>`;
    - a session in a checkout shared with another session must give `--session` (D5);
    - D2's rules for a slash command's rows depend on Claude Code's transcript shape, which may change.
  - Files.

- [ ] **Step 5: Index the records.** Add a row to `.shop/records/README.md` after the row for `plan-8-conversation.md`:
  `| \`2026-11-04-workflow-simplification/plan-8-implementation.md\` | plan 8 executed: conversation (\`work quote\` with the turns around the person's words committed in \`.shop/quotes/\`, the UserPromptSubmit hook keeping the session, \`work show quote-<n>\`, \`work names\` at SessionStart), brainstorming r3 through shaping-items, Sonnet 4 and Haiku 4 priced only as the table lists, 5 requirements out of \`unbuilt:\`, none left | report |`.
  Tick every box of this plan.

- [ ] **Step 6: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-8-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-8-conversation.md
  git commit -m "records: plan 8 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-8-review.md`. It reads `<this plan's
  commit>..HEAD` on `workflow-simplification` against this plan's Review Focus and D2-D5, D8 and D10.
