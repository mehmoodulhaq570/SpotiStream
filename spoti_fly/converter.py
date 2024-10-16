# spoti_fly/converter.py
import os
import subprocess

def convert_webm_to_mp3(webm_file_path, mp3_file_name, download_dir='songs'):
    mp3_file_path = os.path.join(download_dir, mp3_file_name)
    try:
        # Suppressing FFmpeg logs by redirecting stdout and stderr
        subprocess.run(['ffmpeg', '-i', webm_file_path, mp3_file_path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"Converted to MP3: {mp3_file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {webm_file_path} to MP3: {e}")


