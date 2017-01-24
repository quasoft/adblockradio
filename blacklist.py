from PyQt4 import QtGui

from storage import Storage


class BlacklistStorage(Storage):
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
