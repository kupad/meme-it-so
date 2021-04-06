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
functions for interacting with and creating the whoosh captions full text search index
"""

import os
import logging
import sqlite3

import click
from flask.cli import with_appcontext, current_app

import whoosh.index as index
from whoosh import qparser
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import *

from .. import db

def query(qstr):
    """
    query the caption index
    Return hits as a list of dicts.
    """
    caption_index_dir=current_app.config['CAPTION_INDEX_DIR']

    try:
        ix, q = _get_querier(qstr, caption_index_dir)
    except index.EmptyIndexError:
        logging.error("captions.query: Did you create the whoosh index?")
        raise index.EmptyIndexError

    scenes = None
    with ix.searcher() as s:
        results = s.search(q, limit=None)
        scenes = _make_dicts(results)
    return scenes

def query_page(qstr, page=1, pagelen=20):
    """
    query the caption index,
    paginate the results
    Returns:
        (hits as a list of dicts, page of results, total pagecount)
    """
    caption_index_dir=current_app.config['CAPTION_INDEX_DIR']

    try:
        ix, q = _get_querier(qstr, caption_index_dir)
    except index.EmptyIndexError:
        logging.error("captions.query: Did you create the whoosh index?")
        raise index.EmptyIndexError

    with ix.searcher() as s:
        results = s.search_page(q, page, pagelen=pagelen)
        scenes = _make_dicts(results)
        return scenes, results.pagenum, results.pagecount

def _get_querier(qstr, caption_index_dir):
    ix = index.open_dir(caption_index_dir)

    qp = qparser.QueryParser("content", schema=ix.schema)
    q = qp.parse(qstr)
    return ix, q

def _make_dicts(results):
    dicts = []
    for hit in results:
        dicts.append({
            'id': int(hit['dbid']),
            'episode': hit['episode'],
            'srtidx': int(hit['srtidx'])})
    return dicts

###############################
#####  cli commands
###############################

def init_app(app):
    """register the cli commands with app in __init__py"""
    app.cli.add_command(init_caption_index_command)

@click.command('init-fts-idx')
@with_appcontext
def init_caption_index_command():
    """creates whoosh full text search index for captions"""
    caption_index_dir=current_app.config['CAPTION_INDEX_DIR']

    click.echo('creating fts caption index. this will take a few moments.')

    ##create schema
    #we store the ids, but not the text we're indexing. querying will involve
    #looking rows by id in the db
    schema = Schema(dbid=ID(stored=True),
                    episode=ID(stored=True),
                    srtidx=ID(stored=True),
                    content=TEXT(stored=False, analyzer=StandardAnalyzer(minsize=1)))

    #create the index dir if it doesn't exist
    if not os.path.exists(caption_index_dir):
        os.makedirs(caption_index_dir, exist_ok=True)

    #create the index. this will delete a previous exiting one
    ix = index.create_in(caption_index_dir, schema)

    #get all caption rows from the database and add them to the index
    writer = ix.writer()
    cur = db.get_db().cursor()
    rows = cur.execute("""SELECT * FROM captions""")
    for row in rows:
        writer.add_document(dbid=str(row['id']),
                            episode=row['episode'],
                            srtidx=str(row['srtidx']),
                            content=row['content'])
    writer.commit()

    click.echo('caption index created')
