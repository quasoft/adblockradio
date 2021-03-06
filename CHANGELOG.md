# Change Log
Change log introduced in version 0.2.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).

## [Release 0.3.2] - 2017-04-19
### Changed
- Released Win32 binary package (tested with Windows 10 64-bit)
- Update: Small changes to support freezing with PyInstaller

## [Release 0.3.1] - 2017-02-05
### Changed
- Fix: Added missing development dependencies in Makefile
- Updated README

## [Release 0.3.0] - 2017-02-05
### Added
- Released package for Ubuntu 16.04 64-bit
- Introduced Makefile for developers and setup.py

### Changed
- Changed project structure to make release of OS packages easier
- Fix: Do not add an empty item in blacklist and favourites files, if last line already ends with a newline 

## [Release 0.2] - 2017-01-24
### Added
- Allow user to record currently playing song
- When user clicks "Record this song", the whole song is saved to file, instead of only the part of it after that moment.
  This is achieved with prerecording currently playing song to memory. This prerecord buffer is added to file before recording starts.
- Added GUI editors for list of favourites songs and blacklist patterns

### Changed
- Update: Move blacklist configuration in separate file (.local/shared/adblockradio/blacklist.txt)
- Fix: Do not terminate application when a dialog window is closed
- Fix: Mark as advertisement (Blacklist) menu was not actually saving the pattern anywhere

[Release 0.1]: https://github.com/quasoft/adblockradio/tree/0.1
