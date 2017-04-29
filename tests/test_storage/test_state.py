import os
import unittest
import logging
import sys
import tempfile

from storage import userdata
from storage.state import StateStorage


class MockStateStorage(StateStorage):
    @classmethod
    def get_filepath(cls):
        return os.path.join(cls.tmpdir, cls.filename)


class TestStateStorage(unittest.TestCase):
    def test_get_file_name(self):
        path = StateStorage.get_filepath()
        expected_path = os.path.join(userdata.get_data_dir(), 'last_station.txt')
        self.assertEqual(path, expected_path)

    def test_set_last_station(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            MockStateStorage.tmpdir = tmpdir

            sample_station_uri = "http://somedomainofradiostation.com/station1.m3u"
            MockStateStorage.set_last_station(sample_station_uri)

            last_uri = MockStateStorage.get_last_station()
            self.assertEqual(last_uri, sample_station_uri)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    unittest.main()
