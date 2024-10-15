import subprocess
import os
import sys

def install_scoop():
    try:
        # Check if Scoop is already installed
        subprocess.run(["scoop", "help"], check=True)
        print("Scoop is already installed.")
    except Exception:
        print("Installing Scoop...")
        # Install Scoop using PowerShell
        subprocess.run(['powershell.exe', '-Command',
                        'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; '
                        'iwr get.scoop.sh -useb | iex'], check=True)

def install_ffmpeg():
    try:
        # Check if FFmpeg is already installed
        subprocess.run(["ffmpeg", "-version"], check=True)
        print("FFmpeg is already installed.")
    except Exception:
        print("Installing FFmpeg...")
        # Install FFmpeg using Scoop
        subprocess.run(["scoop", "install", "ffmpeg"], check=True)

