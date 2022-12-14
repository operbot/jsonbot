# jsonbot/plugs/core/sort.py
#
#

""" sort bot results. """

__author__ = "Wijnand 'maze' Modderman <http://tehmaze.com>"
__license__ = "BSD"

# jsonbot imports

import optparse
import time

from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples
from jsonbot.utils.generic import waitforqueue

# basic imports


# SortError exception


class SortError(Exception):
    pass


# SortOptionParser class


class SortOptionParser(optparse.OptionParser):

    """options parsers for the sort command."""

    def __init__(self):
        optparse.OptionParser.__init__(self)
        self.add_option(
            "-f",
            "--ignore-case",
            help="fold lower case to upper case characters",
            default=False,
            action="store_true",
            dest="ignorecase",
        )
        self.add_option(
            "-n",
            "--numeric-sort",
            default=False,
            help="compare according to string numerical value",
            action="store_true",
            dest="numeric",
        )
        self.add_option(
            "-r",
            "--reverse",
            default=False,
            help="reverse the result of comparisons",
            action="store_true",
            dest="reverse",
        )
        self.add_option(
            "-u",
            "--unique",
            default=False,
            help="output only the first of an equal run",
            action="store_true",
            dest="unique",
        )

    def format_help(self, formatter=None):
        """ask maze."""
        raise SortError(
            "sort [-fnru] [--ignore-case] [--numeric-sort] [--reverse] [--unique]"
        )

    def error(self, msg):
        """ask maze."""
        return self.exit(msg=msg)

    def exit(self, status=0, msg=None):
        """ask maze."""
        if msg:
            raise SortError(msg)
        else:
            raise SortError


# muneric_compare function


def numeric_compare(x, y):
    try:
        a = int(x)
    except:
        return cmp(x, y)
    try:
        b = int(y)
    except:
        return cmp(x, y)
    return a - b


# sort command


def handle_sort(bot, ievent):
    """no arguments - sort the result list, use this command in a pipeline."""
    parser = SortOptionParser()
    args = []
    try:
        options, args = parser.parse_args(ievent.args)
    except SortError as e:
        ievent.reply(str(e))
        return
    if not ievent.inqueue:
        time.sleep(0.5)
    result = list(ievent.inqueue)
    if not result:
        result = args
    if options.unique:
        result = list(set(result))
    if options.numeric:
        result.sort(numeric_compare)
    else:
        result.sort()
    if options.ignorecase:
        sort(lambda a, b: cmp(a.upper(), b.upper()), result)
    if options.reverse:
        reverse(result)
    if result:
        ievent.reply("results: ", result)
    else:
        ievent.reply("no result")


cmnds.add("sort", handle_sort, ["OPER", "USER", "GUEST"])
examples.add("sort", "sort the output of a command", "list ! sort")
