"""The feature generator a batch's workspace holds (batches r170, b740), over batches_handlers_amend's world: once
the batch is made (T.AFTER_BATCH), its branch `batch-<n>` given a commit of a stand-in generator, as the plugin's own
repository holds one: `scripts/features_generate.py` and an executable `scripts/features` whose `generate` (with
`--root`, `--preview FILE` or capability names, and `features --dir DIR`) writes each feature as the one line
`MARK`. `work batch amend` run from the base's checkout then writes the item's capability's feature on the batch's
branch with that generator, not its own; the Thens read the feature on `batch-<n>`."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
MARK = "# written by the workspace's feature generator"
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
    """`the workspace w1 has the feature generator f1`: the batch's workspace holds a generator of its own."""
    (k1, _), (k2, n2) = parts(step)
    if (k1, k2) != ("worktree", "feature generator"):
        return False
    step.context["generator"] = n2


def generator(step, name):
    """The stand-in generator committed on the batch's branch (T.AFTER_BATCH), after the task branches are made."""
    if "generator" not in step.context:
        return
    tree = T.outside(step) / ("generator-%s" % T.batch_name(step, name))
    T.git(step, "worktree", "add", "-q", str(tree), T.batch_name(step, name))
    scripts = tree / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "features_generate.py").write_text('"""A stand-in of the feature generator."""\n')
    (scripts / "features").write_text(FEATURES)
    (scripts / "features").chmod(0o755)
    T.git(step, "add", "-A", cwd=tree)
    T.git(step, "commit", "-q", "-m", "the workspace's feature generator", cwd=tree)
    T.git(step, "worktree", "remove", "--force", str(tree))


T.AFTER_BATCH.append(generator)


def _feature(step):
    """The amended item's capability's feature on the batch's branch, once the amend exited 0."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    capability = step.context["amended"][0][0]
    branch = T.batch_name(step, next(iter(step.context["given"]["batch"])))
    return T.git(step, "show", "%s:features/%s.feature" % (branch, capability))


@four("ThenDoes", "has", *BOTH)
def generator_has(step):
    """`the feature generator f1 has the feature f2`: the batch branch's feature is the one its generator writes."""
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("feature generator", "feature") or "generator" not in step.context:
        return False
    text = _feature(step)
    assert text.splitlines() == [MARK], (step.text, text[:300])


@four("ThenDoes", "holds", *BOTH)
def workspace_holds(step):
    """`the workspace w2 holds the feature f2`: the batch's branch holds the item's capability's feature."""
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("worktree", "feature") or "generator" not in step.context:
        return False
    assert _feature(step), step.text
