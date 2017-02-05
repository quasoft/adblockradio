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

How it works
------------

Coming soon...

Download:
---------

Binary packages for the following OSes are provided:

-  Ubuntu 16.04

   Coming soon....

-  Windows 10 64 bit

   Coming soon....


If you want to run the player on another OS, you might need to install
it manually - see below.

How to customize:
-----------------

#. Edit list of radio stations in ``config.py``

#. Add blacklist patterns for advertisements in
   ``~/.local/share/adblockradio/blacklist.txt``

#. Start player with GUI in system tray:

   ::

       python3 adblockradio/adblockradio.py

   or, to start with a specific radio station:

   ::

       python3 adblockradio/adblockradio.py --station URL_TO_RADIO_STREAM


How to contribute:
------------------

Ubuntu 16.04:
~~~~~~~~~~~~~

Development has been done under Ubuntu 16.04 64 bit:

#. Download project:

   ::

       cd ~/
       git clone https://github.com/quasoft/adblockradio.git
       cd adblockradio

#. Install dependencies and desktop file

   ::

       make develop

#. Start player with GUI in system tray:

   ::

       python3 adblockradio/adblockradio.py


   or in console mode (eg. for debugging purposes):

   ::

       python3 adblockradio/adblockradio.py --console

    If you have Anaconda Python installed, use full path to Python binary (replace ``python3`` with ``/usr/bin/python3``)

   *You can add more radio stations to config.py file*


How to build installer/OS package:
----------------------------------

For Ubuntu/Debian:
~~~~~~~~~~~~~~~~~~

::

    make init
    make deb
    sudo gdebi deb_dist/python3-adblockradio_0.3-1_all.deb

For Windows 10 64 bit:
~~~~~~~~~~~~~~~~~~~~~~

::

Coming soon...

Credits
-------

-  System tray icons by https://www.iconfinder.com/ChihabJr
