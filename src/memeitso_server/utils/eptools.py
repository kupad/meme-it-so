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

import os
import re
import csv
import logging

from flask import current_app

#episode guide: csv that contains information about episode (like title, airdate).
#this is different than video information (duration, fps...)
#http://epguides.com/StarTrekTheNextGeneration/
#http://epguides.com/common/exportToCSVmaze.asp?maze=491
#number,season,episode,airdate,title,tvmaze link
def read_episode_guide():
    """
    read the entire episode guide into memory
    episode guide has info like: title, airdate
    """
    episode_guide_path=current_app.config['EPISODE_GUIDE_PATH']

    logging.info("reading episode_guide into memory")
    episode_guide = []
    with open(episode_guide_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            season_num  = int(row['season'])
            episode_num = int(row['episode'])
            episode = f'S{season_num:02}E{episode_num:02}'
            episode_guide.append((episode, season_num, episode_num, row['title'], row['airdate']))
    return episode_guide

def episode_from_filename(filename):
    """video and srt files are expected to contain a S{number}E{number} like S07E02"""
    m = re.search('S([0-9]+)E([0-9]+)', filename) #eg: S07E02
    return m.group(0) if m is not None else None

#repeated in vidtools. FIXME. watchout for circular import
def is_video(filename):
    """checks if file is a video file"""
    return filename.endswith('mkv') or filename.endswith('avi') or filename.endswith('mp4')

def collect_episodes(source_dir):
    """
    Get all the episodes in the source_dir.
    Files are recognized as episodes if they contain an "episode descriptor" which looks like: S07E02,
    which means "Season 7, Episode 2.
    Returns a list of tuples. First element is the episode descriptor, second is the path to the file
    """
    #collect the paths to every file
    episodes = []
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            if not is_video(filename): continue

            path = os.path.join(dirpath, filename)
            ep = episode_from_filename(filename) #eg: S07E02
            if ep is None:
                print("warning: skipping because it does not contain match SsEe format", path)
                continue
            episodes.append( (ep, path))
    episodes.sort()
    return episodes

def get_season(epdescr_str):
    """given a string that contains S07E02 extract the season portion: S07"""
    m = re.search('S([0-9]+)', epdescr_str)
    return m.group(0) if m is not None else None
