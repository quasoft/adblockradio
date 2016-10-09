# AdBlockRadio - console radio player that blocks advertisements

*Note: Project is still in experimental state. Work is in progress and ads are currently not blocked*

## Requirements:

* Python 3.X
* GStreamer 1.X
* Python bindings for GStreamer
* python-daemon package

## How to install:

1. Install python-daemon:

        pip install python-daemon

   or

        sudo apt-get install python3-pip
        /usr/bin/python3 -m pip install python-daemon

2. Install GStreamer:

        sudo apt-get install gstreamer1.0
        sudo apt-get install gst-plugins-base1.0
        sudo apt-get install gst-plugins-good1.0

3. Download project:

        cd ~/
        git clone https://github.com/quasoft/adblockradio.git
        cd adblockradio

4. Start player:

        ./adblockradio.sh start http://mp3channels.webradio.antenne.de/chillout

   *You can also add the URI to the radio station to `station.txt` file*

5. Stop player:

        ./adblockradio.sh stop
