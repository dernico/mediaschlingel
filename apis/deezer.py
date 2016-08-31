from urllib import urlencode
from Helper import Helper
from Player.DeezerPlayer import Player
import Config

import json

deezer_key = Config.get_deezer_key()
Base_Url = "http://api.deezer.com"


def search(query):

    path = 'search'
    param = {
        'q': query,
    }
    result = _call(path, param)
    return get_tracks(query, result)


def get_tracks(query, dz_result):
    currentTracks = {}
    currentTracks["q"] = query
    #if 'nextPageToken' in yt_result:
    #    currentTracks["nextPageToken"] = yt_result["nextPageToken"]
    #if 'prevPageToken' in yt_result:
    #    currentTracks["prevPageToken"] = yt_result["prevPageToken"]

    currentTracks["tracks"] = []
    for item in dz_result['data']:
        try:
            
            track = {}
            track["title"] = item["title"]
            track["id"] = item["id"]

            track["artist"] = {}
            track["artist"]["name"] = item["artist"]["name"]
            track["artist"]["picture"] = item["artist"]["picture_medium"]
            
            track["album"] = {}
            track["album"]["title"] = item["album"]["title"]
            track["album"]["cover"] = item["album"]["cover_medium"]

            currentTracks["tracks"].append(track)
        except Exception as e:
            print(str(e))
    return currentTracks

def play(dz_id):
    Player.play(dz_id, handleNext)

def handleNext():
    print("Play next deezer song ...")

def _call(path, param=None):
        #print('call radio with path=%s, param=%s', path, param)
        url = '{0}/{1}'.format(Base_Url, path)
        if param:
            url += '?' + urlencode(param)
        print("call radio with url: " + url)
        response = Helper.downloadString(url)
        json_data = json.loads(response)
        return json_data