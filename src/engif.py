#!/usr/bin/python3

import os
import argparse
import sys
import csv
#import time
from math import floor, ceil

import srt
from moviepy.editor import *
from PIL import Image

from conf import *
import utils.video_index as video_index
from utils.make_gif import make_gif
from utils.episode_utils import get_episode, get_season

#TODO: decompose the functions in engif and move into utils. Flask and engif need to use the same things

#FIXME: quickly made this a dict so that it will serialize in flask, but it can't stay this way!
class Scene(dict):
    """initialize a scene from a row in the subtitle csv file"""
    CONTENT_IDX = 4
    #csvrow: 'episode','srtidx','start(ms)','end(ms)','content'
    def __init__(self, csvrow):
        self.ep = csvrow[0]
        self.srtidx = int(csvrow[1])
        self.start = int(csvrow[2])
        self.end = int(csvrow[3])
        self.content = csvrow[4]
        dict.__init__(self, ep=self.ep, srtidx=self.srtidx, start=self.start, end=self.end, content=self.content)


def find_matches(query):
    """
    find all matching subtitle 'scenes'
    return list of (ep, Scene) pairs
    """
    lc_query = query.lower()

    #TODO: check for existance of the csv file

    #open the csv subtitle database and find all matching scenes
    matches = []
    with open(SUBTITLES_CSV_PATH, 'r') as subcsv:
        csvreader = csv.reader(subcsv)
        csvreader.__next__() #toss header
        matches = [ Scene(row) for row in csvreader if lc_query in row[Scene.CONTENT_IDX].lower() ]
        #sort by episode
        matches.sort(key=lambda scene: scene.ep)
    return matches

def ms2frame(scene, fps):
    """
    given a 'scene' return the start and end frames of the scene
    - thumbnails are stored by frame number, not time offset
    - srt files use time offsets
    - this function widens the scene by 2 seconds
    """
    start_frame = floor( (scene.start / 1000 - 1) * fps)
    end_frame =  ceil( (scene.end / 1000 + 1) * fps)
    return start_frame, end_frame

def scene2str(scene):
    content = scene.content.replace('\n','  ')
    return f"{scene.ep} {scene.start} --> {scene.end}: {content}"

def user_select(matches):
    """
    given a list of scenes that matched the query,
    prompt the user to select one
    """
    for i,scene in enumerate(matches):
        print(f"{i}) {scene2str(scene)}")
    selection = int(input("select: "))
    #TODO: make sure selection is valid
    return matches[selection]

def get_fps(ep):
    vindex = video_index.read_index(VIDEO_INDEX_PATH)
    return vindex[ep]['fps']

def scene2gif(scene):
    ep = scene.ep

    orig_fps = get_fps(ep)

    #find the start and end frames
    start_frame, end_frame = ms2frame(scene, orig_fps)
    #print('sub.start', sub.start, 'start_frame', start_frame)
    #print('sub.end', sub.end, 'end_frame', end_frame)

    #get the dir that contains the thumbnails for this episode
    season = get_season(ep)
    ep_thumbs_dir = os.path.join(THUMBNAILS_DIR, season, ep)

    gif_filename= f'{ep}.{scene.srtidx}.gif'

    make_gif(source_dir=ep_thumbs_dir,
            orig_fps=25,
            start_frame=start_frame,
            end_frame=end_frame,
            dest_fps=GIF_FPS,
            dest_dir=GIFS_DIR,
            dest_fname=gif_filename)

def query2gif(query):
    """
    given a query generate a gif
    returns True/False found match
    """

    #find all scenes that match the search term
    #print("start find_matches()")
    #tic = time.perf_counter()
    matches = find_matches(query)
    #toc = time.perf_counter()
    #print(f"find_matches() in {toc - tic:0.4f} seconds")

    #if no matches found, return now
    if len(matches) == 0:
        print("no match found")
        return False

    #we want exactly 1 match to turn into a gif
    #if we found more than 1 match, the user is prompted to select one
    if len(matches) == 1:
        match = matches[0]
        print('Found: ', scene2str(match))
    else:
        match = user_select(matches)
    #match = matches[0] if len(matches) == 1 else user_select(matches)

    #turn the matching scene into a gif
    scene2gif(match)
    return True


def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("source_thumbnail_dir", help="path to thumbnails with ms offset in filename")
    #parser.add_argument("source_srt", help="srt file")
    parser.add_argument("search", help="search for phrase")
    args = parser.parse_args()

    found_match = query2gif(args.search)
    sys.exit(0 if found_match else 1)

if __name__ == "__main__":
    main()
