#!/usr/bin/env python3
import random
import re
import requests
import unicodedata
from PyQt4 import QtGui
import urllib
import webbrowser

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


def is_valid_blacklist_pattern(pattern):
    """
    If value contains at least five characters (not spaces), consider this a valid pattern
    :param pattern: The regex pattern to check
    :return: True if pattern is valid
    """
    matches = re.findall('[\S]+', pattern, re.LOCALE)
    return len(matches) >= 5


def input_query(parent, title, prompt, default_value="", width=500, height=100):
    """
    Opens an dialog box for entering a single text value
    :param parent: Parent widget
    :param title: Dialog title
    :param prompt: Label text before input box
    :param default_value: Default value
    :param width: Dialog width
    :param height: Dialog height
    :return: tuple (value, ok) - (text value entered by user, was OK button clicked)
    """
    dlg = QtGui.QInputDialog(parent)
    dlg.setInputMode(QtGui.QInputDialog.TextInput)
    dlg.setWindowTitle(title)
    dlg.setLabelText(prompt)
    dlg.setTextValue(default_value)
    dlg.resize(width, height)
    ok = dlg.exec_()
    value = dlg.textValue()
    dlg.close()
    return value, ok


def sanitize_filename(filename):
    value = unicodedata.normalize('NFKC', filename)
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def open_in_azlyrics(title):
    params = {'q': title}
    url = 'http://search.azlyrics.com/search.php?' + urllib.parse.urlencode(params)
    webbrowser.open(url)