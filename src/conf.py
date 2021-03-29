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

import os

#where meme-it-so lives
BASE_DIR = os.path.dirname("/home/kupad/dev/meme-it-so/")

#series specific information
SERIES_NAME = "STTNG"
SERIES_DIR  = '/mnt/nfs/NAS/media/tv/Star.Trek-.The.Next.Generation/'

#data generated here
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUTS = os.path.join(DATA_DIR, 'inputs')
OUTPUTS  = os.path.join(DATA_DIR, 'outputs')

#database
DATABASE_PATH = os.path.join(DATA_DIR, 'memeitso.db')

#episode guide
EPISODE_GUIDE_PATH = os.path.join(INPUTS,SERIES_NAME, 'episode_guide.csv')

#video source info
VIDEO_INDEX_PATH = os.path.join(OUTPUTS,SERIES_NAME, 'video_index.csv')
VIDEO_FPS   = 23.976023976023978 #default, but video info index will extract the actual number

#subtitle INFO
SOURCE_SRT_DIR = SERIES_DIR
SUBTITLES_DIR = os.path.join(OUTPUTS, SERIES_NAME, 'subtitles')
SUBTITLES_CSV_PATH = os.path.join(SUBTITLES_DIR, 'subtitles.csv')
CAPTION_INDEX_DIR = os.path.join(OUTPUTS, SERIES_NAME, 'caption_index')

#thumnail info
#THUMBNAILS_DIR='/mnt/nfs/NAS/media/memeitso/sttng/thumbs/' #slower, more space
THUMBNAILS_DIR=os.path.join(OUTPUTS, SERIES_NAME, 'thumbnails')     #faster, less space

#gif info
GIFS_DIR = os.path.join(OUTPUTS, "gifs")
GIF_FPS=15
GIF_WIDTH=480
GIF_HEIGHT=356
