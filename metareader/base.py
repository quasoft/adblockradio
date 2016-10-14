from threading import Thread, Event


class BaseReader:
    def __init__(self, uri):
        self._uri = uri
        self._stopFlag = Event()
        self._thread = None
        self.event_title_read = None

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

    def fire_title_read(self, title):
        if self.event_title_read:
            self.event_title_read(self, title)
