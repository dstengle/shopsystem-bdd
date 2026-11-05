"""The UserPromptSubmit hook's `work quote --hook` (capability conversation; workflow simplification plan 8, D5): the
session and its transcript, read from the hook's stdin, kept in `<git dir>/shopsystem/prompt.json` for `work quote`.
The git dir is the worktree's own and never tracked, so nothing is committed; the hook prints nothing, puts no tokens
in the session's context, and never fails a prompt. Standard library only."""
import datetime
import json
import os
import subprocess
from pathlib import Path

from migrate_write import top_level

POINTER = Path("shopsystem") / "prompt.json"


def git_dir(root):
    """The absolute git dir of the repository `root` is in, or None outside one."""
    try:
        done = subprocess.run(["git", "rev-parse", "--absolute-git-dir"], cwd=root, capture_output=True, text=True,
                              timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return Path(done.stdout.strip()) if done.returncode == 0 and done.stdout.strip() else None


def keep(cwd, stdin_text):
    """Write the pointer of the hook's session and transcript, when the cwd's top level has a `.shop/`; anything else
    writes nothing. Never raises."""
    try:
        given = json.loads(stdin_text)
        session, transcript = given.get("session_id"), given.get("transcript_path")
        if not isinstance(session, str) or not isinstance(transcript, str):
            return
        root = top_level(cwd)
        where = git_dir(root) if root is not None and (root / ".shop").is_dir() else None
        if where is None:
            return
        target = where / POINTER
        target.parent.mkdir(exist_ok=True)
        part = target.with_name(".%s.%d" % (target.name, os.getpid()))
        now = datetime.datetime.now(datetime.UTC).isoformat()
        part.write_text(json.dumps({"session": session, "transcript": transcript, "at": now}), encoding="utf-8")
        part.replace(target)
    except Exception:  # noqa: BLE001  (a hook never fails a prompt: D5)
        return


def kept(root):
    """(session, transcript) of the pointer the hook kept for `root`'s worktree, or None when there is none or it
    cannot be read."""
    where = git_dir(root)
    try:
        given = json.loads((where / POINTER).read_text(encoding="utf-8")) if where is not None else None
    except (OSError, ValueError):
        return None
    if not isinstance(given, dict):
        return None
    session, transcript = given.get("session"), given.get("transcript")
    return (session, transcript) if isinstance(session, str) and isinstance(transcript, str) else None
