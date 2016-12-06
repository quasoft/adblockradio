#!/usr/bin/env python3
import sys
import functools
from PyQt4 import QtGui

import config


ICON_BLOCKED = "ui/blocked.svg"
ICON_PLAYING = "ui/playing.svg"
ICON_PAUSED = "ui/paused.svg"


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        self.event_play_click = None
        self.event_pause_click = None
        self.event_add_to_fav_click = None
        self.event_station_select = None
        self.event_exit_click = None

        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        self._icon_blocked = QtGui.QIcon(ICON_BLOCKED)
        self._icon_playing = QtGui.QIcon(ICON_PLAYING)
        self._icon_paused = QtGui.QIcon(ICON_PAUSED)
        self._last_icon = None

        self._last_tooltip = ""
        self._last_song_title = ""

        menu = QtGui.QMenu(parent)
        self._play_action = menu.addAction("Play", self.on_play_click)
        self._pause_action = menu.addAction("Pause", self.on_pause_click)

        menu.addSeparator()
        self._current_song_menu = menu.addMenu("Current song")
        self._add_to_fav_action = self._current_song_menu.addAction("Add to favourites", self.on_add_to_fav_click)

        menu.addSeparator()
        self._stations_menu = menu.addMenu("Stations")
        for station in config.stations:
            item = self._stations_menu.addAction(station['name'], functools.partial(self.on_station_select, station))
            item.setCheckable(True)

        menu.addSeparator()
        self._exit_action = menu.addAction("Exit", self.on_exit_click)

        self.setContextMenu(menu)

        self.activated.connect(self.on_icon_click)
        self.show()

    def on_play_click(self):
        print("Play clicked")
        self.fire_play_click()

    def on_pause_click(self):
        print("Pause clicked")
        self.fire_pause_click()

    def on_add_to_fav_click(self):
        print("Add to favourites clicked", self._last_song_title)
        if self._last_song_title:
            self.fire_add_to_fav_click(self._last_song_title)

    def on_station_select(self, station):
        print("Station changed to '%s'" % station['name'])
        self.fire_station_select(station)

    def on_exit_click(self):
        self.fire_exit_click()
        print("Exit clicked")
        exit(0)

    def on_icon_click(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            print("System tray icon clicked")
            # TODO: Toggle play/pause

    def fire_play_click(self):
        if self.event_play_click:
            self.event_play_click(self)

    def fire_pause_click(self):
        if self.event_pause_click:
            self.event_pause_click(self)

    def fire_add_to_fav_click(self, song):
        if self.event_add_to_fav_click:
            self.event_add_to_fav_click(self, song)

    def fire_station_select(self, station):
        if self.event_station_select:
            self.event_station_select(self, station)

    def fire_exit_click(self):
        if self.event_exit_click:
            self.event_exit_click(self)

    def update_ui_state(self, is_playing):
        if is_playing:
            new_icon = self._icon_playing
        else:
            new_icon = self._icon_paused

        if self._last_icon != new_icon:
            self.setIcon(new_icon)
            self._last_icon = new_icon

        self._play_action.setVisible(not is_playing)
        self._pause_action.setVisible(is_playing)

    def update_ui_station(self, station_name):
        if config.show_systray_tooltip:
            if self._last_tooltip != station_name:
                self.setToolTip(station_name)
                self._last_tooltip = station_name

        for item in self._stations_menu.actions():
            item.setChecked(item.text() == station_name)

    def update_ui_title(self, title):
        if config.show_song_title:
            if self._last_song_title != title:
                self._current_song_menu.setTitle('Current song: %s' % title)
                self._last_song_title = title


class SystemTrayApp:
    def __init__(self):
        self.event_exit_app = None
        """Called when the user clicks the Exit option from the system tray context menu"""

        self._app = QtGui.QApplication(sys.argv)
        self._widget = QtGui.QWidget()
        self._icon = SystemTrayIcon(QtGui.QIcon(ICON_PLAYING), self._widget)
        self._icon.event_exit_click = self.on_exit_click

    def run(self):
        sys.exit(self._app.exec_())

    def fire_exit_app(self):
        if self.event_exit_app:
            self.event_exit_app(self)

    def on_exit_click(self, sender):
        self.fire_exit_app()


if __name__ == '__main__':
    app = SystemTrayApp()
    app.run()
