import os

GIT_DIR = ".hit"


def init():
    os.makedirs(GIT_DIR, exist_ok=True)
