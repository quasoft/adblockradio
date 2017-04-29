#!/usr/bin/env python3
import sys
import threading
import time

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject
from PyQt4 import QtGui

import config
import dispatchers
import utils
from ui import systray
from storage.state import StateStorage
from storage.blacklist import BlacklistStorage
from storage.favourites import FavouritesStorage
from player import Player


class App(QtGui.QApplication):
    def __init__(self, argv):
        QtGui.QApplication.__init__(self, argv)
        self.setQuitOnLastWindowClosed(False)

        self._widget = None
        self._icon = None
        self.show_tray_icon = True

        self._player = Player()

        dispatchers.app.exit_clicked += self.on_exit_click

        # Keep IDE from removing those ununsed imports
        StateStorage()
        BlacklistStorage()
        FavouritesStorage()

    def init_tray_icon(self):
        self._widget = QtGui.QWidget()
        self._icon = systray.SystemTrayIcon(self._widget)

    def run(self, uri):
        if self.show_tray_icon:
            self.init_tray_icon()

        self._player.play(uri)

        StateStorage.set_last_station(uri)

        sys.exit(self.exec_())

    def terminate(self):
        utils.is_closing = True

        self._player.stop()

        super().quit()

    def on_exit_click(self):
        self.terminate()


class ConsoleApp:
    def __init__(self):
        GObject.threads_init()

        self._loop = GObject.MainLoop()
        self._player = Player()

    def run(self, uri):
        self._player.play(uri)


        threading.Thread(target=self._loop.run).start()
        while True:
            time.sleep(1)

    def terminate(self):
        self._player.stop()
        self._loop.quit()


def main(
    station: ('URI to radio station (direct link, not playlist)', 'option', 's') = "",
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
        uri = StateStorage.get_last_station()
        if uri:
            print("Connecting to last station selected: %s" % utils.get_station_name(uri))
    if not uri:
        station = utils.get_random_station(config.stations)
        uri = station['uri']
        if uri:
            print("Station randomly selected: %s" % station['name'])
    if not uri:
        raise ValueError('Specify radio station URI as start argument or add one in config.py file!')

    # Start as console app, if requested
    if console:
        app = App(sys.argv)
        app.show_tray_icon = False
        app.run(uri)
    else:
        app = App(sys.argv)
        app.run(uri)


if __name__ == '__main__':
    import plac
    plac.call(main)
