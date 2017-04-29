import os
import random
import unittest
import logging
import sys

import config
import utils


class TestModule(unittest.TestCase):
    def setUp(self):
        config.stations = [
            {'name': 'Station1', 'uri': 'http://somenonexistentradiostation1.local'},
            {'name': 'Station2', 'uri': 'http://somenonexistentradiostation2.local'},
            {'name': 'Station3', 'uri': 'http://somenonexistentradiostation3.local'}
        ]

    def test_get_other_stations(self):
        other_stations = utils.get_other_stations('http://somenonexistentradiostation2.local')
        self.assertEqual(2, len(other_stations))
        self.assertEqual('Station1', other_stations[0]['name'])
        self.assertEqual('Station3', other_stations[1]['name'])

    def test_get_station(self):
        station = utils.get_station('http://somenonexistentradiostation2.local')
        self.assertIsNotNone(station)
        self.assertEqual('Station2', station['name'])

    def test_get_random_station(self):
        random.seed(0)
        station = utils.get_random_station(config.stations)
        self.assertIsNotNone(station)
        self.assertEqual('Station2', station['name'])

    def test_get_station_name(self):
        station_name = utils.get_station_name('http://somenonexistentradiostation3.local')
        self.assertEqual('Station3', station_name)

    def test_read_uri_from_m3u_string(self):
        file_name = os.path.join(os.path.dirname(__file__), 'samples', 'simple-playlist.m3u')
        with open(file_name, 'r') as f:
            uri = utils.read_uri_from_m3u_string(f.read())
        self.assertEqual('http://somenonexistentradiostation3.local:8008/stream.mp3', uri)

    def test_read_uri_from_m3u_with_empty_string(self):
        uri = utils.read_uri_from_m3u_string('')
        self.assertIsNone(uri)

    def test_read_uri_from_pls_string(self):
        file_name = os.path.join(os.path.dirname(__file__), 'samples', 'simple-playlist.pls')
        with open(file_name, 'r') as f:
            uri = utils.read_uri_from_pls_string(f.read())
        self.assertEqual('http://somenonexistentradiostation3.local:8008/stream.mp3', uri)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    unittest.main()
