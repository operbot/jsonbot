# jsonbot/plugs/core/count.py
#
#

""" count number of items in result queue. """

# jsonbot imports

from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples
from jsonbot.utils.generic import waitforqueue

# basic imports


# count command


def handle_count(bot, ievent):
    """no arguments - show nr of elements in result list .. use this command in a pipeline."""
    # if ievent.prev: ievent.prev.wait()
    a = ievent.inqueue
    size = len(a)
    ievent.reply(size)


cmnds.add("count", handle_count, ["OPER", "USER", "GUEST"])
examples.add("count", "count nr of items", "list ! count")
