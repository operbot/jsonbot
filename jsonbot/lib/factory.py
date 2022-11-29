# jsonbot/lib/factory.py
#
#

""" Factory to produce instances of classes. """

# jsonbot imports

import logging

from jsonbot.lib.errors import NoSuchBotType, NoUserProvided
from jsonbot.utils.exception import handle_exception

# basic imports


# Factory base class


class Factory(object):
    pass


# BotFactory class


class BotFactory(Factory):
    def create(self, type=None, cfg={}):
        try:
            type = cfg["type"] or type or None
        except KeyError:
            pass
        try:
            if "xmpp" in type:
                try:
                    import waveapi
                    from jsonbot.drivers.gae.xmpp.bot import XMPPBot

                    bot = XMPPBot(cfg)
                except ImportError:
                    from jsonbot.drivers.xmpp.bot import SXMPPBot

                    bot = SXMPPBot(cfg)
            elif type == "web":
                from jsonbot.drivers.gae.web.bot import WebBot

                bot = WebBot(cfg)
            elif type == "wave":
                from jsonbot.drivers.gae.wave.bot import WaveBot

                bot = WaveBot(cfg, domain=cfg.domain)
            elif type == "irc":
                from jsonbot.drivers.irc.bot import IRCBot

                bot = IRCBot(cfg)
            elif type == "console":
                from jsonbot.drivers.console.bot import ConsoleBot

                bot = ConsoleBot(cfg)
            elif type == "base":
                from jsonbot.lib.botbase import BotBase

                bot = BotBase(cfg)
            elif type == "convore":
                from jsonbot.drivers.convore.bot import ConvoreBot

                bot = ConvoreBot(cfg)
            elif type == "tornado":
                from jsonbot.drivers.tornado.bot import TornadoBot

                bot = TornadoBot(cfg)
            elif type == "sleek":
                from jsonbot.drivers.sleek.bot import SleekBot

                bot = SleekBot(cfg)
            else:
                raise NoSuchBotType("%s bot .. unproper type %s" % (type, cfg.dump()))
            return bot
        except NoUserProvided as ex:
            logging.info("%s - %s" % (cfg.name, str(ex)))
        except AssertionError as ex:
            logging.warn("%s - assertion error: %s" % (cfg.name, str(ex)))
        except Exception as ex:
            handle_exception()


bot_factory = BotFactory()
