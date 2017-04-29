PYTHON = /usr/bin/python3
NAME = `/usr/bin/python3 setup.py --name`
USERNAME := $(shell whoami)

init:
	sudo apt-get install python3-pip gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly python3-gst-1.0
	sudo apt-get install python3-pyqt4 pyqt4-dev-tools
	sudo apt-get install fakeroot python3-all
	# sudo apt-get install python3-stdeb qt4-designer
	$(PYTHON) -m pip install appdirs plac requests

dist: source deb

source:
	$(PYTHON) setup.py sdist

deb:
	$(PYTHON) setup.py --command-packages=stdeb.command bdist_deb

debsrc:
	$(PYTHON) setup.py --command-packages=stdeb.command sdist_dsc

rpm:
	$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

check:
	# pyflakes adblockradio/*.py
	# find adblockradio/ -name \*.py | grep -v "^test_" | xargs pylint --errors-only --reports=n | grep -v "PyQt4"
	# pep8
	# pyntch
	# pychecker
	# pymetrics

clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST dist build adblockradio.egg-info deb_dist
	find . -name '*.pyc' -delete

develop : adblockradio/adblockradio.py
	sudo apt-get install python3-pip python3-pyqt4 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly python3-gst-1.0 pyqt4-dev-tools qt4-designer python3-stdeb fakeroot python3-all
	$(PYTHON) -m pip install -r requirements.txt

test:
	nosetests --with-coverage --cover-erase --cover-html --cover-package=adblockradio --all-modules --cover-branches

install : adblockradio/adblockradio.py
	sed -i -e "s|/home/user/|/home/$(USERNAME)/|g" share/adblockradio.desktop
	sudo cp share/adblockradio.desktop /usr/share/applications

# Compile Qt designs to python classes
adblockradio/ui/ui_text_item_editor.py : adblockradio/ui/ui_text_item_editor.ui
	pyuic4 adblockradio/ui/ui_text_item_editor.ui -o adblockradio/ui/ui_text_item_editor.py

.PHONY: init dist source deb rpm check clean develop install test
