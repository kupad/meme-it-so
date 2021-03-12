import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUTS = os.path.join(DATA_DIR, "inputs")
OUTPUTS = os.path.join(DATA_DIR, 'outputs')

VIDEO_FPS=23.976
SERIES_DIR= '/mnt/nfs/NAS/media/tv/Star.Trek-.The.Next.Generation/'

#THUMBNAILS_DIR='/mnt/nfs/NAS/media/memeitso/sttng/thumbs/' #slower, more space
THUMBNAILS_DIR=os.path.join(OUTPUTS, 'sttng', 'thumbs')     #faster, less space

GIFS_DIR = os.path.join(OUTPUTS, "gifs")
GIF_FPS=15
GIF_WIDTH=480
GIF_HEIGHT=356


