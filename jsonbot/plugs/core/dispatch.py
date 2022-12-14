# jsonbot/plugs/core/dispatch.py
#
#

""" this is the dispatch plugin that dispatches events to commands. """

# jsonbot imports

import copy
import logging

from jsonbot.lib.callbacks import last_callbacks
from jsonbot.lib.commands import cmnds
from jsonbot.lib.errors import NoSuchCommand, NoSuchUser
from jsonbot.utils.exception import handle_exception
from jsonbot.utils.generic import waitforqueue

# basic logging


# defines

cpy = copy.deepcopy

# dispatch-precondition


def predispatch(bot, event):
    """check whether we should check for commands."""
    if event.status == "done":
        logging.debug("dispatch - event is done .. ignoring")
        return False
    if event.isremote():
        logging.debug("event is remote .. not dispatching")
        return False
    if event.isrelayed:
        logging.debug("event is relayed .. not dispatching")
        return False
    if event.blocked():
        logging.warn("blocking %s" % event.userhost)
        return False
    # if not event.woulddispatch() and not event.wouldmatchre(): return False
    return True


# dispatch-callback


def dispatch(bot, event):
    """dispatch an event."""
    logging.info("dispatch - doing event %s" % event.tojson())
    if event.userhost in bot.ignore:
        logging.warn("%s - ignore on %s" % (bot.name, event.userhost))
        return
    if event.nodispatch:
        logging.warn(
            "dispatch - nodispatch option is set - ignoring %s" % event.userhost
        )
        return
    bot.status = "dispatch"
    event.bind(bot)
    if event.iscommand or event.hascc():
        try:
            event.iscommand = True
            if not event.options:
                event.makeoptions()
            try:
                result = event.execute()
            except NoSuchCommand as ex:
                logging.warn("no such command: %s" % event.usercmnd)
                if event.giveresponse:
                    event.reply("no %s command found" % str(ex).strip())
                event.launched()
                event.ready()
        except Exception as ex:
            handle_exception()
    else:
        logging.debug("dispatch - no go for %s" % event.auth or event.userhost)
        event.launched()
        event.ready()


# register callback

last_callbacks.add("PRIVMSG", dispatch, predispatch, speed=3)
last_callbacks.add("MESSAGE", dispatch, predispatch)
last_callbacks.add("BLIP_SUBMITTED", dispatch, predispatch)
last_callbacks.add("WEB", dispatch, predispatch)
last_callbacks.add("CONSOLE", dispatch, predispatch)
last_callbacks.add("DCC", dispatch, predispatch)
last_callbacks.add("DISPATCH", dispatch, predispatch)
last_callbacks.add("CMND", dispatch, predispatch)
last_callbacks.add("CONVORE", dispatch, predispatch)
last_callbacks.add("TORNADO", dispatch, predispatch)
