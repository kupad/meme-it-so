#!/usr/bin/python3

import os
import argparse

from moviepy.editor import *
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path to source video file")
    args = parser.parse_args()


    clip = VideoFileClip(args.source)
    nframes = clip.reader.nframes
    duration = clip.reader.duration
    fps = clip.reader.fps
    print('nframes', nframes)
    print('duration', duration)
    print('fps', fps)
    print('duration*fps', duration*fps)

if __name__ == "__main__":
    main()

