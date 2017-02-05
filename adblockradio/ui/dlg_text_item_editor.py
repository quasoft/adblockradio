from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QStandardItem
from PyQt4.QtGui import QStandardItemModel
from event import Event

from .ui_text_item_editor import Ui_TextItemEditor
from ui import utils


class DlgTextItemEditor(QDialog, Ui_TextItemEditor):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        Ui_TextItemEditor.__init__(self)
        self.setupUi(self)
        self.itemName = "Value"
        # Create an empty model for the list's data
        self._model = QStandardItemModel(self.list_view)

    def setupUi(self, TextItemEditor):
        super().setupUi(TextItemEditor)
        TextItemEditor.btn_add.clicked.connect(self.on_add_click)
        TextItemEditor.btn_edit.clicked.connect(self.on_edit_click)
        TextItemEditor.btn_delete.clicked.connect(self.on_delete_click)

    def get_items(self):
        for i in range(self._model.rowCount()):
            yield self._model.item(i).text()

    def set_items(self, items):
        self._model.clear()
        for item in items:
            list_item = QStandardItem(item)
            self._model.appendRow(list_item)
        self.list_view.setModel(self._model)

    def get_selected(self):
        indexes = self.list_view.selectedIndexes()
        index = indexes[0] if indexes else None
        if not index:
            return None, None

        return self._model.itemFromIndex(index).text(), index

    def on_add_click(self):
        item, ok = utils.input_query(None, "Adding %s" % self.itemName.lower(), self.itemName + ":")
        if ok:
            list_item = QStandardItem(item)
            self._model.appendRow(list_item)
            self.list_view.setCurrentIndex(self._model.indexFromItem(list_item))
            self.event_add(item)

    def on_edit_click(self):
        text, index = self.get_selected()
        if not index:
            QMessageBox.question(
                None,
                'Information',
                "Select %s from list" % self.itemName.lower(),
                QMessageBox.Ok
            )
            return

        item, ok = utils.input_query(
            None,
            "Editing %s" % self.itemName.lower(),
            self.itemName + ":",
            text
        )
        if ok:
            self._model.itemFromIndex(index).setText(item)
            self.event_edit(item)

    def on_delete_click(self):
        text, index = self.get_selected()
        if not index:
            QMessageBox.question(
                None,
                'Information',
                "Select %s from list" % self.itemName.lower(),
                QMessageBox.Ok
            )
            return

        should_delete = QMessageBox.question(
            None,
            "Deleting %s" % self.itemName.lower(),
            "Delete '%s'?" % text,
            QMessageBox.Yes, QMessageBox.No
        )
        if should_delete == QMessageBox.Yes:
            self.event_delete(text)
            self._model.removeRow(index.row())

    @Event
    def event_add(self, item):
        """Signals the parent that an item has been added to the list
        :param item: str
        """

    @Event
    def event_edit(self, item):
        """Signals the parent that an item has been added to the list
        :param item: str
        """

    @Event
    def event_delete(self, item):
        """Signals the parent that an item has been removed from the list
        :param item: str
        """
