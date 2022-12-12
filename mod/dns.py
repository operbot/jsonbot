# jsonbot/plugs/socket/dns.py
#
#

""" do a fqdn loopup. """

# jsonbot imports

import re
from socket import getfqdn, gethostbyname

from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples

# basic imports


# dns command


def handle_dns(bot, event):
    """arguments: <ip>|<hostname> - do a dns lookup."""
    if not event.rest:
        event.missing("<ip>|<hostname>")
        return
    query = event.rest.strip()
    ippattern = re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}$", query)
    hostpattern = re.match(r"(\w+://)?(?P<hostname>\S+\.\w+)", query)
    if ippattern:
        try:
            answer = getfqdn(ippattern.group(0))
            event.reply(
                "%(hostname)s is %(answer)s" % {"hostname": query, "answer": answer}
            )
        except:
            event.reply("Couldn't lookup ip")
    elif hostpattern:
        try:
            answer = gethostbyname(hostpattern.group("hostname"))
            event.reply("%(ip)s is %(answer)s" % {"ip": query, "answer": answer})
        except:
            event.reply("Couldn't look up the hostname")
    else:
        return


cmnds.add("dns", handle_dns, ["OPER", "USER", "GUEST"])
examples.add("dns", "resolve the ip or the hostname", "dns google.com")
