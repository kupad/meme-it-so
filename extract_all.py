#!/usr/bin/python3

import os

import conf
from utils.episode_utils import get_episode, get_season
from utils.extract_thumbs import ffmpeg_extract_thumbs 

def get_episodes(source_dir):
    """
    Get all the episodes in the source_dir.
    Files are recognized as episodes if they contain an "episode descriptor" which looks like: S07E02,
    which means "Season 7, Episode 2.
    Returns a list of tuples. First element is the episode descriptor, second is the path to the file
    """
    #collect the paths to every file
    episodes = []
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            ep = get_episode(filename) #eg: S07E02
            if ep is None: 
                print("warning: skipping because it does not contain match SsEe format", path)
                continue
            episodes.append( (ep, path))
    episodes.sort()
    return episodes

def extract(source_dir, output_dir, width, height):
    #get all the episodes from the source_dir
    episodes = get_episodes(source_dir)

    #iterate over the exercises, extracting thumbnails from each of them
    for ep, source_path in episodes:
        season = get_season(ep)
        dest_dir = os.path.join(output_dir, season, ep)
        os.makedirs(dest_dir, exist_ok=True)
        print(f'extracting thumbnails for {ep} -> {dest_dir}')
        ffmpeg_extract_thumbs(source_path, dest_dir, width, height)

def main():
    extract(source_dir = conf.SERIES_DIR,
            output_dir = conf.THUMBNAILS_DIR,
            width = conf.GIF_WIDTH,
            height = conf.GIF_HEIGHT)
   
if __name__ == "__main__":
    main()


