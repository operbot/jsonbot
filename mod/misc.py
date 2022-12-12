# jsonbot/plugs/core/misc.py
#
#

""" misc commands. """

# jsonbot imports

import _thread
import copy

from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples
from jsonbot.lib.persiststate import UserState
from jsonbot.utils.exception import handle_exception

# basic imports


# defines

cpy = copy.deepcopy

# test command


def handle_test(bot, ievent):
    """no arguments - give test response."""
    ievent.reply(
        "%s (%s) - %s - it works!"
        % (ievent.auth or ievent.userhost, ievent.nick, ievent.user.data.name)
    )


cmnds.add("test", handle_test, ["USER", "GUEST"])
examples.add("test", "give test response", " test")

# source command


def handle_source(bot, ievent):
    """no arguments - show where to fetch the bot source."""
    ievent.reply("see http://jsonbot.googlecode.com")


cmnds.add("source", handle_source, ["USER", "GUEST"])
examples.add("source", "show source url", "source")
