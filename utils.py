#!/usr/bin/env python3
import random

import config


def get_random_station(stations):
    random_idx = random.randint(0, len(stations) - 1)
    return stations[random_idx]


def get_station_name(uri):
    station = next(station for station in config.stations if station['uri'] == uri)
    return station['name']
