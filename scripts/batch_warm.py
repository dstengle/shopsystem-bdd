"""The warming of a base's state (b588): what the next `work batch start` reads of the base, made ahead of it, so that
opening a batch after a merge that changed the vocabulary does not wait on it. `work batch merged` starts it
(`start`): this file run by a fresh interpreter in a session of its own, its output dropped, never waited on, and a
start that fails or a warming that fails nothing more than a batch opened cold. The warming (`warm`) is the readiness
bar's before state of a copy of the base (readiness_before, as readiness_bar's `well_formed` copies `spec/` and the
construct catalogue for the first item it checks), whose computing compiles grammar 4 and parses every line of the
base into spec_parse_cache side by side (spec_prefetch); a state already kept is read, not computed again."""
import contextlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


@contextlib.contextmanager
def copied(root):
    """A copy of `root`'s `spec/` and construct catalogue, as the readiness bar makes it, removed afterwards."""
    import spec_catalogued
    copy = Path(tempfile.mkdtemp(prefix="readiness-"))
    try:
        shutil.copytree(Path(root) / "spec", copy / "spec")
        spec_catalogued.copy(root, copy)
        yield copy
    finally:
        shutil.rmtree(copy, ignore_errors=True)


def warm(root):
    """The base at `root` warmed: its before state kept (grammar 4 compiled, its lines parsed on the way)."""
    import readiness_bar
    import readiness_before
    import spec_held
    import spec_lexicon
    import spec_prefetch
    import spec_rgl_vocab
    with copied(root) as copy, spec_held.held(copy):
        outer = spec_rgl_vocab.outer(copy)

        def unlaid():          # readiness_bar's state before the lay, computed as it computes it
            spec_prefetch.prefetch(copy, spec_prefetch.texts(copy))
            return set(spec_lexicon.problems(spec_lexicon.read(copy), outer)), readiness_bar._violations(copy)[0]
        readiness_before.before(copy, unlaid)


def start(root):
    """The warming of `root` started detached; its process, or None when it could not be started."""
    try:
        return subprocess.Popen([sys.executable, str(Path(__file__).resolve()), str(root)], cwd=tempfile.gettempdir(),
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                start_new_session=True)
    except OSError:
        return None


if __name__ == "__main__":
    try:
        warm(sys.argv[1])
    except Exception:       # noqa: BLE001, S110  a warming that fails leaves the next batch to open cold, nothing more
        pass
