"""`work run`'s pool of workers (capability supervision): which work-items get a worker, how many run at the same time, and
the order in which implementers that ended have their branches merged. Standard library only; a part of supervise.Run."""
import fnmatch
import threading
import tomllib

import workqueue
from supervise_worker import git
from workqueue import Refused

WORKERS = 4      # the number of workers when .shop/delivery.toml gives none (r60)


def claimed(entry, tracked):
    """What one file set entry claims: itself, and each of the `tracked` files it matches as a glob or holds as a
    directory."""
    under = entry.rstrip("/") + "/"
    return {entry} | {f for f in tracked if fnmatch.fnmatchcase(f, entry) or f.startswith(under)}


def overlap(first, second):
    """Whether two claims share a file; a claim of None is every file, one of no file is the empty set."""
    if first is None:
        return second is None or bool(second)
    if second is None:
        return bool(first)
    return bool(first & second)


class Pool:
    """The part of supervise.Run that decides who is worked on, side by side, and in which order the merges go."""

    def read_delivery(self):
        """.shop/delivery.toml, once and before anything changes; a Refused (r10) when it cannot be read as TOML or its
        `workers` is no positive integer."""
        path = self.root / ".shop" / "delivery.toml"
        try:
            self.delivered = tomllib.loads(path.read_text()) if path.is_file() else {}
        except (tomllib.TOMLDecodeError, UnicodeDecodeError) as error:
            raise Refused("%s cannot be read: %s" % (self.rel(path), error)) from error
        workers = self.delivered.get("workers", WORKERS)
        if isinstance(workers, bool) or not isinstance(workers, int) or workers < 1:
            raise Refused("workers in %s is %r, not a positive integer" % (self.rel(path), workers))
        self.limit = workers
        self.slots = threading.Semaphore(workers)

    def blocked(self, name, statuses):
        """Whether `name` is blocked_by a work-item that is not green (r63); a blocker is named by its id or its name."""
        data, _ = workqueue.frontmatter((self.dir / (name + ".md")).read_text())
        by = data.get("blocked_by") or []
        return any(statuses.get(str(b).rsplit("/", 1)[-1]) != "green" for b in (by if isinstance(by, list) else [by]))

    def claim(self, name, tracked):
        """The files the implementer of `name` would edit: its file set's, else None (every file)."""
        data, _ = workqueue.frontmatter((self.dir / (name + ".md")).read_text())
        if not data.get("fileset"):
            return None
        return {f for entry in data["fileset"] for f in claimed(entry, tracked())}

    def choose(self, running, movable):
        """The work-items to start now, in the queue's order, while fewer workers than the limit run (r59, r60): not a
        blocked one (r63), and an implementer only when its claim shares no file with that of one running (r20)."""
        statuses = {name: status for _, name, status in workqueue.items(self.root)}
        statuses.update(self.items())     # this initiative's reading wins for a name more than one holds
        tracked = {}

        def files():
            if "files" not in tracked:
                tracked["files"] = git(self.root, "ls-files").stdout.splitlines()
            return tracked["files"]
        chosen = []
        for name, status in self.items():
            if status not in movable or name in running or self.blocked(name, statuses):
                continue
            if status == "planned":
                chosen.append((name, status))     # a move only, no worker
                continue
            if len(running) >= self.limit:
                break
            claim = self.claim(name, files) if status == "ready" else set()
            if any(overlap(claim, other) for other in running.values()):
                continue
            running[name] = claim
            chosen.append((name, status))
        return chosen

    def pull(self, movable):
        """Start a worker for every work-item that can move, side by side, until none can and none runs; a fault ends the
        starting, and the workers running end first (r40). A failure other than a fault is raised once they have."""
        running, ended, errors = {}, [], []
        done = threading.Condition()

        def work(name, status):
            try:
                self.step(name, status)
            except Exception as error:     # noqa: BLE001 -- carried to the run's own thread, which ends with it (r10)
                errors.append(error)
            finally:
                with done:
                    ended.append(name)
                    done.notify_all()
        threads = []
        while True:
            with done:
                for name in ended:
                    running.pop(name, None)
                ended.clear()
            chosen = [] if self.faults or errors else self.choose_locked(running, movable)
            for name, status in chosen:
                if status == "planned":
                    try:
                        self.step(name, status)
                    except Exception as error:     # noqa: BLE001 -- as above
                        errors.append(error)
                    continue
                threads.append(threading.Thread(target=work, args=(name, status)))
                threads[-1].start()
            if chosen:
                continue
            with done:
                if not running:
                    break
                done.wait_for(lambda: ended)
        for thread in threads:
            thread.join()
        if errors:
            raise errors[0]

    def choose_locked(self, running, movable):
        with self.lock:     # the files are not read half written
            return self.choose(running, movable)

    def await_turn(self, name):
        """Wait until `name`'s implementer is the first of those that ended and have not been merged (r61)."""
        with self.turns:
            self.turns.wait_for(lambda: self.finished and self.finished[0] == name)

    def release(self, name):
        """`name`'s implementer is merged, or is not to be; the next one that ended has its turn."""
        with self.turns:
            if name in self.finished:
                self.finished.remove(name)
            self.turns.notify_all()
