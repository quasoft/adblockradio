#!/usr/bin/env python3
import threading
import re
import config
from metareader.icecast import IcecastReader
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst


class Player:
    def __init__(self):
        self._in_ad_block = False

        # Initialize threads
        GObject.threads_init()

        # Initialize GStreamer
        Gst.init(None)

        self._loop = None

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
        # TODO: connect to events

        self._meta_reader = None
        """
        Metareader is only used if config.blacklisted_tags have been
        configured. Those tags are used to detect beginning and ending
        of advertisement blocks
        """

    @property
    def volume(self):
        return self._amplify.get_property('amplification')

    @volume.setter
    def volume(self, value):
        self._amplify.set_property('amplification', value)

    # Handle song metadata
    def _title_read_handler(self, sender, title):
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
                    print('Advertisement tag detected. Reducing volume.')
                    self.volume = config.ad_block_volume
                    self._in_ad_block = True
            else:
                if self._in_ad_block:
                    print('Restoring volume to maximum.')
                    self.volume = config.max_volume
                    self._in_ad_block = False

    def play(self, uri):
        # Set URI to online radio
        self._player.set_property('uri', uri)

        # Start playing
        self._player.set_state(Gst.State.PLAYING)

        self._loop = GObject.MainLoop()
        threading.Thread(target=self._loop.run).start()

        if len(config.blacklisted_tags) > 0:
            # TODO: Determine server type and use different reader for each
            self._meta_reader = IcecastReader(uri)
            self._meta_reader.event_title_read = self._title_read_handler
            self._meta_reader.start()

    def stop(self):
        # Stop metadata reader, if using one
        if self._meta_reader:
            self._meta_reader.stop()

        # Stop playing
        self._player.set_state(Gst.State.NULL)

        # Stop loop
        self._loop.quit()
