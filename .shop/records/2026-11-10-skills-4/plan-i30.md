# The authoring skills in 4.0 (b162, b214) Implementation Plan

> **For agentic workers:** carried out as CLAUDE.md says a plan is: one fresh agent carries every task in order on
> one branch, `plan-skills-4` from `origin/main`, in the worktree `.shop/worktrees/plan-skills-4`, then one fresh
> reviewer reviews the whole branch. Steps use checkbox (`- [ ]`) syntax.

**Goal:** the design's I30 (`.shop/records/2026-11-09-cnl-4/design.md`, section 10.3, and the skills row of section
9) and the skill part of b214: every skill that writes, checks or explains requirement lines teaches the controlled
language 4 as plugin 4.0.0 has it on `main`, and names only commands and options that exist. No requirement line:
the skills have no capability, so the item is carried as this plan (design section 13 point 2).

**What 4.0 changed for a session that writes lines** (sources: design sections 4-7, `grammar/language.md`,
`grammar/constructs.md`, `grammar/packs/`):

- A codified spec says `language: codified-2` in `spec/index.md` and in every capability file; `codified-1` is
  refused by `model check` (`v_p0`, naming `migrate upgrade`). A skill that triggers on `codified-1` alone no longer
  triggers (b214).
- The vocabulary is layered: the base grammar, the packs `spec/index.md` imports (`imports: [cli, spec]`; plugin packs
  in `grammar/packs/`, a context's own in `spec/packs/`), the glossary, each capability's `## Terms`. A word a pack
  defines and the context defines again carries `Redefines: <pack>`. `model lexicon` marks a pack's words
  (`[pack cli]`).
- Entries: the part of speech is `noun`, `proper noun`, `adjective of <kind>`, `attribute of <kind>`,
  `verb, state` or `verb, action`, `artifact`; a verb has one or more `Frame:` lines (one meaning) and a second entry
  of the same verb is a second meaning that its kinds must tell apart; `This:` makes a kind's "this K" the run's own;
  an artifact may give `Schema:`. A condition (adjective) is defined by a sentence of the base grammar, never prose.
- Lines are sentence structure over plain words: a state is said with a structure ("an item whose status is not
  `shaped`", "a comment that does not conform to the comment form", "a commit that cites no item"), never a coined
  adjective. States go in a While clause (state verbs, "has V-ed"), events in When or If (action verbs); a state
  in the trigger's noun phrase moves to While (STATE-MOVE). A command's option is in the trigger ("runs `work
  backlog` with the `--json` option", "without the `--tier` option"); Where is kept for a product feature. A
  refusal is "If ..., then `work` shall refuse the command and name X": the error exit and "change nothing" are
  entailed (the CLI pack's refuse, U12) and `model explain` shows them. The agent is explicit (the person, a
  session, `work`). "the K" binds to something the line gave, an image of a relation, or a `This:` kind, else the
  line is refused; "does not V a K" in a condition is refused (say "Vs no K" or "a K that X does not V"). Example
  data goes in the group's given block: a code that names no declared constant is a parameter (`w_example`). A
  format is an artifact a line conforms to. A line about the language names a construct by its catalogue code (`a
  requirement that uses `rc-object``), a check by its rule code (`a term that violates `v_t11``). Compounds:
  attribute- or relation-derived ("the batch status", "a request comment") or declared; an attributive noun tells
  two things apart.
- One meaning or refused: a line whose readings differ is refused naming the words.
- Commands: `model parse "<line>"` and `--file`, `--form` (the logical form); `model explain <cap>#r<n>` (what a line
  also means, what takes precedence over it); `model constructs` (the catalogue, `--check`); `model lexicon`;
  `work line --retires <cap>#r<n>` (a line that replaces a live one, the old id into `retired:`; with `--universal`,
  `universal#U<n>`); `work line --recodify <cap>` (only a capability still saying `codified-1`). `model parse` has no
  `--capability` and no `--grammar`.
- A glossary change recompiles the grammar (minutes the first time): an item's terms are written all at once,
  before its lines are checked by `work ready`, not one term between checks.

## Task 1: shaping-items

- [ ] Description: triggers on a codified spec (`spec/index.md` with `language: codified-2`).
- [ ] Overview: the bar's checks as 4.0 has them (each line parses to one meaning in grammar 4).
- [ ] Replace "No command rewords or removes an item's line yet" with: an item's own line is reworded by editing its
  bullet; a delivered line is changed with `work line --retires`; `--recodify` only for a capability still in
  `codified-1`.
- [ ] Step 2: points to raising-a-request's writing rules; terms first, all of them, with their part of speech in
  4.0's labels and `Redefines:` where a pack has the word; example data with `--given`; `model parse --form` and
  `model explain` to check a line means what was meant.
- [ ] Red flags: coined adjective, option in Where, long refusal, example data in a line, a term added between two
  `work ready` runs.

## Task 2: raising-a-request

- [ ] Description: `codified-2`; also when a line needs a word or construct.
- [ ] "The forms" table: Where for a product feature only; options in the trigger; refusal short form; the agent
  explicit; states in While. Replace `docs/capability-format.md` (it still describes `codified-1`) with `grammar/language.md` and
  `grammar/constructs.md` under the plugin.
- [ ] A section "Writing a line in 4.0": the rules above, each with an example from `main`'s spec.
- [ ] Step 1: `model lexicon`'s categories and pack marks; entries in 4.0's labels; packs and `Redefines:`; compounds.
- [ ] Step 3: `model parse --file`, then `--form`; the refusals 4.0 gives (`parsed up to`, `may follow`, two
  readings, an unbound "the").
- [ ] Step 5: a missing word as a 4.0 entry (`verb, action` with `Frame:`), a missing format as an artifact.
- [ ] Red flags for the 4.0 rules.

## Task 3: taking-in-a-request

- [ ] Step 3: a line is judged in grammar 4 by `work outcome`; a counter-proposal rewords a line to 4.0's rules
  (coined adjective, example data, long refusal, option in Where); an accepted line with example data gets its
  group's given block on the item after `work accept` (`work line --given`).
- [ ] Red flags for it.

## Task 4: building-a-batch

- [ ] Step 4's builder brief: what a line means is `model explain <cap>#r<n>` (and `model parse --form`); a
  `# entailed:` comment in a feature is no step to build; a given block's values bind the line's parameters; an item
  with `retired:` (a reword) whose new scenario XPASSes because the behaviour exists: confirm the steps check the line
  as worded, then take the id out of `unbuilt:`; the retired id's scenario and its now unused handlers go.

## Task 5: the others

- [ ] analyzing-a-batch: judges findings, defects and parks, not lines; unchanged unless a step names a removed
  command. bdd-red-green: no SKILL.md (two empty untracked folders); nothing to change.
- [ ] Every command and option a skill names: run its `--help`.
- [ ] `python3 -m pytest -q`, `python3 scripts/tools check`, `python3 scripts/tools size --limit 300`; push.

## Left out

- b214's code half (`scripts/intake_moves.py:93`, a counter-proposal parsed with no capability): moot since the old
  pipeline was removed (every line is grammar 4); b214 can close with this plan.
- `docs/capability-format.md` still describes `codified-1`; the user documentation is b170's.
