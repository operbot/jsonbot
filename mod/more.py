# jsonbot/plugs/core/more.py
#
#

""" access the output cache. """

# jsonbot imports

from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples
from jsonbot.lib.less import outcache

# basic imports


# more command


def handle_more(bot, ievent):
    """no arguments - pop message from the output cache."""
    if ievent.msg and bot.type == "irc":
        target = ievent.nick
    else:
        target = ievent.channel
    try:
        txt, size = outcache.more("%s-%s" % (bot.cfg.name, target))
    except IndexError:
        txt = None
    if not txt:
        ievent.reply("no more data available for %s" % target)
        return
    txt = bot.outputmorphs.do(txt, ievent)
    if size:
        txt += "<b> - %s more</b>" % str(size)
    bot.outnocb(target, txt, event=ievent)
    bot.outmonitor(ievent.origin or ievent.userhost, ievent.channel, txt)


cmnds.add("more", handle_more, ["USER", "GUEST"])
examples.add("more", "return txt from output cache", "more")
