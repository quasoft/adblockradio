#!/usr/bin/env python3

import os
import sys
import signal
import time
import lockfile
import threading

import gi

import userdata
import utils

gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject

from PyQt4 import QtGui

import config
import systray
from player import Player


class App(QtGui.QApplication):
    def __init__(self, argv):
        QtGui.QApplication.__init__(self, argv)

        self._widget = None
        self._icon = None
        self.show_tray_icon = True
        self.last_uri = ""

        self._player = Player()
        self._player.event_state_change = self.on_state_change
        self._player.event_title_change = self.on_title_change

    def init_tray_icon(self):
        self._widget = QtGui.QWidget()
        self._icon = systray.SystemTrayIcon(QtGui.QIcon("ui/playing.svg"), self._widget)
        self._icon.event_play_click = self.on_play_click
        self._icon.event_pause_click = self.on_pause_click
        self._icon.event_add_to_fav_click = self.on_add_to_fav_click
        self._icon.event_station_select = self.on_station_select
        self._icon.event_exit_click = self.on_exit_click

    def run(self, uri):
        if self.show_tray_icon:
            self.init_tray_icon()

        self._player.play(uri)

        userdata.set_last_station(uri)

        sys.exit(self.exec_())

    def terminate(self):
        self._player.stop()
        super().quit()

    def update_ui_state(self):
        if self._icon:
            self._icon.update_ui_state(self._player.is_playing)

    def update_ui_station(self):
        if self._icon:
            station_name = utils.get_station_name(self._player.current_uri)
            self._icon.update_ui_station(station_name)

    def on_play_click(self, sender):
        self._player.play()

    def on_pause_click(self, sender):
        self._player.stop()

    def on_add_to_fav_click(self, sender, value):
        userdata.add_song_to_favourites(value)

    def on_station_select(self, sender, station):
        self._player.stop()
        self._player.play(station["uri"])
        self.update_ui_state()
        self.update_ui_station()

        userdata.set_last_station(station["uri"])

    def on_exit_click(self, sender):
        self.terminate()

    def on_state_change(self, sender):
        self.update_ui_state()
        self.update_ui_station()

    def on_title_change(self, sender, title):
        if self._icon:
            self._icon.update_ui_title(title)


class ConsoleApp:
    def __init__(self):
        GObject.threads_init()

        self._player = Player()

    def run(self, uri):
        self._player.play(uri)

        self._loop = GObject.MainLoop()
        threading.Thread(target=self._loop.run).start()
        while True:
            time.sleep(1)

    def terminate(self):
        self._player.stop()
        self._loop.quit()


def main(
    station: ('URI to radio station (direct link, not playlist)', 'option', 's') = "",
    daemon: ('Start radio as daemon', 'flag', 'd') = False,
    console: ('Start as console application', 'flag', 'c') = False
):
    """
    The main function to start the application. App can be started in three modes:
      * Qt application with system tray icon, default, no options
      * Console process, with -c option
    """

    # Determine radio station
    # TODO: If no station specified, play last one or a random one
    uri = station
    if not uri:
        uri = userdata.get_last_station()
        if uri:
            print("Connecting to last station selected: %s" % utils.get_station_name(uri))
    if not uri:
        station = utils.get_random_station(config.stations)
        uri = station['uri']
        if uri:
            print("Station randomly selected: %s" % station['name'])
    if not uri:
        raise ValueError('Specify radio station URI as start argument or add one in config.py file!')

    # Start as daemon, if requested
    if daemon:
        import daemon as python_daemon
        context = python_daemon.DaemonContext(
            working_directory='/',
            umask=2,
            pidfile=lockfile.FileLock('/tmp/adblockradio')
        )

        app = ConsoleApp()
        context.signal_map = {
            signal.SIGTERM: app.terminate,
            signal.SIGHUP: 'terminate'
        }
        with context:
            app.run(uri)

    elif console:
        app = App(sys.argv)
        app.show_tray_icon = False
        app.run(uri)
    else:
        app = App(sys.argv)
        app.run(uri)


if __name__ == '__main__':
    import plac
    plac.call(main)
