#!/usr/bin/env python3
import threading
import time

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst

import config
import dispatchers
import utils
from storage.blacklist import BlacklistStorage
from metareader.icecast import IcecastReader
from player_tee import PlayerTee


class Player:
    def __init__(self):
        self._in_ad_block = False
        self._last_ad_time = None
        self._last_uri = ""
        self._last_title = ""
        self._just_switched = True
        GObject.timeout_add(1000, self.on_timer_check_ad_duration)

        # Initialize GStreamer
        Gst.init(None)

        self._tee_bin = PlayerTee()

        # Create playbin and add the custom audio sink to it
        self._player = Gst.ElementFactory.make("playbin", "player")
        self._player.set_property('audio_filter', self._tee_bin.get_bin_element())

        # Listen for player events
        self._bus = self._player.get_bus()
        self._bus.enable_sync_message_emission()
        self._bus.add_signal_watch()
        self._bus.connect('message::tag', self.on_tag)
        # TODO: watch status messages
        self._bus.connect("message", self.on_message)
        # TODO: connect to events

        self._meta_reader = None
        """
        Metareader is only used if config.blacklisted_tags have been
        configured. Those tags are used to detect beginning and ending
        of advertisement blocks
        """
        dispatchers.player.play_clicked += self.play
        dispatchers.player.pause_clicked += self.stop
        dispatchers.player.change_station_clicked += self.on_change_station_clicked
        dispatchers.recorder.recording_started += self.on_recording_started
        dispatchers.recorder.recording_stopped += self.on_recording_stopped

    def get_recorder(self):
        return self._tee_bin.get_recorder()

    @property
    def is_playing(self):
        state = self._player.get_state(100)[1]
        return state == Gst.State.PLAYING or state == Gst.State.READY

    @property
    def current_uri(self):
        return self._last_uri

    @property
    def volume(self):
        return self._tee_bin.amplification

    @volume.setter
    def volume(self, value):
        self._tee_bin.amplification = value

    def on_tag(self, bus, message):
        taglist = message.parse_tag()

        if not self._meta_reader or not self._meta_reader.is_running:
            title = taglist.get_string('title')
            if title and title.value:
                title = title.value
                title = title.strip(" \"'")
                self.on_title_read(title)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.stop()
            self.play()
        elif t == Gst.MessageType.EOS:
            self.stop()
        elif t == Gst.MessageType.BUFFERING:
            # TODO: pause stream
            # Check message.buffer_percent
            pass
        elif t == Gst.MessageType.STATE_CHANGED:
            self.fire_state_change()

    # Handle song metadata
    def on_title_read(self, title):
        assert threading.current_thread() == threading.main_thread()

        if title is None:
            return

        if title != self._last_title:
            self._last_title = title

            # TODO: Fade volume gradually
            # TODO: Allow user to choose what to do when an advertisement block is detected.
            #       Ideas for possible options:
            #       * reduce or mute volume
            #       * play random audio file from a local directory
            #       * switch to another radio station
            #       * repeat part of last song
            print("Title changed to %s" % title)

            # If the title contains a blacklisted tag, reduce volume
            if BlacklistStorage.is_blacklisted(title):
                if not self._in_ad_block:
                    print('Advertisement tag detected.')
                    if config.block_mode in (config.BlockMode.REDUCE_VOLUME, config.BlockMode.REDUCE_AND_SWITCH):
                        print('Reducing volume.')
                        self.volume = config.ad_block_volume
                        self._in_ad_block = True
                        self._last_ad_time = time.time()
                    elif config.block_mode == config.BlockMode.SWITCH_STATION:
                        self.switch_to_another_station()
            else:
                if self._in_ad_block:
                    print('Restoring volume to maximum.')
                    if config.block_mode in (config.BlockMode.REDUCE_VOLUME, config.BlockMode.REDUCE_AND_SWITCH):
                        self.volume = config.max_volume
                    self._in_ad_block = False
                    self._last_ad_time = None
                    self._just_switched = False

            dispatchers.player.song_changed(title)

    def on_timer_check_ad_duration(self):
        if not self._last_ad_time:
            return True
        duration = time.time() - self._last_ad_time

        if self._in_ad_block and self._just_switched:
            # If we have just switched to a new station, and this station is also
            # in advertisement block, switch immediately again to another one
            print("Switch again immediately.")
            if config.block_mode in (config.BlockMode.SWITCH_STATION, config.BlockMode.REDUCE_AND_SWITCH):
                # Switch to another radio station
                self.switch_to_another_station()
        elif self._in_ad_block:
            print("Ad block with duration of %d seconds." % duration)
            if (config.block_mode == config.BlockMode.REDUCE_AND_SWITCH
                    and duration > config.max_ad_duration):
                # Switch to another radio station
                self.switch_to_another_station()
        else:
            # If 10 seconds have passed since last switch of station, reset the timer /
            # disable immediate switch to yet another station
            if self._just_switched and duration > config.max_ad_duration:
                print("Reset just_switched")
                self._just_switched = False

        return True

    def fire_state_change(self):
        assert threading.current_thread() == threading.main_thread()
        dispatchers.player.playing_state_changed(self.is_playing)

    def play(self, uri=""):
        self._last_title = ""

        # Play last URI, if none provided
        if not uri:
            uri = self._last_uri

        # Automatically extract uri to stream from m3u playlists
        stream_uri = uri
        if stream_uri.endswith("m3u"):
            stream_uri = utils.get_stream_from_playlist(stream_uri)

        # Set URI to online radio
        self._player.set_property('uri', stream_uri)

        # Start playing
        self._player.set_state(Gst.State.PLAYING)

        # Reset volume level
        self.volume = config.max_volume

        if not BlacklistStorage.is_empty():
            # TODO: Determine server type and use different reader for each
            self._meta_reader = IcecastReader(uri)
            self._meta_reader.user_agent = config.user_agent
            self._meta_reader.event_title_read += self.on_title_read
            self._meta_reader.start()

        self.fire_state_change()

        if uri != self._last_uri:
            self._last_uri = uri
            dispatchers.player.station_changed(utils.get_station(uri))

    def stop(self):
        if self.get_recorder().is_recording:
           self.get_recorder().stop()

        # Stop metadata reader, if using one
        if self._meta_reader:
            self._meta_reader.stop()

        # Stop playing
        self._player.set_state(Gst.State.NULL)

        self._in_ad_block = False
        self._last_ad_time = None
        self._just_switched = False
        self._last_title = ""

        self.fire_state_change()

    def switch_to_another_station(self):
        print('Switching to another station.')
        other_stations = utils.get_other_stations(self._last_uri)
        station = utils.get_random_station(other_stations)

        print("Station chosen: %s" % station['name'])

        self.stop()
        self.play(station['uri'])

        self._just_switched = True
        self._last_ad_time = time.time()

        dispatchers.player.station_changed(station)

    def on_change_station_clicked(self, station):
        self.stop()
        self.play(station["uri"])

        dispatchers.player.station_changed(station)

    def on_recording_started(self, title):
        if config.recording['prerecord']:
            # Flush prebuffered part of song to file
            self._tee_bin.prerecord_release()
        # When a recording branch is attached to tee, playback should be restarted
        if self.is_playing:
            self._player.set_state(Gst.State.PLAYING)

    def on_recording_stopped(self):
        if config.recording['prerecord']:
            self._tee_bin.prerecord_empty()
            self._tee_bin.prerecord_hold()
        if self.is_playing:
            self._player.set_state(Gst.State.PLAYING)
