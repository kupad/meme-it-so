"""
load all data into the sqlite db

NOTE: loading the video_info will take a few moments
"""

import os
import csv
import sqlite3
import logging

import srt
from moviepy.editor import VideoFileClip

from conf import SOURCE_SRT_DIR, SERIES_DIR, EPISODE_GUIDE_PATH, DATABASE_PATH
from utils.episode_utils import get_episode, get_season

import conf
from utils.episode_utils import collect_episodes

def get_connection():
    con = sqlite3.connect(DATABASE_PATH)
    return con

def td2ms(td):
    return int(td.total_seconds()*1000)

def is_srt(filename):
    """is this an srt file? (well, does it claim to be?)"""
    return filename.endswith('.srt')

def read_srt(srt_dir=SOURCE_SRT_DIR):
    """
    Search through the srt_dir to find all srt files.
    Parse each file, and return as a list of tuples, sorted asc by episoe-srtidx
    """
    logging.info("reading srt data")
    #first read in all the subtitles
    allsubs = []
    for dirpath, dirnames, filenames in os.walk(srt_dir):
        for filename in filenames:

            #skip non-srt files
            if not is_srt(filename): continue

            ep = get_episode(filename) #eg: S07E02

            #skip if the srt file does not contain episode information
            if ep is None:
                print("warning: skipping because it does not contain match SsEe format", path)
                continue

            path = os.path.join(dirpath, filename)

            with open(path, 'r') as srtfile:
                subs = srt.parse(srtfile)
                for sub in subs:
                    if 'opensubtitles' in sub.content.lower(): continue
                    if ('VPN' in sub.content) or ('iSubDB' in sub.content): continue
                    if 'VPN' in sub.content: continue
                    allsubs.append( (ep, int(sub.index), td2ms(sub.start), td2ms(sub.end), sub.content))
    allsubs.sort(key=lambda s: (s[0],s[1]))
    return allsubs

def read_video_info(source_video_dir=SERIES_DIR):
    """
    From the source videos, read in video information
    Looking for things like: fps, duration, nframes
    FYI: This takes a little while, since reading the information from each file takes
        about a second
    return a list of dictionaries
    """
    logging.info("reading video information")
    #get all the episodes from the source_dir
    episodes = collect_episodes(source_video_dir)

    #collect video information
    video_info = []
    for episode, source_path in episodes:
        logging.debug(f"reading video info: {episode}")
        clip = VideoFileClip(source_path)
        video_info.append((
            episode,
            clip.reader.fps,
            clip.reader.duration,
            clip.reader.nframes,
        ))
    return video_info

#http://epguides.com/StarTrekTheNextGeneration/
#http://epguides.com/common/exportToCSVmaze.asp?maze=491
#number,season,episode,airdate,title,tvmaze link
def read_episode_guide(episode_guide_path=EPISODE_GUIDE_PATH):
    """
    read the entire episode guide into memory
    episode guide has info like: title, airdate
    """
    logging.info("reading episode_guide into memory")
    episode_guide = []
    with open(episode_guide_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            season_num  = int(row['season'])
            episode_num = int(row['episode'])
            episode = f'S{season_num:02}E{episode_num:02}'
            episode_guide.append((episode, season_num, episode_num, row['title'], row['airdate']))
    return episode_guide

def load_subs(allsubs):
    """load subtitles into database"""
    #logging.debug(allsubs)
    logging.info("loading subtitles into db")
    con = get_connection()
    cur = con.cursor()
    con.executemany("INSERT INTO captions (episode, srtidx, start_offset, end_offset, content) VALUES (?,?,?,?,?)", allsubs)
    con.commit()
    con.close()

def load_video_info(video_info):
    """load video info database"""
    logging.info("loading video_info into db")
    con = get_connection()
    cur = con.cursor()
    con.executemany("INSERT INTO video_info (episode, fps, duration, nframes) VALUES (?,?,?,?)", video_info)
    con.commit()
    con.close()

def load_episode_guide(episode_guide):
    """load video info database"""
    logging.info("loading episode_guide into db")
    con = get_connection()
    cur = con.cursor()
    con.executemany("INSERT INTO episode_guide (episode, season, episode_num, title, airdate) VALUES (?,?,?,?,?)", episode_guide)
    con.commit()
    con.close()

#TODO: move this to a schema file
def create_schema():
    """creates the schema. probably should move into a schema.sql file"""
    logging.info("creating schema")
    con = get_connection()
    cur = con.cursor()

    #captions table
    cur.execute('''DROP TABLE IF EXISTS captions''')
    cur.execute('''CREATE TABLE captions
        (id INTEGER PRIMARY KEY AUTOINCREMENT, episode TEXT, srtidx INTEGER, start_offset INTEGER, end_offset INTEGER, content TEXT)''')

    #video_info table
    cur.execute('''DROP TABLE IF EXISTS video_info''')
    cur.execute('''CREATE TABLE video_info
        (id INTEGER PRIMARY KEY AUTOINCREMENT, episode TEXT, fps REAL, duration REAL, nframes INTEGER)''')

    #episode_guide table
    cur.execute('''DROP TABLE IF EXISTS episode_guide''')
    cur.execute('''CREATE TABLE episode_guide
        (id INTEGER PRIMARY KEY AUTOINCREMENT, episode TEXT, season INTEGER, episode_num INTEGER, title TEXT, airdate TEXT)''')

    con.commit()
    con.close()

def main():
    logging.basicConfig(level=logging.DEBUG)
    create_schema()
    load_subs(read_srt())
    load_video_info(read_video_info())
    load_episode_guide(read_episode_guide())

if __name__ == "__main__":
    main()
