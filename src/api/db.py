"""
db utilities
This links dbs with the g object, making it convenient to work with the db from
our views.
The code is taken from examples in the flask documentation
"""

import sqlite3

import click
from flask import g, current_app
from flask.cli import with_appcontext

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

from conf import SOURCE_SRT_DIR, SERIES_DIR, EPISODE_GUIDE_PATH, DATABASE_PATH
from .utils.eptools import episode_from_filename, collect_episodes

def td2ms(td):
    return int(td.total_seconds()*1000)

def is_srt(filename):
    """is this an srt file? (well, does it claim to be?)"""
    return filename.endswith('.srt')

def read_srt(srt_dir=SOURCE_SRT_DIR):
    """
    Search through the srt_dir to find all srt files.
    Parse each file, and return as a list of tuples, sorted asc by episoe-srtidx
    """
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

def read_video_info(source_video_dir=SERIES_DIR):
    """
    From the source videos, read in video information
    Looking for things like: fps, duration, nframes
    FYI: This takes a little while, since reading the information from each file takes
        about a second
    return a list of dictionaries
    """
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

#http://epguides.com/StarTrekTheNextGeneration/
#http://epguides.com/common/exportToCSVmaze.asp?maze=491
#number,season,episode,airdate,title,tvmaze link
def read_episode_guide(episode_guide_path=EPISODE_GUIDE_PATH):
    """
    read the entire episode guide into memory
    episode guide has info like: title, airdate
    """
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
    load_video_info(read_video_info())
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
