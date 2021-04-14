# This file is part of Meme It So
#
# "Meme It So" is a media (TV show and movies) screen capture and text caption
# database and image macro generator.
# Copyright (C) 2021  Phillip Dreizen
#
# Meme It So is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Meme It So is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Tools for manipulating video:
    - extracting thumbnails
"""

import os
import glob
import argparse
import subprocess
import csv
import logging

from moviepy.editor import *
from PIL import Image

import click
from flask.cli import with_appcontext, current_app

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

def is_jpg(filename):
    """checks if file is a jpg file"""
    return filename.endswith('jpg')


def was_extracted(ep, dest_dir):
    tolerance = 200
    #FIXME: what was I thinking relying on the db here? No, I should read the info from the video first
    try:
        vinfo = db.query_db("""SELECT * FROM video_info where episode = ?""", (ep,), one=True)
        nframes = vinfo['nframes']
        num_files = len([fname for fname in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, fname)) and fname.endswith('.jpg')])
        diff = abs(num_files - nframes)
        extracted = diff <= tolerance
    except:
        extracted = False
    return extracted

def find_video(episode):
    """given an episode (SsEe), find the path to the video file"""
    video_dir = current_app.config['VIDEO_DIR']

    for dirpath, dirnames, filenames in os.walk(video_dir, followlinks=True):
        for filename in filenames:
            if not is_video(filename): continue

            cand_ep = episode_from_filename(filename)
            if episode == cand_ep:
                path = os.path.join(dirpath, filename)
                return path
    return None

def read_source_video_info():
    """
    From the source videos, read in video information
    Looking for things like: fps, duration, nframes
    FYI: This takes a little while, since reading the information from each file takes
        about a second
    return a list of dictionaries
    """
    source_video_dir = current_app.config['VIDEO_DIR']

    logging.info("reading video information")
    #get all the episodes from the source_dir
    episodes = collect_episodes(source_video_dir)

    #collect video information
    video_info = []
    for episode, source_path in episodes:
        logging.debug(f"reading video info: {episode}")
        clip = VideoFileClip(source_path)
        video_info.append((
            episode,
            clip.reader.fps,
            clip.reader.duration,
            clip.reader.nframes,
        ))
    return video_info

def write_video_meta_csv(video_info):
    """
    given video meta info read in from the original source video files
    write the video_info into csv
    """
    logging.info("writing video information")
    video_meta_path = current_app.config['VIDEO_META_PATH']
    with open(video_meta_path, 'w') as csvfile:
        fieldnames = ['episode', 'fps', 'duration', 'nframes']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for v in video_info:
            writer.writerow(list(v))

def read_video_meta_csv():
    """
    read the video information from the video meta file
    """
    video_meta_path = current_app.config['VIDEO_META_PATH']
    video_info = []
    with open(video_meta_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            video_info.append(row)
    return video_info

def extract_episode(ep, source_path, force_extract=False):
    output_dir= current_app.config['THUMBNAILS_DIR']
    width  = current_app.config['GIF_WIDTH']
    height = current_app.config['GIF_HEIGHT']

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

def make_small_thumbs(ep):
    logging.info('making small thumbs for: %s', ep)
    large_thumbs_dir = current_app.config['THUMBNAILS_DIR']
    small_thumbs_dir = current_app.config['SMALL_THUMBNAILS_DIR']
    width = current_app.config['SMALL_WIDTH']
    height = current_app.config['SMALL_HEIGHT']
    nthframe = current_app.config['NTH_FRAME']

    season = get_season(ep)
    orig_dir = os.path.join(large_thumbs_dir, season, ep)
    dest_dir = os.path.join(small_thumbs_dir, season, ep)
    os.makedirs(dest_dir, exist_ok=True)

    for infile in glob.glob(orig_dir + "/*.jpg"):
        basename = os.path.basename(infile)
        fname, ext = os.path.splitext(basename)
        frame = int(fname)
        if frame % nthframe != 0: continue
        dest_filepath = os.path.join(dest_dir, basename)
        #logging.debug(dest_filepath)
        with Image.open(infile) as im:
            im.thumbnail((width,height))
            im.save(dest_filepath)

@click.command('extract-all-thumbs')
@with_appcontext
def extract_all_thumbs_cmd():
    """extract all thumbnails. it will skip episodes already extracted"""
    click.echo('Extracting thumbs')
    source_dir= current_app.config['VIDEO_DIR']

    #get all the episodes from the source_dir
    episodes = collect_episodes(source_dir)

    #iterate over the episodes, extracting thumbnails from each of them
    for ep, source_path in episodes:
        extract_episode(ep, source_path)

    click.echo('Thumbnails extracted')

@click.command('make-small-thumbs')
@with_appcontext
def make_small_thumbs_cmd():
    """for resizing extracting thumbnails"""
    click.echo('resizing thumbs')

    #can come from db now?
    source_dir = current_app.config['VIDEO_DIR']

    #get all the episodes from the source_dir
    episodes = collect_episodes(source_dir)

    #iterate over the episodes, extracting thumbnails from each of them
    for ep, source_path in episodes:
        make_small_thumbs(ep)

    click.echo('Thumbnails resized')

@click.command('extract-season-thumbs')
@click.argument("season")  #ie S01
@with_appcontext
def extract_season_thumbs_cmd(season):
    """extract thumbnails for a given season. it will not skip episodes already extracted"""

    click.echo('Extracting thumbs')
    source_dir = current_app.config['VIDEO_DIR']

    #get all the episodes from the source_dir
    episodes = collect_episodes(source_dir)
    for ep, source_path in episodes:
        if get_season(ep) == season:
            extract_episode(ep, source_path)


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

@click.command('create-video-meta-csv')
@with_appcontext
def write_video_meta_csv_cmd():
    """create video_meta_csv"""
    click.echo('creating video info csv')
    write_video_meta_csv(read_source_video_info())

def init_app(app):
    app.cli.add_command(extract_all_thumbs_cmd)
    app.cli.add_command(extract_season_thumbs_cmd)
    app.cli.add_command(extract_ep_thumbs_cmd)
    app.cli.add_command(write_video_meta_csv_cmd)
    app.cli.add_command(make_small_thumbs_cmd)
