"""
Tools for manipulating video:
    - extracting thumbnails
"""

import os
import argparse
import subprocess

from moviepy.editor import *
from PIL import Image

import click
from flask.cli import with_appcontext

import conf
from .. import db
from .eptools import get_season, episode_from_filename, collect_episodes

"""
--The following will extract every frame
ffmpeg -i input.mkv -s 480x356 -q:v 2 -frame_pts 1 %05d.jpg

#FYI: get every 6th frame
ffmpeg -i $IN -vf "select=not(mod(n\,6))" -s 480x356 -vsync vfr -q:v 2 -frame_pts 1 %05d.jpg
"""
def ffmpeg_extract_thumbs(source_path,  dest_dir, dest_width, dest_height):
    """
    extract all thumbnails from a video using ffmpeg
    ffmpeg -i input.mkv -s 480x356 -q:v 2 -frame_pts 1 %05d.jpg
    """
    return subprocess.run(
            ['nice',
                'ffmpeg',
                '-i', source_path,
                '-s', f'{dest_width}x{dest_height}',
                '-q:v', '2',
                '-frame_pts', '1',
                os.path.join(dest_dir,'%05d.jpg')])

def moviepy_extract_thumbs(source_path,  dest_dir, dest_fps, dest_width):
    """uses moviepy to extract thumbnails. painfully slow compared to ffmpeg"""
    clip = VideoFileClip(source_path)

    if dest_width is not None:
        clip = clip.resize(width=dest_width)

    if dest_fps is None:
        dest_fps = clip.fps

    #we'll be extracting every nth frame
    nthframe = round(clip.fps / dest_fps)

    for i, frame in enumerate(clip.iter_frames()):
        if i % nthframe != 0: continue

        curr_ms = int((i / clip.fps) * 1000)
        if(i % round(clip.fps*10) == 0):
            print(f"{source_path} -> {dest_dir} curr_ms: {curr_ms}")
        new_img = Image.fromarray(frame)
        new_img_filepath = os.path.join(dest_dir, f"{curr_ms:07}.jpg")
        new_img.save(new_img_filepath)

#FIXME: actually examine the file?
def is_video(filename):
    """checks if file is a video file"""
    return filename.endswith('mkv') or filename.endswith('avi') or filename.endswith('mp4')

def was_extracted(ep, dest_dir):
    tolerance = 200
    vinfo = db.query_db("""SELECT * FROM video_info where episode = ?""", (ep,), one=True)
    nframes = vinfo['nframes']
    num_files = len([fname for fname in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, fname)) and fname.endswith('.jpg')])
    diff = abs(num_files - nframes)
    extracted = diff <= tolerance
    return extracted

def find_video(episode):
    """given an episode (SsEe), find the path to the video file"""
    for dirpath, dirnames, filenames in os.walk(conf.SERIES_DIR):
        for filename in filenames:
            if not is_video(filename): continue

            cand_ep = episode_from_filename(filename)
            if episode == cand_ep:
                path = os.path.join(dirpath, filename)
                return path
    return None

def extract_episode(ep, source_path, force_extract=False):
    output_dir=conf.THUMBNAILS_DIR
    width=conf.GIF_WIDTH
    height=conf.GIF_HEIGHT

    #get the outputdir
    season = get_season(ep)
    dest_dir = os.path.join(output_dir, season, ep)
    os.makedirs(dest_dir, exist_ok=True)

    extract = force_extract or not was_extracted(ep, dest_dir)

    if extract:
        print(f'extracting thumbnails for {ep} -> {dest_dir}')
        ffmpeg_extract_thumbs(source_path, dest_dir, width, height)
    else:
        print(f'skipping {ep}...was extracted')

def init_app(app):
    app.cli.add_command(extract_all_thumbs_cmd)
    app.cli.add_command(extract_ep_thumbs_cmd)

@click.command('extract-all-thumbs')
@with_appcontext
def extract_all_thumbs_cmd():
    """extract all thumbnails. it will skip episodes already extracted"""
    click.echo('Extracting thumbs')
    source_dir=conf.SERIES_DIR

    #get all the episodes from the source_dir
    episodes = collect_episodes(source_dir)

    #iterate over the episodes, extracting thumbnails from each of them
    for ep, source_path in episodes:
        extract_episode(ep, source_path)

    click.echo('Thumbnails extracted')

@click.command('extract-ep-thumbs')
@click.argument("ep")  #ie S01E15
@with_appcontext
def extract_ep_thumbs_cmd(ep):
    """extract thumbnails for a given episode. it will not skip episodes already extracted"""

    #find path to video for this episode
    source_path = find_video(ep)

    #bail if we didn't find anything
    if source_path is not None:
        extract_episode(ep, source_path, force_extract=True)
    else:
        print(f'video for episode {episode} not found')
