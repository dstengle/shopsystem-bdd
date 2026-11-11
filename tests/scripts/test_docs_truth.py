"""The docs' commands run (the user docs' design, §9, item 4, beyond test_docs.py's reading of argparse): each command
path a ```console block of the docs shows of a plugin tool (`work batch start`, `model parse` ...) is run as its own
process with `--help`, and exits 0 printing that path's usage. test_docs.py reads the tools' argparse in this process;
this test runs the tools as a person does, so a tool that fails to start, or a subcommand whose help fails, is caught.
The docs' requirement lines and links are test_docs.py's."""
import concurrent.futures
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain
from docs_testing import REPO, console_commands, parser, subcommands, tool_words


def command_path(tool, words):
    """The subcommand words of a console command, from its tool down to the last subcommand its argparse knows:
    ("work", "batch", "start") of `work batch start batch-34`. Options and their values are passed over."""
    path, p = [tool], parser(tool)
    for w in words:
        subs = subcommands(p)
        if not subs:
            break
        if w in subs:
            p = subs[w]
            path.append(w)
    return tuple(path)


def shown_paths():
    """{command path: the first page:line that shows it} of every console command of a plugin tool in the docs."""
    out = {}
    for where, command in console_commands():
        run = tool_words(command)
        if run:
            out.setdefault(command_path(*run), where)
    return out


def help_of(path):
    return subprocess.run([sys.executable, str(REPO / "scripts" / path[0]), *path[1:], "--help"], cwd=REPO,
                          capture_output=True, text=True, timeout=300)


def test_the_docs_show_commands_of_every_tool():
    assert {p[0] for p in shown_paths()} == {"work", "model", "features", "tools", "measure", "migrate"}


def test_command_path_reads_subcommands_and_passes_over_the_rest():
    assert command_path("work", ["batch", "start"]) == ("work", "batch", "start")
    assert command_path("work", ["batch", "done", "batch-34", "t1"]) == ("work", "batch", "done")
    assert command_path("model", ["--root", "x", "parse", "a line"]) == ("model", "parse")


def test_each_command_the_docs_show_runs_its_help():
    """Each command path shown runs `--help` as a process, exits 0 and prints a usage naming its last word."""
    toolchain.require()
    paths = shown_paths()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        done = dict(zip(paths, pool.map(help_of, paths)))
    wrong = ["%s: %s --help exited %d\n  %s" % (paths[p], " ".join(p), d.returncode, (d.stderr or d.stdout)[-400:])
             for p, d in done.items() if d.returncode != 0 or "usage:" not in d.stdout or p[-1] not in d.stdout]
    assert wrong == [], "\n".join(wrong)
