import requests
import re
from .base import BaseReader


class IcecastReader(BaseReader):
    def __init__(self, uri):
        super().__init__(uri)
        self.user_agent = 'iTunes/9.1.1'

    def _run(self):
        resp = requests.get(
            self._uri,
            headers={
                'User-Agent': self.user_agent,
                'Icy-MetaData': 1
            },
            stream=True
        )
        resp.raise_for_status()

        meta_interval = resp.headers.get('icy-metaint')
        if meta_interval is None:
            raise ValueError("Stream has no icecast metadata (no icy-metaint value received). Fallback to audio data tags.")
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
                #meta_data = str(resp.raw.read(meta_length))
                meta_data = resp.raw.read(meta_length)

                meta_data = meta_data.decode(resp.encoding or 'utf-8')

                # Parse it and retrieve the StreamTitle
                self._parse(meta_data)

        resp.close()

    def _parse(self, data):
        if not data:
            return

        # TODO: use character encoding
        #data = unicode(data)

        r = re.search("StreamTitle=(.+?);", data)
        if r:
            title = r.group(1)
            if title:
                title = title.strip(" \"'")
                self.emit_title_read(title.strip())
