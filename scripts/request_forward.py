"""`work watch --forward` (capability requests, r57, r58): the watch woken by GitHub's events, not a poll of the issues.

The repositories it watches are those of the issues of the requests that are not closed and this context's own
(request_gh), read again at each wake, so that a request raised meanwhile is watched too. On a repository the account
administers (`gh repo view --json viewerPermission` says ADMIN) it runs `gh webhook forward` (the cli/gh-webhook
extension, installed when `gh extension list` does not name it) for the `issues` and `issue_comment` events to a
listener on a port of 127.0.0.1. Elsewhere (an upstream's repository, when this context is the asker), or when gh
cannot forward (the extension will not install, or the forward ends), it polls GitHub's notifications instead
(`GET /notifications` with If-Modified-Since, at the interval its X-Poll-Interval asks; a 304 costs no rate limit),
and says on stderr which repositories it polls.

At its start, once the forwards run, it checks once as `work watch` polls (request_watch's `report`), for what came
while no watch ran; then each event, and each notification of a polled repository, wakes the same check. What it
finds it prints, and it exits 0, as `work watch` does: it writes nothing in the repository. One wait lasts at most
`--every` seconds; `--polls <n>` ends a watch that has found nothing after n waits, exit 1. The forwards end with it.
"""
import email.utils
import http.server
import json
import os
import queue
import re
import shlex
import subprocess
import sys
import threading
import time

import batch_gh
import request_gh
import request_moves
import request_sync
import request_watch
import shop_files
from request_text import field

COMMAND = "work watch"
EVENTS = "issues,issue_comment"
EXTENSION = "cli/gh-webhook"


def gh_argv():
    return shlex.split(os.environ.get(batch_gh.GH) or "gh")


def repos(root):
    """The GitHub repositories watched: this context's own, then each live request's issue's, in order, once each."""
    out = []
    try:
        out.append(request_gh.own_repo(root, COMMAND))
    except shop_files.Refused:
        pass
    for name, status, _, _ in request_moves.requests(root):
        issue = "" if status in request_sync.CLOSED else field(
            shop_files.read(request_moves.path_of(root, name), root), "issue") or ""
        found = re.match(r"https://github\.com/(%s)/issues/\d+" % request_gh.REPO, issue)
        if found and found.group(1) not in out:
            out.append(found.group(1))
    return out


def administered(root, repo):
    try:
        out = batch_gh.gh(root, "repo", "view", repo, "--json", "viewerPermission", command=COMMAND)
        return json.loads(out).get("viewerPermission") == "ADMIN"
    except (shop_files.Refused, ValueError, AttributeError):
        return False


def installed(root):
    """The cli/gh-webhook extension, installed when gh does not list it; False when it cannot be."""
    try:
        if EXTENSION in batch_gh.gh(root, "extension", "list", command=COMMAND):
            return True
        batch_gh.gh(root, "extension", "install", EXTENSION, command=COMMAND)
        return True
    except shop_files.Refused as refused:
        print("%s; GitHub's events cannot be forwarded" % refused, file=sys.stderr)
        return False


def listener(events):
    """An HTTP server on a port of 127.0.0.1, in a thread, that puts each event's repository on `events`."""
    class Events(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
            try:
                repo = (json.loads(body).get("repository") or {}).get("full_name")
            except (ValueError, AttributeError):
                repo = None
            events.put(repo)
            self.send_response(200)
            self.end_headers()

        def log_message(self, *args):
            pass
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Events)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


class Notifications:
    """GitHub's notifications, polled with If-Modified-Since at the interval GitHub asks (at least `floor` seconds)."""

    def __init__(self, root, floor=60):
        self.root, self.since, self.interval, self.due = root, None, floor, 0.0

    def changed(self, polled):
        """Whether a notification of a repository in `polled` came since the last call; the first call is the
        baseline, and a call before the interval asked for, or a gh that fails, is no change."""
        if time.time() < self.due:
            return False
        args = ["api", "--include", "notifications"]
        if self.since:
            args[1:1] = ["-H", "If-Modified-Since: %s" % self.since]
        try:
            done = subprocess.run([*gh_argv(), *args], cwd=self.root, capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired) as err:
            print("%s: gh api notifications failed: %s" % (COMMAND, err), file=sys.stderr)
            return False
        head, _, body = done.stdout.replace("\r\n", "\n").partition("\n\n")
        status = re.match(r"HTTP/\S+ (\d{3})", head)
        if not status:
            print("%s: gh api notifications failed: %s" % (COMMAND, (done.stderr.strip() or "no status")
                                                          .splitlines()[0]), file=sys.stderr)
            return False
        headers = {k.strip().lower(): v.strip() for k, _, v in
                   (line.partition(":") for line in head.splitlines()[1:])}
        interval = headers.get("x-poll-interval", "")
        self.due = time.time() + (int(interval) if interval.isdigit() else self.interval)
        if status.group(1) != "200":
            return False
        first, self.since = self.since is None, headers.get("last-modified") or email.utils.formatdate(usegmt=True)
        try:
            listed = json.loads(body or "[]")
        except ValueError:
            return False
        return not first and any((n.get("repository") or {}).get("full_name") in polled for n in listed
                                 if isinstance(n, dict))


class Watched:
    """The repositories watched: each forwarded (its gh process) or polled."""

    def __init__(self, root, port):
        self.root, self.port, self.forwards, self.polled, self.can = root, port, {}, [], None

    def arm(self):
        """Each repository not yet watched forwarded, or polled; a forward that ended polled; said on stderr."""
        new = []
        for repo, proc in list(self.forwards.items()):
            if proc.poll() is not None:
                del self.forwards[repo]
                new.append(repo)
        for repo in repos(self.root):
            if repo in self.forwards or repo in self.polled or repo in new:
                continue
            if administered(self.root, repo) and self.installed():
                self.forwards[repo] = subprocess.Popen(
                    [*gh_argv(), "webhook", "forward", "--repo", repo, "--events", EVENTS,
                     "--url", "http://127.0.0.1:%d/" % self.port], cwd=self.root, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, start_new_session=True)
            else:
                new.append(repo)
        if new:
            self.polled.extend(new)
            print("%s: polling GitHub's notifications for %s" % (COMMAND, ", ".join(new)), file=sys.stderr)

    def installed(self):
        if self.can is None:
            self.can = installed(self.root)
        return self.can

    def end(self):
        for proc in self.forwards.values():
            if proc.poll() is None:
                proc.terminate()
        for proc in self.forwards.values():
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


def check(root):
    try:
        return request_watch.report(root)
    except shop_files.Refused as refused:
        print("%s; waiting again" % refused, file=sys.stderr)
        return False


def forward(root, every=60, polls=None):
    """Wait on GitHub's events; print what a wake finds, 0; nothing after `polls` waits: 1."""
    events = queue.Queue()
    server = listener(events)
    watched = Watched(root, server.server_address[1])
    notes = Notifications(root)
    try:
        watched.arm()
        if check(root):
            return 0
        done = 0
        while True:
            try:
                events.get(timeout=every)
                woke = True
            except queue.Empty:
                woke = False
            watched.arm()
            woke = bool(watched.polled and notes.changed(watched.polled)) or woke
            if woke and check(root):
                return 0
            done += 1
            if polls is not None and done >= polls:
                print("%s: nothing new after %d wait%s" % (COMMAND, done, "" if done == 1 else "s"), file=sys.stderr)
                return 1
    finally:
        watched.end()
        server.shutdown()
