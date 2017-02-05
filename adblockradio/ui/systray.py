#!/usr/bin/env python3
import re
import sys
import functools
from PyQt4 import QtGui
import pkg_resources

import config
import dispatchers
import utils
import ui


ICON_PATH = "ui/svg/"
ICON_BLOCKED = ICON_PATH + "blocked.svg"
ICON_PLAYING = ICON_PATH + "playing.svg"
ICON_PAUSED = ICON_PATH + "paused.svg"
ICON_PLAYING_AND_RECORDING = ICON_PATH + "playing_recording.svg"


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        self._is_playing = False
        self._is_recording = False

        self._icon_blocked = QtGui.QIcon(pkg_resources.resource_filename("adblockradio", ICON_BLOCKED))
        self._icon_playing = QtGui.QIcon(pkg_resources.resource_filename("adblockradio", ICON_PLAYING))
        self._icon_paused = QtGui.QIcon(pkg_resources.resource_filename("adblockradio", ICON_PAUSED))
        self._icon_playing_and_recording = QtGui.QIcon(pkg_resources.resource_filename("adblockradio", ICON_PLAYING_AND_RECORDING))
        self._last_icon = None

        QtGui.QSystemTrayIcon.__init__(self, self._icon_playing, parent)

        self._last_tooltip = ""
        self._last_song_title = ""

        menu = QtGui.QMenu(parent)
        self._play_action = menu.addAction("Play", self.on_play_click)
        self._pause_action = menu.addAction("Pause", self.on_pause_click)

        menu.addSeparator()
        self._current_song_menu = menu.addMenu("Current song")
        self._add_to_fav_action = self._current_song_menu.addAction(
            "Add to favourites",
            self.on_add_to_fav_click
        )
        self._search_for_lyrics_action = self._current_song_menu.addAction(
            "Search for lyrics online", self.on_search_for_lyrics_click
        )
        self._current_song_menu.addSeparator()
        self._blacklist_action = self._current_song_menu.addAction(
            "Mark as advertisement (Blacklist)",
            self.on_blacklist_click
        )
        self._current_song_menu.addSeparator()
        self._start_recording_action = self._current_song_menu.addAction(
            "Record this song",
            self.on_record_click
        )

        menu.addSeparator()
        self._stations_menu = menu.addMenu("Stations")
        for station in config.stations:
            item = self._stations_menu.addAction(station['name'], functools.partial(self.on_station_select, station))
            item.setCheckable(True)

        menu.addSeparator()
        self._manage_menu = menu.addMenu("Manage")
        self._manage_blacklist_action = self._manage_menu.addAction(
            "Blacklist patterns...",
            self.on_manage_blacklist_click
        )
        self._manage_favourites_action = self._manage_menu.addAction(
            "Favourites...",
            self.on_manage_favourites_click
        )

        menu.addSeparator()
        self._exit_action = menu.addAction("Exit", self.on_exit_click)

        self.setContextMenu(menu)

        self.activated.connect(self.on_icon_click)
        self.show()

        dispatchers.player.station_changed += self.on_station_changed
        dispatchers.player.playing_state_changed += self.on_playing_state_changed
        dispatchers.player.song_changed += self.on_song_changed
        dispatchers.recorder.recording_stopped += self.on_recording_stopped
        dispatchers.recorder.recording_state_changed += self.on_recording_state_changed

    def on_play_click(self):
        print("Play clicked")
        dispatchers.player.play_clicked()

    def on_pause_click(self):
        print("Pause clicked")
        dispatchers.player.pause_clicked()

    def on_add_to_fav_click(self):
        print("Add to favourites clicked:", self._last_song_title)
        if self._last_song_title:
            dispatchers.storage.add_to_favourites_clicked(self._last_song_title)

    def on_search_for_lyrics_click(self):
        print("Search for lyrics clicked:", self._last_song_title)
        if self._last_song_title:
            ui.utils.open_in_azlyrics(self._last_song_title)

    def on_blacklist_click(self):
        print("Blacklist clicked:", self._last_song_title)
        if self._last_song_title:
            dispatchers.storage.blacklist_song_clicked(self._last_song_title)

    def on_record_click(self):
        if self._is_recording:
            print("Stop recording clicked")
            dispatchers.recorder.stop_record_clicked()
        else:
            print("Start recording clicked:", self._last_song_title)
            if self._last_song_title:
                dispatchers.recorder.start_record_clicked(self._last_song_title)

                add_to_favourites = QtGui.QMessageBox.question(
                    None,
                    'Add to favourites?',
                    "Song '%s' will be recorded.\nAdd song to favourites?" % self._last_song_title,
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No
                )
                if add_to_favourites == QtGui.QMessageBox.Yes:
                    dispatchers.storage.add_to_favourites_clicked(self._last_song_title)

    def on_station_select(self, station):
        print("Station changed to '%s'" % station['name'])
        self.update_ui_title("")
        dispatchers.player.change_station_clicked(station)

    def on_manage_blacklist_click(self):
        dispatchers.storage.manage_blacklist_clicked()

    def on_manage_favourites_click(self):
        dispatchers.storage.manage_favourites_clicked()

    def on_exit_click(self):
        print("Exit clicked")
        dispatchers.app.exit_clicked()

    def on_icon_click(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            print("System tray icon clicked")
            # TODO: Toggle play/pause

    def on_station_changed(self, station):
        if utils.is_closing:
            return

        station_name = station['name'] if station else ''
        self.update_ui_station(station_name)

    def on_playing_state_changed(self, new_state):
        if utils.is_closing:
            return

        self.update_ui_state(is_playing=new_state)

    def on_song_changed(self, title):
        if utils.is_closing:
            return

        self.update_ui_state()
        self.update_ui_title(title)

    def on_recording_stopped(self):
        if utils.is_closing:
            return

        self.update_ui_title("")

    def on_recording_state_changed(self, new_state):
        if utils.is_closing:
            return

        self.update_ui_state(is_recording=new_state)

    def update_ui_state(self, **kwargs):
        if utils.is_closing:
            return

        if 'is_playing' in kwargs:
            self._is_playing = kwargs['is_playing']

        if 'is_recording' in kwargs:
            self._is_recording = kwargs['is_recording']

        if self._is_playing and self._is_recording:
            new_icon = self._icon_playing_and_recording
        elif self._is_playing:
            new_icon = self._icon_playing
        else:
            new_icon = self._icon_paused

        if self._last_icon != new_icon:
            self.setIcon(new_icon)
            self._last_icon = new_icon

        self._play_action.setVisible(not self._is_playing)
        self._pause_action.setVisible(self._is_playing)

        self._start_recording_action.setText('Stop recording' if self._is_recording else 'Record this song')
        self._start_recording_action.setEnabled(self._is_playing)

    def update_ui_station(self, station_name):
        if utils.is_closing:
            return

        if config.show_systray_tooltip:
            if self._last_tooltip != station_name:
                self.setToolTip(station_name)
                self._last_tooltip = station_name

        for item in self._stations_menu.actions():
            item.setChecked(item.text() == station_name)

    def update_ui_title(self, title):
        if utils.is_closing:
            return

        if config.show_song_title:
            if self._last_song_title != title:
                self._current_song_menu.setTitle('Current song: %s' % utils.truncate_song_title(title))
                self._last_song_title = title
