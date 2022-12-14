# jsonbot/plugs/common/imdb.py
#
# author: melmoth

""" query the imdb database. """

# jsonbot imports

from jsonbot.imports import getjson
from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples
from jsonbot.utils.url import decode_html_entities, geturl2, striphtml

# basic imports


# defines

URL = "http://www.deanclatworthy.com/imdb/?q=%s"

# imdb command


def handle_imdb(bot, event):
    """arguments: <query> - query the imdb databae at http://www.deanclatworthy.com/imdb/"""
    if not event.rest:
        event.missing("<query>")
        return
    query = event.rest.strip()
    urlquery = query.replace(" ", "+")
    result = {}
    rawresult = getjson().loads(geturl2(URL % urlquery))
    # the API are limited to 30 query per hour, so avoid querying it just for testing purposes
    # rawresult = {u'ukscreens': 0, u'rating': u'7.7', u'genres': u'Animation,&nbsp;Drama,Family,Fantasy,Music', u'title': u'Pinocchio', u'series': 0, u'country': u'USA', u'votes': u'23209', u'languages': u'English', u'stv': 0, u'year': None, u'usascreens': 0, u'imdburl': u'http://www.imdb.com/title/tt0032910/'}
    if not rawresult:
        event.reply("couldn't look up %s" % query)
        return
    if "error" in rawresult:
        event.reply("%s" % rawresult["error"])
        return
    print(rawresult)
    for key in list(rawresult.keys()):
        if not rawresult[key]:
            result[key] = "n/a"
        else:
            result[key] = rawresult[key]
    for key in list(result.keys()):
        try:
            result[key] = striphtml(decode_html_entities(rawresult[key]))
        except AttributeError:
            pass
    if "year" in list(rawresult.keys()):
        event.reply(
            "%(title)s (%(country)s, %(year)s): %(imdburl)s | rating: %(rating)s (out of %(votes)s votes) | Genres %(genres)s | Language: %(languages)s"
            % result
        )
    else:
        event.reply(
            "%(title)s (%(country)s): %(imdburl)s | rating: %(rating)s (out of %(votes)s votes) | Genres %(genres)s | Language: %(languages)s"
            % result
        )


cmnds.add("imdb", handle_imdb, ["OPER", "USER", "GUEST"])
examples.add("imdb", "query the imdb database.", "imdb the matrix")
