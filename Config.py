# -*- coding: utf-8 -*-

import os

def getMediaDirs():
    return ["/home/nico/Music", "C:\\Users\\Nico\\Music"]

def getOutputDir():
    coverdir = os.path.join(os.curdir, "Cover")
    if not os.path.exists(coverdir):
        os.makedirs(coverdir)
    return coverdir