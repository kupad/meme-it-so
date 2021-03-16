import os
import re

def get_episode(filename):
    """
    video and srt files are expected to contain a S{number}E{number} like S07E02
    """
    m = re.search('S([0-9]+)E([0-9]+)', filename) #eg: S07E02
    return m.group(0) if m is not None else None

def get_season(epdescr_str):
    """given a string that contains S07E02 extract the season portion: S07"""
    m = re.search('S([0-9]+)', epdescr_str)
    return m.group(0) if m is not None else None

#FIXME: actually examine the file?
def is_video(filename):
    return filename.endswith('mkv') or filename.endswith('avi') or filename.endswith('mp4')

def collect_episodes(source_dir):
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
            if not is_video(filename): continue

            path = os.path.join(dirpath, filename)
            ep = get_episode(filename) #eg: S07E02
            if ep is None: 
                print("warning: skipping because it does not contain match SsEe format", path)
                continue
            episodes.append( (ep, path))
    episodes.sort()
    return episodes





