# jsonbot/datadir.py
#
#

""" the data directory of the bot. """

# jsonbot imports

import logging
import os
import os.path
import shutil

from jsonbot.utils.source import getsource

# basic imports


# the global datadir

try:
    homedir = os.path.abspath(os.path.expanduser("~"))
except:
    homedir = os.getcwd()

isgae = False

try:
    import waveapi

    logging.info("datadir - skipping makedirs")
    datadir = "data"
    isgae = True
except ImportError:
    logging.info("datadir - shell detected")
    datadir = homedir + os.sep + ".jsonbot"

# helper functions


def touch(fname):
    """touch a file."""
    fd = os.open(fname, os.O_WRONLY | os.O_CREAT)
    os.close(fd)


def doit(ddir, mod, target=None):
    source = getsource(mod)
    if not source:
        raise Exception("can't find %s package" % mod)
    shutil.copytree(source, ddir + os.sep + (target or mod.replace(".", os.sep)))


# makedir function


def makedirs(ddir=None):
    """make subdirs in datadir."""
    # if os.path.exists("/home/jsonbot/.jsonbot") and getpass.getuser() == 'jsonbot': ddir = "/home/jsonbot/.jsonbot"
    global datadir
    datadir = ddir or getdatadir()
    logging.warn("datadir - set to %s" % datadir)
    if isgae:
        return
    if not os.path.isdir(ddir):
        try:
            os.mkdir(ddir)
        except:
            raise Exception("can't make %s dir" % ddir)
        logging.info("making dirs in %s" % ddir)
    try:
        os.chmod(ddir, 0o700)
    except:
        pass
    if ddir:
        setdatadir(ddir)
    last = datadir.split(os.sep)[-1]
    # if not os.path.isdir(ddir): doit(ddir, "jsonbot.data")
    try:
        doit(ddir, "jsonbot.plugs.myplugs")
    except:
        pass
    try:
        doit(ddir, "jsonbot.data.examples")
    except:
        pass
    try:
        doit(ddir, "jsonbot.data.static", "static")
    except:
        pass
    try:
        doit(ddir, "jsonbot.data.templates", "templates")
    except:
        pass
    try:
        touch(ddir + os.sep + "__init__.py")
    except:
        pass
    if not os.path.isdir(ddir + os.sep + "config"):
        os.mkdir(ddir + os.sep + "config")
    if not os.path.isfile(ddir + os.sep + "config" + os.sep + "mainconfig"):
        source = getsource("jsonbot.data.examples")
        if not source:
            raise Exception("can't find jsonbot.data.examples package")
        try:
            shutil.copy(
                source + os.sep + "mainconfig.example",
                ddir + os.sep + "config" + os.sep + "mainconfig",
            )
        except (OSError, IOError) as ex:
            logging.error(
                "datadir - failed to copy jsonbot.data.config.mainconfig: %s" % str(ex)
            )
    if not os.path.isfile(ddir + os.sep + "config" + os.sep + "credentials.py"):
        source = getsource("jsonbot.data.examples")
        if not source:
            raise Exception("can't find jsonbot.data.examples package")
        try:
            shutil.copy(
                source + os.sep + "credentials.py.example",
                ddir + os.sep + "config" + os.sep + "credentials.py",
            )
        except (OSError, IOError) as ex:
            logging.error("datadir - failed to copy jsonbot.data.config: %s" % str(ex))
    try:
        touch(ddir + os.sep + "config" + os.sep + "__init__.py")
    except:
        pass
    # myplugs
    initsource = getsource("jsonbot.plugs.myplugs")
    if not initsource:
        raise Exception("can't find jsonbot.plugs.myplugs package")
    initsource = initsource + os.sep + "__init__.py"
    if not os.path.isdir(ddir + os.sep + "myplugs"):
        os.mkdir(ddir + os.sep + "myplugs")
    if not os.path.isfile(ddir + os.sep + "myplugs" + os.sep + "__init__.py"):
        try:
            shutil.copy(initsource, os.path.join(ddir, "myplugs", "__init__.py"))
        except (OSError, IOError) as ex:
            logging.error("datadir - failed to copy myplugs/__init__.py: %s" % str(ex))
    # myplugs.common
    if not os.path.isdir(os.path.join(ddir, "myplugs", "common")):
        os.mkdir(os.path.join(ddir, "myplugs", "common"))
    if not os.path.isfile(os.path.join(ddir, "myplugs", "common", "__init__.py")):
        try:
            shutil.copy(
                initsource, os.path.join(ddir, "myplugs", "common", "__init__.py")
            )
        except (OSError, IOError) as ex:
            logging.error(
                "datadir - failed to copy myplugs/common/__init__.py: %s" % str(ex)
            )
    # myplugs.gae
    if not os.path.isdir(os.path.join(ddir, "myplugs", "gae")):
        os.mkdir(os.path.join(ddir, "myplugs", "gae"))
    if not os.path.isfile(os.path.join(ddir, "myplugs", "gae", "__init__.py")):
        try:
            shutil.copy(initsource, os.path.join(ddir, "myplugs", "gae", "__init__.py"))
        except (OSError, IOError) as ex:
            logging.error(
                "datadir - failed to copy myplugs/gae/__init__.py: %s" % str(ex)
            )
    # myplugs.socket
    if not os.path.isdir(os.path.join(ddir, "myplugs", "socket")):
        os.mkdir(os.path.join(ddir, "myplugs", "socket"))
    if not os.path.isfile(os.path.join(ddir, "myplugs", "socket", "__init__.py")):
        try:
            shutil.copy(
                initsource, os.path.join(ddir, "myplugs", "socket", "__init__.py")
            )
        except (OSError, IOError) as ex:
            logging.error(
                "datadir - failed to copy myplugs/socket/__init__.py: %s" % str(ex)
            )
    if not os.path.isdir(ddir + os.sep + "botlogs"):
        os.mkdir(ddir + os.sep + "botlogs")
    if not os.path.isdir(ddir + "/run/"):
        os.mkdir(ddir + "/run/")
    if not os.path.isdir(ddir + "/users/"):
        os.mkdir(ddir + "/users/")
    if not os.path.isdir(ddir + "/channels/"):
        os.mkdir(ddir + "/channels/")
    if not os.path.isdir(ddir + "/fleet/"):
        os.mkdir(ddir + "/fleet/")
    if not os.path.isdir(ddir + "/pgp/"):
        os.mkdir(ddir + "/pgp/")
    if not os.path.isdir(ddir + "/plugs/"):
        os.mkdir(ddir + "/plugs/")
    if not os.path.isdir(ddir + "/old/"):
        os.mkdir(ddir + "/old/")
    if not os.path.isdir(ddir + "/containers/"):
        os.mkdir(ddir + "/containers/")
    if not os.path.isdir(ddir + "/chatlogs/"):
        os.mkdir(ddir + "/chatlogs/")
    if not os.path.isdir(ddir + "/botlogs/"):
        os.mkdir(ddir + "/botlogs/")
    if not os.path.isdir(ddir + "/spider/"):
        os.mkdir(ddir + "/spider/")
    if not os.path.isdir(ddir + "/spider/data/"):
        os.mkdir(ddir + "/spider/data")
    if os.path.isfile(ddir + "/globals"):
        try:
            os.rename(ddir + "/globals", ddir + "/globals.old")
        except:
            pass
    if not os.path.isdir(ddir + "/globals/"):
        os.mkdir(ddir + "/globals/")


def getdatadir():
    global datadir
    return datadir


def setdatadir(ddir):
    global datadir
    datadir = ddir
