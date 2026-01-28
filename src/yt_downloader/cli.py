from __future__ import annotations

import argparse
from pathlib import Path
import logging
import sys

from yt_downloader.config import DownloadConfig, load_config
from yt_downloader.downloader import download_urls


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yt-downloader",
        description="Production-ready YouTube downloader powered by yt-dlp.",
    )
    parser.add_argument("urls", nargs="+", help="One or more YouTube URLs to download.")
    parser.add_argument("--config", type=Path, help="Path to a TOML config file.")
    parser.add_argument("--output-dir", type=Path, help="Directory to store downloads.")
    parser.add_argument("--format", dest="format", help="yt-dlp format selector.")
    parser.add_argument("--audio-only", action="store_true", help="Extract audio only.")
    parser.add_argument("--audio-format", default="mp3", help="Audio format for extraction.")
    parser.add_argument("--subtitles", action="store_true", help="Download subtitles.")
    parser.add_argument("--sub-lang", default="en", help="Subtitle language code.")
    parser.add_argument("--no-playlist", action="store_true", help="Disable playlist downloads.")
    parser.add_argument("--rate-limit", help="Throttle download rate (e.g., 1M, 500K).")
    parser.add_argument("--retries", type=int, default=10, help="Retry attempts on failure.")
    parser.add_argument("--proxy", help="Proxy URL, e.g. socks5://127.0.0.1:9050")
    parser.add_argument("--cookies", type=Path, help="Path to cookies.txt.")
    parser.add_argument("--log-level", default="INFO", help="Logging level.")
    return parser


def _merge_config(base: DownloadConfig, args: argparse.Namespace) -> DownloadConfig:
    return DownloadConfig(
        output_dir=args.output_dir or base.output_dir,
        format=args.format or base.format,
        audio_only=args.audio_only or base.audio_only,
        audio_format=args.audio_format or base.audio_format,
        subtitles=args.subtitles or base.subtitles,
        sub_lang=args.sub_lang or base.sub_lang,
        no_playlist=args.no_playlist or base.no_playlist,
        rate_limit=args.rate_limit or base.rate_limit,
        retries=args.retries if args.retries is not None else base.retries,
        proxy=args.proxy or base.proxy,
        cookies=args.cookies or base.cookies,
    )


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    config = _merge_config(load_config(args.config), args)
    download_urls(args.urls, config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
