#!/usr/bin/env python3
import threading
import re
import random

import utils
from metareader.icecast import IcecastReader
import config

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst

class Player:
    def __init__(self):
        self._in_ad_block = False
        self._last_uri = ""

        self.event_state_change = None

        # Initialize GStreamer
        Gst.init(None)

        # Create element to attenuate/amplify the signal
        self._amplify = Gst.ElementFactory.make('audioamplify')
        self._amplify.set_property('amplification', config.max_volume)

        # Create playbin and add the custom audio sink to it
        self._player = Gst.ElementFactory.make("playbin", "player")
        self._player.set_property('audio_filter', self._amplify)

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

    @property
    def is_playing(self):
        state = self._player.get_state(100)[1]
        return state == Gst.State.PLAYING or state == Gst.State.READY

    @property
    def current_uri(self):
        return self._last_uri

    @property
    def volume(self):
        return self._amplify.get_property('amplification')

    @volume.setter
    def volume(self, value):
        self._amplify.set_property('amplification', value)

    def on_tag(self, bus, message):
        taglist = message.parse_tag()

        if not self._meta_reader.is_running:
            title = taglist.get_string('title')
            if title and title.value:
                title = title.value
                title = title.strip(" \"'")
                self.on_title_read(self, title)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.stop()
        elif t == Gst.MessageType.EOS:
            self.stop()
        elif t == Gst.MessageType.BUFFERING:
            # TODO: pause stream
            pass

    # Handle song metadata
    def on_title_read(self, sender, title):
        if title is not None:
            # TODO: Fade volume gradually
            # TODO: Allow user to choose what to do when an advertisement block is detected.
            #       Ideas for possible options:
            #       * reduce or mute volume
            #       * play random audio file from a local directory
            #       * switch to another radio station
            #       * repeat part of last song
            print("Title changed to %s" % title)

            # If the title contains a blacklisted tag, reduce volume
            if any(re.search(p, title) for p in config.blacklisted_tags):
                if not self._in_ad_block:
                    print('Advertisement tag detected.')
                    if config.block_mode == config.BlockMode.REDUCE_VOLUME:
                        print('Reducing volume.')
                        self.volume = config.ad_block_volume
                        self._in_ad_block = True
                    elif config.block_mode == config.BlockMode.SWITCH_STATION:
                        print('Switching to another station.')

                        other_stations = list(filter(lambda s: s['uri'] != self._last_uri, config.stations))

                        station = utils.get_random_station(other_stations)

                        print("Station chosen: %s" % station['name'])

                        self.stop()
                        self.play(station['uri'])
            else:
                if self._in_ad_block:
                    print('Restoring volume to maximum.')
                    if config.block_mode == config.BlockMode.REDUCE_VOLUME:
                        self.volume = config.max_volume
                    self._in_ad_block = False

    def fire_state_change(self):
        if self.event_state_change:
            self.event_state_change(self)

    def play(self, uri=""):
        # Play last URI, if none provided
        if uri:
            self._last_uri = uri
        else:
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

        if len(config.blacklisted_tags) > 0:
            # TODO: Determine server type and use different reader for each
            self._meta_reader = IcecastReader(uri)
            self._meta_reader.user_agent = config.user_agent
            self._meta_reader.event_title_read = self.on_title_read
            self._meta_reader.start()

        self.fire_state_change()

    def stop(self):
        # Stop metadata reader, if using one
        if self._meta_reader:
            self._meta_reader.stop()

        # Stop playing
        self._player.set_state(Gst.State.NULL)

        self._in_ad_block = False

        self.fire_state_change()
