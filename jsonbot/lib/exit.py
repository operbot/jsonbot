# jsonbot/exit.py
#
#

""" jsonbot's finaliser """

# jsonbot imports

import logging
import os
import sys
import time

from jsonbot.lib.boot import ongae
from jsonbot.lib.persist import cleanup
from jsonbot.memcached import killmcdaemon
from jsonbot.utils.locking import globallocked

from .runner import callbackrunner, cmndrunner, waitrunner

# basic imports


# functions


@globallocked
def globalshutdown(exit=True):
    """shutdown the bot."""
    try:
        try:
            sys.stdout.write("\n")
        except:
            pass
        logging.error("shutting down".upper())
        from .fleet import getfleet

        fleet = getfleet()
        if fleet:
            logging.warn("shutting down fleet")
            fleet.exit()
        logging.warn("shutting down plugins")
        from jsonbot.lib.plugins import plugs

        plugs.exit()
        logging.warn("shutting down runners")
        cmndrunner.stop()
        callbackrunner.stop()
        waitrunner.stop()
        logging.warn("cleaning up any open files")
        while cleanup():
            time.sleep(1)
        try:
            os.remove("jsonbot.pid")
        except:
            pass
        killmcdaemon()
        logging.warn("done")
        if not ongae:
            print("")
        if exit and not ongae:
            os._exit(0)
    except Exception as ex:
        print(str(ex))
        if exit and not ongae:
            os._exit(1)
