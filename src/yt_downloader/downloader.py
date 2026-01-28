from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable
import logging

from yt_dlp import YoutubeDL

from yt_downloader.config import DownloadConfig


LOGGER = logging.getLogger(__name__)


def _build_output_template(output_dir: Path) -> str:
    return str(output_dir / "%(title).200s.%(ext)s")


def download_urls(urls: Iterable[str], config: DownloadConfig) -> None:
    output_dir = config.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    options: dict[str, object] = {
        "outtmpl": _build_output_template(output_dir),
        "format": config.format,
        "noplaylist": config.no_playlist,
        "ratelimit": config.rate_limit,
        "retries": config.retries,
        "proxy": config.proxy,
        "cookiefile": str(config.cookies) if config.cookies else None,
        "quiet": False,
        "no_warnings": True,
    }

    if config.audio_only:
        options.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": config.audio_format,
                        "preferredquality": "192",
                    }
                ],
            }
        )

    if config.subtitles:
        options.update(
            {
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": [config.sub_lang],
            }
        )

    cleaned_options = {key: value for key, value in options.items() if value is not None}
    LOGGER.info("Download configuration: %s", asdict(config))

    with YoutubeDL(cleaned_options) as ydl:
        ydl.download(list(urls))
