# jsonbot/lib/convore/event.py
#
#

""" convore event. """

# jsonbot imports

import _thread
import logging

from jsonbot.imports import getjson
from jsonbot.lib.eventbase import EventBase
from jsonbot.utils.lazydict import LazyDict
from jsonbot.utils.locking import lockdec

# basic imports


# defines

json = getjson()

# locks

parselock = _thread.allocate_lock()
locked = lockdec(parselock)

# ConvoreEvent


class ConvoreEvent(EventBase):
    """Convore Event."""

    def parse(self, bot, message, root):
        m = LazyDict(message)
        self.root = LazyDict(root)
        type = m.kind.replace("-", "_")
        self.type = type
        self.cbtype = "CONVORE"
        self.bottype = bot.type
        self.username = m.user["username"]
        self.userhost = "%s_%s" % ("CONVORE_USER", self.username)
        self._id = m._id
        self.userid = m.user["id"]
        try:
            self.channel = m.topic["id"]
            self.groupchat = True
        except:
            self.channel = self.userid
            self.msg = True
        self.auth = self.userhost
        self.txt = m.message
        self.nick = self.username
        self.printto = self.channel
        logging.debug("convore - parsed event: %s" % self.dump())
        return self
