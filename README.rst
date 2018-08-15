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

-  Ubuntu 16.04 64-bit:

   `python3-adblockradio_0.3.2-1_all.deb`_

If you want to run the player on another OS, you might need to install
it manually - see below.

How to customize:
-----------------

After you install the player you need to add your radio stations and setup blacklist patterns.

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

The steps to build the installer are only needed if you have modified the project or want to build the installer yourself for some reason.

For Ubuntu/Debian:
~~~~~~~~~~~~~~~~~~

::

    make init
    make deb
    sudo gdebi deb_dist/python3-adblockradio_0.3.2-1_all.deb

For Windows 10 64 bit:
~~~~~~~~~~~~~~~~~~~~~~

To build the binary package for Window yourself, follow these steps:

#. Install Python 3.4, 32-bit version. This is important as PyGi currently does not support Python versions newer than 3.4.

#. Install All-In-One PyGI/PyGObject for Windows (tested with pygi-aio-3.18.2_rev12-setup). During setup you have to select the following libraries:

   - Gst-plugins 1.10.4
   - Gst-plugins-extra 1.10.4
   - GStreamer 1.10.4
   - GTK+ 3.18.9

#. Upgrade pip of Python 3.4:

   ::
   
   python.exe -m pip install --upgrade pip
   
#. Find and download a suitable wheel file for PyQt4 (tested with PyQt4-4.11.4-cp34-cp34m-win32.whl)
   
#. Install PyQt4 for Python:

   ::
   
   python.exe -m pip install PyQt4-4.11.4-cp34-cp34m-win32.whl

#. Make sure the player works - ``python.exe adblockradio\adblockradio.py``

#. Run ``pyinstaller adblockradio.spec``

#. The ready binary package should be available in folder ``adblockradio\dist\adblockradio``


Credits
-------

-  System tray icons by https://www.iconfinder.com/ChihabJr


.. _`python3-adblockradio_0.3.2-1_all.deb`: https://github.com/quasoft/adblockradio/releases/download/0.3.2/python3-adblockradio_0.3.2-1_all.deb
.. _`adblockradio_0.3.2.zip`: https://github.com/quasoft/adblockradio/releases/download/0.3.2/adblockradio_0.3.2.zip
