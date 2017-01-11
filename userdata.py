#!/usr/bin/env python3
from appdirs import AppDirs


def get_data_dir():
    dirs = AppDirs("adblockradio", "quasoft")
    return dirs.user_data_dir
