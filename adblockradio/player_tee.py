#!/usr/bin/env python3
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst

from recorder import Recorder
import config


class PlayerTee:
    def __init__(self):
        self._adjust_timestamps = False

        # Create a bin element that will process audio stream before sending it to player
        self._bin = Gst.Bin.new('audiosink')

        # Create tee that splits audio stream in two branches:
        # - one for live playing of stream
        # - one for recording of stream to file
        self._tee = Gst.ElementFactory.make('tee')
        self._bin.add(self._tee)

        # Create branch, which will be responsible for
        # processing of live data and passing it to the player
        # ----------------------------------------------------
        self._live_queue = self.init_live_branch()

        # Create branch, which will be responsible for
        # on demand recording of audio to file
        # ----------------------------------------------------
        self._rec_queue = self.init_recording_branch()

        # Create ghost pads for the custom bin.
        # The source of the bin is linked to the src of the tee element
        # The sink of the bin is linked to the sink of the amplify element
        # Note: Pad direction is reversed, that is way it says sink instead of src and vise versa.
        # ----------------------------------------------------
        self._bin.add_pad(Gst.GhostPad.new('sink', self._tee.get_static_pad('sink')))
        self._bin.add_pad(Gst.GhostPad.new('src', self._amplify.get_static_pad('src')))

    def get_bin_element(self):
        """Returns a custom bin element with both src and sink pad,
           that is responsible for both audio filtering and recording.
        :rtype: Gst.Element
        :return:
        """
        return self._bin

    def init_live_branch(self):
        """
        Creates the branch, that will be responsible for
        processing of live data and passing it to the player
        :return: Queue element
        """
        queue = Gst.ElementFactory.make('queue')
        self._bin.add(queue)
        tee_pad = self._tee.get_request_pad("src_%u")
        queue_pad = queue.get_static_pad('sink')
        tee_pad.link(queue_pad)

        # Create element to attenuate/amplify the signal
        self._amplify = Gst.ElementFactory.make('audioamplify')
        self._amplify.set_property('amplification', config.max_volume)
        self._bin.add(self._amplify)
        queue.link(self._amplify)

        return queue

    def init_recording_branch(self):
        """
        Creates the branch, that will be responsible for
        on demand recording of audio to file
        :return: Queue element
        """

        # Create a queue element and link it to tee (required by tee)
        queue = Gst.ElementFactory.make('queue')
        if config.recording['prerecord']:
            # Set maximums to about 10 minutes of data - the maximum song duration we expect to prebuffer
            queue.set_property('max-size-buffers', 20 * 12 * 200)
            queue.set_property('max-size-bytes', 20 * 12 * 10485760)
            queue.set_property('max-size-time', 20 * 60 * (10 ** 9))
            queue.set_property('min-threshold-time', 10 * 60 * (10 ** 9))
        queue.set_property('leaky', 2)
        self._bin.add(queue)
        tee_pad = self._tee.get_request_pad("src_%u")
        queue_pad = queue.get_static_pad('sink')
        tee_pad.link(queue_pad)

        # Recording elements are created and managed by RecorderBin object
        self._recorder = Recorder(self._bin)
        queue.link(self._recorder.get_src_element())

        return queue

    @property
    def amplification(self):
        return self._amplify.get_property('amplification')

    @amplification.setter
    def amplification(self, value):
        self._amplify.set_property('amplification', value)

    def get_recorder(self):
        return self._recorder

    def prerecord_empty(self):
        """Flush all data in record queue without passing it downstream"""
        self._rec_queue.set_property('max-size-time', 0)
        self._rec_queue.set_property('min-threshold-time', 0)

    def prerecord_hold(self):
        """Start filling the prerecord buffer (up to 10 minutes of data)"""
        self._rec_queue.set_property('max-size-time', 20 * 60 * (10 ** 9))
        self._rec_queue.set_property('min-threshold-time', 10 * 60 * (10 ** 9))

    def prerecord_release(self):
        """Stop filling prerecord buffer"""
        self._rec_queue.set_property('max-size-time', 20 * 60 * (10 ** 9))
        self._rec_queue.set_property('min-threshold-time', 0)
