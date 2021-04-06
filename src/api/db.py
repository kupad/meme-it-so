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

# db utilities
# This links dbs with the g object, making it convenient to work with the db from
# our views.
# The code is taken from examples in the flask documentation

import sqlite3

import click
from flask import g, current_app
from flask.cli import with_appcontext

from .utils.vidtools import read_video_meta_csv

def make_dicts(cursor, row):
    """convert rows to dictionary"""
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        #g.db.row_factory = sqlite3.Row #alternative to dicts will make namedtuples
        g.db.row_factory = make_dicts

    return g.db

def query_db(query, args=(), one=False):
    """
    convenience function to run a query and get results in one go
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


############################################
##### db cli
############################################

import os
import csv
import logging

import srt
from moviepy.editor import VideoFileClip

from .utils.eptools import episode_from_filename, collect_episodes

def td2ms(td):
    return int(td.total_seconds()*1000)

def is_srt(filename):
    """is this an srt file? (well, does it claim to be?)"""
    return filename.endswith('.srt')

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

def load_subs(allsubs):
    """load subtitles into database"""
    #logging.debug(allsubs)
    logging.info("loading subtitles into db")
    con = get_db()
    cur = con.cursor()
    cur.executemany("INSERT INTO captions (episode, srtidx, start_offset, end_offset, content) VALUES (?,?,?,?,?)", allsubs)
    con.commit()

def load_video_info(video_info):
    """load video info database"""
    logging.info("loading video_info into db")
    con = get_db()
    cur = con.cursor()
    cur.executemany("INSERT INTO video_info (episode, fps, duration, nframes) VALUES (?,?,?,?)", video_info)
    con.commit()

def load_episode_guide(episode_guide):
    """load video info database"""
    logging.info("loading episode_guide into db")
    con = get_db()
    cur = con.cursor()
    cur.executemany("INSERT INTO episode_guide (episode, season, episode_num, title, airdate) VALUES (?,?,?,?,?)", episode_guide)
    con.commit()

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def load_db():
    """Clear existing data and create new tables."""
    logging.basicConfig(level=logging.DEBUG)
    load_subs(read_srt())
    load_video_info(read_video_meta_csv())
    load_episode_guide(read_episode_guide())

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """create tables and load data into database"""
    click.echo('Clearing database and recreating tables')
    init_db()
    click.echo('Initialized the database.')
    click.echo('Loading data into database.')
    load_db()
    click.echo('Data loaded into database.')
