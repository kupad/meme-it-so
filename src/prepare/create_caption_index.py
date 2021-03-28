import os
import sqlite3

import whoosh.index as index
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import *

from conf import CAPTION_INDEX_DIR, DATABASE_PATH

#fixme: from flask's db.py
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def main():
    schema = Schema(dbid=ID(stored=True),
                    episode=ID(stored=True),
                    srtidx=ID(stored=True),
                    content=TEXT(stored=False, analyzer=StandardAnalyzer(minsize=1)))

    if not os.path.exists(CAPTION_INDEX_DIR):
        os.makedirs(CAPTION_INDEX_DIR, exist_ok=True)

    ix = index.create_in(CAPTION_INDEX_DIR, schema)
    writer = ix.writer()

    con = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = make_dicts
    cur = con.cursor()
    rows = cur.execute("""SELECT * FROM captions""")
    for row in rows:
        writer.add_document(dbid=str(row['id']),
                            episode=row['episode'],
                            srtidx=str(row['srtidx']),
                            content=row['content'])
    writer.commit()
    con.close()

if __name__ == "__main__":
    main()
