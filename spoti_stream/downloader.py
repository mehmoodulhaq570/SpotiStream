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


def get_video_file_path(song_name, artist_name, download_dir, extension='mkv'):
    sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
    return os.path.join(download_dir, f"{sanitized_song_name}.{extension}")


def find_existing_video_file(song_name, artist_name, download_dir):
    for extension in ('mkv', 'mp4', 'webm'):
        video_file_path = get_video_file_path(song_name, artist_name, download_dir, extension)
        if os.path.exists(video_file_path):
            return video_file_path
    return None


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
        print("\rDownload complete. Finalizing file...          ")


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


def get_video_format(quality):
    quality = str(quality).strip().lower()
    if quality in ('best', 'hd', '1', ''):
        return 'bestvideo*+bestaudio/best'

    quality_map = {
        '2': '1080',
        '3': '720',
        '4': '480',
        '5': '360',
        '1080': '1080',
        '720': '720',
        '480': '480',
        '360': '360',
    }
    height = quality_map.get(quality, '720')
    return f'bestvideo*[height<={height}]+bestaudio/best[height<={height}]/best'


def get_video_quality_label(quality):
    quality = str(quality).strip().lower()
    quality_map = {
        '1': 'best available / HD',
        'best': 'best available / HD',
        'hd': 'best available / HD',
        '2': '1080p',
        '1080': '1080p',
        '3': '720p',
        '720': '720p',
        '4': '480p',
        '480': '480p',
        '5': '360p',
        '360': '360p',
    }
    return quality_map.get(quality, '720p')


def get_video_height_limit(quality):
    quality = str(quality).strip().lower()
    quality_map = {
        '2': 1080,
        '1080': 1080,
        '3': 720,
        '720': 720,
        '4': 480,
        '480': 480,
        '5': 360,
        '360': 360,
    }
    return quality_map.get(quality)


def get_format_max_height(video_info):
    heights = [
        video_format.get('height')
        for video_format in video_info.get('formats', [])
        if video_format.get('vcodec') != 'none' and video_format.get('height')
    ]
    return max(heights, default=0)


def get_best_video_search_result(query, max_results=5):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'extract_flat': False,
    }

    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=show_busy_progress,
        args=(f"Checking top {max_results} YouTube results for HD video...", stop_event),
        daemon=True,
    )
    progress_thread.start()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_info = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"\nCould not inspect YouTube search results: {e}")
        return None
    except Exception as e:
        print(f"\nAn error occurred while checking YouTube search results: {e}")
        return None
    finally:
        stop_event.set()
        progress_thread.join()

    entries = search_info.get('entries', []) if search_info else []
    entries = [entry for entry in entries if entry]

    if not entries:
        return None

    best_entry = max(entries, key=get_format_max_height)
    best_height = get_format_max_height(best_entry)
    title = best_entry.get('title', 'Unknown title')
    url = best_entry.get('webpage_url') or best_entry.get('url')

    if url and not url.startswith('http'):
        url = f"https://www.youtube.com/watch?v={url}"

    print(f"Selected result: {title}")
    if best_height:
        print(f"Highest available quality found: {best_height}p")
    else:
        print("Could not detect available quality before download.")

    return url


def get_format_value(video_format, key, default=0):
    value = video_format.get(key)
    return value if isinstance(value, (int, float)) else default


def choose_exact_video_format(video_info, quality):
    height_limit = get_video_height_limit(quality)
    formats = video_info.get('formats', [])

    video_formats = [
        video_format
        for video_format in formats
        if video_format.get('vcodec') != 'none'
        and video_format.get('height')
        and (height_limit is None or video_format.get('height') <= height_limit)
    ]
    audio_formats = [
        audio_format
        for audio_format in formats
        if audio_format.get('acodec') != 'none'
        and audio_format.get('vcodec') == 'none'
    ]

    if not video_formats:
        return None, None, None

    best_video = max(
        video_formats,
        key=lambda video_format: (
            get_format_value(video_format, 'height'),
            get_format_value(video_format, 'fps'),
            get_format_value(video_format, 'tbr'),
            get_format_value(video_format, 'vbr'),
        ),
    )
    best_audio = max(
        audio_formats,
        key=lambda audio_format: (
            get_format_value(audio_format, 'abr'),
            get_format_value(audio_format, 'tbr'),
            get_format_value(audio_format, 'filesize'),
        ),
        default=None,
    )

    selected_format = best_video.get('format_id')
    if best_audio:
        selected_format = f"{selected_format}+{best_audio.get('format_id')}"

    fallback_format = get_video_format(quality)
    video_format_id = best_video.get('format_id')
    if video_format_id:
        selected_format = f"{selected_format}/{video_format_id}+bestaudio/{fallback_format}"

    return selected_format, best_video, best_audio


def inspect_video_source(source, quality):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web'],
            },
        },
    }

    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=show_busy_progress,
        args=("Inspecting available video qualities...", stop_event),
        daemon=True,
    )
    progress_thread.start()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(source, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"\nCould not inspect video formats: {e}")
        return None, None
    except Exception as e:
        print(f"\nAn error occurred while inspecting video formats: {e}")
        return None, None
    finally:
        stop_event.set()
        progress_thread.join()

    if video_info and video_info.get('entries'):
        video_info = next((entry for entry in video_info.get('entries', []) if entry), None)

    if not video_info:
        return None, None

    selected_format, best_video, best_audio = choose_exact_video_format(video_info, quality)
    if best_video:
        print(
            "Selected video stream: "
            f"{best_video.get('format_id')} | "
            f"{best_video.get('height')}p | "
            f"{best_video.get('ext')} | "
            f"{best_video.get('vcodec')}"
        )
    if best_audio:
        print(
            "Selected audio stream: "
            f"{best_audio.get('format_id')} | "
            f"{best_audio.get('ext')} | "
            f"{best_audio.get('acodec')}"
        )

    return selected_format, video_info.get('webpage_url') or source


def build_video_ydl_options(song_name, artist_name, download_dir, quality='best'):
    sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
    return {
        'format': get_video_format(quality),
        'outtmpl': os.path.join(download_dir, f"{sanitized_song_name}.%(ext)s"),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'merge_output_format': 'mkv',
        'format_sort': ['res', 'fps', 'br'],
        'format_sort_force': True,
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


def download_video(source, song_name, artist_name, quality='best', download_dir='videos', message=None):
    existing_video_file = find_existing_video_file(song_name, artist_name, download_dir)
    video_file_path = get_video_file_path(song_name, artist_name, download_dir)
    video_file_name = os.path.basename(video_file_path)
    os.makedirs(download_dir, exist_ok=True)

    if existing_video_file:
        print(f"'{song_name} by {artist_name}' is already downloaded as video. Skipping: {os.path.basename(existing_video_file)}")
        return True

    if message:
        print(message)
    print(f"Requested video quality: {get_video_quality_label(quality)}")
    selected_format, resolved_source = inspect_video_source(source, quality)

    ydl_opts = build_video_ydl_options(song_name, artist_name, download_dir, quality)
    if selected_format:
        ydl_opts['format'] = selected_format
        source = resolved_source
    else:
        print("Could not choose an exact HD stream. Falling back to yt-dlp automatic best format.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([source])
            print(f"Downloaded video: {video_file_name}")
            return True
        except yt_dlp.utils.DownloadError as e:
            print(f"Video download error for {song_name} by {artist_name}: {e}")
            if 'HTTP Error 403' in str(e):
                print("Tip: run 'python -m pip install -U yt-dlp' if this keeps happening. YouTube often returns 403 when yt-dlp is outdated.")
        except Exception as e:
            print(f"An error occurred while downloading video {song_name} by {artist_name}: {e}")
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


def download_video_by_song(song_name, artist_name, quality='best', download_dir='videos'):
    query = f"{song_name} {artist_name} official music video"
    video_url = get_best_video_search_result(query)
    if not video_url:
        video_url = f"ytsearch1:{query}"

    return download_video(
        video_url,
        song_name,
        artist_name,
        quality,
        download_dir,
        f"Searching and downloading video: {query}",
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


def download_videos_from_youtube_playlist(playlist_url, quality='best', download_dir='videos'):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
    }

    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=show_busy_progress,
        args=("Fetching YouTube video playlist from online...", stop_event),
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

    downloaded_videos = set()
    for index, entry in enumerate(entries, start=1):
        title = entry.get('title') or f'Video {index}'
        uploader = entry.get('uploader') or entry.get('channel')
        song_name, artist_name = parse_song_details_from_youtube_title(title, uploader)
        video_key = normalize_song_key(song_name, artist_name)

        if video_key in downloaded_videos:
            print(f"\n[{index}/{len(entries)}] Duplicate video already handled. Skipping: {song_name} by {artist_name}")
            continue

        downloaded_videos.add(video_key)
        print(f"\n[{index}/{len(entries)}] {song_name} by {artist_name}")

        video_url = entry.get('webpage_url') or entry.get('url')
        if video_url and not video_url.startswith('http'):
            video_url = f"https://www.youtube.com/watch?v={video_url}"

        if video_url:
            success = download_video(
                video_url,
                song_name,
                artist_name,
                quality,
                download_dir,
                f"Downloading playlist video: {title}",
            )
            if not success:
                print("Trying again with YouTube search...")
                download_video_by_song(song_name, artist_name, quality, download_dir)
        else:
            download_video_by_song(song_name, artist_name, quality, download_dir)


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
