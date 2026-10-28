# Review of w219 (spec-integration r54, r55)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. One Important finding is triaged observation. Under r55, the code reads "the person has not approved" as "the glossary-proposal's status is not `approved`". Once supervision r165/r166 are built, that reading will tell a glossary-proposal's own apply round to apply none of its terms. No code writes a glossary-proposal yet (r158 is not delivered), so nothing reaches this today.

## Commits reviewed

The brief's `Commits:` are, oldest first:
- 085527d8: spec-integration r54, a glossary entry in the change list
- 55bed875: spec-integration r55, an apply round withholds the terms of unapproved glossary-proposals

They match the commits the implementer's `result.json` lists. Base `a732bf6e` is `work: w219 ready -> claimed`. The suite comes from the brief's record: 1036 passed and 0 failed at 55bed875. I did not run it.

## Removed and weakened tests

None. I searched `git diff a732bf6e 55bed875 -- tests features`. Only `tests/scenarios/spec_integration_steps.py` and `tests/scenarios/spec_integration_apply_steps.py` changed, and both only gained lines. There were no deleted test functions, no dropped parametrize cases, no removed or loosened `assert`, and no skip or xfail. `answered_proposal` was split into a helper, `answered_proposal_in`, that writes the same file and makes the same commit, so the step still proves what it did. Nothing under `features/` changed. The plan's "Tests the decisions break" says none.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commits agree: no existing test was changed beyond the behaviour-preserving split above.

## Cannot verify

- The report says the red runs failed for the expected reasons: r54 on "an entry of its `changes` names no `capability`", and r55 on the brief lacking "Apply none of them to spec/index.md". These runs happened before the commits, so I cannot verify them from the commits. The code change is consistent with both.
- Whether an `initiative-round` session actually keeps withheld terms out of `spec/index.md`. That is the agent's behaviour under its brief. The scenario's stand-in round never writes `spec/index.md`, so only the brief text is checked (see finding 3).

## Findings

### 1. Important, observation: r55 "not approved" read as "status other than `approved`" (scripts/supervise_glossary.py:15, scripts/supervise_brief.py:86)
- **What is wrong:** `withheld` holds back the terms of every glossary-proposal whose status is not `approved`, and `Briefs` adds the withholding line to every `apply` brief, whatever kind of part the round is for. Supervision r166 sets a glossary-proposal to `approved` only *after* its own apply round. r165 starts that apply round once the person has answered the gate's questions, and those answers are the person's approval.
- **Why it matters:** once r165 is built, a glossary-proposal's own apply round gets a brief that says "The person has not approved these terms ... Apply none of them to spec/index.md", listing its own terms. That contradicts r165/r166 and decision 0073 ("approved at the gate before they are applied"). The same goes for a capability-proposal applied after the person answered a glossary-proposal but before its apply round.
- **Today:** not reachable, because nothing writes a glossary-proposal (supervision r158 is undelivered and its scenarios are expected failures). That is why the triage is observation.
- **Reproduction (by reading, since a Python probe is outside the commands allowed):**
  - `supervise_brief.py:83-86` runs for every `stage == "apply"`.
  - `supervise_glossary.py:15` skips only `status == "approved"`.
  - `grep -n "r166\]" spec/capabilities/supervision.md` returns "transition the proposal to `approved`" after the apply round ends.
- **Fix:** in the work-item that builds r165, leave the round's own glossary-proposal out of the withheld terms. Also count a glossary-proposal whose gate questions are all answered as approved, or decide the reading through integrating-a-proposal.

### 2. Minor, observation: a glossary entry's form is barely checked (scripts/supervise_change.py:26-35)
- **What is wrong:** `entries` accepts:
  - more than one glossary entry;
  - ids in a glossary entry that are not `term/` ids;
  - `term/` ids in a capability entry;
  - an entry with `"glossary": true` and a `capability` key, which it silently reads as a capability entry.
- **Why it matters:** the brief tells the writer about one glossary entry only. A malformed list passes, and r158, once built, would take such ids as the glossary-proposal's. No client sends this today, and the plan's §5 leaves it open on purpose (decision 3).
- **Reproduction:** read lines 26-35. The only test is `each.get("glossary") is True and "capability" not in each`, and no id is checked for a prefix.
- **Fix:** decide it with r158: refuse a list with a second glossary entry or a non-`term/` id in one, through a line.

### 3. Minor, observation: the r55 Thens on spec/index.md cannot fail (tests/scenarios/spec_integration_apply_steps.py:102-111)
- **What is wrong:** the stand-in apply round (`plan["round:apply"]`) writes nothing to `spec/index.md`, so "no term refund" and "order as it was" hold whatever `work run` does. The steps catch a regression only through their extra assertion that the brief names `term/refund`, `term/order` and "Apply none of them to spec/index.md".
- **Why it matters:** this is acceptable because `work run`'s part in r55 is the brief, but the scenario's index assertions say more than they test.
- **Fix:** none needed now. If `work run` ever checks `spec/index.md` after an apply, make the stand-in write the terms.

### 4. Minor, observation: docstrings still say "every entry is a capability" (scripts/supervise_change.py:1-3, 17)
- **What is wrong:** the module docstring and `entries`' docstring still describe only `{"capability": name, ...}` entries.
- **Fix:** name the glossary entry, `{"capability": None, "glossary": True, ...}`. This is cheap.

### 5. Minor, observation: ruff B023 in a touched file, already present (scripts/supervise_change.py:90, :117)
- `tools check` reports three B023 errors in lines `git blame` dates to 2026-10-25 and 2026-10-27, before this work-item. w219 did not touch those lines, so this is named as already present and is not w219's.

### No "code no line asks for"
Each piece of new behaviour serves r54 or r55:
- the glossary entry accepted;
- `unknown` and `write_proposals` skipping the glossary entry;
- the CHANGE_LIST wording;
- the apply brief's withheld-terms line.

`rewrite_lists` (supervise_change.py:66) and `supervise_rounds.py:148` read `each["capability"]`. A glossary entry has `None` there, which matches no `argues` and is never in `absent`, so it causes no crash and no wrong match. I verified this by reading `supervise_rounds.py:136-170` and `:210-225`. A change list holding only a glossary entry is no longer refused, and it writes no proposal, because r158 is out of scope. That is what plan decision 3 says.

## Checks
- `tools check --base a732bf6e`:
  - **ruff:** 3 errors, B023 at supervise_change.py:90 and :117, all already present (finding 5).
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `tools size --limit 300`: printed nothing, so no file is over the limit.
- CLAUDE.md module map: a row for `scripts/supervise_glossary.py` was added (new concern, new module).

## Commands run
- `git log --stat 134745663..55bed875`
- `git diff a732bf6e 55bed875`
- `git diff --stat a732bf6e 55bed875 -- features tests`
- `git log --oneline -3`
- `git blame -L 85,118 55bed875 -- scripts/supervise_change.py`
- `grep -n '\["capability"\]\|get("capability")\|entries(' scripts/*.py`, and `grep -n "self.dir" scripts/supervise_brief.py`
- `sed -n 130,170p` and `210,230p scripts/supervise_rounds.py`, and `sed -n 55,75p scripts/supervise_change.py`
- `grep -n "term/\|change list\|each capability" agents/capability-writer.md`
- `grep -n "r16[0-9]\]\|r170\]\|r158\]" spec/capabilities/supervision.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base a732bf6ea7033d389f7874fea527b2a0d27793f1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
