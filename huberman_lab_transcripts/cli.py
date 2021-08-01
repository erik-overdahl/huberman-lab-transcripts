#!/usr/bin/env python3

from typing import List, Optional
from pathlib import Path

import typer

from .download import PodcastInfoDownloader
from .extract import PodcastExtractor
from .generate import create_markdown_file


app = typer.Typer(name="huberman-transcripts")

@app.command()
def download(video_or_playlist_ids: List[str] = typer.Argument(..., help="One or more youtube video ids or playlist ids"),
             data_dir: str = typer.Option('./data', help="Directory into which to download data")):
    """A wrapper around youtube-dl for downloading video data"""
    downloader = PodcastInfoDownloader(Path(data_dir))
    downloader.download(video_or_playlist_ids)


@app.command()
def generate(video_ids: List[str] = typer.Argument(None, help="The youtube video ids for which to generate markdown files. If empty, generate files for all ids in [DATA_DIR]"),
             data_dir: str = typer.Option('./data', help="Directory of raw video data"),
             target_dir: str = typer.Option('./site/content/posts', help="Directory into which to place generated markdown files for static site generator")):
    """Generate markdown files for Pelican"""
    extractor = PodcastExtractor(Path(data_dir).expanduser().absolute())
    podcasts = extractor.extract_all(video_ids)
    target_dir = Path(target_dir).expanduser().absolute()
    if not target_dir.exists():
        target_dir.mkdir()
    for pod in podcasts:
        create_markdown_file(pod, target_dir)


if __name__ == '__main__':
    app()
