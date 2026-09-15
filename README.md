[![Version](https://img.shields.io/badge/version-1.3-blue)](https://pypi.org/project/spoti-stream/)
[![Package](https://img.shields.io/badge/package-spoti__stream-blue)](https://pypi.org/project/spoti-stream/)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# SpotiStream

## Overview
SpotiStream is a Python tool designed to help users download and save songs from their Spotify playlists. The application fetches songs from Spotify and offers multiple options for downloading them. This package leverages the Spotify API to access and manage playlists, and supports different methods of song input for maximum flexibility.

## Motivation
The idea for SpotiStream came after my Spotify account was blocked due to a payment issue. This experience led me to think about creating a tool that could provide an alternative way to download songs in MP3 format without depending solely on Spotify's premium services. With SpotiStream, users can download their favorite tracks in a simple, user-friendly way and avoid interruptions due to service outages or account problems.

## Features
- **Spotify Playlist Download**: Fetch and download songs directly from your Spotify playlists.
- **YouTube Playlist Download**: Provide a YouTube playlist URL, fetch each video title, and download matching MP3 files one by one.
- **Video Download**: Search by song and artist, then download the matching YouTube video.
- **Video Quality Selection**: Choose best available, 1080p, 720p, 480p, or 360p.
- **Custom File Inputs**: Users can input songs via CSV or TXT files for downloading songs in bulk.
- **Manual Song Input**: Option to manually type in song names and artists for direct downloads.
- **Auto-Save Credentials**: Automatically saves Spotify credentials for faster authentication in future sessions.
- **Error Handling and Timeout**: Handles authentication timeouts and ensures the program exits if credentials are incorrect or authentication takes too long (set to 60 seconds).
- **Cross-Platform**: Designed to work across different operating systems (Windows, macOS, Linux).

## How It Works
- **Authenticate with Spotify**: When downloading from a Spotify playlist, you will be prompted to authenticate your Spotify account by providing your client ID and secret.
- **Select a Playlist**: Once authenticated, SpotiStream fetches your playlists, allowing you to select which one to download.
- **Download from YouTube Playlist**: Paste a YouTube playlist URL and SpotiStream will use the video titles to download songs one by one.
- **Download Videos**: Enter a song name and artist, choose a quality, and save the video into the `videos` folder.
- **Download YouTube Playlist Videos**: Paste a YouTube playlist URL, choose a quality, and download each video.
- **Download from CSV/TXT**: Alternatively, you can upload a CSV or TXT file of songs and artists for downloading in bulk.
- **Manual Song Input**: If you prefer, you can manually input the song name and artist for downloading.

## Installation

### Usage

Install the tool by running this command:
```bash
pip install spoti_stream
````

Run SpotiStream from the command line:
```bash
python -m spoti_stream
````

### Clone the Repository
To modify SpotiStream according to your need, clone this repository and follow the steps below:

```bash
git clone https://github.com/mehmoodulhaq570/SpotiStream.git
cd SpotiStream
````

### Installation

### Install Dependencies
Create a virtual environment using conda or virtualenv, and install the dependencies:

#### Using conda
```bash
conda create --name spotistream python=3.x
conda activate spotistream
````

### Install Required Packages
```bash
pip install -r requirements.txt
````

SpotiStream uses `yt-dlp` for downloading audio and FFmpeg for MP3 conversion. If MP3 conversion fails, install FFmpeg and make sure it is available in your terminal.

For full YouTube support, install Deno so `yt-dlp` can solve YouTube's playback challenges. On Windows:

```powershell
winget install --id DenoLand.Deno --exact
```

Restart the terminal after installing Deno.

## Get Spotify API Credentials

You will need a Spotify Developer account to use SpotiStream. Follow the steps:

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create a new app and get your Client ID and Client Secret.
3. Add the credentials when prompted during authentication or store them in a `spotify_credentials.txt` file in the root directory of the project.

## Main Menu

The program will prompt you to choose one of the following options:

- **Download from Spotify Playlist**: Choose one of your playlists to download.
- **Download from CSV/TXT**: Enter a file path to download songs from a `.csv` or `.txt` file.
- **Manual Song Input**: Manually input the song name and artist.
- **Download from YouTube Playlist**: Enter a YouTube playlist URL to download each listed song.
- **Download Video by Song Name**: Enter a song and artist, then choose the video quality.
- **Download Videos from YouTube Playlist**: Enter a YouTube playlist URL and choose the video quality.
- **Exit**: Exit the application.

## Error Handling and Timeouts

- **Request Timeout**: If the Spotify API fails to authenticate within 60 seconds, the program will exit to prevent hanging.
- **Invalid Credentials**: If invalid Spotify credentials are provided, the program will terminate after 30 seconds.
- **File Not Found**: If the `spotify_credentials.txt` file is missing, no error will be displayed, but you will be prompted to input your credentials manually.

## Upcoming Features

- **Enhanced CLI**: Further improvements to the command-line interface for easier and more intuitive usage.
- **Track Metadata**: Export more detailed track metadata such as album names, track durations, and release dates.

## Future Enhancements

- **Batch Downloading**: Enable batch downloading of multiple playlists in one go.
- **Progress Tracking**: Display download progress for each song.
- **Extended File Format Support**: Add support for different file formats such as `.json` and `.xlsx` for input.

## Contributing

We welcome contributions! Please feel free to submit issues or pull requests to help improve SpotiStream.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes and a history of notable changes.

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.


