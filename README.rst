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

   `Package for Ubuntu 16.04 64-bit`_

-  Windows 10 64 bit

   Coming soon....


If you want to run the player on another OS, you might need to install
it manually - see below.

How to customize:
-----------------

After you install the player you need to add your your radio stations and setup blacklist patterns.

#. Edit list of radio stations in ``config.py``

#. Add blacklist regex patterns for advertisements from the context menu of the notification icon.
   Blacklist patterns are saved in file ``~/.local/share/adblockradio/blacklist.txt``, which can also be edited manually.

#. Start player with GUI in system tray:

   ::

       python3 adblockradio/adblockradio.py

   or, to start with a specific radio station:

   ::

       python3 adblockradio/adblockradio.py --station URL_TO_RADIO_STREAM


How to install manually:
------------------------

Ubuntu 16.04:
~~~~~~~~~~~~~

#. Download project:

   ::

       cd ~/
       git clone https://github.com/quasoft/adblockradio.git
       cd adblockradio

#. Install dependencies and desktop file

   ::

       make develop
       make install

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
    sudo gdebi deb_dist/python3-adblockradio_0.3.1-1_all.deb

For Windows 10 64 bit:
~~~~~~~~~~~~~~~~~~~~~~

::

Coming soon...

Credits
-------

-  System tray icons by https://www.iconfinder.com/ChihabJr


.. _`Package for Ubuntu 16.04 64-bit`: https://github.com/quasoft/adblockradio/releases/download/0.3.1/python3-adblockradio_0.3.1-1_all.deb
