"""The one refusal (b145, design-decision one-refusal-path): `Refused`, the base every command's refusal reaches, so
that each tool catches it once, prints `<tool>: <reason>` and exits 1. Standard library only, and it imports nothing
of the project, so that any module can import it without a cycle."""


class Refused(Exception):
    """What was asked cannot be done; the message says why, and nothing was changed."""
