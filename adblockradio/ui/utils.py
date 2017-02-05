from PyQt4 import QtGui
import requests
import webbrowser


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


def open_in_azlyrics(title):
    params = {'q': title}
    base = 'http://search.azlyrics.com/search.php'
    url = requests.Request('GET', base, params=params).prepare().url
    webbrowser.open(url)