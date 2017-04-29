from threading import Thread, Event

from PyQt4 import QtCore

import utils
import event


class BaseReader(QtCore.QObject):
    signal_title_read = QtCore.pyqtSignal(object)

    def __init__(self, uri):
        super().__init__()
        self._uri = uri

        # Automatically extract uri to stream from m3u playlists
        self._uri = utils.read_uri_from_playlist(self._uri)

        self._stopFlag = Event()
        self._thread = None
        self.signal_title_read.connect(self._slot_title_read)

    @property
    def is_running(self):
        return self._thread.isAlive()

    def start(self):
        if self._thread:
            raise ValueError("Reader has already been started!")

        self._stopFlag.clear()
        self._thread = Thread(target=self._run)
        self._thread.start()

    def stop(self):
        if self._thread:
            self._stopFlag.set()
            self._thread.join()

    def _run(self):
        raise NotImplementedError("Abstract method BaseMetaReader._run()!")

        # Example:
        # while True:
        #     if self._stopFlag.is_set():
        #         break

    def _slot_title_read(self, title):
        self.event_title_read(title)

    @event.Event
    def event_title_read(self, title):
        pass

    # Descendants should use the emit_title_read method to signal for a new title.
    # _slot_title_read and _fire_title_read are used internally in base class for synchronization
    # with main thread
    def emit_title_read(self, title):
        self.signal_title_read.emit(title)

