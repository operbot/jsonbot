# gozerbot/periodical.py
#
#

""" provide a periodic structure. """

__author__ = "Wijnand 'tehmaze' Modderman - http://tehmaze.com"
__license__ = "BSD License"

# jsonbot imports

import _thread
import datetime
import logging
import sys
import time

import jsonbot.lib.threads as thr
from jsonbot.lib.callbacks import callbacks
from jsonbot.utils.exception import handle_exception
from jsonbot.utils.locking import lockdec
from jsonbot.utils.timeutils import strtotime
from jsonbot.utils.trace import calledfrom, whichmodule

# basic imorts


# locks

plock = _thread.allocate_lock()
locked = lockdec(plock)

# defines

pidcount = 0

# JobError class


class JobError(Exception):

    """job error exception."""


# Job class


class Job(object):

    """job to be scheduled."""

    group = ""
    pid = -1

    def __init__(self):
        global pidcount
        pidcount += 1
        self.pid = pidcount

    def id(self):
        """return job id."""
        return self.pid

    def member(self, group):
        """check for group membership."""
        return self.group == group

    def do(self):
        """try the callback."""
        try:
            self.func(*self.args, **self.kw)
        except Exception:
            handle_exception()


class JobAt(Job):

    """job to run at a specific time/interval/repeat."""

    def __init__(self, start, interval, repeat, func, *args, **kw):
        Job.__init__(self)
        self.func = func
        self.args = args
        self.kw = kw
        self.repeat = repeat
        self.description = ""
        self.counts = 0
        if type(start) in [int, float]:
            self.next = float(start)
        elif type(start) in [bytes, str]:
            d = strtotime(start)
            if d and d > time.time():
                self.next = d
            else:
                raise JobError("invalid date/time")
        if type(interval) in [int]:
            d = datetime.timedelta(days=interval)
            self.delta = d.seconds
        else:
            self.delta = interval

    def __repr__(self):
        """return a string representation of the JobAt object."""
        return "<JobAt instance next=%s, interval=%s, repeat=%d, function=%s>" % (
            str(self.next),
            str(self.delta),
            self.repeat,
            str(self.func),
        )

    def check(self):
        """run check to see if job needs to be scheduled."""
        if self.next <= time.time():
            logging.info("running %s - %s" % (str(self.func), self.description))
            self.func(*self.args, **self.kw)
            self.next += self.delta
            self.counts += 1
            if self.repeat > 0 and self.counts >= self.repeat:
                return False
        return True


class JobInterval(Job):

    """job to be scheduled at certain interval."""

    def __init__(self, interval, repeat, func, *args, **kw):
        Job.__init__(self)
        self.func = func
        self.args = args
        self.kw = kw
        self.repeat = int(repeat)
        self.counts = 0
        self.interval = float(interval)
        self.description = ""
        self.next = time.time() + self.interval
        self.group = None
        logging.warn(
            "scheduled next run of %s in %d seconds" % (str(self.func), self.interval)
        )

    def __repr__(self):
        return (
            "<JobInterval instance next=%s, interval=%s, repeat=%d, group=%s, function=%s>"
            % (
                str(self.next),
                str(self.interval),
                self.repeat,
                self.group,
                str(self.func),
            )
        )

    def check(self):
        """run check to see if job needs to be scheduled."""
        if self.next <= time.time():
            logging.info("running %s - %s" % (str(self.func), self.description))
            self.next = time.time() + self.interval
            thr.start_new_thread(self.do, ())
            self.counts += 1
            if self.repeat > 0 and self.counts >= self.repeat:
                return False
        return True


class Periodical(object):

    """periodical scheduler."""

    def __init__(self):
        self.jobs = []
        self.running = []
        self.run = True

    def size(self):
        return len(self.jobs)

    def addjob(self, sleeptime, repeat, function, description="", *args, **kw):
        """add a periodical job."""
        job = JobInterval(sleeptime, repeat, function, *args, **kw)
        job.group = calledfrom(sys._getframe())
        job.description = str(description) or whichmodule()
        self.jobs.append(job)
        return job.pid

    def changeinterval(self, pid, interval):
        """change interval of of peridical job."""
        for i in periodical.jobs:
            if i.pid == pid:
                i.interval = interval
                i.next = time.time() + interval

    def looponce(self, bot, event):
        """loop over the jobs."""
        for job in self.jobs:
            if job.next <= time.time():
                self.runjob(job)

    def runjob(self, job):
        """run a periodical job."""
        if not job.check():
            self.killjob(job.id())
        else:
            self.running.append(job)

    def kill(self):
        """kill all jobs invoked by another module."""
        group = calledfrom(sys._getframe())
        self.killgroup(group)

    def killgroup(self, group):
        """kill all jobs with the same group."""

        def shoot():
            """knock down all jobs belonging to group."""
            deljobs = [job for job in self.jobs if job.member(group)]
            for job in deljobs:
                self.jobs.remove(job)
                try:
                    self.running.remove(job)
                except ValueError:
                    pass
            logging.warn("killed %d jobs for %s" % (len(deljobs), group))
            del deljobs

        return shoot()

    def killjob(self, jobId):
        """kill one job by its id."""

        def shoot():
            deljobs = [x for x in self.jobs if x.id() == jobId]
            numjobs = len(deljobs)
            for job in deljobs:
                self.jobs.remove(job)
                try:
                    self.running.remove(job)
                except ValueError:
                    pass
            del deljobs
            return numjobs

        return shoot()


def interval(sleeptime, repeat=0):
    """interval decorator."""
    group = calledfrom(sys._getframe())

    def decorator(function):
        decorator.__dict__ = function.__dict__

        def wrapper(*args, **kw):
            job = JobInterval(sleeptime, repeat, function, *args, **kw)
            job.group = group
            job.description = whichmodule()
            periodical.jobs.append(job)
            logging.warn(
                "new interval job %d with sleeptime %d" % (job.id(), sleeptime)
            )

        return wrapper

    return decorator


def at(start, interval=1, repeat=1):
    """at decorator."""
    group = calledfrom(sys._getframe())

    def decorator(function):
        decorator.__dict__ = function.__dict__

        def wrapper(*args, **kw):
            job = JobAt(start, interval, repeat, function, *args, **kw)
            job.group = group
            job.description = whichmodule()
            periodical.jobs.append(job)

        wrapper.__dict__ = function.__dict__
        return wrapper

    return decorator


def persecond(function):
    """per second decorator."""
    minutely.__dict__ = function.__dict__
    group = calledfrom(sys._getframe())

    def wrapper(*args, **kw):
        job = JobInterval(1, 0, function, *args, **kw)
        job.group = group
        job.description = whichmodule()
        periodical.jobs.append(job)
        logging.debug("new interval job %d running per second" % job.id())

    return wrapper


def minutely(function):
    """minute decorator."""
    minutely.__dict__ = function.__dict__
    group = calledfrom(sys._getframe())

    def wrapper(*args, **kw):
        job = JobInterval(60, 0, function, *args, **kw)
        job.group = group
        job.description = whichmodule()
        periodical.jobs.append(job)
        logging.warn("new interval job %d running minutely" % job.id())

    return wrapper


def hourly(function):
    """hour decorator."""
    logging.warn("@hourly(%s)" % str(function))
    hourly.__dict__ = function.__dict__
    group = calledfrom(sys._getframe())

    def wrapper(*args, **kw):
        job = JobInterval(3600, 0, function, *args, **kw)
        job.group = group
        job.description = whichmodule()
        logging.warn("new interval job %d running hourly" % job.id())
        periodical.jobs.append(job)

    return wrapper


def daily(function):
    """day decorator."""
    logging.warn("@daily(%s)" % str(function))
    daily.__dict__ = function.__dict__
    group = calledfrom(sys._getframe())

    def wrapper(*args, **kw):
        job = JobInterval(86400, 0, function, *args, **kw)
        job.group = group
        job.description = whichmodule()
        periodical.jobs.append(job)
        logging.warb("new interval job %d running daily" % job.id())

    return wrapper


periodical = Periodical()

callbacks.add("TICK", periodical.looponce)


def size():
    return periodical.size()
