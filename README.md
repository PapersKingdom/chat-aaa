# YouTube Video Downloader (yt-downloader)

A production-ready YouTube video downloader built on top of the `yt-dlp` library. It avoids any external APIs and relies solely on local libraries for download orchestration.

## Features

- Download single videos or playlists
- Select format codes or use best defaults
- Audio-only extraction with automatic conversion
- Subtitle download (manual or auto)
- Custom output directories and filename templates
- Cookie and proxy support
- Rate limiting and download retries
- TOML configuration file support

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
yt-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Common examples

Download the best video + audio:

```bash
yt-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ --format "bv*+ba/b"
```

Download audio-only as mp3:

```bash
yt-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ --audio-only --audio-format mp3
```

Download subtitles in English:

```bash
yt-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ --subtitles --sub-lang en
```

Download a playlist (default):

```bash
yt-downloader https://www.youtube.com/playlist?list=YOUR_LIST_ID
```

Disable playlist processing:

```bash
yt-downloader https://www.youtube.com/playlist?list=YOUR_LIST_ID --no-playlist
```

## Configuration

Create a `yt-downloader.toml` file and pass it with `--config`:

```toml
output_dir = "downloads"
format = "bv*+ba/b"
no_playlist = false
rate_limit = "2M"
retries = 10
subtitles = true
sub_lang = "en"
```

Then run:

```bash
yt-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ --config yt-downloader.toml
```

## Notes

- This tool depends on `yt-dlp` and uses your local network access.
- Respect YouTube's Terms of Service and copyright laws.

## License

MIT
