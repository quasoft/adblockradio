#!/usr/bin/env python3
import gi
import threading
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst

class Player:
    def __init__(self):
        # Initialize threads
        GObject.threads_init()

        # Initialize GStreamer
        Gst.init(None)

        # Create element to attenuate/amplify the signal
        self.amplify = Gst.ElementFactory.make('audioamplify')
        self.amplify.set_property('amplification', 1.0)

        # Create playbin and add the custom audio sink to it
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.player.set_property('audio_filter', self.amplify)

        # Listen for metadata
        self.bus = self.player.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.add_signal_watch()
        self.bus.connect('message::tag', self.on_tag)

    # Handle song metadata
    def on_tag(self, bus, msg):
        taglist = msg.parse_tag()
        print('')
        print('Tags:', taglist.n_tags())
        for key in range(taglist.n_tags()):
            print('\t%s = %s' % (taglist.nth_tag_name(key), taglist.get_string(taglist.nth_tag_name(key)).value))


    def play(self, uri):
        # Set URI to online radio
        self.player.set_property('uri', uri)

        # Start playing
        self.player.set_state(Gst.State.PLAYING)

        self.loop = GObject.MainLoop()
        threading.Thread(target=self.loop.run).start()

    def stop(self):
        # Stop playing
        self.player.set_state(Gst.State.NULL)

        # Stop loop
        self.loop.quit()
