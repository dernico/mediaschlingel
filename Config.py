# -*- coding: utf-8 -*-
import os
import json

configpath = os.path.join(os.curdir, "..", "schlingel.conf")
Config = {}

def loadConfig():
    global Config
    with open(configpath) as configcontent:
        Config = json.load(configcontent)

def getMediaDirs():
    return Config["musicfolder"]

def getOutputDir():
    coverdir = os.path.join(os.curdir, "Cover")
    if not os.path.exists(coverdir):
        os.makedirs(coverdir)
    return coverdir

def getTracksApiKey():
    return Config["8tracksApiKey"]

def getYoutubeApiKey():
    return Config["YouTubeApiKey"]

def get_shares():
    return Config["shares"]

def get_deezer_key():
    return Config["deezerKey"]

loadConfig()