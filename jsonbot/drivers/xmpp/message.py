# jsonbot/socklib/xmpp/message.py
#
#

""" jabber message definition .. types can be normal, chat, groupchat,
    headline or  error
"""

# jsonbot imports

import _thread
import logging
import time

from jsonbot.lib.errors import BotNotSetInEvent
from jsonbot.lib.eventbase import EventBase
from jsonbot.lib.gozerevent import GozerEvent
from jsonbot.utils.exception import handle_exception
from jsonbot.utils.generic import fromenc, jabberstrip, toenc
from jsonbot.utils.locking import lockdec
from jsonbot.utils.trace import whichmodule

# xmpp import


# basic imports


# locks

replylock = _thread.allocate_lock()
replylocked = lockdec(replylock)

# classes


class Message(GozerEvent):

    """jabber message object."""

    def __init__(self, nodedict={}):
        self.element = "message"
        self.jabber = True
        self.cmnd = "MESSAGE"
        self.cbtype = "MESSAGE"
        self.bottype = "xmpp"
        self.type = "normal"
        self.speed = 8
        GozerEvent.__init__(self, nodedict)

    def __copy__(self):
        return Message(self)

    def __deepcopy__(self, bla):
        m = Message()
        m.copyin(self)
        return m

    def parse(self, bot=None):
        """set ircevent compat attributes."""
        self.bot = bot
        self.jidchange = False
        try:
            self.resource = self.fromm.split("/")[1]
        except IndexError:
            pass
        self.channel = self["fromm"].split("/")[0]
        self.origchannel = self.channel
        self.nick = self.resource
        self.jid = self.fromm
        self.ruserhost = self.jid
        self.userhost = self.jid
        self.stripped = self.jid.split("/")[0]
        self.printto = self.channel
        for node in self.subelements:
            try:
                self.txt = node.body.data
                break
            except (AttributeError, ValueError):
                continue
        self.time = time.time()
        if self.type == "groupchat":
            self.groupchat = True
            self.auth = self.userhost
        else:
            self.showall = True
            self.groupchat = False
            self.auth = self.stripped
            self.nick = self.jid.split("@")[0]
        self.msg = not self.groupchat
        self.makeargs()
        self.prepare()
        return self

    def errorHandler(self):
        """dispatch errors to their handlers."""
        try:
            code = self.get("error").code
        except Exception as ex:
            handle_exception()
        try:
            method = getattr(self, "handle_%s" % code)
            if method:
                logging.error(
                    "sxmpp.core - dispatching error to handler %s" % str(method)
                )
                method(self)
        except AttributeError as ex:
            logging.error("sxmpp.core - unhandled error %s" % code)
        except:
            handle_exception()

    def normalize(self, what):
        return self.bot.normalize(what)
