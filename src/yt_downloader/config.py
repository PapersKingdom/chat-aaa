from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomli


@dataclass(frozen=True)
class DownloadConfig:
    output_dir: Path = Path("downloads")
    format: str = "bv*+ba/b"
    audio_only: bool = False
    audio_format: str = "mp3"
    subtitles: bool = False
    sub_lang: str = "en"
    no_playlist: bool = False
    rate_limit: str | None = None
    retries: int = 10
    proxy: str | None = None
    cookies: Path | None = None


def load_config(path: Path | None) -> DownloadConfig:
    if path is None:
        return DownloadConfig()

    data = tomli.loads(path.read_text(encoding="utf-8"))

    return DownloadConfig(
        output_dir=Path(data.get("output_dir", "downloads")),
        format=data.get("format", "bv*+ba/b"),
        audio_only=bool(data.get("audio_only", False)),
        audio_format=data.get("audio_format", "mp3"),
        subtitles=bool(data.get("subtitles", False)),
        sub_lang=data.get("sub_lang", "en"),
        no_playlist=bool(data.get("no_playlist", False)),
        rate_limit=data.get("rate_limit"),
        retries=int(data.get("retries", 10)),
        proxy=data.get("proxy"),
        cookies=Path(data["cookies"]) if data.get("cookies") else None,
    )
