"""The tests that failed in a task's last `work batch done`, run first by its next one (b474).

A refused `done` keeps the ids pytest's short summary names (`FAILED <id>`, `ERROR <id>`) in the git dir,
`<git common dir>/shopsystem-bdd/rerun/<key>`, never committed. The next `done` of that task runs those ids first: a
fix that still fails is refused in seconds; once they pass, the whole of `[batch] tests` is run, and a pass forgets
them. A focused run that fails naming no test (an id gone, a usage error) falls back to the whole run."""
import re

from batch_git import common_dir

SUMMARY = re.compile(r"^(?:FAILED|ERROR) (\S.*?)(?: - .*)?$")


def failed(output):
    """The ids of the tests pytest's short summary names failed or in error, in its order, each once."""
    found = []
    for line in output.splitlines():
        match = SUMMARY.match(line.rstrip())
        if match and match.group(1) not in found:
            found.append(match.group(1))
    return found


def where(root, key):
    return common_dir(root) / "shopsystem-bdd" / "rerun" / key


def kept(root, key):
    path = where(root, key)
    return path.read_text().split("\n")[:-1] if path.is_file() else []


def keep(root, key, ids):
    """`ids` kept for the task `key`; none forgets what was kept."""
    path = where(root, key)
    if not ids:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(i + "\n" for i in ids))


def tests(root, key, run):
    """(command, completed process) of the task's tests: `run(args)` runs `[batch] tests` with `args` after it; the
    kept ids first, then, once they pass, the whole run, whose failures are kept."""
    ids = kept(root, key)
    if ids:
        command, done = run(ids)
        again = failed(done.stdout + done.stderr)
        if done.returncode != 0 and again:
            keep(root, key, again)
            return command, done
    command, done = run(())
    keep(root, key, failed(done.stdout + done.stderr) if done.returncode != 0 else [])
    return command, done
