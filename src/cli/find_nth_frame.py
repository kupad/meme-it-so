import os
import sys

nthframe=6
dir = sys.argv[1]

for dirpath, dirnames, filenames in os.walk(dir):
    for fname in filenames:
        frame = int(fname.replace(".jpg",""))
        if frame % nthframe == 0:
            filepath = os.path.join(dirpath.replace(dir,''),fname)
            print(filepath)
