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

"""query and return hits from the database"""

import os
import argparse

from ..api.utils import captions
from conf import CAPTION_INDEX_DIR

def query(qstr):
    results = captions.query(qstr, CAPTION_INDEX_DIR)
    print(results)
    for r in results:
        print(r)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search", help="search for phrase")
    args = parser.parse_args()
    query(args.search)


if __name__ == "__main__":
    main()
