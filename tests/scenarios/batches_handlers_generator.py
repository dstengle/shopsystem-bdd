"""The feature generator a task's workspace holds (batches r199, b740, b874), over batches_handlers_amend's world: once
the batch is made (T.AFTER_BATCH), each of its task branches `batch-<n>-<item>` given a commit of a stand-in
generator, as the plugin's own repository holds one: `scripts/features_generate.py` and an executable `scripts/features` whose `generate` (with
`--root`, `--preview FILE` or capability names, and `features --dir DIR`) writes each feature as the one line
`MARK`. `work batch amend` run from the base's checkout then writes the item's capability's feature on its task's
branch with that generator, not its own; the Thens read the feature there. An `unresponsive` generator (r201, b749)
sleeps `STALL` seconds before it writes, and the run's time limit `$SHOPSYSTEM_GENERATE_TIMEOUT` is one second, so
`work batch amend` refuses naming the feature generator."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
MARK = "# written by the workspace's feature generator"
STALL = "import time\ntime.sleep(30)\n"       # longer than the time limit, far shorter than the run's
FEATURES = '''#!/usr/bin/env python3
"""A stand-in of `features`: `generate` writes each capability's feature as one line."""
import argparse
import os
import sys

MARK = %r
parser = argparse.ArgumentParser(prog="features")
parser.add_argument("--dir", default="features")
sub = parser.add_subparsers(dest="command", required=True)
gen = sub.add_parser("generate")
gen.add_argument("--root", default=".")
gen.add_argument("--preview")
gen.add_argument("names", nargs="*", metavar="CAPABILITY")
args = parser.parse_args()
if args.preview:
    sys.stdout.write(MARK + "\\n")
    sys.exit(0)
out = args.dir if os.path.isabs(args.dir) else os.path.join(args.root, args.dir)
os.makedirs(out, exist_ok=True)
for name in args.names:
    with open(os.path.join(out, "%%s.feature" %% name), "w") as f:
        f.write(MARK + "\\n")
''' % MARK


@four("GivenK", "feature generator", *BOTH)
@four("GivenK", "feature", *BOTH)
def given_named(step):
    """A feature generator, or the feature a Then says it writes."""


@four("GivenDoes", "has", *BOTH)
def has_generator(step):
    """`the workspace w1 has the feature generator f1`: the task's workspace holds a generator of its own."""
    (k1, _), (k2, n2) = parts(step)
    if (k1, k2) != ("worktree", "feature generator"):
        return False
    step.context["generator"] = n2


@four("GivenK_A", "feature generator", *BOTH)
def responsiveness(step):
    """The responsiveness of the feature generator f1 is `unresponsive`: a run of it outlasts its time limit."""
    if step.attribute != "responsiveness":
        return False
    if step.values[0].strip("`") == "unresponsive":
        step.context["stalled"] = True
        step.context.setdefault("env", {})["SHOPSYSTEM_GENERATE_TIMEOUT"] = "1"


def generator(step, name):
    """The stand-in generator committed on each task branch of the batch (T.AFTER_BATCH), once they are made."""
    if "generator" not in step.context:
        return
    batch = T.batch_name(step, name)
    for branch in T.git(step, "branch", "--list", "%s-b*" % batch, "--format=%(refname:short)").split():
        _commit_generator(step, branch)


def _commit_generator(step, branch):
    tree = T.outside(step) / ("generator-%s" % branch)
    T.git(step, "worktree", "add", "-q", str(tree), branch)
    scripts = tree / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "features_generate.py").write_text('"""A stand-in of the feature generator."""\n')
    (scripts / "features").write_text(FEATURES.replace("import argparse\n", "import argparse\n" + STALL)
                                      if step.context.get("stalled") else FEATURES)
    (scripts / "features").chmod(0o755)
    T.git(step, "add", "-A", cwd=tree)
    T.git(step, "commit", "-q", "-m", "the workspace's feature generator\n\nItem: %s" % branch.rsplit("-", 1)[1],
          cwd=tree)
    T.git(step, "worktree", "remove", "--force", str(tree))


T.AFTER_BATCH.append(generator)


def _feature(step):
    """The amended item's capability's feature on its task's branch, once the amend exited 0."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    capability = step.context["amended"][0][0]
    batch = T.batch_name(step, next(iter(step.context["given"]["batch"])))
    branch = "%s-%s" % (batch, B.ident(next(n for n, f in step.context["given"]["item"].items()
                                             if T.status_of(step, n) == "in-batch")))
    return T.git(step, "show", "%s:features/%s.feature" % (branch, capability))


@four("ThenDoes", "name", *BOTH)
def names_generator(step):
    """`the batches service names the feature generator f1`: the refusal says the feature generator."""
    if parts(step)[1][0] != "feature generator":
        return False
    done = step.context["result"]
    assert done.returncode == 1 and "feature generator" in done.stderr, (step.text, done.stdout, done.stderr)


@four("ThenDoes", "has", *BOTH)
def generator_has(step):
    """`the feature generator f1 has the feature f2`: the task branch's feature is the one its generator writes."""
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("feature generator", "feature") or "generator" not in step.context:
        return False
    text = _feature(step)
    assert text.splitlines() == [MARK], (step.text, text[:300])


@four("ThenDoes", "holds", *BOTH)
def workspace_holds(step):
    """`the workspace w2 holds the feature f2`: the task's branch holds the item's capability's feature."""
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("worktree", "feature") or "generator" not in step.context:
        return False
    assert _feature(step), step.text
