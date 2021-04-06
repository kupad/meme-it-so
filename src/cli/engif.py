# This file is part of Meme It So
#
# "Meme It So" is a media (TV show and movies) screen capture and text caption
# database and image macro generator.
# Copyright (C) 2021  Phillip Dreizen
#
# Meme It So is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Meme It So is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#FIXME-- lots of changes since this was first written, and it's not being maintained

import os
import argparse
import sys

from conf import *
from utils.video_index import read_video_index
from utils.make_gif import make_gif
from utils.episode_utils import get_episode, get_season
from utils.subtitles import Scene, find_matches, ms2frame

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

def scene2gif(scene):
    ep = scene.ep

    video_info = read_video_index()
    orig_fps = video_info[ep]

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
