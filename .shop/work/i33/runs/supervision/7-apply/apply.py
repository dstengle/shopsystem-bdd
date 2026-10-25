def sub(p, pairs):
    s = open(p).read()
    for a, b in pairs:
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    open(p, 'w').write(s)


def line(p, start):
    return [x for x in open(p) if x.startswith(start)][0]


sup = 'spec/capabilities/supervision.md'
l74 = line(sup, '- [r74]')
r121 = "- [r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status.\n"
r119 = line(sup, '- [r119]')
r120 = "- [r120] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is.\n"
sub(sup, [
    (l74, l74 + r121),
    (r119, r119 + r120),
    ("that is not `done`, that has at least one work-item, whose", "that is not `done`, that has at least one work-item that is `green`, whose"),
    ("- [r75] **When** every work-item of an initiative is `green` or `withdrawn` and its kept",
     "- [r75] **When** every work-item of an initiative is `green` or `withdrawn` and at least one of them is `green` and its kept"),
])
wq = 'spec/capabilities/work-queue.md'
l12 = line(wq, '- [r12]')
l23 = line(wq, '- [r23]')
n23 = l23.replace("at least one work-item,", "at least one work-item that is `green`,")
sub(wq, [
    (l12, l12 + "- [r32] **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing.\n"),
    (l23, n23 + "- [r31] **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is.\n"),
])
