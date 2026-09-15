import sys
import threading

from rich.console import Console
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table


if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

console = Console()


def format_bytes(value):
    if not value:
        return "--"
    size = float(value)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if size < 1024 or unit == "GiB":
            return f"{size:.1f}{unit}"
        size /= 1024


def format_time(seconds):
    if seconds is None:
        return "--:--"
    seconds = max(0, int(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"


class DownloadProgress:
    """Render yt-dlp stream progress and optional playlist totals in place."""

    def __init__(self, playlist_name=None, total_items=None):
        self.playlist_name = playlist_name
        self.total_items = total_items
        self.counts = {"downloaded": 0, "skipped": 0, "failed": 0}
        self.current_status = None
        self.current_index = 0
        self.current_title = ""
        self._tasks = {}
        self._lock = threading.RLock()
        self._started = False
        self.progress = Progress(
            TextColumn("{task.description:<10}"),
            BarColumn(bar_width=24),
            TaskProgressColumn(),
            TextColumn("{task.fields[details]}", justify="left"),
            console=console,
            refresh_per_second=8,
        )

    @property
    def is_playlist(self):
        return self.total_items is not None

    def __enter__(self):
        if self.playlist_name:
            console.print(f"\n[bold]Playlist:[/bold] {self.playlist_name}")
        self.progress.start()
        self._started = True
        if self.is_playlist:
            self._tasks["Overall"] = self.progress.add_task(
                "Overall", total=self.total_items, details=f"0/{self.total_items} items"
            )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._started:
            self.progress.stop()
            self._started = False
        if self.is_playlist:
            self.print_summary()

    def start_item(self, index, title):
        if not self.is_playlist:
            return
        with self._lock:
            self.current_index = index
            self.current_title = title
            self.current_status = None
            old_task = self._tasks.pop("Current", None)
            if old_task is not None:
                self.progress.remove_task(old_task)
            self._tasks["Current"] = self.progress.add_task(
                "Current", total=None, details=f"[{index}/{self.total_items}] {title}"
            )

    def finish_item(self, status):
        if not self.is_playlist or self.current_status is not None:
            return
        if status not in self.counts:
            status = "failed"
        with self._lock:
            self.current_status = status
            self.counts[status] += 1
            overall = self._tasks.get("Overall")
            if overall is not None:
                completed = sum(self.counts.values())
                self.progress.update(
                    overall,
                    completed=completed,
                    details=f"{completed}/{self.total_items} items",
                )
            current = self._tasks.get("Current")
            if current is not None:
                self.progress.update(current, total=1, completed=1, details=status.capitalize())

    def _stream_label(self, data):
        if self.is_playlist:
            return "Current"
        info = data.get("info_dict") or {}
        video_codec = info.get("vcodec")
        audio_codec = info.get("acodec")
        if video_codec and video_codec != "none" and (not audio_codec or audio_codec == "none"):
            return "Video"
        if audio_codec and audio_codec != "none" and (not video_codec or video_codec == "none"):
            return "Audio"
        return "Download"

    def download_hook(self, data):
        status = data.get("status")
        if status not in ("downloading", "finished"):
            return
        with self._lock:
            label = self._stream_label(data)
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            completed = data.get("downloaded_bytes") or 0
            speed = data.get("speed")
            eta = data.get("eta")

            task_id = self._tasks.get(label)
            if task_id is None:
                task_id = self.progress.add_task(label, total=total, details="Starting...")
                self._tasks[label] = task_id

            if status == "finished":
                completed = total or completed or 1
                total = total or completed

            size_text = format_bytes(completed)
            if total:
                size_text = f"{size_text}/{format_bytes(total)}"
            details = f"{size_text}  {format_bytes(speed)}/s  {format_time(eta)}"
            self.progress.update(task_id, total=total, completed=completed, details=details)

    def postprocessor_hook(self, data):
        postprocessor = data.get("postprocessor") or "Processing"
        if "Merger" not in postprocessor:
            return
        with self._lock:
            task_id = self._tasks.get("Merging")
            if task_id is None:
                task_id = self.progress.add_task("Merging", total=1, details="Processing...")
                self._tasks["Merging"] = task_id
            if data.get("status") == "finished":
                self.progress.update(task_id, completed=1, details="Complete")

    def print_summary(self):
        table = Table(title="Download summary", show_header=False, box=None)
        table.add_column(style="bold")
        table.add_column(justify="right")
        table.add_row("[green]✓ Downloaded[/green]", str(self.counts["downloaded"]))
        table.add_row("[yellow]⊘ Skipped[/yellow]", str(self.counts["skipped"]))
        table.add_row("[red]✗ Failed[/red]", str(self.counts["failed"]))
        console.print(table)
