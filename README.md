# AdBlockRadio - console radio player that blocks advertisements

*Note: Project is still in experimental state. Work is in progress and ads are currently not blocked*

## Requirements:

* Python 3.X
* GStreamer 1.X
* Python bindings for GStreamer
* python-daemon package

## How to install:

1. Install python-daemon (for daemonizing player):

        pip install python-daemon

   or

        sudo apt-get install python3-pip
        /usr/bin/python3 -m pip install python-daemon

2. Install GStreamer (for streaming audio):

        sudo apt-get install gstreamer1.0
        sudo apt-get install gstreamer1.0-plugins-base
        sudo apt-get install gstreamer1.0-plugins-good

3. Install PyQT4 (for system tray icon):

        sudo apt-get install python3-pyqt4

4. Download project:

        cd ~/
        git clone https://github.com/quasoft/adblockradio.git
        cd adblockradio

5. Start player as daemon:

        ./adblockradio.sh start http://mp3channels.webradio.antenne.de/chillout

        or, to start Python script, directly, as a regular process:

        /usr/bin/python3 adblockradio.py --station http://mp3channels.webradio.antenne.de/chillout

   *You can also add the URI to the radio station to `station.txt` file*

6. Stop daemon of player:

        ./adblockradio.sh stop


## Credits

* System tray icons by https://www.iconfinder.com/ChihabJr