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


