# jsonbot/plugs/core/uniq.py
#
#

""" used in a pipeline .. unique elements. """

__author__ = "Wijnand 'tehmaze' Modderman - http://tehmaze.com"
__license__ = "BSD"

# jsonbot imports

import time

from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples
from jsonbot.utils.generic import waitforqueue

# basic imports


# uniq command


def handle_uniq(bot, ievent):
    """no arguments - uniq the result list, use this command in a pipeline."""
    if not ievent.inqueue:
        time.sleep(0.5)
    result = list(ievent.inqueue)
    if not result:
        ievent.reply("no result")
    else:
        ievent.reply("result: ", result)


cmnds.add("uniq", handle_uniq, ["OPER", "USER", "GUEST"])
examples.add("uniq", "sort out multiple elements", "list ! uniq")
