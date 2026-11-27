"""A feature written by the generator the tree holds (b740, batches r170): a tree that holds the plugin's own feature
generator (`scripts/features` and `scripts/features_generate.py`: the repository is the plugin, and a batch's
workspace may hold a newer generator than the checkout a command runs in) has its features written by that tree's
`scripts/features generate --root <tree>`, run with this interpreter in a process of its own; any other tree (a
consumer's, whose generator is the plugin's own) by features_generate in this process. Read by laying_inprocess's
prepare and lift and by batch_reached, so `work batch start`, `park` and `amend` all write with the tree's
generator. A run that outlasts its time limit (`$SHOPSYSTEM_GENERATE_TIMEOUT` seconds, default 600) or cannot be
started is a GenerateError naming the feature generator (`Unresponsive`, b871), which those commands refuse with (b749, batches r175,
r176)."""
import contextlib
import io
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import features_generate

TIMEOUT = 600


class Unresponsive(features_generate.GenerateError):
    """A run of the tree's generator that outlasts its time limit or cannot start: the feature generator
    unresponsive (b871), the refusal reason of the specification service's apply."""

    def __init__(self, message, program):
        super().__init__(message)
        self.program = str(program)


def _timeout():
    """The time limit of a run of the tree's generator, in seconds."""
    try:
        return float(os.environ.get("SHOPSYSTEM_GENERATE_TIMEOUT", TIMEOUT))
    except ValueError:
        return TIMEOUT


def _program(tree):
    """The tree's own `scripts/features`, or None when it holds no generator of its own."""
    scripts = Path(tree) / "scripts"
    found = scripts / "features"
    return found if found.is_file() and (scripts / "features_generate.py").is_file() else None


def _run(program, *args):
    """The tree's `features` run with this interpreter, its own scripts first on its path (none inherited); a run
    that outlasts its time limit or cannot start a GenerateError naming the feature generator and why."""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    limit = _timeout()
    try:
        return subprocess.run([sys.executable, str(program), *args], capture_output=True, text=True, env=env,
                              timeout=limit, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        raise Unresponsive("the feature generator %s timed out after %g s" % (program, limit), program) from None
    except OSError as err:
        raise Unresponsive("the feature generator %s could not start: %s" % (program, err), program) from None


def generate(tree, path):
    """The feature of the capability file `path` as the tree's generator writes it; GenerateError when it refuses."""
    program = _program(tree)
    if program is None:
        with contextlib.redirect_stderr(io.StringIO()):     # the groups it skips are the bar's to name
            return features_generate.generate(tree, path)
    done = _run(program, "generate", "--root", str(tree), "--preview", str(path))
    if done.returncode != 0:
        said = [line for line in done.stderr.splitlines() if line.strip() and "goes in the next release" not in line]
        raise features_generate.GenerateError(said[-1] if said else "exit %d" % done.returncode)
    return done.stdout


def generate_all(tree, paths):
    """{path: its feature, or None when the generator refuses it or writes none} of each capability file of `paths`:
    one run of the tree's own generator for them all, each by itself when that run fails (b749: times out or cannot
    start among them)."""
    program = _program(tree)
    if program is not None and paths:
        with tempfile.TemporaryDirectory() as out:
            try:
                done = _run(program, "--dir", out, "generate", "--root", str(tree), *[Path(p).stem for p in paths])
            except features_generate.GenerateError:
                done = None
            if done is not None and done.returncode == 0:
                return {p: _read(Path(out) / ("%s.feature" % Path(p).stem)) for p in paths}
    found = {}
    for path in paths:
        try:
            found[path] = generate(tree, path)
        except features_generate.GenerateError:
            found[path] = None
    return found


def _read(path):
    return path.read_text() if path.is_file() else None
