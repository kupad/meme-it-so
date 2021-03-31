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

#frames.py: tools for working with:
#times, frames, and images that represent frames

from .eptools import get_season


thumbnails='/static/thumbnails' #base url for thumbnails
nthframe=6 #work with every 6th frame

def frame_to_url(ep, frame):
    """translates a frame to an img url"""
    season = get_season(ep)
    img_url = f'{thumbnails}/{season}/{ep}/{frame:05}.jpg'
    return img_url

def closest_frame(ms, fps):
    """returns the closest frame to the time offset"""
    est_frame = round( (ms / 1000) * fps)
    frame = est_frame - (est_frame % nthframe)
    return frame

#TODO: take fps as a param. I don't think fps is an obvious field for a scene...
def repr_frame(scene):
    """returns the frame that represents this scene"""
    return closest_frame(scene['start_offset'], scene['fps'])

#TODO: take fps as a param. I don't think fps is an obvious field for a scene...
def repr_img_url(scene):
    """return an image_url that will represent this scene"""
    return frame_to_url(scene['episode'], repr_frame(scene))
