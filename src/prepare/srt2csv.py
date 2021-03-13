#!/usr/bin/python3

"""
read ALL the srts from SOURCE_SRT_DIR and create one giant csv file from them
"""

import os
import srt
import csv

from conf import *
from utils.episode_utils import get_episode, get_season

def td2ms(td):
    return int(td.total_seconds()*1000)

def is_srt(filename):
    """is this an srt file? (well, does it claim to be?)"""
    return filename.endswith('.srt')

def srt2csv():
    os.makedirs(SUBTITLES_DIR, exist_ok=True)

    allsubs = []
    for dirpath, dirnames, filenames in os.walk(SOURCE_SRT_DIR):
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
                    allsubs.append( [ep,sub.index,td2ms(sub.start),td2ms(sub.end),sub.content])
   
    allsubs.sort(key=lambda s: (s[0],s[1]))

    with open(SUBTITLES_CSV_PATH, 'w') as subcsv:
        csvwriter = csv.writer(subcsv, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['episode','srtidx','start(ms)','end(ms)','content'])
        csvwriter.writerows(allsubs)

def main():
    srt2csv()

if __name__ == "__main__":
    main()

