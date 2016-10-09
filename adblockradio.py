#!/usr/bin/env python3

import signal
import daemon
import lockfile
import time
from player import Player

player = None


def setup():
    global player
    player = Player()


def close():
    global player
    player.stop()


def reload():
    print("Reload config")


def run():
    global player
    player.play("http://stream.radioreklama.bg:80/city64")
    # player.set_property('uri', 'http://mp3channels.webradio.antenne.de/chillout')
    # player.set_property('uri', 'http://149.13.0.81/city64.m3u')
    # player.set_property('uri', 'http://stream.radioreklama.bg:80/city64')
    # player.set_property('uri', 'http://stream.radioreklama.bg:80/radio1rock128')
    # player.set_property('uri', 'http://stream.radioreklama.bg:80/nrj128')
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
