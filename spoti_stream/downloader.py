# spoti_stream/downloader.py

import os
import re
import threading
import time

import imageio_ffmpeg
import yt_dlp


YOUTUBE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
}

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)


def get_output_basename(song_name, artist_name=None, output_name=None):
    if output_name:
        return sanitize_filename(output_name)
    return sanitize_filename(f"{song_name} by {artist_name}")


def is_placeholder_title(title):
    if not title:
        return True
    return title in ('YouTube video',) or bool(re.match(r'^(Video|Track) \d+$', title))


def get_source_title(source):
    try:
        info = get_stream_info(source)
    except Exception:
        return None
    if info and info.get('entries'):
        info = next((entry for entry in info.get('entries', []) if entry), None)
    return info.get('title') if info else None


def get_mp3_file_path(song_name, artist_name, download_dir, output_name=None):
    output_basename = get_output_basename(song_name, artist_name, output_name)
    return os.path.join(download_dir, f"{output_basename}.mp3")


def get_video_file_path(song_name, artist_name, download_dir, extension='mp4', output_name=None):
    output_basename = get_output_basename(song_name, artist_name, output_name)
    return os.path.join(download_dir, f"{output_basename}.{extension}")


def find_existing_video_file(song_name, artist_name, download_dir, output_name=None):
    for extension in ('mkv', 'mp4', 'webm'):
        video_file_path = get_video_file_path(song_name, artist_name, download_dir, extension, output_name)
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


def build_ydl_options(song_name, artist_name, download_dir, output_name=None):
    output_basename = get_output_basename(song_name, artist_name, output_name)
    return {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_dir, f"{output_basename}.%(ext)s"),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'progress_hooks': [show_download_progress],
        'retries': 3,
        'fragment_retries': 3,
        'continuedl': True,
        'http_headers': YOUTUBE_HEADERS,
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
        '2': '2160',
        '4k': '2160',
        '2160': '2160',
        '3': '1440',
        '1440': '1440',
        '4': '1080',
        '1080': '1080',
        '5': '720',
        '720': '720',
        '6': '480',
        '480': '480',
        '7': '360',
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
        '2': '4K',
        '4k': '4K',
        '2160': '4K',
        '3': '1440p',
        '1440': '1440p',
        '4': '1080p',
        '1080': '1080p',
        '5': '720p',
        '720': '720p',
        '6': '480p',
        '480': '480p',
        '7': '360p',
        '360': '360p',
    }
    return quality_map.get(quality, '720p')


def get_video_height_limit(quality):
    quality = str(quality).strip().lower()
    quality_map = {
        '2': 2160,
        '4k': 2160,
        '2160': 2160,
        '3': 1440,
        '1440': 1440,
        '4': 1080,
        '1080': 1080,
        '5': 720,
        '720': 720,
        '6': 480,
        '480': 480,
        '7': 360,
        '360': 360,
    }
    return quality_map.get(quality)


def get_ydl_extract_options(extract_flat=False, noplaylist=False):
    return {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'extract_flat': extract_flat,
        'noplaylist': noplaylist,
        'http_headers': YOUTUBE_HEADERS,
    }


def is_url(query):
    return bool(re.match(r'^(https?://|www\.)', query.strip(), flags=re.IGNORECASE))


def normalize_youtube_url(url):
    url = url.strip()
    if url.startswith('www.'):
        return f"https://{url}"
    return url


def get_video_url(entry):
    url = entry.get('webpage_url') or entry.get('original_url') or entry.get('url')
    if url and not url.startswith('http'):
        url = f"https://www.youtube.com/watch?v={url}"
    return url


def flatten_video_entries(info):
    if not info:
        return []

    if info.get('entries') is None:
        return [info]

    entries = []
    for entry in info.get('entries') or []:
        if not entry:
            continue
        if entry.get('entries'):
            entries.extend(flatten_video_entries(entry))
        else:
            entries.append(entry)
    return entries


def resolve_input(query):
    """
    Accepts a YouTube URL, playlist URL, channel URL, or search text.
    Returns a list of video metadata dictionaries.
    """
    source = normalize_youtube_url(query)
    if not is_url(source):
        source = f"ytsearch10:{query}"

    ydl_opts = get_ydl_extract_options(extract_flat=True)
    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=show_busy_progress,
        args=("Resolving YouTube input...", stop_event),
        daemon=True,
    )
    progress_thread.start()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(source, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"\nCould not resolve YouTube input: {e}")
        return []
    except Exception as e:
        print(f"\nAn error occurred while resolving YouTube input: {e}")
        return []
    finally:
        stop_event.set()
        progress_thread.join()

    return flatten_video_entries(info)


def get_stream_info(url):
    ydl_opts = get_ydl_extract_options(extract_flat=False, noplaylist=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


def get_stream_groups(info):
    formats = info.get('formats') or []
    video_streams = [
        video_format
        for video_format in formats
        if video_format.get('vcodec') != 'none'
        and video_format.get('acodec') == 'none'
        and video_format.get('height')
    ]
    audio_streams = [
        audio_format
        for audio_format in formats
        if audio_format.get('acodec') != 'none' and audio_format.get('vcodec') == 'none'
    ]
    muxed_streams = [
        muxed_format
        for muxed_format in formats
        if muxed_format.get('vcodec') != 'none'
        and muxed_format.get('acodec') != 'none'
        and muxed_format.get('height')
    ]

    sort_key = lambda stream: (
        get_format_value(stream, 'height'),
        get_format_value(stream, 'fps'),
        get_format_value(stream, 'tbr'),
        get_format_value(stream, 'vbr'),
    )

    return {
        'video': sorted(video_streams, key=sort_key, reverse=True),
        'audio': sorted(audio_streams, key=lambda stream: (
            get_format_value(stream, 'abr'),
            get_format_value(stream, 'tbr'),
            get_format_value(stream, 'filesize'),
        ), reverse=True),
        'muxed': sorted(muxed_streams, key=sort_key, reverse=True),
    }


def select_video_stream(streams, quality):
    height_limit = get_video_height_limit(quality)
    video_streams = streams.get('video') or []

    if height_limit is None:
        return video_streams[0] if video_streams else None

    allowed_streams = [
        stream for stream in video_streams
        if stream.get('height') and stream.get('height') <= height_limit
    ]
    return allowed_streams[0] if allowed_streams else None


def select_muxed_stream(streams, quality):
    height_limit = get_video_height_limit(quality)
    muxed_streams = streams.get('muxed') or []

    if height_limit is None:
        return muxed_streams[0] if muxed_streams else None

    allowed_streams = [
        stream for stream in muxed_streams
        if stream.get('height') and stream.get('height') <= height_limit
    ]
    return allowed_streams[0] if allowed_streams else None


def select_audio_stream(streams):
    audio_streams = streams.get('audio') or []
    return audio_streams[0] if audio_streams else None


def select_download_streams(info, quality):
    streams = get_stream_groups(info)
    selected_video = select_video_stream(streams, quality)
    selected_audio = select_audio_stream(streams)
    selected_muxed = select_muxed_stream(streams, quality)

    if not selected_video and selected_muxed:
        return selected_muxed.get('format_id'), selected_muxed, None, 'muxed'

    if not selected_video:
        return None, None, None, None

    prefer_muxed = get_video_height_limit(quality) is not None
    if prefer_muxed and selected_muxed and get_format_value(selected_muxed, 'height') >= get_format_value(selected_video, 'height'):
        return selected_muxed.get('format_id'), selected_muxed, None, 'muxed'

    if selected_audio:
        return f"{selected_video.get('format_id')}+{selected_audio.get('format_id')}", selected_video, selected_audio, 'dash'

    if selected_video.get('acodec') != 'none':
        return selected_video.get('format_id'), selected_video, None, 'muxed'

    fallback_format = get_video_format(quality)
    return f"{selected_video.get('format_id')}+bestaudio/{fallback_format}", selected_video, None, 'dash'


def get_format_max_height(video_info):
    heights = [
        video_format.get('height')
        for video_format in video_info.get('formats', [])
        if video_format.get('vcodec') != 'none' and video_format.get('height')
    ]
    return max(heights, default=0)


def get_best_video_search_result(query, max_results=5):
    ydl_opts = get_ydl_extract_options(extract_flat=True)

    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=show_busy_progress,
        args=(f"Finding top YouTube result from {max_results} matches...", stop_event),
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

    best_entry = entries[0]
    title = best_entry.get('title', 'Unknown title')
    url = get_video_url(best_entry)

    print(f"Selected result: {title}")

    return url


def get_format_value(video_format, key, default=0):
    value = video_format.get(key)
    return value if isinstance(value, (int, float)) else default


def choose_exact_video_format(video_info, quality):
    selected_format, best_video, best_audio, _ = select_download_streams(video_info, quality)
    return selected_format, best_video, best_audio


def inspect_video_source(source, quality):
    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=show_busy_progress,
        args=("Inspecting available video qualities...", stop_event),
        daemon=True,
    )
    progress_thread.start()

    try:
        video_info = get_stream_info(source)
    except yt_dlp.utils.DownloadError as e:
        print(f"\nCould not inspect video formats: {e}")
        return None, None, None
    except Exception as e:
        print(f"\nAn error occurred while inspecting video formats: {e}")
        return None, None, None
    finally:
        stop_event.set()
        progress_thread.join()

    if video_info and video_info.get('entries'):
        video_info = next((entry for entry in video_info.get('entries', []) if entry), None)

    if not video_info:
        return None, None, None

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

    return selected_format, video_info.get('webpage_url') or source, video_info.get('title')


def build_video_ydl_options(song_name, artist_name, download_dir, quality='best', output_name=None):
    output_basename = get_output_basename(song_name, artist_name, output_name)
    return {
        'format': get_video_format(quality),
        'outtmpl': os.path.join(download_dir, f"{output_basename}.%(ext)s"),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'merge_output_format': 'mp4',
        'format_sort': ['res', 'fps', 'br'],
        'format_sort_force': True,
        'progress_hooks': [show_download_progress],
        'retries': 3,
        'fragment_retries': 3,
        'continuedl': True,
        'http_headers': YOUTUBE_HEADERS,
    }


def is_http_403_error(error):
    return 'HTTP Error 403' in str(error) or '403: Forbidden' in str(error)


def get_video_retry_formats(selected_format, quality):
    automatic_format = get_video_format(quality)
    return [
        ('yt-dlp automatic quality selector', automatic_format),
        ('MP4 up to 1080p', 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]/best[height<=1080]'),
        ('best muxed stream', 'best[ext=mp4]/best'),
    ]


def refresh_selected_video_format(source, quality):
    selected_format, refreshed_source, _ = inspect_video_source(source, quality)
    return selected_format, refreshed_source


def merge(video_path, audio_path, output_path):
    import subprocess
    command = [
        imageio_ffmpeg.get_ffmpeg_exe(),
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        output_path,
    ]
    subprocess.run(command, check=True)


def download_audio(source, song_name, artist_name, download_dir='songs', message=None, output_name=None, use_source_title=False):
    if use_source_title and is_placeholder_title(output_name):
        output_name = get_source_title(source)

    mp3_file_path = get_mp3_file_path(song_name, artist_name, download_dir, output_name)
    mp3_file_name = os.path.basename(mp3_file_path)
    os.makedirs(download_dir, exist_ok=True)

    if os.path.exists(mp3_file_path):
        print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
        return True

    ydl_opts = build_ydl_options(song_name, artist_name, download_dir, output_name)

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


def download_video(source, song_name, artist_name, quality='best', download_dir='videos', message=None, output_name=None):
    os.makedirs(download_dir, exist_ok=True)

    if message:
        print(message)
    print(f"Requested video quality: {get_video_quality_label(quality)}")
    selected_format, resolved_source, source_title = inspect_video_source(source, quality)
    final_output_name = output_name or source_title
    existing_video_file = find_existing_video_file(song_name, artist_name, download_dir, final_output_name)
    video_file_path = get_video_file_path(song_name, artist_name, download_dir, output_name=final_output_name)
    video_file_name = os.path.basename(video_file_path)

    if existing_video_file:
        print(f"'{video_file_name}' is already downloaded as video. Skipping: {os.path.basename(existing_video_file)}")
        return True

    if selected_format:
        source = resolved_source
    else:
        print("Could not choose an exact HD stream. Falling back to yt-dlp automatic best format.")

    last_error = None
    retry_source = source
    retry_formats = get_video_retry_formats(selected_format, quality)
    selected_stream_retry_count = 3 if selected_format else 0

    for attempt_index in range(1, selected_stream_retry_count + len(retry_formats) + 1):
        if attempt_index <= selected_stream_retry_count:
            attempt_label = f"refreshed selected HD stream attempt {attempt_index}"
            if attempt_index > 1:
                refreshed_format, refreshed_source = refresh_selected_video_format(source, quality)
                if refreshed_format:
                    selected_format = refreshed_format
                    retry_source = refreshed_source
            format_selector = selected_format
        else:
            attempt_label, format_selector = retry_formats[attempt_index - selected_stream_retry_count - 1]

        ydl_opts = build_video_ydl_options(song_name, artist_name, download_dir, quality, final_output_name)
        ydl_opts['format'] = format_selector

        if attempt_index > 1:
            print(f"Retrying same video with {attempt_label}...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([retry_source])
                print(f"Downloaded video: {video_file_name}")
                return True
            except yt_dlp.utils.DownloadError as e:
                last_error = e
                print(f"Video download error using {attempt_label}: {e}")
                if not is_http_403_error(e):
                    break
            except Exception as e:
                last_error = e
                print(f"An error occurred while downloading video {song_name} by {artist_name}: {e}")
                break

    if last_error:
        print(f"Video download error for {song_name} by {artist_name}: {last_error}")
        if is_http_403_error(last_error):
            print("All same-video retry formats failed with HTTP 403. Try updating yt-dlp if this keeps happening: python -m pip install -U yt-dlp")
    return False


def download_video_entry(entry, quality='best', download_dir='videos'):
    title = entry.get('title') or entry.get('fulltitle') or 'YouTube video'
    uploader = entry.get('uploader') or entry.get('channel') or 'YouTube'
    song_name, artist_name = parse_song_details_from_youtube_title(title, uploader)
    video_url = get_video_url(entry)
    output_name = None if is_placeholder_title(title) else title

    if not video_url:
        print(f"Could not find a playable URL for: {title}")
        return False

    return download_video(
        video_url,
        song_name,
        artist_name,
        quality,
        download_dir,
        f"Downloading YouTube video: {title}",
        output_name,
    )


def download_videos_from_youtube_input(query, quality='best', download_dir='videos'):
    entries = resolve_input(query)
    if not entries:
        print("No YouTube videos found.")
        return

    print(f"Resolved {len(entries)} YouTube video(s).")
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
        success = download_video_entry(entry, quality, download_dir)
        if not success:
            print("Skipping this video after same-video retry formats failed.")


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
    download_videos_from_youtube_input(playlist_url, quality, download_dir)


def download_songs_from_youtube_playlist(playlist_url, download_dir='songs'):
    entries = resolve_input(playlist_url)

    if not entries:
        print("No videos found for this YouTube input.")
        return

    print(f"Resolved {len(entries)} YouTube video(s).")

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

        video_url = get_video_url(entry)
        output_name = None if is_placeholder_title(title) else title

        if video_url:
            success = download_audio(
                video_url,
                song_name,
                artist_name,
                download_dir,
                f"Downloading from playlist video: {title}",
                output_name,
                True,
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
