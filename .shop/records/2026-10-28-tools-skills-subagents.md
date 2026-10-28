# More tools, skills or subagents? The last five initiatives (i37, i38, i40, i41, i42)

Read-only analysis. Scope: 87 `claude -p` sessions, which are every `session.json` under `.shop/work/i{37,38,40,41,42}/runs/`, and their 87 transcripts (`transcript_path` in each session.json, all present), with the subagent transcripts under `<session>/subagents/`. Nothing of i43 or i44 was read.

## How the figures were made

The scripts are in `.shop/records/2026-10-28-tools-skills-subagents/` (the derived `rows.json` and `analyzed.json` were not kept; `collect.py` and `analyze.py` regenerate them from the session transcripts; the scripts are kept as `.py.txt`, rename to run):
- `collect.py` reads every session.json into `rows.json`: stage kind = the run directory's name less `<k>-`, and `branch-review` for `runs/branch-review/<k>`.
- `analyze.py` reads each transcript into `analyzed.json`. Tool calls are counted once per `tool_use` id (the transcripts repeat a call's block, so a naive count doubles it). Errors are the `is_error` tool results. A re-read is a second Read of the same path. The first word of each Bash command is kept.
- `summary.py`, `deny.py`, `poll.py`, `wall.py` and `gaps.py` produce the per-kind table, the denial causes (regex classes over `permission_denials[].tool_input`), the waiting after a dispatch, the wall time and gaps over 300 s.
- The ad-hoc queries cited below were run inline against `analyzed.json`.

"Turns" is `num_turns` from session.json. "Calls" is tool calls in the transcript. The two differ for rounds that dispatch in the background (see the caveat at the end).

## How `work run` starts a stage

`scripts/supervise_worker.py:224-228` runs:

`claude -p "Read the brief file <brief> and do what it says." --agent shopsystem-bdd:<agent> --plugin-dir <plugin root> --session-id <id> --output-format json --permission-mode acceptEdits --allowedTools <TOOLS[stage] + Skill(<each skill in the agent's skills:>)> [--max-turns 80 for research]`

`TOOLS` is at `supervise_worker.py:31-58`. `.shop/delivery.toml` can override it, and none exists. The agent's own `tools:` frontmatter limits which tools exist at all. `--allowedTools` decides which calls pass unprompted, and in `-p` mode every other call is a `permission_denial`.

| Stage | Bash allowed |
|---|---|
| research and review (READER) | `python3 -m pytest*`, `python3 <scripts>/{features,model,tools} *`, `git status/diff/log/show*` |
| implement | the same, plus `git add` and `git commit`, minus `git log` and `git show` |
| plan | no Bash (role-boundaries r6) |
| rounds (integrate/gate/apply/formulate) | READER, plus `git add`, `git commit`, `Agent` and `work note` |

Claude Code also passes its read-only built-ins (ls, cat, grep, wc, sed -n, diff, test, sleep in an `until` loop). It refuses a compound command when any part fails the check, as well as any variable or `$( )`, heredocs, `for` loops with `$(seq)`, `timeout … bash -c`, and Writes outside the worktree.

## Per stage kind

| Kind | Sessions | Mean turns | Mean calls | Cost (total / per session / per call) | Denials (sessions with any) | Denials as % of calls |
|---|---|---|---|---|---|---|
| research (code-scout, Haiku) | 9 | 57.8 | 56.8 | $2.07 / $0.23 / $0.004 | 17 (8/9) | 3% |
| plan (bdd-planner, Opus) | 10 | 22.6 | 21.6 | $7.13 / $0.71 / $0.033 | 0 (0/10) | 0% |
| implement (Sonnet) | 19 | 37.4 | 35.4 | $9.99 / $0.53 / $0.015 | 34 (14/19) | 5% |
| review (task reviewer, Opus) | 12 | 23.4 | 22.4 | $8.91 / $0.74 / $0.033 | 19 (12/12) | 7% |
| integrate round (+ capability-writer) | 6 | 13.7* | 19.5 | $5.17 / $0.86 / $0.044 | 14 (4/6) | 12% |
| gate round | 8 | 6.8 | 5.8 | $0.75 / $0.09 / $0.016 | 11 (7/8) | 24% |
| apply round | 8 | 17.5 | 16.5 | $1.39 / $0.17 / $0.011 | 27 (8/8) | 20% |
| formulate round (+ feature-formulator) | 7 | 45.0 | 52.4 | $6.92 / $0.99 / $0.019 | 35 (7/7) | 10% |
| branch review (Opus; already being fixed) | 8 | 47.6 | 46.6 | $12.74 / $1.59 / $0.034 | 73 (8/8) | 20% |

\* undercounted; see the caveat at the end.

Outside the branch review there were **157 denials in 2,331 calls (6.7%) over 79 sessions**. Each denial is one wasted call, and usually a retry follows. Costed at each kind's cost per call, the denials come to about $3.0 of $42.3. Branch reviews add a further 73.

### Denial causes per kind (`deny.py`; regex classes, so approximate)

- **research (17):**
  - 7 compound commands (`… 2>&1 | grep -v "^$" | tail`, `; git check-ignore`)
  - 4 variable assignments (`P=…/scripts; python3 $P tests-of …`, e.g. cb02ac9a, 95ee7145)
  - 3 unlisted commands (`git check-ignore`, `cd /dev/null`)
  - 2 `sed -i` on a probe
  - 1 plugin script at an unlisted path
- **implement (34):**
  - 11 variable assignments (`S=…/0.26.0/scripts; for t in …; python3 $S/features retire "$t"`: a75c0318, 8099e16a, 087300b5)
  - 6 Python heredocs editing a file by string replace (8099e16a, 087300b5, 829a84f2, 36ffe1b9, 647bc7ff)
  - 5 unlisted commands (`env | grep`, `pip list`, `PYTEST_ADDOPTS= python3 -m pytest`, `cat pytest.ini`)
  - 5 `cat > report.md <<EOF` heredocs
  - 4 other compound commands
  - 3 `sed -i`
- **review (19):** 11 of the 19 are the `tools check …; echo "exit $?"; python3 … tools size` compound, hit in 11 of the 12 sessions. Of the rest, 3 are `for d in …` loops over run directories and the others are `C=$(git log --grep …)` lookups.
- **integrate (14):** 5 waiting loops after the dispatch, 6 compound commands, 2 variables, 1 heredoc.
- **gate (11):** 9 attempts to write `result.json` through a heredoc or a scratch Python script (a69b7fc4, abda526d, 077f75bd, 1abdd795, 6f319911, 1e981e53, bd6434a0), including 1 Write to `/tmp/g.py` (077f75bd).
- **apply (27):**
  - 10 variables (`D=…/drafts/round-1; diff …`)
  - 10 hand-written merge/splice scripts (`merge.py`, `splice.py`, `apply.py`, `python3 - <<`)
  - 3 heredocs
  - 3 cases of `scripts/model check` run without `python3` or by the wrong path
  - 1 Write outside the worktree
- **formulate (35):**
  - 14 splice/deprecate scripts (45c94753, 438fd050, 7399c7af, 7e9beada, 275d82aa)
  - 8 waiting loops
  - 6 compound commands
  - 3 variables
  - 5 plugin scripts not run with `python3` or at an unlisted path
  - 1 Write outside the worktree

### Top repeated patterns (`summary.py`)

- **research:**
  - 69 pytest runs, 28 of them probe files under `.shop/scratch` in i37-i41. i42 has 0 probes after e35ed6de ("no probes"), and its research ran 41-44 turns at $0.04-0.06, against 36-83 turns before.
  - 151 Reads, 108 Greps, 23 `wc -l`, 28 `tools refs`/`tests-of`.
  - 9 `tools --help`: the CLI is re-learnt every session.
  - **6 `tests-of` calls failed with "no map: make one with tools map"**, in b3767360 (i40 w203), cb02ac9a (i42 w213) and 95ee7145 (i42 w214). The researcher is told "you do not make one" (`agents/code-scout.md:42`), and a new worktree never has `.shop/scratch/tools/coverage`.
- **plan:** 109 Reads, 61 Greps (mostly spec-id and tag patterns such as `\[r(131|132…)\]` and `@r45`), 16 Globs, 11 re-reads, 0 errors and 0 denials.
- **implement:**
  - 76 pytest runs, 147 Edits, 153 Reads, 37 shell `grep`.
  - 24 `features retire` calls, one title per call, because `retire` takes one positional `title` (`scripts/features:119-121`). The `for` loops that tried several titles at once were refused.
  - In 4 of 19 sessions (a75c0318, 8099e16a, 03329291, 1ab5d8dc) the implementer probed why pytest selected only the work-item's scenarios (`env | grep`, `echo "[$PYTEST_ADDOPTS]"`, `PYTEST_ADDOPTS= python3 -m pytest`). `with_scripts()` sets `PYTEST_ADDOPTS=--work-item <it>` (`supervise_worker.py:91-92`), and no brief, agent or skill tells the implementer this.
- **review:**
  - 35 `tools check`/`tools size` calls in 12 sessions, nearly all after a refused compound.
  - Version-control reads: 28 `git show`, 22 `git log`, 14 `git diff`.
  - Shell reads: 25 `grep`, 21 `cat`.
  - Before the brief carried `Commits:` (i37-i41), 6 sessions each spent 2-4 calls finding the claimed commit with `git log --grep`, and 6 of those calls exited with 128. i42's reviews no longer do this.
- **rounds:**
  - 115 of the 484 calls in integrate and formulate rounds were waiting for the dispatched subagent's reply file (`poll.py`).
  - 26 calls in 11 of the 29 round sessions went to locating and reading a skill's `SKILL.md` by Glob, `find /` or `ls` of the plugin cache, and 6 of them were refused.
  - Apply and formulate rounds made 32 calls to hand-written splice/merge scripts, 24 of them refused.

## Recommendations (ranked by calls saved)

### 1. Rounds: stop the wait-for-dispatch waste (a sandbox allowance or helper, and possibly a foreground subagent)

**Evidence.**
- In all 13 dispatching rounds, `subagent_stats.started_in_background` is 1. That holds even for the 3 rounds that left `run_in_background` unset (i38/1-integrate, i40/1-integrate, i42/1-integrate). `agents/initiative-round.md:52-59` therefore tells the round to wait "in one shell command".
- The shapes it tries are refused: `for i in $(seq 1 100); do [ -f $f ] && break; sleep 5; done` and `timeout 540 bash -c 'until …'`. That is 13 denials. Only a bare `until test -f X; do sleep 5; done` passes, and Claude Code backgrounds it.
- In i38 supervision/3-formulate (45c94753), every wait shape was refused or blocked ("Blocked: sleep 240 followed by …"). The round then polled with `ls …round-1/; date` 68 times, 77 waiting calls in all: **182 calls and $3.09**, against a median of 35 calls and about $0.80 for the other formulate rounds.
- In total, 115 waiting calls and 13 denials (`poll.py`).

**Change.**
- (a) Give the rounds one allowed wait command. One option is a plugin helper `python3 <scripts>/tools wait <file>… --timeout 540`, allowed for rounds only. That would be a new `tools` subcommand, and `tools` is already allowed. The other is to name in `initiative-round.md` the exact shape that passes (`until test -f <file>; do sleep 5; done`, with the Bash `timeout` parameter).
- (b) Also try one round with `run_in_background: false` on the Agent call. `subagent_stats.requested.foreground` exists as a field, so a foreground request is plausible in `-p` mode. If it is honoured, the dispatch returns the reply directly and the waiting disappears. I could not verify this from the data, because no round asked for it.

**Saving.** Up to about 100 of the 484 integrate and formulate calls (115 waits less the one wait call each round needs), and 13 denials. At $0.019-0.044 a call, that is about $2-3 over these five initiatives. The tail risk of the i38 kind ($2.30 above median) goes away.

**Role boundary.** None: `initiative-round` stays the only dispatcher (r1).

**Measure.** Calls per integrate and formulate round from transcripts, `permission_denials` = 0 in rounds, and formulate cost per round.

### 2. Every brief carries the code-scout's account of what the shell refuses, and the plugin scripts get a short form

**Evidence.**
- 157 denials outside the branch review (table above). Variable assignment and `$( )` account for about 36 of them, and plugin scripts called by an unlisted path or without `python3` for 11 more. Heredocs and inline Python account for 30, mostly writing reports and results, or editing a file that Edit/Write would handle.
- `agents/code-scout.md:65` is the only agent body that states what is refused. The researcher has the lowest denial rate of the shell-holding stages (3%), against 5% for the implementer, 7% for the reviewer and 10-24% for the rounds.
- Every brief prints `Scripts: /home/vscode/.claude/plugins/cache/.../0.28.1/scripts`. The agents then shorten it with `S=…; python3 $S/features …`, which is refused (a75c0318, 8099e16a, 087300b5, 95ee7145, cb02ac9a and others).

**Change.**
- Put one paragraph in every stage's brief (`supervise_brief.py`). It states:
  - one operation a call: no `;`/`&&` chains with variables, no `$VAR`, `$( )` or `$?`, no heredocs, no `for` loops, no `sed -i`
  - write files with Write and edit with Edit
  - the full command lines to copy (`python3 <scripts>/tools check --base <base>`, and so on)
- Optionally, prepend the scripts directory to `PATH` in `with_scripts()` and allow `Bash(tools *)`, `Bash(features *)` and `Bash(model *)`. The commands become short enough that no agent sets a variable.

**Saving.** Most of the 157 denials, and their retries. At about one wasted call each, that is about 5-7% of worker calls and about $3 over five initiatives. More in rounds: gate calls fall by up to 24% and apply calls by up to 20%.

**Role boundary.** None. The allowance stays per stage.

**Measure.** `permission_denials` per stage kind in session.json. The target is under 0.3 per session, down from 1.8 (implement), 1.6 (review), 3.4 (apply) and 5.0 (formulate).

### 3. `work run` precomputes what workers re-run or cannot make: the task review's check, and the researcher's coverage map

**Evidence (review).**
- All 12 reviews ran `tools check --base <base>` and `tools size --limit 300` (35 calls). 11 of the 12 had their first attempt refused (`; echo "exit $?"`).
- `agents/bdd-task-reviewer.md:23` already takes the suite from the brief's `Suite record:`. `tools check` and `tools size` are the same kind of fixed run.
- The i37 analysis (`.shop/records/2026-10-26-i37-analysis.md:97`) already proposed exactly this, after the denial on those commands in w197.

**Evidence (research).**
- 6 `tests-of` calls failed with "no map" in 3 of the 4 most recent research sessions (b3767360, cb02ac9a, 95ee7145). The scout's own method starts from `tests-of` (`code-scout.md:39,58`) and then falls back to Grep (108 Greps in research).

**Change.**
- `work run` puts a `Check record:` (the output and exit code of `tools check --base <Base>` and `tools size`) in the task reviewer's brief, as it is doing for the branch review.
- `work run` builds the coverage map once per initiative base (`tools map`) and copies it into each research worktree's `.shop/scratch/tools/`.

**Saving.**
- Review: about 3 calls of 22.4 per review (the refused call, then check and size), so 36 calls and 11 denials, about $1.2 at $0.033 a call.
- Research: 6 failed calls, plus the Grep fallback that `tests-of` replaces. The research gain is small in money (Haiku, $0.004 a call) but would make "tests that break" exact rather than "by search".
- Cost: one map run per initiative (a suite run under coverage).

**Role boundary.** None. The reviewer keeps its read-only Bash for focused checks, and the researcher still does not make the map.

**Measure.** Review calls per session (22.4 now) and review denials (19 now). For research, `tests-of` errors = 0 and the share of notes lists marked `tests-of` rather than `by search`.

### 4. Give `initiative-round` the Skill tool

**Evidence.**
- `agents/initiative-round.md` lists `skills: [integrating-a-proposal, formulating-features]` but `tools: Read, Glob, Grep, Bash, Write, Edit, Agent`, with no `Skill`. `work run` adds `Skill(shopsystem-bdd:…)` to `--allowedTools` (`supervise_worker.py:122-128`), but the tool does not exist in the session.
- The rounds made 0 Skill calls. Instead, 26 calls in 11 sessions located `SKILL.md` by `Glob **/formulating-features/SKILL.md`, `find / -name SKILL.md`, or `ls` of the plugin cache, and 6 of those were refused.
- They also read different copies:
  - the installed 0.26.0 or 0.28.1 cache (most)
  - the worktree (c490626a, 19e8fc7e)
  - the main checkout `/home/vscode/shopsystem-bdd/skills/…` (7399c7af, i41)

  The skill a round followed is therefore not certainly the version `work run` runs.

**Change.** Add `Skill` to `initiative-round`'s `tools:`, as r4 does for the implementer. Possibly add a role-boundaries line for it.

**Saving.** About 2 calls and 0.5 denials per integrate or formulate round: roughly 26 calls and 6 denials over the five initiatives. The bigger gain is reading the right version of the skill.

**Role boundary.** None. Skill only loads instructions, and `--allowedTools` still limits it to the two named skills.

**Measure.** Skill calls = 1 per round, and no Glob or find on `SKILL.md` in round transcripts.

### 5. Batch and splice in the plugin's own commands

**Evidence.**
- `features retire` and `features deprecate` take one title each (`scripts/features:112-121`). The implementer made 24 retire calls across 8 sessions, and its `for t in …` attempts were refused 6 times. The formulate rounds made 20 deprecate calls, plus a hand-written `deprecate.py` (45c94753).
- Apply and formulate rounds merge a draft into `spec/capabilities/*.md` or `features/*.feature` with ad-hoc `merge.py`, `splice.py` or `apply.py` scripts, or `python3 - <<` (32 calls, 24 refused, in 9 of 15 sessions: ae7f6d2f, 328e139a, 872c6db8, 35c9a98e, 438fd050, 7399c7af, 7e9beada, 275d82aa, 45c94753).
- The gate likewise builds `result.json` through Python scripts (9 calls, 8 refused) instead of using Write.

**Change.**
- Make `retire` and `deprecate` take several titles.
- Add one plugin command that writes a round's drafted lines or scenarios into the live file by id or tag, for example `features splice <draft>` and `model apply-draft <draft>`.
- In `initiative-round.md`, have the gate write `result.json` with Write.

**Saving.** About 40-50 calls (24 + 20 one-title calls become a few) and 32 denials, chiefly in rounds. A determinate splice also replaces 9 differently written merge scripts.

**Role boundary.** None. No new tool for any agent: the rounds already run `features` and `model`.

**Measure.** Splice-script and `retire`/`deprecate` call counts per session, and apply/formulate denials (27 and 35 now).

## Not recommended, and why

- **Bash for the planner** (r6 forbids it). The planner had 0 denials and 0 errors in 216 calls. Its 61 Greps are spec-id and tag lookups that Grep answers in one call each. Nothing in the transcripts was blocked for lack of `git log` or `tools refs`. Granting Bash would break r6 and buy at most a few calls per plan.
- **More subagents.** `claude -p` does run subagents. 13 rounds each spawned one plugin agent (`subagent_type: shopsystem-bdd:capability-writer` or `feature-formulator`) via `--plugin-dir`, and `--agents '<json>'` could also define session agents. But:
  - They run in the background by default, which is the source of recommendation 1's waste.
  - Only `initiative-round` may dispatch (r1).
  - The candidates do not pay. Research is Haiku at $0.23 a session, and fan-out would multiply the context reads. Task reviews are already one session per work-item, run side by side by the pool. Plans (Opus, $0.71) re-read about 11 files, and a Haiku reader subagent would add a context hand-off per question. Splitting the branch review per work-item meets the same objection, with 1-3 work-items per initiative.
  - The data shows no stage limited by serial reading. The cost is in retries and re-runs, which tools and allowances fix more cheaply.
- **New skills for workers.** The implementer loads `bdd-red-green` once per session (19 Skill calls in 19 sessions), so no waste there. The procedural knowledge re-derived each run is small and stage-specific:
  - `tools --help` 9 times in research
  - the `PYTEST_ADDOPTS` narrowing, puzzled over in 4 implement sessions
  - the refused command shapes (everywhere)

  A brief line costs no turn, whereas a skill costs a Skill call. That makes these brief text (recommendation 2), not new skills.
- **Unused or wasteful tools.**
  - Reviewers and implementers often use shell `grep` and `cat` instead of Grep and Read (review: 25 grep, 21 cat; implement: 37 grep). This costs no denials when standalone, but it is the main source of the refused compound commands.
  - The `Skill(…)` entries in the rounds' allowedTools are dead (recommendation 4).
  - The planner's Glob is lightly used (16 calls), which is harmless.

## Caveats, and what could not be determined

- **`num_turns` and `duration_ms` undercount background-dispatching rounds.** i38/1-integrate (d50dc29f) and i41/1-integrate (19e8fc7e) report `num_turns` 1 and `duration_ms` 2711 and 4454, yet their transcripts hold 21 and 20 tool calls. session.json reports only the last turn after the subagent's completion notification woke the session. `measure`'s turns and time for integrate and formulate rounds are therefore too low, and rounds should be measured from the transcripts or `modelUsage`.
- **Waiting is invisible in some transcripts.** Many waiting calls have no tool result in the transcript: they ran as background tasks, and the result arrived as a task-notification. Whether they timed out or succeeded is inferred from what followed.
- **Denial causes are approximate.** They come from regexes over the command text (`deny.py`). A command with several faults is counted under the first match.
- **One stall is unexplained.** i37 w197 review (33f0f014) has two gaps of about 30 minutes each, one after reading its brief and one after a `git log … ; git diff` whose result was exit 128 (`gaps.py`). The transcript does not show why the session stalled. The i37 analysis linked the gap to the permission denial, and I could not confirm that.
- **The cost of each denial is estimated, not measured.** Each denial is costed at its kind's mean cost per call. The real cost depends on context size at that turn, and on the output tokens spent writing the refused heredoc or script, which is often long.
- **Foreground subagents in `-p` mode are untried.** Whether a foreground `Agent` call (`run_in_background: false`) is honoured cannot be told from these runs, because no round requested it.
