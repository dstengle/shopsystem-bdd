# Plan of w235: `work delegate`, and a session that records the person's delegation with it

From the research notes (`.shop/work/i60/runs/w235/1-research/notes.md`). The notes record one run, `python3 -m pytest -q --work-item w235`: 11 failed, 180 passed, 1 skipped. All of the accepted scenarios are in features/requests.feature, bound by tests/scenarios/test_requests.py.

## 1. What goes green

Why most of them are red, from the notes:
- **(a)** `scripts/work` has no `delegate` subcommand.
- **(b)** The When step "the upstream runs `work delegate`, giving q1 and the delegation …" (requests_steps.py, the_upstream_runs) only reads resolve's `version` form. On the delegate form it raises IndexError.

| Requirement | Scenario | Red today because |
|---|---|---|
| requests#r65 | "delegate given a request that holds <before> writes the delegation given in the request, in place of any it had" (no delegation; the delegation "answer any question on line 2") | (a), (b); also undefined steps: the Givens "q1 holds no delegation" and "q1 holds the delegation …", and the Thens "q1's delegation is …" and "q1 holds no other delegation". |
| requests#r66 | "delegate writing a delegation in a request commits the request on the current branch" | (a), (b) (run). |
| requests#r67 | "delegate given an empty delegation is refused, and nothing changes" | the Given "q1 holds the delegation …" is undefined; (a). |
| requests#r68 | "delegate given a request that is <status> is refused, naming <status>, and nothing changes" (delivered, refused, withdrawn) | (a), (b); the Then "the command is refused, naming <status>" is undefined. |
| requests#r72 | "a session the person gives a delegation for a request writes it, in the same reply, through delegate as the person's words with the date" | undefined session steps (the When, and both Thens); nothing tells a session to do it; (a). |
| requests#r70 | "delegate run in the <side>'s turn writes the delegation" (upstream, asker) | (a), (b) (run). |
| requests#r71 | "delegate writing a delegation in a request keeps the request's status and turn" | (a), (b) (run). |

The work-item has no Retires section, so it retires no deprecated scenario.

## 2. Where the change lands

- `scripts/work`: a `delegate` subparser (the request, then the delegation text) and its dispatch entry.
- `scripts/workqueue_request.py`: a `delegate` function that goes through `_change`, so the commit is made by `workqueue.committed` (r66). It:
  - refuses an empty delegation because the delegation is empty (r67);
  - refuses a delivered, refused or withdrawn request, naming its status (r68);
  - otherwise writes the frontmatter field `delegation`, JSON-quoted as take-in writes it. It replaces the field's value where there is one and adds the field where there is none (r65).
  - It leaves status and turn as they are (r71) and does no turn check (r70).
  - Writing a field that may be absent needs the insert-when-absent described in Decision 4.
- `scripts/migrate`: a new subcommand for the plugin's UserPromptSubmit hook (Decision 5). It always exits 0, like `compacting`.
- `scripts/migrate_prompt.py` (new): what that hook tells a session about the repository's requests: the r72 instruction.
- `hooks/hooks.json`: a UserPromptSubmit entry that runs the new `migrate` subcommand.
- `tests/scenarios/requests_steps.py`: the_upstream_runs also reads the delegate form ("giving q1 and the delegation \"…\"", the text possibly empty). It runs `work delegate` with the request and the text.
- `tests/scenarios/requests_write_steps.py`, new steps:
  - the Givens "q1 holds no delegation" and "q1 holds the delegation \"…\"";
  - the Thens "q1's delegation is \"…\"" (read and JSON-decoded from the request), "q1 holds no other delegation" (exactly one `delegation` field) and "the command is refused, naming <status>".
  - The Then "q1's delegation is …" must take both the double-quoted form and r72's single-quoted form, whose text holds double quotes.
- `tests/scenarios/requests_session_steps.py` (new, one module a concern): the r72 steps (Decision 6).
- `tests/scenarios/test_requests.py`: imports the new step module.
- `CLAUDE.md`: in the module map, `delegate` added to the `workqueue_request.py` row, and a row for `scripts/migrate_prompt.py`.
- `README.md`: a `work delegate` line beside `--delegation` (line 233), and a line on the UserPromptSubmit hook.

These are added to the researcher's set: `scripts/migrate`, `scripts/migrate_prompt.py`, `hooks/hooks.json`, `tests/scenarios/requests_session_steps.py` and `tests/scenarios/test_requests.py`, all for Decisions 5 and 6. Files read but not edited: `scripts/workqueue.py` (294 lines, so no room for the change), `scripts/supervise_answers.py` and `scripts/migrate_session.py`.

## 3. Decisions

1. **The refusal set is new.** `work delegate` refuses exactly delivered, refused and withdrawn. `SETTLED` (accepted, refused, withdrawn) is not reused: that would refuse an `accepted` request, which r68 does not name. Rests on requests#r68.
2. **No side or turn check, and no status or turn change.** `work delegate` takes no other-side refusal under r16 or r55, and it changes neither status nor turn. The scenarios run it as the upstream in the asker's turn. Rests on requests#r70 and requests#r71. A delegation is not among the parts r4 and r5 give to a side, so r55 does not apply.
3. **The same field, kept JSON-quoted.** The delegation goes in the frontmatter field `delegation`, JSON-quoted as `request` writes it at take-in. That way `supervise_answers.delegation` reads it with no change and picks up the new value at its next read. Rests on the Implementation note for r65 and r66, and on design-decision/requests-written-through-work (how `work` keeps a request is its own).
4. **Insert when absent.** When the request has no `delegation` field, it is added to the frontmatter. Whether `_with_field` is extended or a helper is added beside it is the implementer's choice, inside `workqueue_request.py`. The take-in path must still write the field as it does today. Rests on requests#r65 (the "no delegation" example).
5. **r72's instruction is carried by a new UserPromptSubmit hook, not the SessionStart hook.**
   - The SessionStart hook is ruled out. migration-tools#r24 says it tells the session nothing in a repository with no pending upgrade step and no open initiative. A repository that keeps a request may be one of those.
   - The new hook runs a `migrate` subcommand, alongside the hook commands `status --hook` and `compacting`. It reads the harness's prompt JSON on stdin and always exits 0.
   - It tells the session only when the repository keeps at least one request that is not delivered, refused or withdrawn. Its text says: when the person gives a delegation for a request outside `work request`, in that same reply, run `work delegate <request>` with the delegation as `The person, <date>: "<the person's words>"`. It names the scripts path, as `compacting`'s text does.
   - Keying on the repository's requests rather than on the prompt's wording keeps r72 independent of how the person phrases it.
   - Rests on requests#r72 and migration-tools#r24 and #r28. The narrator observes only q1's delegation, so this is implementation.
6. **How r72 is shown.** The precedent is supervision#r120, which is shown by the instruction a session is given.
   - The When step runs the UserPromptSubmit command of hooks/hooks.json in the repository, as the harness does, with the person's message as the prompt. The message names q1, the date and the words.
   - A session double then acts only on what the hook gave it. If the hook's text holds the instruction (it names `work delegate`, the same reply, and the form `The person, <date>: "<words>"`), the double runs `work delegate q1` with the delegation formed from the person's words and the message's date, and records the command it ran. If not, it runs nothing, so the scenario is red until the hook is written.
   - The first Then asserts the recorded command: `work delegate`, q1, and the delegation exactly as given. The second asserts q1's delegation read from the request.
   - Rests on requests#r72.

## 4. Tests the decisions break

- `tests/scenarios/requests_steps.py::the_upstream_runs` is a step, not a kept test. It is extended to read the delegate form, and resolve's version form keeps working as it does (Decision 1 and the notes).
- The tests that set up the SessionStart hook are not broken: Decision 5 leaves that hook as it is. Verified by search:
  - `tests/scenarios/migration_upgrade_steps.py`: "tells the session nothing" checks the SessionStart stdout only;
  - `tests/scenarios/migration_version_steps.py`;
  - `tests/scenarios/migration_session_steps.py`: PreCompact.
  - Each of these looks up its hook by key in hooks/hooks.json, so a new UserPromptSubmit key changes none of them.
- Decision 3 breaks no test: the take-in form is unchanged, and the r19 and r22 scenarios passed in the run. Verified by search, since no map exists: the notes list where `delegation` appears in tests.
- Decision 4 must leave the turn and resolve scenarios, which use `_with_field`, as they are (they passed in the run). No assertion changes.
- No other existing test is broken.

## 5. Open cases (for the implementer to name, not to choose)

- The wording of the refusal naming the status (r68), as long as it holds the status's name.
- What the double takes as "the hook's text holds the instruction": the keys it looks for, and what it does if the hook exits non-zero or prints nothing.
- A request file whose frontmatter cannot be read, met by the UserPromptSubmit hook. It still exits 0 and says nothing of that request.
- A delegation text holding a newline, or quotes beyond r72's form, given to `work delegate`.
- `work delegate` given a request that does not exist. Presumably it is refused like the other commands on an unknown request.
- A repository with no `.shop/` or no requests directory, met by the new hook. It tells the session nothing.
