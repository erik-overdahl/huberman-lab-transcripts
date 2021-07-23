#!/usr/bin/env python3

import subprocess
from pathlib import Path
from typing import List

class PodcastInfoDownloader:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir


    def _build_youtube_dl_cmd(self, video_or_playlist_ids: List[str]) -> str:
        name_format = f'{self.data_dir.absolute()}/%(id)s.%(ext)s'
        sub_lang = f'' + "\\"
        return f"""youtube-dl \
                -4 \
                --write-sub --write-auto-sub \
                --sub-lang en,en-US \
                --write-info-json \
               --playlist-reverse \
               --skip-download \
               -o '{name_format}' \
               --restrict-filenames \
               --youtube-skip-dash-manifest \
               {' '.join(video_or_playlist_ids)}"""


    def download(self, video_or_playlist_ids: List[str]) -> None:
        if not self.data_dir.exists():
            self.data_dir.mkdir()
        cmd = self._build_youtube_dl_cmd(video_or_playlist_ids)
        subprocess.run(cmd, shell=True)
