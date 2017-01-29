from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction
import utils
from .dlg_text_item_editor import DlgTextItemEditor


class DlgFavouritesEditor(DlgTextItemEditor):
    def __init__(self, parent):
        super(DlgFavouritesEditor, self).__init__(parent)
        self.itemName = "Favourite"

        self.setWindowTitle("Favourites editor")

        self.list_view.setContextMenuPolicy(Qt.ActionsContextMenu)

        action_search_for_lyrics = QAction("Search for lyrics online", self)
        action_search_for_lyrics.triggered.connect(self.on_search_for_lyrics)
        self.list_view.addAction(action_search_for_lyrics)

    def on_search_for_lyrics(self):
        title, index = self.get_selected()
        if title:
            utils.open_in_azlyrics(title)
