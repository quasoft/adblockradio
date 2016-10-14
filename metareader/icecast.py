import requests
from threading import Thread, Event
from metareader.base_metareader import BaseMetaReader


class IcecastMetaReader(BaseMetaReader):
    def __init__(self, uri):
        super().__init__(uri)
        self._user_agent = 'iTunes/9.1.1'

    def _run(self):
        resp = requests.get(
            self._uri,
            headers={
                'User-Agent': self._user_agent,
                'Icy-MetaData': 1
            },
            stream=True
        )
        resp.raise_for_status()

        meta_interval = int(resp.headers.get('icy-metaint'))

        while True:
            # If main thread has requested, stop reading data
            if self._stopFlag.is_set():
                break

            resp.raw.read(meta_interval)
            meta_blocks = resp.raw.read(1)
            if meta_blocks:
                meta_length = ord(meta_blocks) * 16
                meta_data = resp.raw.read(meta_length)
                print(meta_data)

        resp.close()
