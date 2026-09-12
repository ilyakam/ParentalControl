# Changelog

Notable changes to ParentalControl are recorded here, following
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.4] - 2026-09-12

### Fixed

- Multi-cursor parentheses removal even following an incomplete pair.
- Multi-cursor parentheses addition if it starts at the beginning of the buffer.

## [1.1.3] - 2014-08-20

### Fixed

- Fixed bugs and improved behavior when using multiple cursors.

## [1.1.2] - 2014-05-27

### Fixed

- Fixed parentheses removal with a cursor at position zero or between pairs.

## [1.1.1] - 2014-02-05

### Changed

- Refactored the code, cleaned it up, and expanded comments.

### Fixed

- Fixed removal of complex and nested parentheses.
- Fixed removal of parentheses starting at position zero.

## [1.1.0] - 2014-02-05

### Added

- Added settings for syntax- and language-specific behavior.

### Changed

- Updated the plugin for Sublime Text 3 compatibility.
- Refactored the code.

### Fixed

- Fixed miscellaneous bugs in the Remove Parentheses command.

## 1.0.0

### Added

- Initial release.
