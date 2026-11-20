---
id: vocabulary/missingmass.io/shopsystem/shopsystem-bdd/upgrades
area: upgrades
---

# The words of upgrades

## Terms

- **initiative** (noun) → object initiative. The delivery of one request's accepted lines, named `i<n>`.
- **tracked file** (noun) → object tracked file. A file committed in the repository `migrate` runs in.
- **uncommitted change** (noun) → object uncommitted change. A change to the working tree of a repository that no commit holds: a file git does not track, or a change to a tracked file.
- **old-layout directory** (noun) → object old-layout directory. A directory of the old system's layout at the root of a repository: `decisions/`, `work/`, `records/`, `docs/superpowers/plans/`, `docs/superpowers/specs/`, `docs/superpowers/requests/` or `adrs/`.
- **decision ledger** (noun) → object decision ledger. The old system's ledger of decisions, the file `spec/decisions.md`.
- **ledger entry** (noun) → object ledger entry. One entry `## decision/<name>` of a decision ledger. Plural: ledger entries.
- **qualifier** (noun) → object qualifier. The words after the id a ledger entry supersedes, as `(in part)`.
- **ledger number** (noun) → object ledger number. The `<nnnn>` before the name of a ledger entry.
- **stem** (noun) → object stem. The part of the id of a ledger entry after `decision/`, or the name of a tracked file without its directory and its extension.
- **Behaviour line** (noun) → object Behaviour line. A line of the `## Behaviour` of a capability of the old system.
- **line id** (noun) → object line id. The `[r<n>]` of a Behaviour line.
- **plugin version file** (noun) → object plugin version file. The file `.shop/plugin-version`, one line naming the plugin release a repository is on.
- **content** (noun) → object content. The text a file holds.
- **shop directory** (noun) → object shop directory. The directory `.shop/` of a repository.
- **upgrade step** (noun) → object upgrade step. One step of `migrate upgrade` from one plugin release to the next, named by its title.
- **work-item file** (noun) → object work-item file. The file `.shop/work/<initiative>/<work-item>.md` of a work-item of plugin 0.30.
- **stage directory** (noun) → object stage directory. The directory `.shop/work/<initiative>/runs/<work-item>/` of a work-item's stages.
- **initiative log** (noun) → object initiative log. The file `.shop/work/<initiative>/log.jsonl` of an initiative of plugin 0.30.
- **restated file** (noun) → object restated file. The file `spec/restated.json`, the 0.29 requirements by id.
- **frozen notice** (noun) → object frozen notice. The file `.shop/work/FROZEN.md`, which says that the queue of plugin 0.30 is frozen.
- **frozen request** (noun) → object frozen request. A request of plugin 0.30 under `.shop/work/requests/`.
- **`no upgrade step is pending`** (proper noun) → object no upgrade step is pending. What `migrate upgrade` prints when no upgrade step is pending.
- **`only on the person's yes`** (proper noun) → object only on the person's yes. The SessionStart hook's note that a session runs a pending upgrade only on the person's yes.
- **`update the plugin`** (proper noun) → object update the plugin. The SessionStart hook's note to a session in a repository on a release after the plugin's.
- **`holds no version`** (proper noun) → object holds no version. The SessionStart hook's note on a plugin version file that holds no version.
- **proposed** (adjective) → value initiative.status proposed.
- **started** (adjective) → value initiative.status started.
- **done** (adjective) → value initiative.status done.
- **abandoned** (adjective) → value initiative.status abandoned.
- **0.24.0** (noun) → value upgrade step.release 0.24.0.
- **0.25.0** (noun) → value upgrade step.release 0.25.0.
- **0.30.0** (noun) → value upgrade step.release 0.30.0.
- **0.31.0** (noun) → value upgrade step.release 0.31.0.
- **0.32.0** (noun) → value upgrade step.release 0.32.0.
- **0.33.0** (noun) → value upgrade step.release 0.33.0.
- **0.34.0** (noun) → value upgrade step.release 0.34.0.
- **open** (adjective) → value frozen request.status open.
- **awaiting-asker** (adjective) → value frozen request.status awaiting-asker.
- **awaiting-upstream** (adjective) → value frozen request.status awaiting-upstream.
- **accepted** (adjective) → value frozen request.status accepted.
- **delivered** (adjective) → value frozen request.status delivered.
- **refused** (adjective) → value frozen request.status refused.
- **withdrawn** (adjective) → value frozen request.status withdrawn.
- **asker** (attribute) → attribute frozen request.asker. The `asker:` of a frozen request, `internal` when the bounded context asked it of itself, else the id of the bounded context that asked it.
- **internal** (adjective) → value frozen request.asker internal.
- **query** (verb, action) → operation upgrades.query. Forms: queries, queried. Frame: <actor> queries <repository>.
- **upgrade** (verb, action) → operation upgrades.upgrade. Forms: upgrades, upgraded. Frame: <actor> upgrades <repository>.
- **relocate** (verb, action) → operation upgrades.relocate. Forms: relocates, relocated. Frame: <actor> relocates <bounded context>.
- **the upgrades service** (proper noun) → service upgrades.
- **context scaffold** (noun) → object context scaffold. The files founding a bounded context writes in a repository: `spec/index.md` (the id given, its last part the title, `language: codified-2`, `imports: [request]`), `spec/universal.md` (`language: codified-2`, no condition), `spec/model/`, `spec/vocabulary/`, `spec/capabilities/`, `.shop/backlog/`, `.shop/records/README.md` (an empty records index), `.shop/plugin-version` (the release of the plugin), `.shop/delivery.toml` (every key commented out at its default), `features/` and `tests/scenarios/conftest.py`, in which the check finds no violation and generation writes nothing.
- **the bounded context id form** (proper noun) → object bounded context id form. `bounded-context/<domain>/<path>`, the id of a bounded context, its last part a name.
- **context id** (noun) → object context id. The id a bounded context is founded with, as `bounded-context/<domain>/<path>`.
- **found** (verb, action) → operation upgrades.found. Forms: founds, founded. Frame: <actor> founds <bounded context>.
- **scenario conftest** (noun) → object scenario conftest. The file `tests/scenarios/conftest.py` of a repository, which pytest loads before the scenarios of its features.
- **the scenario conftest form** (proper noun) → object scenario conftest form. The text of the scenario conftest that founding a bounded context writes, which loads `work_items` so that plain pytest registers each tag of the features as a mark.
- **the old scenario conftest form** (proper noun) → object old scenario conftest form. The text of the scenario conftest that founding a bounded context wrote before 0.41.0, which does not load `work_items`.
