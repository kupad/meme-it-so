import csv

from moviepy.editor import VideoFileClip

from utils.episode_utils import collect_episodes

def create_index(source_dir,video_index_path):
    #get all the episodes from the source_dir
    episodes = collect_episodes(source_dir)

    #collect video information
    vid_info = []
    for ep, source_path in episodes:
        clip = VideoFileClip(source_path)
        vid_info.append({
            'episode': ep,
            'fps': clip.reader.fps,
            'duration': clip.reader.duration,
            'nframes': clip.reader.nframes
        })

    #open csv file and write info to it
    with open(video_index_path, 'w') as csvfile:
        fieldnames = ['episode', 'duration', 'fps', 'nframes' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for e in vid_info:
            writer.writerow(e)

def read_index(video_index_path):
    video_index = {}
    with open(video_index_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            video_index[row['episode']] = row
    return video_index

