"""`work watch --hook` (capability requests, r54-r56), the SessionStart hook of the requests: the requests that wait on
the other side, so that a session starts the watch a session that ended had left. A sent request (request_side's: this
repository asked another context) waits on the other side while it is `awaiting-upstream`, a received one (this
repository is its upstream, another context asked) while it is `awaiting-asker`. The hook prints one line for each such request and
a line telling the session to start `work watch --forward` with the Monitor tool; with none it prints nothing. It reads
only the records under .shop/requests/, never GitHub, and writes nothing. Whatever goes wrong, it prints nothing and
exits 0: a hook never fails a session's start (as conversation_hook)."""
import re

import request_moves
import request_side
import shop_files
from request_text import field

START = ("A request waits on the other side: start `work watch --forward` with the Monitor tool, and run `work sync` "
         "when it wakes.")


def waiting(root, text, status):
    """Whether the record `text` with `status` waits on the other side: sent and `awaiting-upstream`, or received and
    `awaiting-asker`."""
    return status == "awaiting-upstream" and request_side.sent(root, text)


def title(text):
    found = re.search(r"(?m)^# (.+)$", text)
    return found.group(1).strip() if found else ""


def lines(root):
    """One line for each request that waits on the other side: its name, status, title and issue."""
    out = []
    for name, status, _, _ in request_moves.requests(root):
        text = shop_files.read(request_moves.path_of(root, name), root)
        if waiting(root, text, status):
            issue = field(text, "issue")
            out.append("%s %s: %s%s" % (name, status, title(text), " (%s)" % issue if issue else ""))
    return out


def hook(root):
    """Print the waiting requests and the line to start the watch; nothing with none. Never raises; 0."""
    try:
        found = lines(root)
        if found:
            print("\n".join(found + [START]))
    except BaseException:  # noqa: BLE001  (a hook never fails a session's start)
        return 0
    return 0
