#!/usr/bin/python3

import os
import sys
import argparse

from conf import *
from utils.episode_utils import get_episode, get_season
from utils.extract_thumbs import ffmpeg_extract_thumbs 

#FIXME: actually examine the file?
def is_video(filename):
    return filename.endswith('mkv') or filename.endswith('avi') or filename.endswith('mp4')

def find_video(episode):
    """
    given an episode (SsEe), find the path to the video file
    """
    for dirpath, dirnames, filenames in os.walk(SERIES_DIR):
        for filename in filenames:
            if not is_video(filename): continue

            cand_ep = get_episode(filename)
            if episode == cand_ep:
                path = os.path.join(dirpath, filename)
                return path
    return ""

def extract(episode):
    #find path to video for this episode
    source_path = find_video(episode)

    #bail if we didn't find anything
    if source_path == "":
        print(f'video for episode {episode} not found')
        return False

    #get the output directory
    season = get_season(episode)
    dest_dir = os.path.join(THUMBNAILS_DIR, season, episode)
    os.makedirs(dest_dir, exist_ok=True)

    print(f'extracting thumbnails for {episode} -> {dest_dir}')
    ffmpeg_extract_thumbs(source_path, dest_dir, GIF_WIDTH, GIF_HEIGHT)

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("episode", help="S{season}xE{episode} ie: S0401")
    args = parser.parse_args()

    rv = extract(args.episode)
    sys.exit(0 if rv else 1)

if __name__ == "__main__":
    main()

