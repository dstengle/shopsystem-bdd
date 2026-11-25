---
id: model/missingmass.io/shopsystem/shopsystem-bdd/upgrades
area: upgrades
kind: generic
imports: [specification, tracking]
---

# Upgrades

## Purpose

A repository moved between plugin releases: its upgrade steps, pending and applied.

```model
object initiative
  attributes: status: proposed | started | done | abandoned
  relations: fulfils → context request (many)

object tracked file kind of file
  relations: has → stem (many)

object uncommitted change kind of text

object old-layout directory kind of file
  relations: holds → tracked file (many)

object decision ledger kind of file
  relations: has → ledger entry (many)

object ledger entry kind of text
  relations: has → qualifier | ledger number | stem | design-decision (many)

object qualifier kind of text

object ledger number kind of text

object stem kind of text

object Behaviour line kind of text
  relations: has → line id (many)

object line id kind of text

object plugin version file kind of file
  relations: holds → version (many); has → content (many)

object content kind of text

object shop directory kind of file

object upgrade step
  attributes: release: 0.24.0 < 0.25.0 < 0.30.0 < 0.31.0 < 0.32.0 < 0.33.0 < 0.34.0

object work-item file kind of file

object stage directory kind of file

object initiative log kind of file

object restated file kind of file

object frozen notice kind of file

object frozen request kind of file
  attributes: status: open | awaiting-asker | awaiting-upstream | accepted | delivered | refused | withdrawn; asker: internal

object index file kind of file
  relations: has → context purpose (one)
  relations: holds → capability (many)

object plugin
  attributes: release: 0.34.1 < 0.99.0
  relations: pins → version (many)

object no upgrade step is pending kind of text

object only on the person's yes kind of text

object update the plugin kind of text

object holds no version kind of text

service upgrades
  operation query(repository)  outcomes: returned → the release and every pending upgrade step | refused: content not a version
  operation upgrade(repository)  outcomes: done | refused: uncommitted change
  operation relocate(bounded context)  outcomes: done | refused: uncommitted change, tracked file of a ledger stem
  operation found(bounded context, context id, context purpose)  outcomes: done | refused: bounded context with no context id, context id not a bounded context id, index file present, shop directory present

object context scaffold kind of file

object context id kind of text

object bounded context id form kind of artifact

object scenario conftest kind of tracked file

object scenario conftest form kind of artifact

object old scenario conftest form kind of artifact

object ignore file kind of tracked file

object ignore file form kind of artifact

object context purpose kind of text
```
