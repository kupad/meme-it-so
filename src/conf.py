import os

#where meme-it-so lives
BASE_DIR = os.path.dirname("/home/kupad/dev/meme-it-so/")

#series specific information
SERIES_NAME = "STTNG"
SERIES_DIR  = '/mnt/nfs/NAS/media/tv/Star.Trek-.The.Next.Generation/'
VIDEO_FPS   = 23.976

#data generated here
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS  = os.path.join(DATA_DIR, 'outputs')

#subtitle INFO
SOURCE_SRT_DIR = SERIES_DIR
SUBTITLES_DIR = os.path.join(OUTPUTS, SERIES_NAME, 'subtitles')
SUBTITLES_CSV_PATH = os.path.join(SUBTITLES_DIR, 'subtitles.csv')

#thumnail info
#THUMBNAILS_DIR='/mnt/nfs/NAS/media/memeitso/sttng/thumbs/' #slower, more space
THUMBNAILS_DIR=os.path.join(OUTPUTS, SERIES_NAME, 'thumbnails')     #faster, less space

#gif info
GIFS_DIR = os.path.join(OUTPUTS, "gifs")
GIF_FPS=15
GIF_WIDTH=480
GIF_HEIGHT=356


