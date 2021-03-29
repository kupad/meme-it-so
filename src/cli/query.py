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
