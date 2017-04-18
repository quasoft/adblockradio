#!/usr/bin/env python3
import random
import re
import requests
import unicodedata
import sys
import os
import pkg_resources

import config

MAX_SONG_TITLE_LENGTH = 35

is_closing = False
"""This flag is set to True when the application begins to shut down.
   Parts of the program that handle events might use this flag as a
   signal to ignore some events like change of player state.
"""


def get_other_stations(uri):
    return list(filter(lambda s: s['uri'] != uri, config.stations))


def get_random_station(stations):
    random_idx = random.randint(0, len(stations) - 1)
    return stations[random_idx]


def get_station(uri):
    station = next(filter(lambda s: s['uri'] == uri, config.stations), None)
    return station


def get_station_name(uri):
    name = next((station['name'] for station in config.stations if station['uri'] == uri), "")
    return name


def get_stream_from_playlist(url):
    resp = requests.get(
        url,
        headers={
            'User-Agent': config.user_agent
        }
    )
    resp.raise_for_status()

    content = str(resp.text)
    resp.close()

    if not content:
        return None

    lines = (line for line in content.splitlines() if line.strip().startswith("http"))

    if not lines:
        return None

    return next(lines)


def sanitize_filename(filename):
    value = unicodedata.normalize('NFKC', filename)
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def truncate_song_title(title):
    value = title.strip()

    # If the title is too long, leave the part after the last delimiter (dash)
    if len(value) > MAX_SONG_TITLE_LENGTH - 3:
        parts = re.split(':|;|-', value)
        value = '...' + parts[-1] if len(parts) > 1 else value

    # If the title is still too long, remove text in brackets
    if len(value) > MAX_SONG_TITLE_LENGTH - 3:
        value = re.sub('[(]+[\w\s]+[)]+', '...', value)

    # If the title is still too long, just trim the beginning
    if len(value) > MAX_SONG_TITLE_LENGTH - 3:
        value = value[:MAX_SONG_TITLE_LENGTH] + '...'

    return value


def is_frozen():
    return getattr(sys, 'frozen', False)


def resource_filename(filename):
    if is_frozen():
        path = os.path.join(sys._MEIPASS, filename)
    else:
        path = pkg_resources.resource_filename("adblockradio", filename)

    return path


def set_gst_plugin_path():
    path = sys._MEIPASS + ";" + os.path.join(sys._MEIPASS, 'gst_plugins')
    os.environ["GST_PLUGIN_PATH"] = path
    os.environ["GST_PLUGIN_PATH_1_0"] = path

