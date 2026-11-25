"""Tracking's operations on an item's lifecycle (decision 0133, b578; items r56-r59): `allocate` (ready -> in-batch),
`deliver` (in-batch -> delivered), `restore` (in-batch -> ready), `suspend` (in-batch -> needs-input, its question
under `## Question`) and `reopen` (ready -> shaped, with the note why), each a move of backlog_moves' rows, refused
with the reason the domain model declares of it (item not ready, item not in-batch: items r60-r63).

Execution changes an item's status only through these: each applies its move to an item in memory, refused naming
the item when its status is not the move's, so that a batch's command commits the items it moved with its plan in
one commit. `work allocate`, `work deliver`, `work restore` and `work suspend` request them of one item, one commit
of its file."""
import backlog_items
import backlog_moves

# The refusal reasons the domain model declares of these operations (spec/model/tracking.md; items r60-r63).
NOT_READY = "item not ready"
NOT_IN_BATCH = "item not in-batch"


def allocate(item):
    """The item given to a batch's work: `ready` -> `in-batch` (items#r59)."""
    return backlog_moves.moved(item, "work allocate", reason=NOT_READY)


def deliver(item):
    """The item's change in the product: `in-batch` -> `delivered` (items#r56)."""
    return backlog_moves.moved(item, "work deliver", reason=NOT_IN_BATCH)


def restore(item):
    """The item back to wait for a batch: `in-batch` -> `ready` (items#r57)."""
    return backlog_moves.moved(item, "work restore", reason=NOT_IN_BATCH)


def suspend(item, question, note=None):
    """The item waiting on an answer: `in-batch` -> `needs-input`, the question kept on it under `## Question`
    (items#r58), and `note` under its `## Notes`."""
    question = backlog_moves.text_line(question, "question")

    def write(found):
        found.sections["Question"] = question
        backlog_moves.add_note(found, note)
    return backlog_moves.moved(item, "work suspend", write, reason=NOT_IN_BATCH)


def reopen(item, note=None):
    """The item back to shaped so that its lines can change: `ready` -> `shaped` (items#r31), `note` under its
    `## Notes`."""
    return backlog_moves.moved(item, "work reopen", lambda found: backlog_moves.add_note(found, note),
                              reason=NOT_READY)


def add_parsers(sub):
    for verb, says in (("allocate", "move an item that is ready to in-batch: it is given to a batch's work"),
                       ("deliver", "move an item that is in-batch to delivered: its change is in the product"),
                       ("restore", "move an item that is in-batch back to ready, to wait for a batch"),
                       ("suspend", "move an item that is in-batch to needs-input, with its question")):
        p = sub.add_parser(verb, help=says)
        p.add_argument("name")
        if verb == "suspend":
            p.add_argument("--question", required=True, help="what the item waits on, under its ## Question")


def _command(verb):
    def run(args):
        change = (lambda item: suspend(item, args.question)) if verb == "suspend" else globals()[verb]
        item = backlog_items.find(args.root, args.name)
        before = change(item)
        backlog_items.commit(args.root, item, "work %s: %s %s -> %s" % (verb, backlog_items.label(item), before,
                                                                       item.status))
        print("%s %s" % (backlog_items.label(item), item.status))
        return 0
    return run


COMMANDS = {verb: _command(verb) for verb in ("allocate", "deliver", "restore", "suspend")}
