#!/usr/bin/env python3

from textwrap import fill
from pathlib import Path
from typing import List
import re

from .podcastobjects import PodcastInfo, PodcastChapter, CaptionType


def format_md_link(text: str, link: str) -> str:
    return f'[{text}]({link})'


def file_header(podcast: PodcastInfo) -> str:
    elems = {'title': podcast.title,
             'date': podcast.date,
             'slug': f'episode-{podcast.episode_num}',
             'lang': 'en',
             'tags': ','.join(podcast.tags),
             'author': podcast.uploader}
    return '\n'.join([f'{key}: {value}' for key, value in elems.items()]) + '\n\n'


def summary_paragraph(podcast: PodcastInfo) -> str:
    summary = fill(podcast.description.split('\n')[0])
    return f'{summary}\n\n[TOC]\n'


def chapter_header(chapter: PodcastChapter) -> str:
    return f'# {format_md_link(chapter.title, chapter.link)}\n\n'


def paragraph_body(chapter: PodcastChapter) -> str:
    body = fill(chapter.full_transcript)
    return f'{body}\n\n'


def file_footer(podcast: PodcastInfo) -> str:
    elems = podcast.description.split('\n')[1:]
    groups = []
    curr_ = []
    for x in elems:
        if x == '':
            groups.append(curr_)
            curr_ = []
        else:
            curr_.append(x)
    groups.append(curr_)
    for group in groups:
        if len(group) > 1 and group[0].endswith(':'):
            for i, text in enumerate(group[1:]):
                group[i+1] = '* ' + text
        elif len(group) == 1:
            group[0] = fill(group[0])

    footer_elems = ['\n'.join(g) for g in groups[1:] if g[0] != 'Timestamps:']
    footer = '\n\n'.join(footer_elems)
    return f'\n\n\n{footer}\n'


def generate(podcast_info: PodcastInfo) -> str:
    file_elements = []
    file_elements.append(file_header(podcast_info))
    file_elements.append(summary_paragraph(podcast_info))

    for chapter in podcast_info.chapters:
        file_elements.append(chapter_header(chapter))
        file_elements.append(paragraph_body(chapter))

    file_elements.append(file_footer(podcast_info))

    return ''.join(file_elements)


def create_markdown_file(podcast_info: PodcastInfo, target_dir: Path) -> None:
    output_file = target_dir.absolute().joinpath(f'episode-{podcast_info.episode_num}.md')
    print('creating ', output_file)
    file_content = generate(podcast_info)
    output_file.write_text(file_content)
