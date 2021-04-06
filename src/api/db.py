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

from .utils.eptools import read_episode_guide
from .utils.srttools import read_srt_csv
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


from moviepy.editor import VideoFileClip

from .utils.eptools import episode_from_filename, collect_episodes


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
    load_subs(read_srt_csv())
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
