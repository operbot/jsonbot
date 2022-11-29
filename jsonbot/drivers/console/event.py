# jsonbot/console/event.py
#
#

""" a console event. """

# jsonbot imports

import getpass

from jsonbot.lib.channelbase import ChannelBase
from jsonbot.lib.errors import NoInput
from jsonbot.lib.eventbase import EventBase

# basic imports


# ConsoleEvent class


class ConsoleEvent(EventBase):
    def parse(self, bot, input, console, *args, **kwargs):
        """overload this."""
        if not input:
            raise NoInput()
        self.bot = bot
        self.console = console
        self.nick = getpass.getuser()
        self.auth = self.nick + "@" + bot.cfg.uuid
        self.userhost = self.auth
        self.origin = self.userhost
        self.txt = input
        self.channel = self.userhost
        self.cbtype = self.cmnd = "CONSOLE"
        self.showall = True
        self.prepare()
        return self
