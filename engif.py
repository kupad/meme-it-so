#!/usr/bin/python3

import os
import argparse
import sys
from math import floor, ceil
#import time

import srt
from moviepy.editor import *
from PIL import Image

from conf import *
from utils.make_gif import make_gif
from utils.episode_utils import get_episode, get_season

DEF_FPS=23.976

def is_srt(filename):
    """is this an srt file? (well, does it claim to be?)"""
    return filename.endswith('.srt')

def find_ep_matches(ep, srtfilepath, lc_search_phrase):
    """
    find matches within a given file
    return list of (ep, Subtitle) pairs
    """
    with open(srtfilepath, 'r') as srtfile:
        subs = srt.parse(srtfile)
        matches = [ (ep, sub) for sub in subs if lc_search_phrase in sub.content.lower() ]
        return matches

def find_matches(query):
    """
    find all matching subtitle 'scenes'
    return list of (ep, Subtitle) pairs
    """
    lc_query = query.lower()

    #iterate through the srt_source_dir looking for srt files
    #parse the srt files and see if they contain the query
    #add all matching scenes to the list of matches. a tuple from (ep -> Subtitle)
    matches = []
    for dirpath, dirnames, filenames in os.walk(SERIES_DIR):
        for filename in filenames:
            #skip non-srt files 
            if not is_srt(filename): continue
            
            ep = get_episode(filename) #eg: S07E02

            #if the srt file does not contain episode information, skip it
            if ep is None: 
                print("warning: skipping because it does not contain match SsEe format", path)
                continue

            path = os.path.join(dirpath, filename)
            ep_matches = find_ep_matches(ep, path, lc_query)
            matches.extend(ep_matches)
    matches.sort()
    return matches

def td2frame(sub, fps=VIDEO_FPS):
    """
    given a 'sub' (a scene) return the start and end frames of the scene
    - thumbnails are stored by frame number, not time offset
    - srt files use time offsets
    - this function widens the scene by 2 seconds
    """
    start_frame = floor(floor(sub.start.total_seconds()-1) * fps)
    end_frame = ceil(ceil(sub.end.total_seconds()+1) * fps)
    return start_frame, end_frame

def scene2str(scene):
    ep, sub = scene
    content = sub.content.replace('\n','  ')
    return f"{ep} {sub.start} --> {sub.end}: {content}"

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

def scene2gif(match):
    ep, sub = match

    #find the start and end frames
    start_frame, end_frame = td2frame(sub)
    #print('sub.start', sub.start, 'start_frame', start_frame)
    #print('sub.end', sub.end, 'end_frame', end_frame)

    #get the dir that contains the thumbnails for this episode
    season = get_season(ep)
    ep_thumbs_dir = os.path.join(THUMBNAILS_DIR, season, ep) 

    output_filename= "found.gif" #TODO: uuid? hash? something better...

    make_gif(source_dir=ep_thumbs_dir,
            orig_fps=VIDEO_FPS,
            start_frame=start_frame,
            end_frame=end_frame,
            dest_fps=GIF_FPS,
            dest_dir=GIFS_DIR,
            dest_fname="found.gif")


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

