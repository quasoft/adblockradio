# Change Log
Change log introduced in version 0.2.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).

## [Release 0.2] - 2017-01-23
### Added
- Allow user to record currently playing song
- When user clicks "Record this song", the whole song is saved to file, instead of only the part of it after that moment.
  This is achieved with prerecording currently playing song to memory. This prerecord buffer is added to file before recording starts.

### Changed
- Update: Move blacklist configuration in separate file (.local/shared/adblockradio/blacklist.txt)
- Fix: Do not terminate application when a dialog window is closed
- Fix: Mark as advertisement (Blacklist) menu was not actually saving the pattern anywhere

[Release 0.1]: https://github.com/quasoft/adblockradio/tree/0.1