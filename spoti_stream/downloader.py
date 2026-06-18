# spoti_stream/downloader.py

import os
import re
import threading
import time

import imageio_ffmpeg
import yt_dlp


def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)


def get_mp3_file_path(song_name, artist_name, download_dir):
    sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
    return os.path.join(download_dir, f"{sanitized_song_name}.mp3")


def normalize_song_key(song_name, artist_name):
    return re.sub(r'\s+', ' ', f"{song_name} by {artist_name}".casefold()).strip()


def parse_song_details_from_youtube_title(title, uploader=None):
    title = re.sub(
        r'\s*\[[^\]]*\]|\s*\([^\)]*(official|audio|video|lyrics|visualizer|mv)[^\)]*\)',
        '',
        title,
        flags=re.IGNORECASE,
    )
    title = re.sub(r'\s+', ' ', title).strip()

    separators = [' - ', ' | ', ' : ']
    for separator in separators:
        if separator in title:
            artist_name, song_name = title.split(separator, 1)
            return song_name.strip(), artist_name.strip()

    return title, uploader or 'Unknown Artist'


def show_busy_progress(message, stop_event):
    frames = ['|', '/', '-', '\\']
    index = 0
    while not stop_event.is_set():
        print(f"\r{message} {frames[index % len(frames)]}", end='', flush=True)
        index += 1
        time.sleep(0.2)
    print(f"\r{message} done.{' ' * 10}")


def show_download_progress(progress):
    if progress.get('status') == 'downloading':
        percent = progress.get('_percent_str', '').strip()
        speed = progress.get('_speed_str', '').strip()
        eta = progress.get('_eta_str', '').strip()
        print(f"\rDownloading: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
    elif progress.get('status') == 'finished':
        print("\rDownload complete. Converting to MP3...          ")


def build_ydl_options(song_name, artist_name, download_dir):
    sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
    return {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_dir, f"{sanitized_song_name}.%(ext)s"),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'progress_hooks': [show_download_progress],
        'retries': 3,
        'fragment_retries': 3,
        'continuedl': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web'],
            },
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }


def download_audio(source, song_name, artist_name, download_dir='songs', message=None):
    mp3_file_path = get_mp3_file_path(song_name, artist_name, download_dir)
    mp3_file_name = os.path.basename(mp3_file_path)
    os.makedirs(download_dir, exist_ok=True)

    if os.path.exists(mp3_file_path):
        print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
        return True

    ydl_opts = build_ydl_options(song_name, artist_name, download_dir)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            if message:
                print(message)
            ydl.download([source])
            print(f"Downloaded: {mp3_file_name}")
            return True
        except yt_dlp.utils.DownloadError as e:
            print(f"Download error for {song_name} by {artist_name}: {e}")
            if 'HTTP Error 403' in str(e):
                print("Tip: run 'python -m pip install -U yt-dlp' if this keeps happening. YouTube often returns 403 when yt-dlp is outdated.")
        except Exception as e:
            print(f"An error occurred while downloading {song_name} by {artist_name}: {e}")
    return False


def download_song(song_name, artist_name, download_dir='songs'):
    query = f"{song_name} {artist_name} audio"
    return download_audio(
        f"ytsearch1:{query}",
        song_name,
        artist_name,
        download_dir,
        f"Searching and downloading: {query}",
    )


def download_songs_from_playlist(sp, playlist_id, playlist_name, download_dir='songs'):
    from .spotify_utils import fetch_songs_from_playlist, save_songs_to_csv
    songs = fetch_songs_from_playlist(sp, playlist_id)
    if songs:
        save_songs_to_csv(songs, playlist_name)
        for song_name, artist_name in songs:
            download_song(song_name, artist_name, download_dir)
    else:
        print(f"No songs found in playlist: {playlist_name}")


def download_songs_from_youtube_playlist(playlist_url, download_dir='songs'):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
    }

    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=show_busy_progress,
        args=("Fetching YouTube playlist from online...", stop_event),
        daemon=True,
    )
    progress_thread.start()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"\nYouTube playlist error: {e}")
        return
    except Exception as e:
        print(f"\nAn error occurred while reading the YouTube playlist: {e}")
        return
    finally:
        stop_event.set()
        progress_thread.join()

    entries = playlist_info.get('entries', []) if playlist_info else []
    entries = [entry for entry in entries if entry]

    if not entries:
        print("No videos found in this YouTube playlist.")
        return

    playlist_title = playlist_info.get('title', 'YouTube Playlist')
    print(f"Found {len(entries)} videos in '{playlist_title}'.")

    downloaded_songs = set()
    for index, entry in enumerate(entries, start=1):
        title = entry.get('title') or f'Track {index}'
        uploader = entry.get('uploader') or entry.get('channel')
        song_name, artist_name = parse_song_details_from_youtube_title(title, uploader)
        song_key = normalize_song_key(song_name, artist_name)

        if song_key in downloaded_songs:
            print(f"\n[{index}/{len(entries)}] Duplicate song already handled. Skipping: {song_name} by {artist_name}")
            continue

        downloaded_songs.add(song_key)
        print(f"\n[{index}/{len(entries)}] {song_name} by {artist_name}")

        video_url = entry.get('webpage_url') or entry.get('url')
        if video_url and not video_url.startswith('http'):
            video_url = f"https://www.youtube.com/watch?v={video_url}"

        if video_url:
            success = download_audio(
                video_url,
                song_name,
                artist_name,
                download_dir,
                f"Downloading from playlist video: {title}",
            )
            if not success:
                print("Trying again with YouTube search...")
                download_song(song_name, artist_name, download_dir)
        else:
            download_song(song_name, artist_name, download_dir)


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
