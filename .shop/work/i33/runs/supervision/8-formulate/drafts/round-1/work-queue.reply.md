## Coverage

| id | line | scenario |
|---|---|---|
| r32 | "**If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing." | Scenario Outline: add given an initiative that is <status> is refused, naming its status, and changes nothing (rows: done, abandoned) |
| r23 | "**When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." | Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done |
| r31 | "**If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is." | Scenario: withdraw that leaves every work-item of an initiative withdrawn leaves the initiative's status as it is |

The new r23 outline replaces both existing @r23 scenarios: the outline of the old version and "retry that makes an initiative's last open work-item green again sets the initiative to done". Both of those should be deprecated, so that r23 is formulated by one scenario.

## Questions

None.

## Cases no line mentions (no scenario written)

- An initiative with no work-items at all: r31's "every work-item is withdrawn" is then vacuously true. r23 does not set it to done anyway, so the two lines agree, but no line says so.
- A work-item that is `done` (a reviewer's answer accepted it, r27): r23 asks for every work-item to be `green` or `withdrawn`, so a `done` work-item keeps its initiative from becoming `done`. No line says whether that is intended.
- `work add` given an initiative that is `proposed`: no line says whether that is refused. Under r32 only `done` and `abandoned` are.
- `work add` given an initiative that does not exist: no line says which refusal comes first, r7's (does not exist) or r32's.
- `work retry`, `work withdraw` or `work answer` on a work-item of an initiative that is `done` or `abandoned`: r32 covers only `work add`.
- An initiative that is already `done` or `abandoned` when a command leaves all its work-items withdrawn: r31 leaves its status alone. No line says whether a later r23 condition re-sets it.

## Drafts

- /tmp/work-run-i33-9vstbbh_/supervision-8-formulate/.shop/scratch/8-formulate/drafts/round-1/work-queue/work-queue.feature
- /tmp/work-run-i33-9vstbbh_/supervision-8-formulate/.shop/scratch/8-formulate/drafts/round-1/work-queue.reply.md
