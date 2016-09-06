from urllib import urlencode
from Helper import Helper
from Player.DeezerPlayer import Player as dz_player
from aplayer import Player
import Config

import json

deezer_key = Config.get_deezer_key()
Base_Url = "http://api.deezer.com"
playlist = []
currentTrack = {}
nextTrack = None


def search(query):

    path = 'search'
    param = {
        'q': query,
    }
    result = _call(path, param)
    return get_tracks(query, result)


def get_tracks(query, dz_result):
    global playlist

    playlist = []
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
            playlist.append(track)
        except Exception as e:
            print(str(e))
    return currentTracks

def play(dz_track):
    global currentTrack
    global nextTrack

    Player.stop()
    #Player.on_media_end = on_media_end
    Player.play_next = on_next
    Player.play_prev = on_prev
    Player.on_pause = on_pause
    Player.on_play = on_resume

    Player.isPlaying = True
    Player.currentlyPlaying = {}
    Player.currentlyPlaying['webpath'] = ""
    Player.currentlyPlaying['name'] = dz_track["artist"]["name"]
    Player.currentlyPlaying['title'] = dz_track["title"]
    Player.currentlyPlaying['album'] = dz_track["album"]["title"]
    Player.currentlyPlaying['cover'] = dz_track["album"]["cover"]
    Player.currentlyPlaying['type'] = "deezer"
    
    dz_id = dz_track["id"]
    currentTrack = dz_track
    dz_player.play(dz_id, on_media_end)

def on_media_end():
    print("Media End")
    play_next()


def on_next():
    # stop automatically calls on_media_end which calls play_next :)
    dz_player.stop()

def play_next():
    global playlist
    global currentTrack

    nexttrack = None

    if nexttrack is None and len(playlist) > 0:
        count = 0
        for track in playlist:
            if str(track["id"]) == str(currentTrack["id"]):
                if count + 1 <= len(playlist):
                    nexttrack = playlist[count+1]
            count = count + 1

    if nexttrack:
        play(nexttrack)

def on_prev():
    # just do nothing :)
    return


def on_pause():
    Player.isPlaying = False
    dz_player.pause()

def on_resume():
    Player.isPlaying = True
    dz_player.resume()

def _call(path, param=None):
        #print('call radio with path=%s, param=%s', path, param)
        url = '{0}/{1}'.format(Base_Url, path)
        if param:
            url += '?' + urlencode(param)
        print("call radio with url: " + url)
        response = Helper.downloadString(url)
        json_data = json.loads(response)
        return json_data