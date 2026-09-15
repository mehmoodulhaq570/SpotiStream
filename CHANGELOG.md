# Changelog

All notable changes to SpotiStream are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added audio downloads from YouTube videos, playlists, channels, URLs, and search queries.
- Added video downloads by song and artist name.
- Added video downloads from YouTube videos, playlists, channels, URLs, and search queries.
- Added video quality selection for best available, 4K, 1440p, 1080p, 720p, 480p, and 360p.
- Added inspection and display of the selected video and audio streams before downloading.
- Added detection of the actual resolution represented by each YouTube format.
- Added graceful cancellation messages when a download is stopped with `Ctrl+C`.

### Changed

- Updated `yt-dlp` to `2026.08.19` and installed it with its default dependency set.
- Added `yt-dlp-ejs` support and documented Deno as the recommended JavaScript runtime for full YouTube support.
- Preserved original YouTube titles when naming downloaded audio and video files.
- Improved download progress output with percentage, speed, and estimated time remaining.
- Improved format selection and fallback behavior when the requested resolution is unavailable.

### Fixed

- Fixed YouTube media downloads failing partway through with `HTTP Error 403: Forbidden` by updating yt-dlp's extractor and JavaScript challenge-solving support.
- Removed the obsolete hard-coded Chrome 126 user-agent so yt-dlp can manage compatible YouTube request headers.
- Added up to three refreshed attempts for the selected stream before trying automatic, MP4 up-to-1080p, and muxed fallback formats.
- Kept retries on the same resolved video instead of accidentally switching search results.
- Improved the error message shown when all YouTube 403 retry paths fail.

## [1.3] - 2026-06-04

### Added

- Added visible progress feedback while downloading songs.
- Added bundled FFmpeg discovery through `imageio-ffmpeg` for direct MP3 conversion.

### Changed

- Updated package metadata and build configuration for the 1.3 PyPI release.
- Updated project badges and documentation links.

### Fixed

- Improved compatibility with YouTube's SABR delivery changes and related HTTP 403 failures.

## [1.1] - 2024-10-18

### Added

- Added Spotify playlist downloads through Spotify API authentication.
- Added CSV and TXT song-list inputs.
- Added manual song and artist input.
- Added saved Spotify credentials and authentication timeout handling.

### Changed

- Renamed the package to `spoti_stream` and added the `python -m spoti_stream` entry point.

[Unreleased]: https://github.com/mehmoodulhaq570/SpotiStream/compare/SoptiStream-1.3...HEAD
[1.3]: https://github.com/mehmoodulhaq570/SpotiStream/releases/tag/SoptiStream-1.3
[1.1]: https://github.com/mehmoodulhaq570/SpotiStream/releases/tag/version_1.1
