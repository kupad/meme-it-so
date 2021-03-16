#!/usr/bin/python3

from conf import * 
from utils.video_index import create_index

def main():
    create_index(source_dir=SERIES_DIR,
                video_index_path=VIDEO_INDEX_PATH)
   
if __name__ == "__main__":
    main()


