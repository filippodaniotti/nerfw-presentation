r"""
Usage:
unix: python3 ./src/utils/extract_gifs.py problem.mp4 interpol.mp4 geometry.webm mipnerf.mp4 waving-flag.gif block-nerf.webm
win: python .\src\utils\extract_gifs.py problem.mp4 interpol.mp4 geometry.webm mipnerf.mp4 waving-flag.gif block-nerf.webm
"""

import os
import sys
import shutil
from os.path import join, isfile, isdir
from subprocess import run
from contextlib import contextmanager

@contextmanager
def ondir(path: str):
    cwd = os.getcwd()
    dest = os.path.join(cwd, path)
    os.chdir(dest)
    yield dest
    os.chdir(cwd)


def incremental_rename(prefix: str, ext: str = None):
	cwd = os.getcwd()
	files = os.listdir()
	files = [f for f in files if isfile(f)]
	if ext is None:
		ext = files[0].split('.')[-1]
	for idx, old_name in enumerate(files):
		os.rename(join(cwd, old_name), join(cwd, f"{prefix}{idx}.{ext}"))

def main(video_path: str):
    video_name = video_path.split('.')[-2]
    with ondir(join('src', 'assets', 'gifs')) as wd:
        if isdir(join(wd, video_name)):
            shutil.rmtree(video_name)
        os.mkdir(video_name)
        run (['ffmpeg', '-i', video_path, join(video_name, '%03d.png')])
        with ondir(video_name):
            incremental_rename(f'{video_name}-')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for video in sys.argv[1:]:
            print(f'Processing {video}...')
            main(video)
            print(f'{video} is done!')
    else:
        raise ValueError('No file was provided')