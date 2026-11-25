"""Two requirement groups of one capability that share a group title (items r55, b581): pytest-bdd collects one
scenario of the two, as spec check's v_s2 finds on a spec; the readiness bar refuses an item whose groups, laid on its
copy, make a group title of a capability its group's and another's, naming the group title (`shared`)."""
import backlog_lines
import spec_read


def shared(copy, blocks):
    """A reason for each group of the item whose title another group of its capability has too, in the laid copy."""
    reasons = []
    for block in blocks:
        path = backlog_lines.capability_file(copy, block.capability)
        if not block.groups or not path.is_file():
            continue
        groups = spec_read.capability(path).groups
        for group in block.groups:
            others = [g.id for g in groups if g.title == group.title and g.id != group.id]
            if others:
                reasons.append("%s#%s: the group title \"%s\" is the title of %s too: give the group a title of "
                               "its own" % (block.capability, group.id, group.title,
                                            ", ".join("%s#%s" % (block.capability, g) for g in others)))
    return reasons
