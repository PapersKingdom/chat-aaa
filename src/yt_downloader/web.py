from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import uuid

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from yt_downloader.config import DownloadConfig
from yt_downloader.downloader import download_urls


@dataclass
class DownloadJob:
    job_id: str
    urls: list[str]
    config: DownloadConfig
    status: str = "queued"
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    finished_at: datetime | None = None
    message: str | None = None


app = FastAPI(title="YT Downloader")
TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
EXECUTOR = ThreadPoolExecutor(max_workers=2)
JOBS: dict[str, DownloadJob] = {}


def _parse_urls(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _parse_optional_path(value: str | None) -> Path | None:
    if value:
        return Path(value)
    return None


def _run_job(job: DownloadJob) -> None:
    job.status = "running"
    job.started_at = datetime.utcnow()
    try:
        download_urls(job.urls, job.config)
    except Exception as exc:  # noqa: BLE001 - surface errors to UI
        job.status = "failed"
        job.message = str(exc)
    else:
        job.status = "completed"
        job.message = "Download finished successfully."
    finally:
        job.finished_at = datetime.utcnow()


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> Any:
    jobs = sorted(JOBS.values(), key=lambda item: item.created_at, reverse=True)[:8]
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "jobs": jobs,
        },
    )


@app.post("/download")
def submit_download(
    request: Request,
    urls: str = Form(...),
    output_dir: str = Form("downloads"),
    format_selector: str = Form("bv*+ba/b"),
    audio_only: bool = Form(False),
    audio_format: str = Form("mp3"),
    subtitles: bool = Form(False),
    sub_lang: str = Form("en"),
    no_playlist: bool = Form(False),
    rate_limit: str | None = Form(None),
    retries: int = Form(10),
    proxy: str | None = Form(None),
    cookies: str | None = Form(None),
) -> RedirectResponse:
    url_list = _parse_urls(urls)
    config = DownloadConfig(
        output_dir=Path(output_dir),
        format=format_selector,
        audio_only=audio_only,
        audio_format=audio_format,
        subtitles=subtitles,
        sub_lang=sub_lang,
        no_playlist=no_playlist,
        rate_limit=rate_limit or None,
        retries=retries,
        proxy=proxy or None,
        cookies=_parse_optional_path(cookies),
    )
    job_id = uuid.uuid4().hex
    job = DownloadJob(job_id=job_id, urls=url_list, config=config)
    JOBS[job_id] = job
    EXECUTOR.submit(_run_job, job)
    return RedirectResponse(url=f"/jobs/{job_id}", status_code=303)


@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request, job_id: str) -> Any:
    job = JOBS.get(job_id)
    return TEMPLATES.TemplateResponse(
        "job.html",
        {
            "request": request,
            "job": job,
        },
    )


def run() -> None:
    uvicorn.run("yt_downloader.web:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
