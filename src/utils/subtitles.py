"""
TODO: remove! replace with captions index
utilies for working with already prepared subtitle information
"""

import csv
from math import floor, ceil

import conf

#FIXME: quickly made this a dict so that it will serialize in flask, but it can't stay this way!
class Scene(dict):
    """initialize a scene from a row in the subtitle csv file"""
    EP_IDX = 0
    SRT_IDX = 1
    START_IDX = 2
    END_IDX = 3
    CONTENT_IDX = 4
    #csvrow: 'episode','srtidx','start(ms)','end(ms)','content'
    def __init__(self, csvrow):
        self.ep = csvrow[0]
        self.srtidx = int(csvrow[1])
        self.start = int(csvrow[2])
        self.end = int(csvrow[3])
        self.content = csvrow[4]
        dict.__init__(self, ep=self.ep, srtidx=self.srtidx, start=self.start, end=self.end, content=self.content)

def find_by_time(ep, ms, subtitles_csv_path=conf.SUBTITLES_CSV_PATH):
    """
    find matching scene by ep and ms offset
    """
    match = None
    with open(subtitles_csv_path, 'r') as subcsv:
        csvreader = csv.reader(subcsv)
        csvreader.__next__() #toss header
        for row in csvreader:
            scene = Scene(row)
            if 'opensubtitles' in scene.content.lower(): continue
            if ep == scene.ep and (ms >= scene.start and ms <= scene.end):
                match = scene
                break
    return match

def find_matches(query, subtitles_csv_path=conf.SUBTITLES_CSV_PATH):
    """
    find all matching subtitle 'scenes'
    return list of (ep, Scene) pairs
    """
    lc_query = query.lower()

    #TODO: check for existance of the csv file

    #open the csv subtitle database and find all matching scenes
    matches = []
    with open(subtitles_csv_path, 'r') as subcsv:
        csvreader = csv.reader(subcsv)
        csvreader.__next__() #toss header
        matches = [ Scene(row) for row in csvreader if lc_query in row[Scene.CONTENT_IDX].lower() ]
        #sort by episode
        matches.sort(key=lambda scene: scene.ep)
    return matches

#TODO: rename
def ms2frame(scene, fps):
    """
    given a 'scene' return the start and end frames of the scene
    - thumbnails are stored by frame number, not time offset
    - srt files use time offsets
    #- this function widens the scene by 1 seconds
    """
    start_frame = floor( (scene['start'] / 1000) * fps)
    end_frame =  ceil( (scene['end'] / 1000 + 1) * fps)
    return start_frame, end_frame

def scene2str(scene):
    content = scene.content.replace('\n','  ')
    return f"{scene.ep} {scene.start} --> {scene.end}: {content}"
