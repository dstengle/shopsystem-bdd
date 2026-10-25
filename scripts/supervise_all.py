"""`work run` with no initiative (capability supervision r66, r81, r82): every initiative that is neither done nor
abandoned is taken through its transitions, the initiatives side by side, each in a thread of its own with a `Run` of its
own. The runs share the one checkout's lock, the one limit of sessions and what each wrote and has not committed. Standard
library only."""
import shutil
import sys
import threading
from pathlib import Path

import supervise_intake
import workqueue
import workqueue_start
import workqueue_status
from supervise import Run
from workqueue import Refused


def unfulfilled(root):
    """The accepted requests of the queue that no initiative under .shop/work/, of any status, fulfils (r103)."""
    held = set()
    for path in (Path(root) / workqueue.WORK).glob("*/initiative.md"):
        data, _ = workqueue.frontmatter(workqueue.read(path, root))
        held.add(str(data.get("fulfils") or "").rsplit("/", 1)[-1])
    return [name for name, status, _, _ in workqueue.requests(root) if status == "accepted" and name not in held]


def run_all(root):
    """Take every open initiative; print each with its status, then its nodes; the exit code is 1 when a node is failed or
    a run was refused, 3 when a node is awaiting-answer, else 0 (r81, r82)."""
    for run in [Run(root, name) for name in workqueue_status.open_names(root)]:
        run.check()     # every refusal comes before anything moves (r10), the start of an initiative included
    for request in unfulfilled(root):     # the same refusals before the first start, as an intake round's (r10, r103)
        supervise_intake.Intake(root, request).check()
    for request in unfulfilled(root):
        workqueue_start.start(root, request)     # r103: the initiative `work start` begins; the run takes it below
    runs = [Run(root, name) for name in workqueue_status.open_names(root)]
    for run in runs:
        run.check()     # every refusal comes before anything moves (r10)
    taken = supervise_intake.intakes(root)     # the requests this context is the upstream of, r67
    for intake in taken:
        intake.check()
    everyone = runs + taken
    lock, slots = threading.RLock(), threading.Semaphore(everyone[0].limit) if everyone else None
    rounds = threading.Lock()     # one integrate, apply or formulate round at a time across the initiatives (r95)
    for run in runs:
        run.lock, run.slots, run.group, run.round_lock = lock, slots, runs, rounds
    for intake in taken:
        intake.lock, intake.slots = lock, slots
    if everyone:
        everyone[0].push_unpushed()
    refused = {}
    for intake in taken:     # every request is given its round before the initiatives are taken
        try:
            intake.take()
        except Refused as error:     # the fault is told and the exit is an error; the others are still taken
            refused[intake.request] = error
        finally:
            for tree in list(intake.trees):
                intake.remove(tree)
            if intake.outside is not None:
                shutil.rmtree(intake.outside, ignore_errors=True)

    def take(run):
        try:
            run.pull_through()
        except Refused as error:     # one initiative's refusal does not stop the others (r66)
            refused[run.initiative] = error
    threads = [threading.Thread(target=take, args=(run,)) for run in runs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    nodes = []
    for run in runs:
        data, _ = workqueue.frontmatter((run.dir / "initiative.md").read_text())
        print("%s %s" % (run.initiative, data.get("status")))
        here = run.items() + [(n, s) for n, s in run.proposals() if n != run.initiative]
        run.show(here, "  ")
        nodes += [s for _, s in here]
    for name, error in refused.items():
        print("work: %s: %s" % (name, error), file=sys.stderr)
    if refused or "failed" in nodes:
        return 1
    return 3 if "awaiting-answer" in nodes else 0
