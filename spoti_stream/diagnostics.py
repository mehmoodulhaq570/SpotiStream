import os
import platform
import shutil
import subprocess
import sys
from importlib import metadata

from rich.table import Table

from .progress import console



def package_version(distribution):
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


def executable_version(command, fallback=None, version_argument="--version"):
    candidates = [shutil.which(command), fallback]
    for executable in dict.fromkeys(candidate for candidate in candidates if candidate):
        try:
            result = subprocess.run(
                [executable, version_argument],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            output = (result.stdout or result.stderr).strip().splitlines()
            if result.returncode == 0 and output:
                return output[0]
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def spotify_credentials_status(path="spotify_credentials.txt"):
    if not os.path.isfile(path):
        return False, "Not configured (optional)"
    try:
        with open(path, encoding="utf-8") as credentials_file:
            values = [line.strip() for line in credentials_file.readlines()[:2]]
        if len(values) == 2 and all(values):
            return True, "Configured"
    except OSError:
        pass
    return False, "File exists but is incomplete"


def run_doctor():
    checks = []
    python_ok = sys.version_info >= (3, 11)
    checks.append(("Python", python_ok, platform.python_version(), "Install Python 3.11 or newer"))

    ytdlp_version = package_version("yt-dlp")
    checks.append((
        "yt-dlp",
        ytdlp_version is not None,
        ytdlp_version or "Missing",
        'Run: python -m pip install -U "yt-dlp[default]"',
    ))

    ejs_version = package_version("yt-dlp-ejs")
    checks.append((
        "yt-dlp-ejs",
        ejs_version is not None,
        ejs_version or "Missing",
        'Run: python -m pip install -U "yt-dlp[default]"',
    ))

    try:
        import imageio_ffmpeg
        ffmpeg_fallback = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg_fallback = None
    ffmpeg_version = executable_version("ffmpeg", ffmpeg_fallback, "-version")
    checks.append(("FFmpeg", ffmpeg_version is not None, ffmpeg_version or "Missing", "Install FFmpeg"))

    deno_fallback = None
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        winget_deno = os.path.join(local_app_data, "Microsoft", "WinGet", "Links", "deno.exe")
        if os.path.isfile(winget_deno):
            deno_fallback = winget_deno
    deno_version = executable_version("deno", deno_fallback)
    checks.append((
        "Deno",
        deno_version is not None,
        deno_version or "Missing",
        "Run: winget install --id DenoLand.Deno --exact, then restart the terminal",
    ))

    spotify_ok, spotify_detail = spotify_credentials_status()
    checks.append(("Spotify", spotify_ok, spotify_detail, "Credentials are requested when Spotify is first used"))

    table = Table(title="SpotiStream System Check", header_style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Component")
    table.add_column("Details")
    table.add_column("Recommendation")

    for name, ok, detail, recommendation in checks:
        status = "[green]✓[/green]" if ok else "[yellow]![/yellow]"
        table.add_row(status, name, detail, "" if ok else recommendation)
    console.print(table)

    required = [check for check in checks if check[0] != "Spotify"]
    healthy = all(check[1] for check in required)
    if healthy:
        console.print("\n[green]✓ SpotiStream is ready to download.[/green]")
        return 0
    console.print("\n[yellow]! Complete the recommendations above before downloading.[/yellow]")
    return 1
