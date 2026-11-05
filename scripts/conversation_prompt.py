"""The UserPromptSubmit hook's `work quote --hook` (capability conversation; workflow simplification plan 8, D5): the
session and its transcript, read from the hook's stdin, kept in `<git dir>/shopsystem/prompt.json` for `work quote`.
The git dir is the worktree's own and never tracked, so nothing is committed; the hook prints nothing, puts no tokens
in the session's context, and never fails a prompt. A prompt whose `cwd` is in another repository is not kept (plan 8's
review, Q3). Standard library only."""
import datetime
import json
import os
import subprocess
from pathlib import Path

from migrate_write import top_level

POINTER = Path("shopsystem") / "prompt.json"


class Unreadable(Exception):
    """The pointer is there but cannot be read; its path is the argument."""


def git_dir(root):
    """The absolute git dir of the repository `root` is in, or None outside one."""
    try:
        done = subprocess.run(["git", "rev-parse", "--absolute-git-dir"], cwd=root, capture_output=True, text=True,
                              timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return Path(done.stdout.strip()) if done.returncode == 0 and done.stdout.strip() else None


def keep(cwd, stdin_text):
    """Write the pointer of the hook's session and transcript, when the cwd's top level has a `.shop/` and the cwd
    stdin gives, if any, is in that top level; anything else writes nothing. Never raises."""
    part = None
    try:
        given = json.loads(stdin_text)
        session, transcript = given.get("session_id"), given.get("transcript_path")
        if not isinstance(session, str) or not isinstance(transcript, str):
            return
        root = top_level(cwd)
        where = git_dir(root) if root is not None and (root / ".shop").is_dir() else None
        said = given.get("cwd")
        if where is None or (isinstance(said, str) and top_level(said) != root):
            return
        target = where / POINTER
        target.parent.mkdir(exist_ok=True)
        part = target.with_name(".%s.%d" % (target.name, os.getpid()))
        now = datetime.datetime.now(datetime.UTC).isoformat()
        part.write_text(json.dumps({"session": session, "transcript": transcript, "at": now}), encoding="utf-8")
        part.replace(target)
    except Exception:  # noqa: BLE001  (a hook never fails a prompt: D5)
        if part is not None:
            try:
                part.unlink(missing_ok=True)
            except OSError:
                pass


def kept(root):
    """(session, transcript) of the pointer the hook kept for `root`'s worktree, or None when there is none; raises
    Unreadable when it is there but cannot be read."""
    where = git_dir(root)
    if where is None or not (where / POINTER).exists():
        return None
    try:
        given = json.loads((where / POINTER).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise Unreadable(where / POINTER) from None
    session, transcript = (given.get("session"), given.get("transcript")) if isinstance(given, dict) else (None, None)
    if not isinstance(session, str) or not isinstance(transcript, str):
        raise Unreadable(where / POINTER)
    return session, transcript
