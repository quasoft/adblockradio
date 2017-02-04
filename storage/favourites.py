from PyQt4 import QtGui

import dispatchers
import utils
from storage import Storage
from ui.dlg_favourites_editor import DlgFavouritesEditor


class FavouritesStorage(Storage):
    filename = "favourite_songs.txt"

    @classmethod
    def is_song_added(cls, title):
        return cls.is_added(title)

    @classmethod
    def add_song(cls, title):
        if cls.is_song_added(title):
            return False

        if not cls.add_line(title):
            return False

        QtGui.QMessageBox.question(
            None,
            'Information',
            "Song added to favourites list.",
            QtGui.QMessageBox.Ok
        )

        return True

    @classmethod
    def manage(cls):
        editor = DlgFavouritesEditor(None)
        editor.set_items(FavouritesStorage.read_items())
        editor.setModal(True)
        editor.exec_()
        FavouritesStorage.write_items(editor.get_items())


dispatchers.storage.add_to_favourites_clicked += FavouritesStorage.add_song
dispatchers.storage.manage_favourites_clicked += FavouritesStorage.manage
