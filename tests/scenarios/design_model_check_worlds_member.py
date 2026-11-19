"""design-model-check's worlds of membership and emptiness (b274, b297), rows design_model_check_worlds' TABLE takes
in its place: a file said in a worktree from its own side (is-in), and r2 forbidding of the worktree's file what r1
obliges (holds-relation); a worktree that holds exactly some files, and one that holds nothing, in a precondition and
on a response's object; an object that holds nothing or no file beside a forbidden one that holds a file, which
no worktree meets both of, and two that hold a file (b314); a worktree that holds exactly the files that cover the line of a stage (b315); in a precondition, one that holds exactly the files that cover a line (b309). On a response's object (b297) the act is one with a recipient, as a feed's "return ... to",
and the files a relative clause's, so the context has the verbs `keep` and `return` too (`RETURNING`). Each world is
codified2_world's, its r1 (r2) the lines here."""
import importlib.util
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C2 = _sibling("codified2_world.py", "shop_codified2_world")

RETURNING = ("- **keep** (verb, state): an agent holds on to a file. Frame: agent keeps file.\n"
             "- **return** (verb, action): an agent hands a thing back to an agent. Frame: agent returns thing to "
             "agent.\n")


def line(*texts, terms="", capability=None):
    """The world of codified2_world's capability `thing` whose lines are `texts`, its index given `terms`; the
    capability the When names `capability` run as `thing`."""
    def build(step):
        C2.context(step.repo, H.PATH, list(texts))
        index = step.repo / "spec" / "index.md"
        index.write_text(index.read_text() + terms)
        if capability:
            step.context.setdefault("ids", {})[capability] = "thing"
    return build


IS_IN = "While a file is in a worktree, when the person runs `work start` on the worktree, `work` shall print the file."
HOLDS = ("While a worktree holds a file, when the person runs `work start` on the worktree, `work` shall not print the "
         "file.")
EXACTLY = ("When the person runs `work start`, `work` shall print a worktree that holds exactly the files whose version "
           "is `2.0.0`.")
UNPRINTED = "When the person runs `work start`, `work` shall not print a worktree."
NOTHING = ("While a worktree holds nothing, when the person runs `work start` on the worktree, `work` shall print the "
           "worktree.")
KEPT = ("When the person runs `work start`, `work` shall return a worktree that holds exactly the files that a session "
        "keeps to the person.")
# b315: the restriction reaches a second thing, the line of a stage
COVERING = ("When the person runs `work start`, `work` shall return a worktree that holds exactly the files that cover "
            "the line of a stage to the person.")
# b309: holds-exactly in a precondition, its restriction a relative clause with a K2 of its own
COVERED = ("While a worktree holds exactly the files that cover a line, when the person runs `work start` on the "
           "worktree, `work` shall print the worktree.")
EMPTY = "When the person runs `work start`, `work` shall return a worktree that holds nothing to the person."
UNRETURNED = "When the person runs `work start`, `work` shall not return a worktree to the person."
FULL = "When the person runs `work start`, `work` shall return a worktree that holds a file to the person."
UNFULL = "When the person runs `work start`, `work` shall not return a worktree that holds a file to the person."
FILELESS = "When the person runs `work start`, `work` shall print a worktree that holds no file."
UNFILLED = "When the person runs `work start`, `work` shall not print a worktree that holds a file."

ROWS = [
    (("precondition use `holds-exactly`", "precondition use `rc-subject`"), line(COVERED, capability="c1"), {}),     # b309
    (("requirement use `is-in`", "requirement forbid act", "requirement use `holds-relation`"), line(IS_IN, HOLDS), {}),
    (("precondition use `is-in`",), line(IS_IN), {}),
    (("requirement use `holds-exactly`", "requirement use `of-relation`", "requirement forbid act"),
     line(COVERING, UNRETURNED, terms=RETURNING), {}),     # b315
    (("requirement use `holds-exactly`", "requirement use `rc-object`", "requirement forbid act"),
     line(KEPT, UNRETURNED, terms=RETURNING), {}),
    (("requirement use `nothing`", "requirement use `rc-subject`", "requirement forbid act",
      "requirement use `holds-relation`"), line(EMPTY, UNFULL, terms=RETURNING), {}),     # b314
    (("requirement use `holds-relation`", "requirement use `rc-subject`", "requirement forbid act"),
     line(FULL, UNFULL, terms=RETURNING), {}),
    (("requirement use `no-noun`", "requirement use `holds-relation`", "requirement forbid act"),
     line(FILELESS, UNFILLED), {}),
    (("requirement use `nothing`", "requirement use `rc-subject`", "requirement forbid act"),
     line(EMPTY, UNRETURNED, terms=RETURNING), {}),
    (("requirement use `holds-exactly`", "requirement forbid act"), line(EXACTLY, UNPRINTED), {}),
    (("requirement use `holds-exactly`",), line(EXACTLY), {}),
    (("precondition use `nothing`",), line(NOTHING), {}),
]
