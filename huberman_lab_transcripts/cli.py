#!/usr/bin/env python3

from typing import List, Optional
from pathlib import Path

import typer

from .download import PodcastInfoDownloader


app = typer.Typer(name="huberman-transcripts")

@app.command()
def download(video_or_playlist_ids: List[str] = typer.Argument(..., help="One or more youtube video ids or playlist ids"),
             data_dir: str = typer.Option('./data', help="Directory into which to download data")):
    downloader = PodcastInfoDownloader(Path(data_dir))
    downloader.download(video_or_playlist_ids)


if __name__ == '__main__':
    app()
