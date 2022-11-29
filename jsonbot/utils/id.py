# jsonbot/utils/id.py
#
#

""" id related functions. """

# jsonbot imports

import uuid

from jsonbot.utils.generic import toenc

# basic imports


# getrssid function


def getrssid(url, time):
    """get an id based on url and time."""
    key = str(url) + str(time)
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, toenc(key)))
