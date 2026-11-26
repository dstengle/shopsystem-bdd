"""The one refusal (b145, design-decision one-refusal-path): `Refused`, the base every command's refusal reaches, so
that each tool catches it once, prints `<tool>: <reason>` and exits 1. Standard library only, and it imports nothing
of the project, so that any module can import it without a cycle.

A refusal carries, beside its message, its business `reason` and the things it `names` by business reference
(`parameter:tier`, `item:b12`, `rule:v_d6`: the domain contract design, §5.4); an old raise with a message alone
reads its message as its reason and names nothing. A message may hold `{names}`, filled with the names as each
adapter spells them (`spelled`): the core says "parameter:summary", the CLI "--summary"."""


class Refused(Exception):
    """What was asked cannot be done; the message says why, and nothing was changed."""

    def __init__(self, message="", *, reason=None, names=()):
        self.template = str(message)
        self.names = list(names)
        self.reason = reason if reason is not None else self.spelled()
        super().__init__(self.spelled())

    def spelled(self, spell=None):
        """The message, `{names}` filled with each name as `spell` gives it (None: the reference's own name)."""
        if "{names}" not in self.template:
            return self.template
        words = [(spell(name) if spell else None) or name.split(":", 1)[-1] for name in self.names]
        return self.template.replace("{names}", ", ".join(words))

    def __str__(self):
        return self.spelled()
