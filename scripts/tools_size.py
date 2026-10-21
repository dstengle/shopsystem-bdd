"""tools size: the tracked Python files over a line limit, as the working tree has them."""
import subprocess
import sys

DEFAULT_LIMIT = 300


def tracked():
    """The tracked paths, read from git NUL-separated so a name with a space is whole."""
    done = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True)
    if done.returncode != 0:
        sys.stderr.write(done.stderr)
        sys.exit(1)
    return sorted(path for path in done.stdout.split("\0") if path)


def is_python(path):
    if path.endswith(".py"):
        return True
    try:
        with open(path, "rb") as handle:
            first = handle.readline(200)
    except OSError:
        return False
    return first.startswith(b"#!") and b"python" in first


def line_count(path):
    with open(path, "rb") as handle:
        data = handle.read()
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def cmd_size(args):
    over = 0
    for path in tracked():
        try:
            if not is_python(path):
                continue
            count = line_count(path)
        except OSError:  # deleted in the working tree: the scenarios are silent
            continue
        if count > args.limit:
            print("%s %d" % (path, count))
            over += 1
    return 1 if over else 0
