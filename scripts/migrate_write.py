"""migrate's check of every change before it makes one, and its writing of them, all or none (migration-tools r7,
r15, r16): no move or write onto a file that is there, through a symbolic link, or under a file; and on a failure part
way, the repository put back as it was."""
import subprocess
from pathlib import Path, PurePosixPath

from migrate_layout import load_model, tracked

INDEX = "spec/decisions/index.md"


class Failed(Exception):
    """A change that failed while migrate was writing, after which it put the repository back."""


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True)


def top_level(cwd):
    """The top level of the git repository `cwd` is in, or None outside one (r1)."""
    done = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd, capture_output=True, text=True)
    return Path(done.stdout.strip()) if done.returncode == 0 else None


def uncommitted(root):
    """Each path git status shows as changed, deleted or untracked (an ignored file is not shown)."""
    out = git(root, "status", "--porcelain", "--untracked-files=all").stdout
    return [line[3:] for line in out.splitlines()]


def in_the_way(root, rel):
    """Why a file cannot be written at `rel`: a directory on the way to it is a symbolic link or not a directory, or
    it is itself a symbolic link; None when nothing is in the way."""
    parts = PurePosixPath(rel).parts
    for i in range(1, len(parts)):
        here = root.joinpath(*parts[:i])
        if here.is_symlink():
            return "%s is a symbolic link" % "/".join(parts[:i])
        if here.exists() and not here.is_dir():
            return "%s is not a directory" % "/".join(parts[:i])
    if (root / rel).is_symlink():
        return "it is a symbolic link"
    return None


def check_moves(plan):
    """Name each move that cannot be made: onto a file that exists, tracked or not, two sources to one destination, or
    where something is in the way; each new file that cannot be written: where a file is, or where a file moves; and
    each write, the decisions index included, that something is in the way of or that would replace a file git does
    not hold."""
    root = plan.root
    held = set(tracked(root))
    present = held - set(plan.moves)
    by_destination = {}
    for old, new in plan.moves.items():
        by_destination.setdefault(new, []).append(old)
    for new, sources in by_destination.items():
        if len(sources) > 1:
            plan.failures.append("could not move both %s to %s" % (" and ".join(sources), new))
        elif new in present or (new not in plan.moves and (root / new).exists()):
            plan.failures.append("could not move %s onto %s" % (sources[0], new))
        elif in_the_way(root, new):
            plan.failures.append("could not move %s to %s: %s" % (sources[0], new, in_the_way(root, new)))
    for new, purpose in plan.created.items():
        if new in by_destination:
            plan.failures.append("could not write %s for %s: %s moves there" % (new, purpose, " and ".join(by_destination[new])))
        elif new in present or (new not in plan.moves and (root / new).exists()):
            plan.failures.append("could not write %s for %s: a file is there" % (new, purpose))
    for rel in sorted(set(plan.texts) - set(by_destination)) + [INDEX]:
        why = in_the_way(root, rel)
        if why is None and rel == INDEX and INDEX not in held and INDEX not in by_destination and (root / INDEX).exists():
            why = "a file git does not hold is there"
        if why:
            plan.failures.append("could not write %s: %s" % (rel, why))


def make_parent(root, rel, made):
    """Make the directories on the way to `rel`, noting each one made."""
    missing = [p for p in (root / rel).parents if not p.exists()]
    for directory in reversed(missing):
        directory.mkdir()
        made.append(directory)


def write_all(plan, made, written):
    root = plan.root
    for old, new in plan.moves.items():
        make_parent(root, new, made)
        git(root, "mv", old, new)
    for old in plan.moves:
        parent = (root / old).parent
        while parent != root and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent
    for rel in plan.removes:
        git(root, "rm", "-q", rel)
    sources = {new: old for old, new in plan.moves.items()}
    for rel, text in list(plan.texts.items()) + [(INDEX, None)]:
        make_parent(root, rel, made)
        if not (root / rel).exists():
            written.append(root / rel)
        if text is None:        # the decisions index, as `model decisions` writes it from the decision files now there
            text = load_model().render_decisions(root)
        ending = "\r\n" if sources.get(rel, rel) in plan.crlf else "\n"
        with open(root / rel, "w", newline=ending) as handle:
            handle.write(text)
        git(root, "add", "-f", "--", rel)       # -f: a file migrate wrote is added even where git ignores it (r16)


def write(plan):
    """Make every change of `plan`; if one fails, put the repository back as it was at its last commit, which r15
    left it at, and raise Failed naming the change."""
    made, written = [], []
    try:
        write_all(plan, made, written)
    except (subprocess.CalledProcessError, OSError) as error:
        reason = error.stderr.strip() if getattr(error, "stderr", None) else str(error)
        subprocess.run(["git", "reset", "-q", "--hard", "HEAD"], cwd=plan.root, capture_output=True)
        for path in written:
            if path.is_file() and not path.is_symlink():
                path.unlink()
        for directory in reversed(made):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
        raise Failed(reason or type(error).__name__)
