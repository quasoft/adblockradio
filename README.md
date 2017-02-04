# AdBlockRadio - Internet radio player that blocks advertisements

Detects advertisements by inspecting song titles inside stream metadata and switches automatically to another radio station, when an ad is detected.

## Requirements:

* Python 3.4 or newer <img align="right" src="docs/screenshot.png">
* GStreamer 1.X
* Python bindings for GStreamer
* PyQt4
* python appdirs package
* python plac package
* python requests package

## How to install:

Tested to work under Ubuntu 16.04 only. Might work on debian based distros too:

1. Install GStreamer (for streaming audio):

        sudo apt-get install gstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good python3-gst-1.0

2. Install PyQT4 (for system tray icon):

        sudo apt-get install python3-pyqt4

3. Install python dependencies:

        sudo apt-get install python3-pip
        /usr/bin/python3 -m pip install appdirs plac requests

4. Download project:

        cd ~/
        git clone https://github.com/quasoft/adblockradio.git
        cd adblockradio

5. Edit list of radio stations in config.py

6. Add blacklist patterns for advertisements in `~/.local/share/adblockradio/blacklist.txt`

7. Start player in system tray:

        /usr/bin/python3 adblockradio.py

   or, to start with a specific radio station:

        /usr/bin/python3 adblockradio.py --station URL_TO_RADIO_STREAM

   *You can add more radio stations to config.py file*

8. Start player as console application:

        ./adblockradio.sh start

9. Start player as daemon:

        ./adblockradio.sh start &

   To stop daemon:

        ./adblockradio.sh stop

## Credits

* System tray icons by https://www.iconfinder.com/ChihabJr
