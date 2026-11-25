"""A job's derived trace in the scratch compact shop, read-only: the serving capability's lines, then each port request
a response makes (a response's verb naming an operation of an area of kind port), the port lines triggered on it, the
adapter specs realising those lines, each provider (its contract held, the provider operation realisations.toml
names), and in a hosted provider the lines triggered on that operation, followed again to --depth. Also each job's
coordination kind, derived as decision 0134 words it. Usage: job_trace.py <shop> [job ...] [--depth N]."""
import sys
from pathlib import Path

from product_lib import Shop, constants, events, parts

REPLIES = ("complete", "refuse", "return")


def port_requests(ctx, form):
    head, resp = parts(form)
    out = []
    for verb, _op, _x in events(resp):
        op = ctx.verbs.get(verb)
        if op and ctx.ops.get(op, {}).get("kind") == "port":
            out.append(op)
    return out


def reply_trigger(ctx, form):
    """The port service whose reply (completes, refuses, returns) triggers the line, else None."""
    head, _ = parts(form)
    names = constants(form)
    for verb, _op, x in events(head):
        svc = ctx.services.get(names.get(x, ""))
        if verb in REPLIES and svc and ctx.areas.get(svc) == "port":
            return verb, svc
    return None


def lines_on(ctx, op):
    """(capability, id, text, form) of each line of ctx triggered by a request of op."""
    for cap, rows in ctx.forms().items():
        for rid, text, form in rows:
            if f"request(e1, {op}," in parts(form)[0]:
                yield cap, rid, text, form


def trace(shop, ctx, caps, depth, out, seen, indent="", only=None):
    for cap in caps:
        for rid, text, form in ctx.forms()[cap]:
            key = (ctx.id, cap, rid)
            if key in seen or (only and rid not in only):
                continue
            seen.add(key)
            reply = reply_trigger(ctx, form)
            out.append(f"{indent}{ctx.name}:{cap}#{rid}" + (f"  [on {reply[1]} {reply[0]}]" if reply else "")
                       + f"  {text}")
            for op in port_requests(ctx, form):
                follow(shop, ctx, op, depth, out, seen, indent + "  ")


def follow(shop, ctx, op, depth, out, seen, indent):
    kind = "reads" if ctx.ops[op].get("reads") else "changes"
    props = ctx.ops[op]["props"].split("outcomes:")[0].strip()
    out.append(f"{indent}-> port request {op} ({kind}{'; ' + props if props else ''})")
    ports = list(lines_on(ctx, op))
    for cap, rid, text, _ in ports:
        out.append(f"{indent}   port line {ctx.name}:{cap}#{rid}  {text}")
        shop.reached.add((ctx.id, cap))
    ids = {f"{cap}#{rid}" for cap, rid, _, _ in ports}
    adapters = [a for a in ctx.adapters.values() if ids & set(a.get("realises", []))]
    if not adapters:
        out.append(f"{indent}   !! no adapter spec realises {sorted(ids) or op}")
    for a in adapters:
        real = shop.realisations.get(a["id"], {}).get(op)
        for prov in a.get("providers", []):
            pid, _, ver = prov.partition("@")
            held = list((a["root"] / "provider" / pid.split("/", 1)[1]).glob(f"{ver or '*'}/contract.toml"))
            has = held and real and f'[operations."{real}"]' in held[0].read_text()
            out.append(f"{indent}   adapter {a['id'].rsplit('/', 1)[1]} -> provider {prov}"
                       f" op {real or '?? (no realisation)'}; contract {'held' if held else 'MISSING'}"
                       f"{'' if has else '; op NOT in held contract' if held else ''}")
            shop.relations.add((ctx.id, pid))
            shop.reached_contexts.add(pid)
            target = shop.contexts.get(pid)
            if not target:
                out.append(f"{indent}   (provider outside the shop: trace stops)")
                continue
            if depth <= 0 or not real:
                continue
            found = list(lines_on(target, real))
            if not found:
                out.append(f"{indent}   !! no line of {target.name} is triggered by a request of {real}")
            for cap, rid, text, form in found:
                shop.reached.add((pid, cap))
                trace(shop, target, [cap], depth - 1, out, seen, indent + "   ", only={rid})


def coordination(shop, ctx, caps):
    ops, replies, compensating = [], 0, set()
    for cap in caps:
        for rid, text, form in ctx.forms()[cap]:
            reqs = port_requests(ctx, form)
            ops += reqs
            reply = reply_trigger(ctx, form)
            if reply:
                replies += 1
                if reply[0] == "refuse":
                    compensating |= set(reqs)
    declared = {o for o in ops if "compensated by" in ctx.ops[o]["props"]}
    changing = sorted({o for o in ops if not ctx.ops[o].get("reads")} - compensating)
    compensations = len(compensating | declared)
    if not ops:
        return "local (no port request)"
    if not replies:
        return f"port request ({', '.join(sorted(set(ops)))}; no line waits on a reply)"
    if len(changing) >= 2 and compensations:
        return f"saga ({len(changing)} state-changing forward requests {changing}; compensated: {sorted(declared)} by declaration, {sorted(compensating)} requested on a refusal)"
    return f"long-running process ({len(set(ops))} port requests, {replies} line(s) on a reply)"


def main(argv):
    depth = int(argv[argv.index("--depth") + 1]) if "--depth" in argv else 2
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--depth")]
    shop = Shop(args[0])
    shop.reached, shop.relations, shop.reached_contexts = set(), set(), set()
    wanted = args[1:] or list(shop.jobs)
    for jid in wanted:
        job = shop.jobs[jid if jid.startswith("job/") else "job/example.org/notes/" + jid]
        ctx = shop.contexts[job["assigned"]]
        caps = [c for c, d in ctx.caps.items() if any(s.endswith("/" + jid.rsplit("/", 1)[-1]) for s in d["serves"])]
        out = []
        trace(shop, ctx, caps, depth, out, set())
        print(f"== {jid.rsplit('/', 1)[-1]} {job['title']}: {ctx.name}, served by {caps}")
        print(f"   coordination: {coordination(shop, ctx, caps)}")
        print("\n".join("   " + l for l in out))
    if "--relations" in argv:
        print("== derived relations (downstream -> upstream)")
        for d, u in sorted(shop.relations):
            print(f"   {d} -> {u}")
    return shop


if __name__ == "__main__":
    main(sys.argv[1:])
