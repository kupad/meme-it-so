#!/usr/bin/python3

import os

import conf
from utils.episode_utils import get_season, collect_episodes
from utils.extract_thumbs import ffmpeg_extract_thumbs 

def extract(source_dir, output_dir, width, height):
    #get all the episodes from the source_dir
    episodes = collect_episodes(source_dir)

    #iterate over the episodes, extracting thumbnails from each of them
    for ep, source_path in episodes:
        season = get_season(ep)
        
        dest_dir = os.path.join(output_dir, season, ep)
        os.makedirs(dest_dir, exist_ok=True)
        
        num_files = len([fname for fname in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, fname)) and fname.endswith('.jpg')])
        if num_files == 0:
            print(f'extracting thumbnails for {ep} -> {dest_dir}')
            ffmpeg_extract_thumbs(source_path, dest_dir, width, height)

def main():
    extract(source_dir = conf.SERIES_DIR,
            output_dir = conf.THUMBNAILS_DIR,
            width = conf.GIF_WIDTH,
            height = conf.GIF_HEIGHT)
   
if __name__ == "__main__":
    main()


