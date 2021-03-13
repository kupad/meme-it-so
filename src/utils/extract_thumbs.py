#!/usr/bin/python3 

import os
import argparse
import subprocess

from moviepy.editor import *
from PIL import Image


"""
--The following will extract every frame
ffmpeg -i input.mkv -s 480x356 -q:v 2 -frame_pts 1 %05d.jpg
"""
def ffmpeg_extract_thumbs(source_path,  dest_dir, dest_width, dest_height):
    """extract all thumbnails from a video using ffmpeg"""
    return subprocess.run(
            ['ffmpeg', 
                '-i', source_path, 
                '-s', f'{dest_width}x{dest_height}', 
                '-q:v', '2',
                '-frame_pts', '1', 
                os.path.join(dest_dir,'%05d.jpg')])

def moviepy_extract_thumbs(source_path,  dest_dir, dest_fps, dest_width):
    """uses moviepy to extract thumbnails. painfully slow compared to ffmpeg"""
    clip = VideoFileClip(source_path)
    
    if dest_width is not None:
        clip = clip.resize(width=dest_width)

    if dest_fps is None:
        dest_fps = clip.fps

    #we'll be extracting every nth frame
    nthframe = round(clip.fps / dest_fps)

    for i, frame in enumerate(clip.iter_frames()):
        if i % nthframe != 0: continue

        curr_ms = int((i / clip.fps) * 1000)
        if(i % round(clip.fps*10) == 0): 
            print(f"{source_path} -> {dest_dir} curr_ms: {curr_ms}")
        new_img = Image.fromarray(frame)
        new_img_filepath = os.path.join(dest_dir, f"{curr_ms:07}.jpg")
        new_img.save(new_img_filepath)

##########

#def example():
#    source_path = os.path.join(conf.INPUTS, 'S0503.Home_Goes_to_College.mkv')
#    thumbnail_dir = os.path.join(conf.OUTPUTS, 'thumbnails')
#    os.makedirs(thumbnail_dir, exist_ok=True)
#    make_thumbs(source_path, thumbnail_dir, conf.FPS)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path to source video file")
    parser.add_argument("dest", help="directory to store extracted thumbnails")
    parser.add_argument("--dest_fps", help="how many frames per second to extract")
    parser.add_argument("--dest_width", help="change width of thumbnails")
    args = parser.parse_args()
    
    moviepy_make_thumbs(source_path=args.source_video_path, 
                dest_dir=args.dest_dir, 
                dest_fps=args.dest_fps, 
                dest_width=args.dest_width)

if __name__ == "__main__":
    main()

