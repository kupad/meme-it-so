"""
functions for interacting with and creating the whoosh captions full text search index
"""

import os
import sqlite3

import click
from flask.cli import with_appcontext

import whoosh.index as index
from whoosh import qparser
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import *

from .. import db
from conf import CAPTION_INDEX_DIR

def query(qstr, caption_index_dir=CAPTION_INDEX_DIR):
    """
    query the caption index
    Return hits as a list of dicts.
    """
    ix = index.open_dir(caption_index_dir)

    #the OrGroup means search terms are combined with OR instead of AND
    #the factory 0.9, means that documents that contain more words they search
    #for scores higher (as opposed to, say, a single term showing up multiple times)
    #see: https://whoosh.readthedocs.io/en/latest/parsing.html#common-customizations
    #og = qparser.OrGroup.factory(0.9)
    #qp = qparser.QueryParser("content", schema=ix.schema, group=og)
    qp = qparser.QueryParser("content", schema=ix.schema)
    q = qp.parse(qstr)

    scenes = []
    with ix.searcher() as s:
        results = s.search(q, limit=None)
        for hit in results:
            scenes.append({
                'id': int(hit['dbid']),
                'episode': hit['episode'],
                'srtidx': int(hit['srtidx'])})
    return scenes

###############################
#####  cli commands
###############################

def hi():
    print('hi!')

def init_app(app):
    """register the cli commands with app in __init__py"""
    app.cli.add_command(init_caption_index_command)

@click.command('init-fts-idx')
@with_appcontext
def init_caption_index_command():
    """creates whoosh full text search index for captions"""
    click.echo('creating fts caption index. this will take a few moments.')

    ##create schema
    #we store the ids, but not the text we're indexing. querying will involve
    #looking rows by id in the db
    schema = Schema(dbid=ID(stored=True),
                    episode=ID(stored=True),
                    srtidx=ID(stored=True),
                    content=TEXT(stored=False, analyzer=StandardAnalyzer(minsize=1)))

    #create the index dir if it doesn't exist
    if not os.path.exists(CAPTION_INDEX_DIR):
        os.makedirs(CAPTION_INDEX_DIR, exist_ok=True)

    #create the index. this will delete a previous exiting one
    ix = index.create_in(CAPTION_INDEX_DIR, schema)

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
