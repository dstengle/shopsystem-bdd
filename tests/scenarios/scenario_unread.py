"""A Given no test world reads (b748): the world pickers' fallbacks fail on it, naming the scenario's node id and what
was not read, so that a new line's scenario fails until its world is built instead of running in a default world
that cannot fail."""


def node_id(step):
    """The pytest node id of the scenario the step is of, or "?" when the step runs outside one."""
    try:
        return step.request.node.nodeid
    except (AttributeError, LookupError):
        return "?"


def unread(step, what):
    raise AssertionError("%s: no test world reads %s; build its world" % (node_id(step), what))
