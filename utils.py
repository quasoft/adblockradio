#!/usr/bin/env python3
import random
import requests

import config


def get_random_station(stations):
    random_idx = random.randint(0, len(stations) - 1)
    return stations[random_idx]


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
