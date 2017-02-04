#!/usr/bin/env python3
import os
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst

import config
import dispatchers
from storage import userdata
import utils


class Recorder:
    def __init__(self, audio_sink):
        self._audio_sink = audio_sink

        self._is_recording = False
        self._should_create_segment = False

        # Create a valve element that will start/stop the recording branch
        self._valve = Gst.ElementFactory.make('valve')
        self._valve.set_property('drop', 1)
        self._audio_sink.add(self._valve)

        # Convert element decodes audio data (if needed)
        self._convert = Gst.ElementFactory.make('audioconvert')
        self._audio_sink.add(self._convert)
        self._valve.link(self._convert)

        # Convert element resamples audio data (if needed)
        self._resample = Gst.ElementFactory.make('audioresample')
        self._audio_sink.add(self._resample)
        self._convert.link(self._resample)

        # Attach a buffer probe to resample, so that we can get
        # hold of audio data, just before it is passed to codec
        self._resample.get_static_pad('sink').add_probe(Gst.PadProbeType.BUFFER, self.buffer_probe)

        self._codec = None
        self._mux = None
        self._filesink = None
        self.title = None

        dispatchers.recorder.start_record_clicked += self.start
        dispatchers.recorder.stop_record_clicked += self.stop
        dispatchers.player.change_station_clicked += lambda station: self.stop()
        dispatchers.player.song_changed += self.on_song_changed

    def get_src_element(self):
        """Returns the first element in the recording pipeline
           that should be used as a source element to link to
        :rtype: Gst.Element
        :return: Returns a GStreamer element
        """
        return self._valve

    def buffer_probe(self, pad, info):
        """Handles a buffer passing through the pipeline and sends an event
           for starting a new segment downstream the pipeline, if needed.
        :param pad: Gst.Pad
        :param info: Gst.BufferInfo
        :rtype: Gst.PadProbeReturn
        :return: Returns
        """
        if not config.recording["create_segments"]:
            return Gst.PadProbeReturn.OK

        if self._should_create_segment:
            self._should_create_segment = False
            print("Creating a new segment")
            segment = Gst.Segment.new()
            segment.rate = 1
            segment.format = Gst.Format.TIME
            segment.start = 0
            segment.stop = Gst.CLOCK_TIME_NONE
            segment.position = 0
            pad.send_event(Gst.Event.new_segment(segment))

        return Gst.PadProbeReturn.OK

    @property
    def is_recording(self):
        """Returns recording state
        :rtype: bool
        :return: True if recording is active
        """
        return self._is_recording

    def start(self, title):
        """Start recording streaming data into audio file.
        Codec and format of file can be specified in config.py script.
        :param title: Song title - used as filename
        :type filename: str
        """
        self.title = title
        filename = utils.sanitize_filename(self.title) + "." + config.recording["file_ext"].lstrip(".")
        dir = os.path.join(userdata.get_data_dir(), "recorded/")
        os.makedirs(dir, mode=0o777, exist_ok=True)
        path = os.path.join(dir, filename)

        if self._is_recording:
            raise ValueError("Recording has already been started")

        if not path.strip():
            raise ValueError("Filename has not been specified")

        # Start recording
        self._is_recording = True

        self._should_create_segment = config.recording["create_segments"]

        # Create codec and link to pipeline
        self._codec = Gst.ElementFactory.make(config.recording["codec_name"])
        for key in config.recording["codec_props"]:
            value = config.recording["codec_props"][key]
            self._codec.set_property(key, value)
        self._audio_sink.add(self._codec)
        self._resample.link(self._codec)

        # Create file muxer
        self._mux = Gst.ElementFactory.make(config.recording["mux_name"])
        for key in config.recording["mux_props"]:
            value = config.recording["mux_props"][key]
            self._mux.set_property(key, value)
        self._audio_sink.add(self._mux)
        self._codec.link(self._mux)

        # Create filesink - the last element in pipeline that writes data to file
        self._filesink = Gst.ElementFactory.make('filesink')
        self._filesink.set_property('location', path)
        self._filesink.set_property('async', 0)
        self._audio_sink.add(self._filesink)
        self._mux.link(self._filesink)

        # Open valve, so stream can start flowing to the filesink
        self._valve.set_property('drop', 0)

        # Fire events
        dispatchers.recorder.recording_started(self.title)
        dispatchers.recorder.recording_state_changed(self._is_recording)

    def stop(self):
        if not self._is_recording:
            return

        # Send an EOS event to codec and mux to signal those elements that encoding/writing to file should stop
        self._codec.send_event(Gst.Event.new_eos())

        # Close the valve, so no new data can pass into the queue
        self._valve.set_property('drop', 1)

        # TODO: Wait for EOS event in a probe and change state only after it reaches muxer!
        #       This is not done at the moment, because closing the valve also stops the
        #       flow of events, so another mechanism is needed.
        #       It usually works without waiting, but we must not rely on that!

        # Close the file
        self._filesink.set_state(Gst.State.NULL)

        # Remove elements from pipeline
        self._mux.unlink(self._filesink)
        self._codec.unlink(self._mux)
        self._resample.unlink(self._codec)
        self._audio_sink.remove(self._filesink)
        self._audio_sink.remove(self._mux)
        self._audio_sink.remove(self._codec)
        del self._filesink
        del self._mux
        del self._codec

        self._is_recording = False
        self.title = ""

        # Fire events
        dispatchers.recorder.recording_stopped()
        dispatchers.recorder.recording_state_changed(self._is_recording)

    def on_song_changed(self, title):
        if self._is_recording and title != self.title:
            self.stop()
