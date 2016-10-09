#!/usr/bin/env python3

import os
import sys
import signal
import daemon
import lockfile
import time
from player import Player

STATION_FILE = 'station.txt'

player = None
uri = ""

def setup():
    global player, uri
    player = Player()

    uri = ""
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    elif os.path.isfile(STATION_FILE):
        with open(STATION_FILE, 'r') as f:
            uri = f.read().strip()

    if len(uri) == 0:
        raise ValueError('Specify radio station URI as start argument or add it in station.txt file!')


def close():
    global player
    player.stop()


def reload():
    print("Reload config")


def run():
    global player, uri

    player.play(uri)

    while True:
        time.sleep(1)


context = daemon.DaemonContext(
    working_directory='/',
    umask=2,
    pidfile=lockfile.FileLock('/tmp/adblockradio')
    )

context.signal_map = {
    signal.SIGTERM: close,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: reload,
    }

setup()

with context:
    run()
