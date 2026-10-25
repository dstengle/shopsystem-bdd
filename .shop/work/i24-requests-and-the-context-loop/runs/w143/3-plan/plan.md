# Plan of w143: integrating-a-proposal and initiative-round without the small-change path, the coordinator sections or gate cards

A guarantees work-item: prose for a skill and an agent, plus one label in a brief. There is no scenario. Its review judges it against spec/capabilities/spec-integration.md as it stands and decision 0068 (design-decision/the-context-runs-without-a-coordinator). Planned from 2-research/notes.md. 1-research ended at its turn limit and left no notes.

## 1. What goes green

- **spec-integration#r35**: the `gate` kind gives one question for each decision in its result, each marking the recommended reading and giving its lines in full. No accepted scenario: there is no `features/spec-integration*.feature`, and the `@r35` tags in features/ belong to other capabilities (notes §1). Today agents/initiative-round.md:29-30 writes card files under `<drafts path>/gate/` and replies with their path and count, and marks "the coordinator's recommendation". skills/integrating-a-proposal/SKILL.md:21 has the session publish a gate page from those cards.
- **spec-integration#r39**: the `apply` kind, given the file of the person's answers or their approval in their words, applies exactly the drafts approved. No accepted scenario. Today the agent's input word is "job", not the spec's "kind" (agents/initiative-round.md:13, 23-31, 38), and the brief labels it `Job:` (scripts/supervise_brief.py:33). The apply text itself (line 31) already does what r39 says.
- Retired with no scenario to deprecate: r8, r10, r11, r34, r36, r37, r38, r41, r42 are already in the capability's `retired` list. Their text goes from the skill: the "If the person is talking to you" section (SKILL.md:18-29), the Small-Change Path (48-59) and the pointer to it (33). The work-item has no Retires section.

## 2. Where the change lands

- `skills/integrating-a-proposal/SKILL.md`:
  - remove "If the person is talking to you" (18-29), the sentence on the small-change path (33) and The Small-Change Path section (48-59);
  - rewrite "Who Does What" (16, 31) so that `work run` starts each `initiative-round` (`integrate`, `gate`, `apply`, `formulate`) and no session writes spec;
  - rewrite Process step 3 so the gate is given as the `gate` round's result questions, which `work run` writes on the capability-proposal and whose answers come back under its `## Answers`;
  - reword step 5's hand-off, the `v_t1` bullet's "through its small-change path" (43) and the Terms section's "by either path" (63).
- `agents/initiative-round.md`:
  - "job" becomes "kind" throughout (13, 18, 23-31, 38, 55);
  - the `gate` kind gives its questions in its result (r35) and no longer writes cards: no `<drafts path>/gate/` and no reply of path and count;
  - the "coordinator" (29), "the session that dispatched you ... keeps the gate" (11) and the frontmatter description "Dispatched by integrating-a-proposal and formulating-features" go: `work run` starts it;
  - the ledger paragraph says "kind", and the `gate` round's ledger line counts its questions rather than files.
- `scripts/supervise_brief.py`: the round brief's input label `Job:` (line 33) becomes `Kind:`, so the input and the agent's text use the same word. This is Decision 2 below. It is one line in a file of 115, far under the 300 limit.

The researcher's set as given. Checked and not changed: spec/capabilities/spec-integration.md (already the target), tests/scripts/test_agents.py, and scripts/supervise_rounds.py, supervise_worker.py and supervise.py (they consume the round's questions: supervision r68/r85, not w143).

## 3. Decisions

1. **The skill keeps r1-r4's gate content and moves it to the gate round's result.** Step 3 still says what the person is shown: every added, changed and removed line with its id, glossary entries, decision files, and questions with the lines their answers give. That becomes the content of the `gate` round's questions, one a decision, the recommended reading marked. No session publishes a page, and no session reads drafts. Rests on spec-integration#r35, #r1-#r4, and design-decision/the-context-runs-without-a-coordinator ("the gate round that writes each drafted capability-proposal's gate as questions on the proposal").
2. **The input names the kind as `Kind:`.** The agent's text says "the kind your input prompt gives", and the brief writes `Kind: <stage>` where it wrote `Job:`. The narrator (the person at the gate) never sees a brief, so this changes nothing they observe. Rests on spec-integration's Implementation ("an input giving the kind integrate, gate or apply") and #r39.
3. **Nothing in either file tells a session to write spec, dispatch a round or keep the gate.** The `v_t1` rewording and the Terms section name the `formulate` round, not a small-change path. The hand-off (step 5) is the `formulate` round that `work run` starts once the apply is committed. Rests on design-decision/the-context-runs-without-a-coordinator ("No skill tells a session to write spec or feature files itself (the small-change paths go), skills lose their 'If the person is talking to you' sections").
4. **The ledger file stays where it is.** r40 (`work note`) is not accepted by w143. Only the word "kind" and the gate's question count change in that paragraph.
5. **The `apply` kind's text keeps its substance.** It takes the answers under the capability-proposal's `## Answers`, as the Implementation says, or the approval in the person's words. Rests on #r39 and the Implementation's second bullet.

## 4. Tests the decisions break

None. Found by search, since there is no coverage map (notes §4). No file under tests/ contains "Job:", "gate/", "Small-Change", "talking to you" or "coordinator". I checked that `Job:` and `Kind:` appear nowhere in the repository outside `.shop/` except scripts/supervise_brief.py:33. tests/scripts/test_agents.py (test_r1, test_r5, ResultFirst) asserts nothing these prose changes touch. tests/scenarios/supervision_rounds_steps.py drives only `apply` and `formulate` rounds and checks no label.

## 5. Open cases

- What shape each gate question takes in the result (one string a decision, in the agent's words): r35 says what it contains, not its form. The implementer names the form; it must stay a list of strings, as `worker()` normalises `questions`.
- How the agent's `integrate` reply relates to the `gate` round once there is no gate page. Whether `gate.md` is still written for the `gate` round to read is a case the spec's Implementation leaves open; name it in the text.
- Dangling pointers this change leaves outside its set: skills/checking-spec-consistency/SKILL.md:53, 64 and skills/migrating-to-capabilities/SKILL.md:106 point at integrating-a-proposal's small-change path, and no work-item of i24 covers them. Rewriting them would change other capabilities' behaviour. Name them in the report for the branch review; do not edit them here.
- formulating-features' own small-change path and "If the person" section belong to w145, not here.
- The round path drops a result's `questions` (scripts/supervise_rounds.py:49-55), and no code starts a `gate` or `integrate` round (notes §5-6, read, not run). These belong to supervision r68/r85; name them, do not fix them here.
