"""`work watch` (capability requests, r43, r44): a session's wait on the other side of its requests. Every `--every`
seconds it polls GitHub, through request_gh as `work sync` reads it (request_sync's `unheld_comments` and
`unheld_issues`), for the issue of each request that is not closed and for the open issues of this context's own
repository. After the first poll that finds a comment a request does not hold or an untaken ask (an issue whose body
is an `ask` no request holds), it prints one line for each and exits 0, so a session starts it in the background and
is woken when it ends: it runs `work sync`, the skill the request's turn calls for, and the watch again.

It writes nothing in the repository and commits nothing; `work sync` records. A readable comment and an untaken ask
are printed by every watch that finds them, until sync has recorded or taken them. An unreadable comment (its block of
fields missing or not parsing, as sync reads it) is never recorded by sync, so it is printed once and kept by its URL
in `<git dir>/shopsystem/watched.json` (the worktree's own git dir, as conversation_prompt keeps its pointer, never
committed), and a later watch passes over it: it does not wake the session in a loop. A poll whose gh fails is said
on stderr and tried again at the next; it does not end the watch. `--polls <n>` ends a watch that has found nothing
after n polls, exit 1: for tests and a bounded wait."""
import json
import sys
import time

import conversation_prompt
import request_form
import request_moves
import request_sync
import shop_files
from request_text import field

COMMAND = "work watch"
KEPT = ("shopsystem", "watched.json")


def kept_path(root):
    where = conversation_prompt.git_dir(root)
    return where.joinpath(*KEPT) if where is not None else None


def kept(root):
    """The URLs of the unreadable comments earlier watches printed; none when the file is missing or cannot be read."""
    path = kept_path(root)
    try:
        given = json.loads(path.read_text(encoding="utf-8")) if path is not None and path.is_file() else []
    except (OSError, ValueError):
        return set()
    return {u for u in given if isinstance(u, str)} if isinstance(given, list) else set()


def keep(root, urls):
    """`urls` added to the unreadable comments earlier watches printed, written whole (a temporary file replaced)."""
    path = kept_path(root)
    if path is None:
        return
    path.parent.mkdir(exist_ok=True)
    part = path.with_name(".%s.part" % path.name)
    part.write_text(json.dumps(sorted(kept(root) | set(urls))), encoding="utf-8")
    part.replace(path)


def is_ask(body):
    try:
        form = request_form.parse(body)
    except request_form.Unreadable:
        return False
    return form is not None and form.step == "ask"


def is_readable(body):
    try:
        return request_form.parse(body) is not None
    except request_form.Unreadable:
        return False


def comment_number(url):
    return url.rsplit("#issuecomment-", 1)[1] if "#issuecomment-" in url else url


def found(root):
    """[(URL, line, unreadable)] of one poll: each comment a live request does not hold, and each untaken ask."""
    out = []
    for name, status, _, _ in request_moves.requests(root):
        if status in request_sync.CLOSED:
            continue
        text = shop_files.read(request_moves.path_of(root, name), root)
        issue = field(text, "issue")
        if not issue:
            continue
        for url, body in request_sync.unheld_comments(root, text, COMMAND):
            line = "%s %s comment %s: %s (`work sync` records it)" % (name, issue, comment_number(url), url)
            out.append((url, line, not is_readable(body)))
    for url, title, body in request_sync.unheld_issues(root, COMMAND):
        if is_ask(body):
            out.append((url, "ask %s %s (`work sync` takes it in)" % (url, " ".join(title.split())), False))
    return out


def report(root):
    """One check: what it finds printed and its unreadable comments kept, True; nothing new, False. A gh that fails
    is refused (shop_files.Refused)."""
    before = kept(root)
    new = [(url, line, bad) for url, line, bad in found(root) if not (bad and url in before)]
    if not new:
        return False
    unreadable = [url for url, _, bad in new if bad]
    if unreadable:
        keep(root, unreadable)
    for _, line, _ in new:
        print(line)
    return True


def watch(root, every=60, polls=None, sleep=time.sleep):
    """Poll until something is found: print it, keep the unreadable comments, 0; nothing after `polls` polls: 1."""
    done = 0
    while True:
        try:
            if report(root):
                return 0
        except shop_files.Refused as refused:
            print("%s; polling again in %ss" % (refused, every), file=sys.stderr)
        done += 1
        if polls is not None and done >= polls:
            print("%s: nothing new after %d poll%s" % (COMMAND, done, "" if done == 1 else "s"), file=sys.stderr)
            return 1
        sleep(every)
