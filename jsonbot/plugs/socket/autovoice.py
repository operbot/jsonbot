# plugins/autovoice.py
#
#

""" do voice on join """

__copyright__ = "this file is in the public domain"

from jsonbot.lib.callbacks import callbacks
from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples


def preautovoice(bot, ievent):
    if ievent.forwarded or ievent.relayed:
        return False
    return True


def cbautovoice(bot, ievent):
    """autovoice callback"""
    chandata = 0
    if not ievent.chan:
        ievent.bind(bot, force=True)
    try:
        chandata = ievent.chan.data.autovoice
    except KeyError:
        return
    if chandata:
        bot.voice(ievent.channel, ievent.nick)


callbacks.add("JOIN", cbautovoice, preautovoice)


def handle_autovoiceon(bot, ievent):
    """autovoice-on .. enable autovoice for channel the command was given in"""
    try:
        ievent.chan.data.autovoice = 1
    except TypeError:
        ievent.reply("no %s in channel database" % ievent.channel)
        return
    ievent.reply("autovoice enabled on %s" % ievent.channel)


cmnds.add("autovoice-on", handle_autovoiceon, "OPER")
examples.add(
    "autovoice-on",
    "enable autovoice on channel in which the command is given",
    "autovoice-on",
)


def handle_autovoiceoff(bot, ievent):
    """autovoice-off .. disable autovoice for the channel the command was given in"""
    try:
        ievent.chan.data.autovoice = 0
        ievent.reply("autovoice disabled on %s" % ievent.channel)
    except TypeError:
        ievent.reply("no %s channel in database" % ievent.channel)


cmnds.add("autovoice-off", handle_autovoiceoff, "OPER")
examples.add(
    "autovoice-off",
    "disable autovoice on channel in which the command is given",
    "autovoice-off",
)
