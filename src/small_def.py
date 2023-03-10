from os.path import exists
from os import getcwd, mkdir
from pathlib import Path

paths : list = []
paths.append(Path(f"{getcwd()}/data/"))
paths.append(Path(f"{getcwd()}/cache/"))


data = paths[0]
cache = paths[1]


def if_not_exist_mkdir(dir):
    if not exists(dir):
        mkdir(dir)
