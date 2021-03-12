import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUTS = os.path.join(DATA_DIR, "inputs")
OUTPUTS = os.path.join(DATA_DIR, 'outputs')

FPS=6
WIDTH=480


