#!/usr/bin/env python3

import os
import sys
import signal
import time

import re

import lockfile
import threading

import gi

import userdata
import utils
from blacklist import BlacklistStorage
from favourites import FavouritesStorage
from state import StateStorage

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
        self.setQuitOnLastWindowClosed(False)

        self._widget = None
        self._icon = None
        self.show_tray_icon = True
        self.last_uri = ""

        self._player = Player()
        self._player.event_state_change = self.on_state_change
        self._player.event_title_change = self.on_title_change

        # Recorder is provided via player, as we want to get the live data streaming through the player
        self._recorder = self._player.get_recorder()
        self._recorder.event_change = self.on_state_change

    def init_tray_icon(self):
        self._widget = QtGui.QWidget()
        self._icon = systray.SystemTrayIcon(QtGui.QIcon("ui/playing.svg"), self._widget)
        self._icon.event_play_click = self.on_play_click
        self._icon.event_pause_click = self.on_pause_click
        self._icon.event_add_to_fav_click = self.on_add_to_fav_click
        self._icon.event_search_for_lyrics_click  = self.on_search_for_lyrics_click
        self._icon.event_blacklist_click = self.on_blacklist_click
        self._icon.event_record_click = self.on_record_click
        self._icon.event_station_select = self.on_station_select
        self._icon.event_exit_click = self.on_exit_click

    def run(self, uri):
        if self.show_tray_icon:
            self.init_tray_icon()

        self._player.play(uri)

        StateStorage.set_last_station(uri)

        sys.exit(self.exec_())

    def terminate(self):
        if self._recorder.is_recording:
            self._recorder.stop()

        self._player.stop()
        super().quit()

    def update_ui_state(self):
        if self._icon:
            self._icon.update_ui_state(self._player.is_playing, self._recorder.is_recording)

    def update_ui_station(self):
        if self._icon:
            station_name = utils.get_station_name(self._player.current_uri)
            self._icon.update_ui_station(station_name)

    def update_ui_title(self, title):
        if self._icon:
            self._icon.update_ui_title(title)

    def on_play_click(self, sender):
        self._player.play()

    def on_pause_click(self, sender):
        if self._recorder.is_recording:
            self._recorder.stop()

        self._player.stop()

    def on_add_to_fav_click(self, sender, value):
        FavouritesStorage.add_song(value)

    def on_search_for_lyrics_click(self, sender, value):
        utils.open_in_azlyrics(value)

    def on_blacklist_click(self, sender, value):
        # If value contains at least five characters (not spaces), consider this a valid pattern
        if utils.is_valid_blacklist_pattern(value):
            # Construct regex pattern from value: '.*value.*'
            pattern = '.*' + value.strip() + '.*'

            # Ask user to modify pattern, if wanted
            pattern, ok = utils.input_query(None, "Mark as advertisement - blacklist meta title", "Regex pattern:", pattern)
            if not ok:
                return

            # Make sure the user entered a pattern that would not match spaces or an otherwise valid title
            if any(re.search(pattern, t, re.LOCALE) for t in ['', ' ', 'JUST SOME TEST', "\n"]):
                QtGui.QMessageBox.question(
                    None,
                    'Warning',
                    "Pattern rejected!\nIt is too broad and matches empty strings.",
                    QtGui.QMessageBox.Ok
                )
                return

            if BlacklistStorage.exists(pattern):
                QtGui.QMessageBox.question(
                    None,
                    'Information',
                    "Pattern already exists!",
                    QtGui.QMessageBox.Ok
                )
                return

            BlacklistStorage.add_pattern(pattern)

    def on_record_click(self, sender, title):
        if self._recorder.is_recording:
            print("Stopping recording")
            self._recorder.stop()
            self.update_ui_state()
        else:
            print("Recording song %s" % title)
            self._recorder.start(title)
            if config.recording['prerecord']:
                self._player.prerecord_release()
            self.update_ui_state()

            add_to_favourites = QtGui.QMessageBox.question(
                self._widget,
                'Add to favourites?',
                "Song %s will be recorded.\nDo you also want to add it to favourites list?" % title,
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No
            )

            if add_to_favourites == QtGui.QMessageBox.Yes:
                FavouritesStorage.add_song(title)

    def on_station_select(self, sender, station):
        if self._recorder.is_recording:
            self._recorder.stop()
        if config.recording['prerecord']:
            self._player.prerecord_empty()
            self._player.prerecord_hold()

        self._player.stop()
        self._player.play(station["uri"])
        self.update_ui_state()
        self.update_ui_station()

        StateStorage.set_last_station(station["uri"])

    def on_exit_click(self, sender):
        self.terminate()

    def on_state_change(self, sender):
        self.update_ui_state()
        self.update_ui_station()

    def on_title_change(self, sender, title):
        if self._recorder.is_recording and title != self._recorder.title:
            self._recorder.stop()
        if config.recording['prerecord']:
            self._player.prerecord_empty()
            self._player.prerecord_hold()

        self.update_ui_state()
        self.update_ui_title(title)


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
