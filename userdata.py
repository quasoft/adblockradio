#!/usr/bin/env python3
import os

from appdirs import AppDirs

LAST_STATION_FILE = "last_station.txt"
FAVOURITE_SONGS_FILE = "favourite_songs.txt"


def get_data_dir():
    dirs = AppDirs("adblockradio", "quasoft")
    return dirs.user_data_dir


def get_last_station_filename():
    return os.path.join(get_data_dir(), LAST_STATION_FILE)


def get_last_station():
    if not os.path.isfile(get_last_station_filename()):
        return ""

    with open(get_last_station_filename()) as f:
        return f.read()


def set_last_station(value):
    os.makedirs(os.path.dirname(get_last_station_filename()), exist_ok=True)
    with open(get_last_station_filename(), 'a+') as f:
        f.truncate(0)
        f.write(value)


def get_favourite_songs_filename():
    return os.path.join(get_data_dir(), FAVOURITE_SONGS_FILE)


def add_song_to_favourites(value):
    os.makedirs(os.path.dirname(get_favourite_songs_filename()), exist_ok=True)
    with open(get_favourite_songs_filename(), 'a+') as f:
        f.write(value + '\n')
