---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-19-ux-trial-bootstrapping-a-checklist-app-on-an-empty-repository
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-19
---

# UX trial: bootstrapping a checklist app on an empty repository

A new user's session, played literally from README.md, docs/getting-started.md and the skills shaping-items and
building-a-batch at plugin 0.39.0 (main d0e2e8a86), bootstrapping a small checklists CLI (create a checklist, add an
item, check an item off, list a checklist) in an empty git repository with no remote. The plugin's tools were run by
absolute path from this repository's `scripts/`. The trial repository's key files are kept in the folder beside
this record (`trial/`).

**How far it got:** from `migrate init` to `work batch start` (batch-1 building, its brief written), but only by
hand-writing `spec/model/checklists.md`, `spec/vocabulary/checklists.md` and `spec/vocabulary/shared.md`: no
command writes them, and the item's new capability refuses the model lines and entries the docs say it takes. The
batch was not run: the fresh context has no step bindings, no adapter contract and no remote, and nothing tells the
task agent how to make those.

## The steps, in order

1. `tools probe` in the empty repository: refused, exit 1, `no analysis tools are known for this project's language
   (looked for Python)`; the grammar block never prints. `tools install` refuses the same way and installs nothing
   (here the grammar tools were installed already, so the trial went on).
2. `migrate init --id bounded-context/example.org/checklists/checklists-cli`: first refused by git (`Author identity
   unknown`; it left nothing behind, as documented); with an identity it wrote and committed the scaffold. `spec
   check`: 0 violations; `features generate`: nothing; `spec forms --check`: exit 0.
3. `work idea "Create checklists, add items, check items off and list them"` printed `b1`. `work quote` refused
   (no session; the hook is the installed plugin's, so not counted). `work shape 1 --note ...`: `there is no item 1
   in .shop/backlog/`; `work shape b1` worked.
4. `work line b1 --capability checklists --narrator "the person" "<purpose>"`: the capability block written (no
   `area:`, no `specifies:`). Then, as docs/recipes.md "Start a new capability" says ("add its model lines,
   vocabulary entries and lines through the same item with `work line b260 --into labels`"):
   - `work line b1 --into checklists --model "object checklist ..."`: `work: there is no codified capability
     checklists in spec/capabilities/`
   - `--term "- **checklist** (noun) → object checklist. ..."`: the same refusal
   - `--relation "checklist: holds → entry (many)"`: the same refusal
   - a requirement line: accepted as checklists#r1.
5. Work-around: the model area and the two vocabulary layers written by hand (copying the shapes of
   docs/examples/notes-cli/), committed on main. `spec check` then: `v_t16` for `name` and `check` (the request pack
   defines the verb *name* and the noun *check*); renamed the attribute to `title` and gave the verb *check*
   `Redefines: request.`. Left: `v_m4` and `v_m7` for every operation and `w_m5`, since the lines live on the item:
   main's `spec check` stays red until the batch lays them.
6. `spec parse` / `--form` on six lines: the grammar compiled from an empty cache in 0.35 s; every line read as
   meant on the first or second try ("adds an item with a text to a checklist" refused, "adds an item to a
   checklist with a text" read). The refusal named what may follow; good.
7. `work line` for six lines (the first `--reword`ed: its group kept the item's title as its scenario title), `work
   rate`, `work ready b1`: ready in 0.5 s.
8. `work batch start`: batch-1, t1 b1, brief written. The lay's commit wrote `spec/capabilities/checklists.md`
   (no `area:`, no `specifies:`, an empty `## Terms`), `features/checklists.feature` (six scenarios, readable),
   `spec/index.md` (a second `## Composition` heading under the scaffold's, a table `capability | narrator | group`
   where the docs show `area | kind | capabilities`) and `grammar/constructs.md`, the plugin's own 1590-line
   construct catalogue: r5's backticked value `done` is read as a citation of the construct `done`. In the batch's
   worktree `spec check` then fails: `v_c3 a catalogue entry mentions no item and no release` on
   `grammar/constructs.md#intransitive` and `#request-params`.
9. Not run: the task. The batch brief gives acceptance tests `python3 -m pytest -q tests/scenarios/test_checklists.py
   -m "r1 or ..."`, but the fresh context has no step definitions, no program, no `spec/adapters/cli.toml` (`spec
   annotate` and `--check` exit 0 silently without one), and the brief and building-a-batch say nothing of making
   them; only getting-started step 7 shows a hand-written pytest-bdd module. pytest-bdd 8.1 does read the generated
   feature (checked with catch-all steps: 6 passed). `work batch review` would need a remote and gh; the repository
   has neither and nothing before `work batch start` says so.

## Friction points, ranked by how hard they block a new user

Each names the backlog item it became or was added to.

1. **A new capability on an item takes no model lines and no vocabulary entries** (blocker; b387). `work line
   --into <new capability> --model|--term|--relation` refuses `there is no codified capability <name> in
   spec/capabilities/`, though recipes.md says they go through the same item; `--capability` gives no `area:` for
   them to go to. The first item of every fresh context hits this.
2. **No command writes a model area, a vocabulary layer or `shared.md`** outside an item (blocker, with 1; note on
   b354). The user copies notes-cli's files and edits them; `spec forms --check` passes such hand-written files
   silently, and main's `spec check` stays red (v_m4, v_m7) until a batch lays the lines.
3. **`tools install` and `tools probe` refuse in a project with no Python file** (blocker on a fresh machine; b388):
   getting-started step 2 runs them in a folder holding only a virtualenv; they exit 1 before the grammar tools are
   installed or probed.
4. **A fresh context has no path from laid lines to a green scenario in a batch** (high; b389, note on b355): no
   skill or brief says how to write the step bindings, the program and the adapter contract a first task needs; the
   brief's acceptance-test command does not load `-p work_items`; no skill fires before `spec/index.md` exists
   (shaping-items needs a codified spec), so the session has nothing to follow between `migrate init` and its first
   item.
5. **The lay writes the plugin's construct catalogue into a consumer's repository** (high; b390): a backticked value
   that equals a construct code (`done`) counts as a citation; the 1590-line `grammar/constructs.md` then fails
   `spec check` (v_c3) there.
6. **A new capability is laid in the pre-0.38 form** (high; b391): no `area:`/`specifies:`, an empty `## Terms`, and
   `spec/index.md` given a second `## Composition` with columns the docs don't show.
7. **shaping-items (and taking-in-a-request) still teach the glossary form** (medium; b392): `--term "- **t** (pos):
   ..."` with no `→ <element>`, `adjective of <kind>`, `attribute of <kind>` with `Values:`, `--relation "| from |
   word | to | cardinality |"`, no `--model`, "shall refuse the command and name X", "each change to the glossary
   recompiles grammar 4 ... takes minutes" (0.35 s here). raising-a-request is current; shaping-items is the one a
   new user's session follows.
8. **Common domain words collide with the request pack** (medium; b393): `name` and `check` are pack words; v_t16
   asks for `Redefines:` but redefining `name` would break "name the title" in every refusal, and nothing says which
   to choose or lists the pack's words up front.
9. **A batch cannot publish without a remote and gh, and nothing says so before it starts** (medium; b394):
   getting-started says gh is not needed on that page; `work batch start` started on a repository with no remote.
10. **The first line of an item takes the item's title as its group's title** (low; b395): it becomes the scenario
    title ("Create checklists, add items, check items off and list them"), and `--reword` keeps it.
11. **`work shape 1` refuses `there is no item 1`** (low; b396): `work idea` printed `b1`; the refusal does not name
    the form it wants.
12. **`migrate init` with no git identity** (low; none filed): git's `Author identity unknown` comes through raw; it
    changed nothing, as documented.

What went well: `migrate init` (clean scaffold, clean rollback), `spec parse` and `--form` (fast, readable, a
refusal that names what may follow), `work ready` and `work batch start` (sub-second), and the generated feature,
which pytest-bdd 8.1 reads as it is.
