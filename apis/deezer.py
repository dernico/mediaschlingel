from urllib import urlencode
from Helper import Helper
from Player.DeezerPlayer import Player as dz_player
from aplayer import Player
import Config

import json

deezer_key = Config.get_deezer_key()
Base_Url = "http://api.deezer.com"
playlist = []


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
    Player.stop()
    #Player.on_media_end = on_media_end
    Player.play_next = on_next
    Player.play_prev = on_prev
    Player.on_pause = on_pause
    Player.on_play = on_resume

    Player.currentlyPlaying = {}
    Player.currentlyPlaying['webpath'] = ""
    Player.currentlyPlaying['name'] = dz_track["artist"]["name"]
    Player.currentlyPlaying['title'] = dz_track["title"]
    Player.currentlyPlaying['cover'] = dz_track["album"]["cover"]
    Player.currentlyPlaying['type'] = "deezer"
    
    dz_id = str(dz_track["id"])
    dz_player.play(dz_id, on_next)

def on_media_end(player):
    print("Media End")
    on_next()


def on_next():
    global playlist
    print("Play next deezer track")
    nexttrack = None

    if len(playlist) > 0:
        nexttrack = playlist[0]
        playlist = playlist[1:]
        # Make sure playlist is not empty
        #if len(playlist) == 0:
        #    get_related_songs(nexttrack)

    if nexttrack:
        play(nexttrack)

def on_prev():
    # just do nothing :)
    return


def on_pause():
    dz_player.pause()

def on_resume():
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