# jsonbot/tick.py
#
#

""" provide system wide clock tick. """

# jsonbot imports

from jsonbot.lib.callbacks import callbacks
from jsonbot.lib.config import getmainconfig
from jsonbot.lib.eventbase import EventBase
from jsonbot.lib.threadloop import TimedLoop

# TickLoop class


class TickLoop(TimedLoop):
    def start(self, bot=None):
        """start the loop."""
        self.bot = bot
        self.counter = 0
        TimedLoop.start(self)

    def handle(self):
        """send TICK events to callback."""
        self.counter += 1
        event = EventBase()
        event.nolog = True
        event.nobind = True
        if self.counter % 60 == 0:
            event.type = event.cbtype = "TICK60"
            callbacks.check(self.bot, event)
        maincfg = getmainconfig()
        t = maincfg.ticksleep or 1
        if self.counter % t == 0:
            event.type = event.cbtype = "TICK"
            callbacks.check(self.bot, event)


# global tick loop

tickloop = TickLoop("tickloop", 1)
