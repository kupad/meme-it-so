#!/usr/bin/python3

import os
import argparse
import sys

import srt
from moviepy.editor import *
from PIL import Image

import conf
from make_gif import make_gif


def find_matches(srtfilepath, search_term):
    with open(srtfilepath, 'r') as srtfile:
        subs = srt.parse(srtfile)
        matches = [ sub for sub in subs if search_term in sub.content ]
        return matches
        
def td2ms(td):
    return int(td.total_seconds()*1000)

def choose(matches):
    for i,sub in enumerate(matches):
        print(f"{i}: {sub.content}")
    selection = int(input("select: "))
    return matches[selection]

def make_it_so(thumbnails, srtfile, search_term):
    matches = find_matches(srtfile, search_term)
    if len(matches) > 1:
        match = choose(matches)
    elif len(matches) == 1:
        match = matches[0]
    else:
        print("no match found")
        return

    start = td2ms(match.start)
    end = td2ms(match.end)
    duration = end - start
    make_gif(thumbnails, start, duration, "found.gif", 'data/outputs/gifs', 6)
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_thumbnail_dir", help="path to thumbnails with ms offset in filename")
    parser.add_argument("source_srt", help="srt file")
    parser.add_argument("search", help="search for phrase")
    args = parser.parse_args()

    ev = make_it_so(args.source_thumbnail_dir, args.source_srt, args.search)
    sys.exit(ev)

if __name__ == "__main__":
    main()

