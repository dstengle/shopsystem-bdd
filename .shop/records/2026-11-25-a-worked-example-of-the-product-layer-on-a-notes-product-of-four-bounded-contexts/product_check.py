"""The product checks of the scratch compact shop, read-only: p1 each job assigned to exactly one hosted or known
bounded context; p2 each job served by exactly one capability in the shop; p3 the serving capability in the assigned
context; p4 the serving capability's narrator is the job's actor (each actor, as the context calls it); p5 a
capability that serves no job (told apart: a port capability, one a trace reaches, one nothing reaches); p6 a
subdomain no bounded context addresses; p7 a job's trace that reaches no context addressing a subdomain the job
names; p8 a job's actor not among the product's; p9 a statement not of the form "When <situation>, <actor> wants
<motivation>, so they can <outcome>". Usage: product_check.py <shop>."""
import io
import re
import sys
from contextlib import redirect_stdout

import job_trace
from product_lib import Shop


def main(root):
    with redirect_stdout(io.StringIO()):
        traced = job_trace.main([root, "--depth", "3"])
    shop = Shop(root)
    found = []
    serving = {}
    for cid, ctx in shop.contexts.items():
        for cap, data in ctx.caps.items():
            for jid in data["serves"]:
                serving.setdefault(jid, []).append((cid, cap, data))
    for jid, job in shop.jobs.items():
        short = jid.rsplit("/", 1)[1]
        assigned = [a.strip() for a in job.get("assigned", "").split(",") if a.strip()]
        if len(assigned) != 1 or assigned[0] not in shop.addressed:
            found.append(f"p1 {short}: assigned to {assigned or 'nothing'}")
        caps = serving.get(jid, [])
        if len(caps) != 1:
            found.append(f"p2 {short}: served by {len(caps)} capabilities {[c for _, c, _ in caps]}")
        for cid, cap, data in caps:
            if assigned and cid != assigned[0]:
                found.append(f"p3 {short}: {cap} is in {cid}, the job is assigned to {assigned[0]}")
            ctxname = cid.rsplit("/", 1)[1]
            for actor in job["actors"]:
                called = shop.actors.get(actor, {}).get(ctxname)
                if called != data.get("narrator"):
                    found.append(f"p4 {short}: {cap}'s narrator is {data.get('narrator')!r}; the actor {actor!r}"
                                 f" is called {called!r} in {ctxname}")
        for actor in job["actors"]:
            if actor not in shop.actors:
                found.append(f"p8 {short}: actor {actor!r} is not among the product's {sorted(shop.actors)}")
        st = job.get("statement", "")
        names = "|".join(re.escape(a) for a in job["actors"])
        if not re.fullmatch(rf"When .+?, (?:{names}) wants .+?, so (?:they|he|she|it) can .+\.", st):
            found.append(f"p9 {short}: the statement is not 'When <situation>, <actor> wants <motivation>, so they"
                         f" can <outcome>' with its actor{'s' if len(job['actors']) > 1 else ''} {job['actors']}")
        reached = {assigned[0]} if assigned else set()
        # the contexts a job's trace reaches: its own, and the providers its trace names
        with redirect_stdout(io.StringIO()) as buf:
            one = job_trace.main([root, short, "--depth", "3"])
        reached |= one.reached_contexts
        covered = {s for c in reached for s in shop.addressed.get(c, {}).get("subdomains", [])}
        for s in job["subdomains"]:
            if s not in covered:
                found.append(f"p7 {short}: names {s} ({shop.subdomains.get(s, {}).get('name')}), which no context"
                             f" its trace reaches addresses (reached: {sorted(c.rsplit('/', 1)[1] for c in reached)})")
    for cid, ctx in shop.contexts.items():
        for cap, data in ctx.caps.items():
            if data["serves"]:
                continue
            port = ctx.ops and data.get("area") and any(o["area"] == data["area"] and o["kind"] == "port"
                                                        for o in ctx.ops.values())
            how = ("a port capability" if port else "reached by a trace" if (cid, cap) in traced.reached
                   else "reached by nothing")
            found.append(f"p5 {ctx.name}:{cap} serves no job ({how})")
    addressed = {s for v in shop.addressed.values() for s in v["subdomains"]}
    for s, data in shop.subdomains.items():
        if s not in addressed:
            found.append(f"p6 {s} ({data['name']}, {data['type']}) is addressed by no bounded context")
    print("\n".join(found) or "no findings")
    print(f"{len(found)} findings")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
