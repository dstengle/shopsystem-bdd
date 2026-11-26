---
id: model/missingmass.io/shopsystem/shopsystem-bdd/analysis
area: analysis
kind: generic
imports: [specification, tracking, upgrades]
---

# Codebase analysis

## Purpose

The codebase read: the toolchain, test coverage, references, lint, file size, and the Gherkin of feature files.

```model
object Python interpreter kind of file
  attributes: environment: virtualenv | system

object analysis tool
  attributes: presence: installed | missing | uninstallable
  relations: has → version | pip command | heading | finding (many)

object pip command kind of text

object coverage map kind of file
  attributes: revision (text)
  relations: has → kept change (many); holds → test (many)

object Python file kind of file
  relations: has → function (many); holds → test (many); defines → identifier (many); exceeds → size limit (many)
  relations: differs from → base branch (one)
  relations: imports → Python file (many)

object function kind of identifier

object identifier

object reference
  relations: to → identifier (many)

object finding kind of text

object heading kind of text

object log line kind of text

object size limit

object dependency file kind of file

object feature file kind of file
  relations: has → docstring | tag | scenario outline | rule block | scenario (many)

object test module kind of file
  relations: has → binding (many)

object subdirectory kind of file
  relations: holds → feature file (many)

object docstring kind of text
  relations: holds → tag | scenario line (many)

object tag kind of text

object requirement tag kind of text

object scenario line kind of text

object scenario outline kind of text
  relations: has → examples row (many)

object examples row kind of text

object rule block kind of text

object scenario title kind of text

object replacement kind of scenario

object binding kind of text
  relations: binds → scenario (many)

object scenarios call kind of binding

object search text kind of text

object handler

object ruff kind of analysis tool

object vulture kind of analysis tool

object coverage kind of analysis tool

object jedi kind of analysis tool

object gf-rgl kind of analysis tool

object toolchain

service toolchain
  operation probe(toolchain, Python interpreter, log (flag))  outcomes: returned → the toolchain | failed → each missing analysis tool
  operation install(toolchain)  outcomes: done | refused: analysis tool missing outside a virtualenv, analysis tool uninstallable

service code analysis
  operation map(repository)  outcomes: done → the coverage map
  operation trace(identifier, file view (flag))  outcomes: returned | refused: identifier undefined, coverage map missing, analysis tool missing
  operation screen(Python file)  outcomes: returned
  operation locate(identifier)  outcomes: returned | refused: identifier undefined, analysis tool missing
  operation lint(file, repository)  outcomes: returned → the findings | failed → each finding
  operation size(repository, size limit)  outcomes: passed | failed → each Python file over the size limit

service feature reading
  operation search(repository, tag, scenario title, search text)  outcomes: returned
  operation count(feature file)  outcomes: returned | refused: feature file with a rule block
  operation scan(repository)  outcomes: returned
  operation vet(repository, unbound listing (flag))  outcomes: passed | failed → each unbound scenario or binding

object base branch
  relations: holds → kept change (many)
```
