# jsonbot/utils/mainloop.py
#
#

""" main loop used in jsonbot binairies. """

# jsonbot imports

import time

from jsonbot.lib.eventhandler import mainhandler
from jsonbot.lib.exit import globalshutdown
from jsonbot.utils.exception import handle_exception

# basic imports


# mainloop function


def mainloop():
    """function to be used as mainloop."""
    while 1:
        try:
            time.sleep(1)
            mainhandler.handle_one()
        except KeyboardInterrupt:
            break
        except Exception as ex:
            handle_exception()
            break
            # globalshutdown()
            # os._exit(1)
    globalshutdown()
    # os._exit(0)
