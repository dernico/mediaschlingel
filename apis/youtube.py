from urllib import urlencode
from Helper import Helper
from Factory.StreamModelFactory import StreamModelFactory
from aplayer import Player

import json
import Config


yt_api_endpoint = 'https://www.googleapis.com/youtube/v3/'
yt_key = Config.getYoutubeApiKey()
playlist = []
currentTracks = {}

def search(q, pageToken):
    global currentTracks
    query = {
        'part': 'id,snippet',
        'maxResults': 15,
        'type': 'video',
        'q': q,
        'key': yt_key
    }
    if pageToken:
        query["pageToken"] = pageToken
        
    yt_result = _call(yt_api_endpoint+'search', param=query)
    #return yt_result
    #print yt_result
    currentTracks = {}
    currentTracks["q"] = q
    if 'nextPageToken' in yt_result:
        currentTracks["nextPageToken"] = yt_result["nextPageToken"]
    if 'prevPageToken' in yt_result:
        currentTracks["prevPageToken"] = yt_result["prevPageToken"]

    currentTracks["tracks"] = []
    for item in yt_result['items']:
        try:
            if item["id"]["kind"] == "youtube#video":
                track = {}
                track["title"] = item["snippet"]["title"]
                id = item["id"]["videoId"]
                track["id"] = id
                track["description"] = item["snippet"]["description"]
                track["thumbnail"] = item["snippet"]["thumbnails"]["high"]["url"]
                track["showPlayNext"] = not is_in_playlist(track["id"])
            	currentTracks["tracks"].append(track)
        except Exception as e:
            print(str(e))
    return currentTracks
    
def get_stream_model(id):
    factory = StreamModelFactory()
    return factory.createFromYouTube(id)

def play(id):
    youtubeStream = get_stream_model(id)
    _play(youtubeStream)

def _play(s):
    Player.on_media_end = on_media_end
    Player.play_next = on_next
    Player.play_prev = on_prev
    Player.on_pause = on_pause
    
    Player.currentlyPlaying = {}
    Player.currentlyPlaying['webpath'] = s.Stream
    Player.currentlyPlaying['name'] = s.Name
    Player.currentlyPlaying['title'] = s.Format
    Player.currentlyPlaying['cover'] = s.Image
    Player.currentlyPlaying['type'] = "youtube"
    Player.playPath(s.Stream)

def is_in_playlist(id):
    global playlist
    for yt in playlist:
        ytId = yt.Id
        if type(yt.Id) is tuple:
            ytId = ytId[0]
        if str(ytId) == str(id):
            return True
    return False

def add_to_playlist(id):
    global playlist
    s = get_stream_model(id)
    playlist.append(s)

def on_media_end(player):
    on_next()

def on_next():
    global playlist
    if len(playlist) > 0:
        nextTrack = playlist[0]
        playlist = playlist[1:]
        _play(nextTrack)

def on_prev():
    # just do nothing :)
    return

def on_pause():
    Player.pause()

def _call(url, param=None):
        #print('call radio with path=%s, param=%s', path, param)
        if param:
            url += '?' + urlencode(param)
        print("call radio with url: " + url)
        response = Helper.downloadString(url)
        json_data = json.loads(response)
        return json_data