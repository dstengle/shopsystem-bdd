"""What the plugin's UserPromptSubmit hook (`migrate prompting`) tells a session about the repository's requests
(requests r72): that a delegation the person gives for a request is written, in the same reply, with `work delegate`.

It speaks only when the repository keeps a request that is not delivered, refused or withdrawn, and always exits 0: a
hook's failure must not stop a session.
"""
import sys
from pathlib import Path

import workqueue
from migrate_write import top_level

ENDED = ("delivered", "refused", "withdrawn")


def prompting(root):
    """What the session is told at `root`; '' when the repository keeps no request whose negotiation has not ended."""
    try:
        names = [name for name, status, _, _ in workqueue.requests(root) if status not in ENDED]
    except workqueue.Refused:
        return ""
    if not names:
        return ""
    return ("This repository keeps the requests %s. When the person gives you a delegation for one of them (which "
            "questions you may answer in their place) outside `work request`, then in that same reply write it with "
            "`work delegate <request> \"<delegation>\"` (python3 %s delegate), the delegation being "
            "The person, <date>: \"<the person's words>\" with today's date.\n"
            % (", ".join(names), Path(__file__).resolve().parent / "work"))


def run():
    """`migrate prompting`: the UserPromptSubmit hook, always exit 0."""
    root = top_level(Path.cwd())
    if root is not None:
        sys.stdout.write(prompting(root))
    return 0
