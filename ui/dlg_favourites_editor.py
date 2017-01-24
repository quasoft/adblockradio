from .dlg_text_item_editor import DlgTextItemEditor


class DlgFavouritesEditor(DlgTextItemEditor):
    def __init__(self, parent):
        super(DlgFavouritesEditor, self).__init__(parent)
        self.itemName = "Favourite"

        self.setWindowTitle("Favourites editor")
