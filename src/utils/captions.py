"""
querying the caption database
"""

import os

import whoosh.index as index
from whoosh import qparser

from conf import CAPTION_INDEX_DIR


def query(qstr, caption_index_dir=CAPTION_INDEX_DIR):
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
                'ep': hit['episode'],
                'srtidx': int(hit['srtidx']),
                'start': int(hit['start']),
                'end': int(hit['end']),
                'content': hit['content']})
    return scenes
