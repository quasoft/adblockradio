import re

from PyQt4 import QtGui

import dispatchers
from .base import BaseStorage
from ui.dlg_blacklist_editor import DlgBlacklistEditor
import ui


class BlacklistStorage(BaseStorage):
    """Manages patterns for blacklisting song titles.
    The storage is a simple text file with separate patterns (regular expressions)
    written on each line.
    Blacklist patterns are used for detecting advertisement blocks.
    When the radio stream contains metadata tag for song title that matches
    any of those patterns, the whole block with this title is considered an advertisement.
    This is useful because many radio streams change the song title to the radio state name
    when an advertisement starts, which is easy detect.
    """
    filename = "blacklist.txt"

    @classmethod
    def exists(cls, pattern):
        """Check if the pattern has already been added to the file"""
        return cls.is_added(pattern)

    @classmethod
    def add_pattern(cls, pattern):
        """Add a new pattern to the file, unless it already exists"""
        if cls.exists(pattern):
            return False

        if not cls.add_line(pattern):
            return False

        QtGui.QMessageBox.question(
            None,
            'Information',
            "Pattern '%s' added to blacklist." % pattern,
            QtGui.QMessageBox.Ok
        )

        return True

    @classmethod
    def is_valid_blacklist_pattern(cls, pattern):
        """
        If value contains at least five characters (not spaces), consider this a valid pattern
        :param pattern: The regex pattern to check
        :return: True if pattern is valid
        """
        matches = re.findall('[\S]+', pattern, re.LOCALE)

        if len(matches) < 5:
            return False

        if any(re.search(pattern, t, re.LOCALE) for t in ['', ' ', 'JUST SOME TEST', "\n"]):
            return False

        return True

    @classmethod
    def is_blacklisted(cls, value):
        return any(re.search(p, value, re.LOCALE) for p in cls.read_items() if p.strip())

    @classmethod
    def manage(cls):
        editor = DlgBlacklistEditor(None)
        editor.set_items(BlacklistStorage.read_items())
        editor.setModal(True)
        editor.exec_()
        BlacklistStorage.write_items(editor.get_items())

    @classmethod
    def add_song_title(cls, title):
        value = title.strip()
        # If value contains at least five characters (not spaces), consider this a valid pattern
        if not cls.is_valid_blacklist_pattern(value):
            return

        # Construct regex pattern from value: '.*value.*'
        pattern = '.*' + value + '.*'

        # Ask user to modify pattern, if wanted
        pattern, ok = ui.utils.input_query(None, "Mark as advertisement - blacklist meta title", "Regex pattern:", pattern)
        if not ok:
            return

        # Make sure the user entered a pattern that would not match spaces or an otherwise valid title
        if not cls.is_valid_blacklist_pattern(pattern):
            QtGui.QMessageBox.question(
                None,
                'Warning',
                "Pattern rejected!\nIt is too broad and matches empty strings.",
                QtGui.QMessageBox.Ok
            )
            return

        if cls.exists(pattern):
            QtGui.QMessageBox.question(
                None,
                'Information',
                "Pattern already exists!",
                QtGui.QMessageBox.Ok
            )
            return

        cls.add_pattern(pattern)


dispatchers.storage.blacklist_song_clicked += BlacklistStorage.add_song_title
dispatchers.storage.manage_blacklist_clicked += BlacklistStorage.manage
