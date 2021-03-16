#!/usr/bin/python3

import os

import conf
import utils.video_index as video_index
from utils.episode_utils import get_season, collect_episodes
from utils.extract_thumbs import ffmpeg_extract_thumbs 

def was_extracted(ep, dest_dir, vindex):
    tolerance = 200 
    nframes = vindex[ep]['nframes']
    num_files = len([fname for fname in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, fname)) and fname.endswith('.jpg')])
    diff = abs(num_files - nframes)
    extracted = diff <= tolerance
    return extracted

def extract(source_dir, output_dir, width, height, force_extract=False):
    #get all the episodes from the source_dir
    episodes = collect_episodes(source_dir)
   
    #get video information
    vindex = video_index.read_index(conf.VIDEO_INDEX_PATH)

    #iterate over the episodes, extracting thumbnails from each of them
    for ep, source_path in episodes:
        season = get_season(ep)
        
        dest_dir = os.path.join(output_dir, season, ep)
        os.makedirs(dest_dir, exist_ok=True)

        extract = force_extract or not was_extracted(ep, dest_dir, vindex)

        if extract:
            print(f'extracting thumbnails for {ep} -> {dest_dir}')
            ffmpeg_extract_thumbs(source_path, dest_dir, width, height)
        else:
            print(f'skipping {ep}...was extracted')

def main():
    extract(source_dir = conf.SERIES_DIR,
            output_dir = conf.THUMBNAILS_DIR,
            width = conf.GIF_WIDTH,
            height = conf.GIF_HEIGHT)
   
if __name__ == "__main__":
    main()


