# -*- coding: utf-8 -*-
import os

def getMediaDirs():
    return ["/home/nico/Music", "C:\\Users\\Nico\\Music"]

def getOutputDir():
    coverdir = os.path.join(os.curdir, "Cover")
    if not os.path.exists(coverdir):
        os.makedirs(coverdir)
    return coverdir

def getTracksApiKey():
    filepath = os.path.join(os.curdir,'..', "8tracks_api_key.txt")
    print filepath
    with open(filepath) as content:
    	return content.readline()