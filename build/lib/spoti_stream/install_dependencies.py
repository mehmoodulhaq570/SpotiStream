import subprocess
import os

def is_installed(command):
    """Check if a command exists on the system."""
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        return True
    except Exception:
        return False

def install_scoop():
    """Install Scoop if it's not already installed."""
    if is_installed('scoop'):
        #print("Scoop is already installed.")
        return
    try:
        # Suppress output and errors using DEVNULL
        subprocess.run(
            'powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser; iwr -useb get.scoop.sh | iex"',
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("Scoop installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install Scoop.")

def install_ffmpeg():
    """Install FFmpeg using Scoop if it's not already installed."""
    if is_installed('ffmpeg'):
        #print("FFmpeg is already installed.")
        return
    try:
        # Suppress output and errors using DEVNULL
        subprocess.run(
            'powershell -Command "scoop install ffmpeg"',
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("FFmpeg installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install FFmpeg.")
