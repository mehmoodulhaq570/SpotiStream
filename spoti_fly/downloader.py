# spoti_fly/downloader.py

import os
import yt_dlp
from .converter import convert_webm_to_mp3
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replaces problematic characters with underscore

def download_song(song_name, artist_name, download_dir='songs'):
    query = f"{song_name} {artist_name} audio"
    sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
    mp3_file_name = f"{sanitized_song_name}.mp3"
    mp3_file_path = os.path.join(download_dir, mp3_file_name)

    if os.path.exists(mp3_file_path):
        print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
        return

    ydl_opts = {
        'format': 'bestaudio[ext=webm]/bestaudio',
        'outtmpl': os.path.join(download_dir, f"{sanitized_song_name}.webm"),
        'noplaylist': True,
        'quiet': True  # Suppress yt-dlp logging
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Searching and downloading: {query}")
            ydl.download([f"ytsearch1:{query}"])
            print(f"Downloaded: {mp3_file_name}")

            # Convert downloaded .webm to .mp3
            convert_webm_to_mp3(os.path.join(download_dir, f"{sanitized_song_name}.webm"), mp3_file_name, download_dir)

            # Remove the .webm file after conversion
            webm_file_path = os.path.join(download_dir, f"{sanitized_song_name}.webm")
            if os.path.exists(webm_file_path):
                os.remove(webm_file_path)

        except yt_dlp.utils.DownloadError as e:
            print(f"Download error for {song_name} by {artist_name}: {e}")
        except Exception as e:
            print(f"An error occurred while downloading {song_name} by {artist_name}: {e}")

def download_songs_from_playlist(sp, playlist_id, playlist_name, download_dir='songs'):
    from .spotify_utils import fetch_songs_from_playlist, save_songs_to_csv
    songs = fetch_songs_from_playlist(sp, playlist_id)
    if songs:
        save_songs_to_csv(songs, playlist_name)
        for song_name, artist_name in songs:
            download_song(song_name, artist_name, download_dir)
    else:
        print(f"No songs found in playlist: {playlist_name}")

def download_songs_from_csv(csv_file_path, download_dir='songs'):
    import csv
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                song_name = row.get('Song Name')
                artist_name = row.get('Artist Name')
                if song_name and artist_name:
                    download_song(song_name, artist_name, download_dir)
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

def download_songs_from_txt(txt_file_path, download_dir='songs'):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as txtfile:
            for line in txtfile:
                song_info = line.strip().split('-')
                if len(song_info) == 2:
                    song_name, artist_name = song_info
                    download_song(song_name.strip(), artist_name.strip(), download_dir)
                else:
                    print(f"Invalid format in TXT file: {line}")
    except FileNotFoundError:
        print(f"File not found: {txt_file_path}")
    except Exception as e:
        print(f"An error occurred while reading the TXT file: {e}")
