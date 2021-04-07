#quick tool for finding the nthframe in a directory of thumbs


import os
import sys

nthframe=6
dir = sys.argv[1]

paths = []
for dirpath, dirnames, filenames in os.walk(dir):
    for fname in filenames:
        filepath = os.path.join(dirpath,fname)
        frame = int(fname.replace(".jpg",""))
        if frame % nthframe == 0:
            print(filepath)
            #paths.append( (frame, filepath))
