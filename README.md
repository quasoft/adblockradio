# AdBlockRadio - Internet radio player that blocks advertisements

The player is currently using metadata tags, containing song title, to detect advertisement blocks.

## Requirements:

* Python 3.4 or newer <img align="right" src="docs/screenshot.png">
* GStreamer 1.X
* Python bindings for GStreamer
* PyQt4
* python appdirs package
* python-daemon package (only needed, if you want the player to run as console daemon)
* python plac package
* python obsub package

## How to install:

1. Install GStreamer (for streaming audio):

        sudo apt-get install gstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good python3-gst-1.0

2. Install PyQT4 (for system tray icon):

        sudo apt-get install python3-pyqt4

3. Install plac, appdirs and python-daemon (for daemonizing player)

        pip install appdirs plac python-daemon obsub

   or

        sudo apt-get install python3-pip
        /usr/bin/python3 -m pip install appdirs plac python-daemon obsub

4. Download project:

        cd ~/
        git clone https://github.com/quasoft/adblockradio.git
        cd adblockradio

5. Edit list of radio stations and blacklisted tags in config.py

6. Start player in system tray:

        /usr/bin/python3 adblockradio.py

   or, to start with a specific radio station:

        /usr/bin/python3 adblockradio.py --station URL_TO_RADIO_STREAM

   *You can add more radio stations to config.py file*

7. Start player as daemon:

        ./adblockradio.sh start

   To stop daemon:

        ./adblockradio.sh stop

## Credits

* System tray icons by https://www.iconfinder.com/ChihabJr
