# jsonbot/plugs/core/rc.py
#
#

""" jsonbot resource files .. files with the .jsonbot extension which consists of commands to be executed. """

# jsonbot imports

import copy

from jsonbot.lib.commands import cmnds
from jsonbot.lib.config import getmainconfig
from jsonbot.lib.examples import examples
from jsonbot.utils.exception import handle_exception
from jsonbot.utils.generic import waitevents, waitforqueue
from jsonbot.utils.url import geturl2

# basic imports


# defines

cpy = copy.deepcopy

# rc command


def handle_rc(bot, event):
    """arguments: <file>|<url> - execute a .jsonbot resource file with bot commands."""
    if not event.rest:
        event.missing("<file>|<url>")
        return
    if not getmainconfig().allowrc:
        event.reply("rc mode is not enabled")
        return
    teller = 0
    t = event.rest
    waiting = []
    try:
        try:
            if getmainconfig().allowremoterc and t.startswith("http"):
                data = geturl2(t)
            else:
                data = open(t, "r").read()
        except IOError as ex:
            event.reply("I/O error: %s" % str(ex))
            return
        if not data:
            event.reply("can't get data from %s" % event.rest)
            return
        for d in data.split("\n"):
            i = d.strip()
            if not i:
                continue
            if i.startswith("#"):
                continue
            e = cpy(event)
            e.txt = "%s" % i.strip()
            e.direct = True
            bot.put(e)
            waiting.append(e)
            teller += 1
        event.reply("%s commands executed" % teller)
    except Exception as ex:
        event.reply("an error occured: %s" % str(ex))
        handle_exception()


cmnds.add("rc", handle_rc, ["OPER"], threaded=True)
examples.add(
    "rc",
    "execute a file of jsonbot commands .. from file or url",
    "1) rc resource.jsonbot 2) rc http://jsonbot.org/resource.jsonbot",
)
