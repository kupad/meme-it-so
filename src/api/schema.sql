DROP TABLE IF EXISTS captions;
DROP TABLE IF EXISTS video_info;
DROP TABLE IF EXISTS episode_guide;

CREATE TABLE captions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode TEXT,
    srtidx INTEGER,
    start_offset INTEGER,
    end_offset INTEGER,
    content TEXT
);

CREATE TABLE video_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode TEXT,
    fps REAL,
    duration REAL,
    nframes INTEGER
);

CREATE TABLE episode_guide (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode TEXT,
    season INTEGER,
    episode_num INTEGER,
    title TEXT,
    airdate TEXT
);
