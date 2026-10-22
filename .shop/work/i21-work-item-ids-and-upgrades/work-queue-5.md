---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-5
kind: work-item
part_of: capability-proposal/ids-work-queue
status: awaiting-ruling
under: work-queue
accepts: [work-queue#r1, work-queue#r12]
---

# work-queue-5

Readings settled by the coordinator under the person's delegation (formulation round f1): `<n>` is read from the file name `w<n>.md`. The unchanged work-queue scenarios that still call `work add i1 w1 ...` take `w1` as the title under the new r1; they stay as they are and must pass.

## Questions
- The deprecated scenarios 'add when the work-item's file already exists leaves the file as it was (deprecated)' (@r2) and '... is refused, saying so, with an error (deprecated)' (@r7) are 'Deprecated for: removal', but work-queue-5 has no Retires section, so the implementer may not retire them, and under r1/r12 neither can pass as it is. Reading A: the work-item gains a Retires section listing both, and they are removed with features retire. The narrator who runs `work add i1 w1 ...` beside an existing w1 sees w2.md written with the heading w1, `w2` printed, and exit 0. Reading B: they stay and must pass. add refuses a title equal to an existing work-item's id, so the narrator sees 'the work-item w1 already exists', an error exit and nothing changed, while any other title is numbered as r12 says.

Ruled by the coordinator under the person's delegation (2026-10-22) and finished by a direct bdd-implementer, merged in 4456bb7 (0.24.0): `work rule` is not yet there. Withdrawn from `work run` for that reason, its requirements built.
