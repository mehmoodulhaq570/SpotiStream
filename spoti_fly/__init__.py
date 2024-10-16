# spoti_fly/__init__.py
from .install_dependencies import install_scoop, install_ffmpeg

# Install Scoop and FFmpeg only if they are not already installed
install_scoop()
install_ffmpeg()


