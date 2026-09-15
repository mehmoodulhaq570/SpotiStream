[![Version](https://img.shields.io/badge/version-1.4.0-blue)](https://pypi.org/project/spoti-stream/)
[![Package](https://img.shields.io/badge/package-spoti--stream-blue)](https://pypi.org/project/spoti-stream/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE.txt)

# SpotiStream

SpotiStream is an interactive Python command-line application for finding and downloading audio or video from YouTube. It can build a download list from a Spotify playlist, a YouTube URL or search, a CSV/TXT file, or manually entered song and artist names.

Current release: [SpotiStream 1.4.0 on PyPI](https://pypi.org/project/spoti-stream/1.4.0/) — released September 16, 2026.

> [!IMPORTANT]
> Spotify is used only to read playlist metadata. Downloadable media is located through YouTube. Only download content when you have permission, and follow the terms and laws that apply to you.

## Features

- Read playlists from Spotify and save their song lists as CSV files.
- Accept a YouTube video, playlist, channel, URL, or search query.
- Download audio as MP3 or download video with its audio stream.
- Search for a video using a song and artist name.
- Select best available, 4K, 1440p, 1080p, 720p, 480p, or 360p video quality.
- Fall back to a lower available resolution when the requested quality is unavailable.
- Retry refreshed YouTube streams and alternate formats after HTTP 403 failures.
- Accept bulk song lists from CSV and TXT files.
- Preserve useful YouTube titles and sanitize filenames for the operating system.
- Skip files and duplicate playlist entries that have already been handled.
- Show live audio/video size, speed, ETA, merge status, playlist progress, and a final result summary.
- Diagnose the local installation with `spotistream doctor`.
- Stop cleanly when `Ctrl+C` is pressed.

## Requirements

- Python 3.11 or newer
- FFmpeg for audio conversion and video/audio merging
- Deno for yt-dlp's YouTube JavaScript challenge solver
- A Spotify Developer application only when using Spotify playlists

The Python dependencies include Spotipy, yt-dlp with its EJS support, imageio-ffmpeg, Requests, and Rich.

## Installation

### Install or upgrade the published package

```bash
python -m pip install --upgrade spoti-stream
```

Version 1.4.0 includes the `spotistream` command, system doctor, Rich download progress, playlist summaries, expanded video quality selection, and updated YouTube challenge support.

### Install the latest source version

```bash
git clone https://github.com/mehmoodulhaq570/SpotiStream.git
cd SpotiStream
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install SpotiStream and create the `spotistream` command:

```bash
python -m pip install -e .
```

For a non-editable installation, use `python -m pip install .` instead.

### Install Deno

On Windows:

```powershell
winget install --id DenoLand.Deno --exact
```

Restart the terminal after installation. For other platforms, follow the [official Deno installation guide](https://docs.deno.com/runtime/getting_started/installation/).

SpotiStream uses the FFmpeg executable supplied by `imageio-ffmpeg` when a system installation is unavailable. Run the doctor command after setup to confirm that FFmpeg and Deno can be detected.

## Quick Start

Open the interactive menu:

```bash
spotistream
```

The module form remains supported:

```bash
python -m spoti_stream
```

Check the installation:

```bash
spotistream doctor
```

Show command help:

```bash
spotistream --help
```

## System Diagnostics

`spotistream doctor` checks:

- Python and its version
- yt-dlp
- the yt-dlp EJS challenge solver
- FFmpeg
- Deno
- the optional Spotify credentials file

Example:

```text
SpotiStream System Check

✓  Python       3.14.0
✓  yt-dlp       2026.8.19
✓  yt-dlp-ejs   0.8.0
✓  FFmpeg       7.1
✓  Deno         2.9.6
!  Spotify      Not configured (optional)

✓ SpotiStream is ready to download.
```

Missing required components produce a recommendation and a non-zero exit status. Missing Spotify credentials do not make the system unhealthy because Spotify support is optional.

## Interactive Menu

Running SpotiStream without a command presents seven choices:

1. **Use a Spotify playlist** — authenticate, select one of your playlists, export its track list to CSV, and download its songs.
2. **Provide a CSV or TXT file** — download every valid song and artist entry in the file.
3. **Manually type song names** — download individual songs until `q` is entered.
4. **Download audio from YouTube input** — accept a video, playlist, channel, URL, or search query and save MP3 audio.
5. **Download a video by song name** — search using a song and artist, then select the desired quality.
6. **Download videos from YouTube input** — accept a video, playlist, channel, URL, or search query and select the desired quality.
7. **Exit from SpotiStream**.

## Download Progress

A video download can contain separate video and audio streams. SpotiStream tracks both streams and their merge operation:

```text
Video      ━━━━━━━━━━━━━━━━━╺━━━━━━  74%  31.2/42.1 MiB  2.8 MiB/s  00:04
Audio      ━━━━━━━━━━━━━━━━━━━━━━━━ 100%   3.5/3.5 MiB
Merging    ━━━━━━━━━━━━━━━━━━━━━━━━ 100%  Complete
```

Playlist downloads show the overall count and current item, followed by a summary:

```text
Playlist: Favourite Songs

Overall    ━━━━━━━━━━━━━━━╺━━━━━━━━  60%  6/10 items
Current    ━━━━━━━━━━━━━━━━━╺━━━━━━  68%  4.1 MiB/s  00:12

✓ Downloaded    5
⊘ Skipped       1
✗ Failed        0
```

The exact appearance depends on the terminal width and Unicode support.

## Input File Formats

### CSV

CSV files must contain the exact headers `Song Name` and `Artist Name`:

```csv
Song Name,Artist Name
Agar Tum Saath Ho,Alka Yagnik
Kun Faya Kun,A. R. Rahman
```

### TXT

TXT files use one `Song Name - Artist Name` entry per line:

```text
Agar Tum Saath Ho - Alka Yagnik
Kun Faya Kun - A. R. Rahman
```

## Spotify Setup

Spotify credentials are needed only for menu option 1.

1. Open the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create an application and copy its Client ID and Client Secret.
3. Configure `http://localhost:8888/callback` as the application's redirect URI.
4. Start SpotiStream and select the Spotify playlist option.
5. Enter the credentials when prompted and finish authorization in the browser.

The credentials are saved as two lines in `spotify_credentials.txt` in the current working directory:

```text
YOUR_CLIENT_ID
YOUR_CLIENT_SECRET
```

> [!CAUTION]
> This file contains a secret in plain text. Do not commit it, publish it, or share it. Add it to your local Git exclusions if you create the file inside a repository.

Spotify authentication includes timeout safeguards for API requests. The credentials file is optional; if it is absent, SpotiStream prompts for the values.

## Output Files

- Audio files are written to `songs/` as MP3 files.
- Video files are written to `videos/`, normally as merged MP4 files.
- Spotify playlist track lists are exported as `<playlist name>.csv` in the current directory.
- Existing destination files are skipped rather than downloaded again.

All relative output paths are based on the directory from which SpotiStream is launched.

## Video Quality Behavior

The quality menu offers:

| Choice | Requested quality |
|---:|---|
| 1 | Best available / HD |
| 2 | 4K / 2160p |
| 3 | 1440p |
| 4 | 1080p |
| 5 | 720p |
| 6 | 480p |
| 7 | 360p |

The requested quality is a maximum preference, not a guarantee. For example, selecting 4K for a source whose highest available stream is 1080p results in a 1080p download. SpotiStream prints the selected video and audio format before downloading.

## Troubleshooting

### HTTP Error 403 from YouTube

Update yt-dlp and its EJS solver together:

```bash
python -m pip install -U "yt-dlp[default]"
```

Confirm Deno is installed, restart the terminal, and run:

```bash
spotistream doctor
```

SpotiStream refreshes the selected stream up to three times before trying automatic selection, MP4 up to 1080p, and a best-muxed fallback. The final quality may therefore be lower than requested.

### `spotistream` is not recognized

Activate the virtual environment in which SpotiStream was installed. You can always use the module form:

```bash
python -m spoti_stream
python -m spoti_stream doctor
```

### FFmpeg is missing

Reinstall the Python dependencies first:

```bash
python -m pip install -r requirements.txt
```

If the doctor still reports FFmpeg as missing, install FFmpeg for your operating system and ensure its executable is available on `PATH`.

### Spotify authentication fails

- Confirm the Client ID and Client Secret are correct.
- Confirm `http://localhost:8888/callback` exactly matches the configured redirect URI.
- Delete or correct `spotify_credentials.txt` if it contains outdated values.
- Make sure the local callback port `8888` is available.

## Project Layout

```text
spoti_stream/
├── __main__.py          CLI entry point and interactive menu
├── diagnostics.py       System doctor checks
├── downloader.py        YouTube resolution and download logic
├── progress.py          Rich progress display and playlist summaries
├── spotify_utils.py     Spotify authentication and playlist access
└── converter.py         FFmpeg conversion helper
```

## Roadmap

- Embed track metadata and cover artwork in downloaded audio.
- Add JSON and XLSX input formats.
- Add persistent configuration for quality and output directories.
- Add a download archive for reliable cross-session duplicate detection.
- Add automated tests and continuous integration.

## Contributing

Bug reports and pull requests are welcome through the [GitHub repository](https://github.com/mehmoodulhaq570/SpotiStream).

## Changelog

See the [1.4.0 release notes](CHANGELOG.md#140---2026-09-16) or the complete [CHANGELOG.md](CHANGELOG.md) for the history of notable changes.

## License

SpotiStream is available under the [MIT License](LICENSE.txt).
