import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUTS = os.path.join(DATA_DIR, "inputs")
OUTPUTS = os.path.join(DATA_DIR, 'outputs')

SERIES_DIR= '/mnt/nfs/NAS/media/tv/Star.Trek-.The.Next.Generation/'
THUMBNAILS_DIR = './data/outputs/thumbnails/'

GIF_FPS=6
GIF_WIDTH=480
GIF_HEIGHT=356


