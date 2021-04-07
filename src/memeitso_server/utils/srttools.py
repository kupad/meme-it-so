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
Tools for manipulating srt:
    -- read through srts, create a single csv file
"""

import os
import csv
import logging
import srt

import click
from flask.cli import with_appcontext, current_app

from .eptools import get_season, episode_from_filename, collect_episodes

def is_srt(filename):
    """is this an srt file? (well, does it claim to be?)"""
    return filename.endswith('.srt')

def td2ms(td):
    """timedelta to ms"""
    return int(td.total_seconds()*1000)

def read_srt():
    """
    Search through the srt_dir to find all srt files.
    Parse each file, and return as a list of tuples, sorted asc by episoe-srtidx
    """
    srt_dir = current_app.config['SRT_DIR']

    logging.info("reading srt data")
    #first read in all the subtitles
    allsubs = []
    for dirpath, dirnames, filenames in os.walk(srt_dir):
        for filename in filenames:

            #skip non-srt files
            if not is_srt(filename): continue

            ep = episode_from_filename(filename) #eg: S07E02

            #skip if the srt file does not contain episode information
            if ep is None:
                print("warning: skipping because it does not contain match SsEe format", path)
                continue

            path = os.path.join(dirpath, filename)

            with open(path, 'r') as srtfile:
                subs = srt.parse(srtfile)
                for sub in subs:
                    if 'opensubtitles' in sub.content.lower(): continue
                    if ('VPN' in sub.content) or ('iSubDB' in sub.content): continue
                    if 'VPN' in sub.content: continue
                    allsubs.append( (ep, int(sub.index), td2ms(sub.start), td2ms(sub.end), sub.content))
    allsubs.sort(key=lambda s: (s[0],s[1]))
    return allsubs

def write_srt_csv(allsubs):
    """
    given all srt data
    write the srt data into csv
    """
    logging.info("writing srt csv")
    srt_csv_path = current_app.config['SRT_CSV_PATH']
    with open(srt_csv_path, 'w') as csvfile:
        fieldnames = ['episode', 'srtidx', 'start_offset(ms)', 'end_offset(ms)', 'content']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for s in allsubs:
            writer.writerow(list(s))

def read_srt_csv():
    """
    read subtiles csv file and return allsubs
    """
    logging.info("reading csv")
    srt_csv_path = current_app.config['SRT_CSV_PATH']
    allsubs = []
    with open(srt_csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            allsubs.append(row)
    return allsubs

def init_app(app):
    app.cli.add_command(write_srt_csv_cmd)

@click.command('create-srt-csv')
@with_appcontext
def write_srt_csv_cmd():
    """create srt csv"""
    click.echo('creating srt csv')
    write_srt_csv(read_srt())
