# Compile Qt designs to python classes
ui/ui_text_item_editor.py : ui/ui_text_item_editor.ui
	pyuic4 ui/ui_text_item_editor.ui -o ui/ui_text_item_editor.py
