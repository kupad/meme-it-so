import os
import csv
from conf import CAPTION_INDEX_DIR, SUBTITLES_CSV_PATH
import whoosh.index as index
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import *

#TODO: should the index store everything?
#or should I get back the ids (episode/srtidx) and then look it up
#in a dictionary
schema = Schema(episode=ID(stored=True),
                srtidx=ID(stored=True),
                start=ID(stored=True),
                end=ID(stored=True),
                content=TEXT(stored=True, analyzer=StandardAnalyzer(minsize=1)))

if not os.path.exists(CAPTION_INDEX_DIR):
    os.makedirs(CAPTION_INDEX_DIR, exist_ok=True)

ix = index.create_in(CAPTION_INDEX_DIR, schema)
writer = ix.writer()

#csvrow: 'episode','srtidx','start(ms)','end(ms)','content'
with open(SUBTITLES_CSV_PATH, 'r') as subcsv:
    csvreader = csv.reader(subcsv)
    csvreader.__next__() #toss header
    for row in csvreader:
        writer.add_document(episode=row[0],
                            srtidx=row[1],
                            start=row[2],
                            end=row[3],
                            content=row[4])
writer.commit()
