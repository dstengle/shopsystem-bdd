---
id: model/missingmass.io/shopsystem/shopsystem-bdd/measurement
area: measurement
kind: generic
imports: [execution, tracking, specification]
---

# Measurement

## Purpose

What work cost: the measurement of a merged batch, the defects found after it, and trials.

```model
object dispatch kind of session

object compaction

object measurement kind of record
  relations: has → stage row | total row | session row (many); holds → tool use | compaction (many); includes → measurement (many)

object trial
  relations: has → target | measurement (many)

object defect kind of file
  relations: for → batch (many)

object stage row kind of text
  relations: has → round trip (many)

object total row kind of text

object round trip

object session row kind of text
  relations: has → round trip | tool use | dispatch | compaction (many)

object tool use

object wall time

object session time

object token

object role kind of text
  relations: has → cost (many)

object cost

object ratio kind of text

object target
  relations: holds → file (many)

object reply kind of text

object trial-runner kind of session

service measurement
  operation measure(batch)  outcomes: done → the measurement
  operation report(defect, item)  outcomes: done → the defect
  operation view(measurement)  outcomes: returned → the measurement
  operation compare(measurement)  outcomes: returned
  operation conduct(trial)  outcomes: done → the measurement
  operation hand(trial, session)  outcomes: done
```
