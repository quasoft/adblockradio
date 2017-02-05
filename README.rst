AdBlockRadio - Internet radio player that blocks advertisements
===============================================================

Detects advertisements by inspecting song titles inside stream metadata
and switches automatically to another radio station, when an ad is
detected.

Requirements:
-------------

-  Python 3.4 or newer
-  GStreamer 1.X
-  Python bindings for GStreamer
-  PyQt4
-  Python packages: appdirs, plac, requests

Download:
---------

Binary packages for the following OSes are provided:

-  Ubuntu 16.04

   Coming soon....

-  Windows 10 64 bit

   Coming soon....


If you want to run the player on another OS, you might need to install
it manually - see below.

How to install manually:
------------------------

Ubuntu 16.04:
~~~~~~~~~~~~~

Tested to work under Ubuntu 16.04. Might work on other debian based
distros too:

#. Download project:

   ::

       cd ~/
       git clone https://github.com/quasoft/adblockradio.git
       cd adblockradio

#. Install dependencies and desktop file

   ::

       make manual_install

#. Edit list of radio stations in config.py

#. Add blacklist patterns for advertisements in
   ``~/.local/share/adblockradio/blacklist.txt``

#. Start player with GUI in system tray:

   ::

       /usr/bin/python3 adblockradio/adblockradio.py

   or, to start with a specific radio station:

   ::

       /usr/bin/python3 adblockradio/adblockradio.py --station URL_TO_RADIO_STREAM

   *You can add more radio stations to config.py file*

#. Start player as console application:

   ::

       bin/adblockradio.sh start

#. Start player as daemon:

   ::

       bin/adblockradio.sh start &

   To stop daemon:

   ::

       bin/adblockradio.sh stop

Windows 10 64 bit:
~~~~~~~~~~~~~~~~~~

- Coming soon....

How to build installer/OS package:
----------------------------------

For Ubuntu/Debian:
~~~~~~~~~~~~~~~~~~

::

    apt-get install python3-stdeb fakeroot python3-all
    make deb

Credits
-------

-  System tray icons by https://www.iconfinder.com/ChihabJr
