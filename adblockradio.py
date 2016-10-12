#!/usr/bin/env python3

import os
import sys
import signal
import daemon as python_daemon
import lockfile
import time
import plac
from player import Player


_player = None


def main(
    station: ('URI to radio station (direct link, not playlist)', 'option', 's'),
    daemon: ('Start radio as daemon', 'flag', 'd'),
    config: ("Path to config file",'option', 'c')
):
    context = python_daemon.DaemonContext(
        working_directory='/',
        umask=2,
        pidfile=lockfile.FileLock('/tmp/adblockradio')
    )

    context.signal_map = {
        signal.SIGTERM: close,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reload,
    }

    # Initialize application
    global _player
    _player = Player()

    # Determine radio station
    uri = ""
    if station:
        uri = station
    #elif os.path.isfile(STATION_FILE):
    #    with open(STATION_FILE, 'r') as f:
    #        uri = f.read().strip()

    if len(uri) == 0:
        raise ValueError('Specify radio station URI as start argument or add it in station.txt file!')

    # Start as daemon, if requested
    if daemon:
        with context:
            run(uri)
    else:
        run(uri)


def close():
    global _player
    _player.stop()


def reload():
    print("Reload config")


def run(uri):
    global _player

    _player.play(uri)

    while True:
        time.sleep(1)


if __name__ == '__main__':
    import plac
    plac.call(main)
