# jsonbot/utils/name.py
#
#

"""
name related helper functions.

google requirements on file names:
  - It must contain only letters, numbers, _, +, /, $, ., and -.
  - It must be less than 256 chars.
  - It must not contain "/./", "/../", or "//".
  - It must not end in "/".
  - All spaces must be in the middle of a directory or file name.


"""

# jsonbot imports

import os
import re
import string

from jsonbot.lib.errors import NameNotSet
from jsonbot.utils.generic import fromenc, toenc

# basic imports


# defines

allowednamechars = string.ascii_letters + string.digits + "_+/$.-"

# slugify function taken from django (not used now)


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata

    value = unicodedata.normalize("NFKD", value)
    value = str(re.sub("[^\w\s-]", "", value).strip())
    return re.sub("[-\s]+", "-", value)


# stripname function


def stripname(namein, allowed=""):
    """strip all not allowed chars from name."""
    if not namein:
        raise NameNotSet(namein)
    n = namein.replace(os.sep, "+")
    n = n.replace("/", "+")
    n = n.replace("@", "+")
    n = n.replace("#", "-")
    n = n.replace("!", ".")
    res = []
    allow = allowednamechars + allowed
    for c in n:
        if ord(c) < 31:
            continue
        elif c in allow:
            res.append(c)
        else:
            res.append("-" + str(ord(c)))
    return "".join(res)


# testname function


def testname(name):
    """test if name is correct."""
    for c in name:
        if c not in allowednamechars or ord(c) < 31:
            return False
    return True


def oldname(name):
    from jsonbot.lib.datadir import getdatadir

    if name.startswith("-"):
        name[0] = "+"
    name = name.replace("@", "+")
    if os.path.exists(getdatadir() + os.sep + name):
        return name
    name = name.replace("-", "#")
    name = prevchan.replace("+", "@")
    if os.path.exists(getdatadir() + os.sep + name):
        return name
    return ""
