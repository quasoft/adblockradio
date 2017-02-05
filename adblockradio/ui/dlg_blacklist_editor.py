from .dlg_text_item_editor import DlgTextItemEditor


class DlgBlacklistEditor(DlgTextItemEditor):
    def __init__(self, parent):
        super(DlgBlacklistEditor, self).__init__(parent)
        self.itemName = "Pattern"

        self.setWindowTitle("Blacklist editor")
