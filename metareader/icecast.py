from metareader.base import BaseReader
import requests
import re


class IcecastReader(BaseReader):
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

            # Drop audio data
            resp.raw.read(meta_interval)

            # Check how many blocks of meta data are available
            # Can be zero, if no data is available
            meta_blocks = resp.raw.read(1)
            if meta_blocks:
                meta_length = ord(meta_blocks) * 16

                # Read all the meta data
                meta_data = resp.raw.read(meta_length)

                # Parse it and retrieve the StreamTitle
                self._parse(str(meta_data))

        resp.close()

    def _parse(self, data):
        if not data:
            return

        r = re.search("StreamTitle=['\"]?([^'\"]+)['\"]?;", data)
        if r:
            title = r.group(1)
            if title:
                self.fire_title_read(title.strip())
