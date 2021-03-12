#!/usr/bin/python3

import os
import argparse

from moviepy.editor import *
from PIL import Image

import conf

def imgs(source_dir):
    """
    given a directory of imgs with format '{ms}.jpg', 
    return image paths as tuples of (ms,path)
    """
    paths = []
    for root,dirs, files in os.walk(source_dir):
        for fname in files:
            filepath = os.path.join(root,fname)
            try:
                ms = int(fname.replace(".jpg",""))
                paths.append( (ms, filepath))
            except:
                key = None


    paths.sort(key=lambda e: e[0])
    return paths

def make_gif(source_dir, start, duration, dest_fname, dest_dir, fps):
    """
    source_dir: contains all the thumbnails
    start: start offset in ms
    duration: number of ms from the start
    dest_fname: name the destination gif
    dest_dir: name of the destination directory
    fps: frames per second of gif
    """

    #the end offset in the episode, in ms
    end = start + duration
   
    #get (offset_ms, path_to_img) tuples
    path_tups = imgs(source_dir)

    #find the start and end indexes in path_tups...
    #   start_idx: last element that is <= to start
    #   end_idx: first element that is >= to end
    #note: using linear search, can be sped up with binary search (see the C++ lower_bounds)
    start_idx = 0
    end_idx = 0
    for idx, (ms,path) in enumerate(path_tups):
        if ms <= start:
            start_idx = idx 
        if ms >= end:
            end_idx = idx
            break
    
    #print('start_idx', start_idx)
    #print('end_idx', end_idx)

    paths = [t[1] for t in path_tups[start_idx:end_idx]] #just the paths of the images we care about

    #create a clip from the relevant images and write them out
    print('nframes',len(paths))
    print(paths)
    clip = ImageSequenceClip( paths, fps=fps)
    output_path = os.path.join(dest_dir,dest_fname)
    #clip.write_gif(output_path, fps=fps, program='ffmpeg')
    clip.write_gif(output_path, fps=fps)


def example():
    THUMBNAILS = os.path.join(conf.OUTPUTS, 'thumbnails')
    os.makedirs(THUMBNAILS, exist_ok=True)
    GIFS = os.path.join(conf.OUTPUTS, "gifs")
    os.makedirs(GIFS, exist_ok=True)

    start = (8*60 + 24)*1000
    make_gif(THUMBNAILS, start, 9000, 'smrt.gif', GIFS, 6)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_thumbnail_dir", help="path to thumbnails with ms offset in filename")
    parser.add_argument("start", help="start time in ms")
    parser.add_argument("duration", help="duration in ms")
    parser.add_argument("fname", help="filename of target gif")
    parser.add_argument("dest_dir", help="directory")
    parser.add_argument("fps", help="fps")
    args = parser.parse_args()

    start = int(args.start)
    duration = int(args.duration)
    fps = int(args.duration)

    make_gif(args.source_thumbnail_dir, start, duration, args.fname, args.dest_dir, fps)

if __name__ == "__main__":
    main()

