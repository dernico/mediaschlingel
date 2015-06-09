from urllib import urlencode
from Helper import Helper
from Factory.StreamModelFactory import StreamModelFactory
from aplayer import Player

import json
import Config


yt_api_endpoint = 'https://www.googleapis.com/youtube/v3/'
yt_key = Config.getYoutubeApiKey()
playlist = []
playnext = []
currentSearch = ''

def search(q, pageToken):
    global currentSearch

    currentSearch = q
    query = {
        'part': 'id,snippet',
        'maxResults': 15,
        'type': 'video',
        'q': currentSearch
    }
    if pageToken:
        query["pageToken"] = pageToken

    yt_result = _call(yt_api_endpoint + 'search', param=query)
    return get_tracks(yt_result)


def get_tracks(yt_result):
    global currentSearch

    currentTracks = {}
    currentTracks["q"] = currentSearch
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


def get_related_songs(video_id):
    global playlist
    yt_result = _call(yt_api_endpoint + 'search',
                      {"part": "id,snippet",
                       "relatedToVideoId": video_id,
                       "maxResults": 50,
                       "type": "video"})
    currentrelatedtracks = get_tracks(yt_result)
    tracks = currentrelatedtracks["tracks"]
    playlist = []
    playlist.extend(tracks)
    return currentrelatedtracks


def get_playlist():
    global playnext
    global playlist
    songs = []
    songs.extend(playnext)
    songs.extend(playlist)
    return {"playlist": songs}

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
    global playnext
    global playlist

    songs = []
    songs.extend(playnext)
    songs.extend(playlist)

    for yt in playnext:
        ytId = yt["id"]
        if type(yt["id"]) is tuple:
            ytId = ytId[0]
        if str(ytId) == str(id):
            return True
    return False


def add_to_playlist(track):
    global playnext
    playnext.append(track)


def on_media_end(player):
    print("Media End")
    on_next()


def on_next():
    global playlist
    global playnext
    print("Play next youtube track")
    nexttrack = None
    if len(playnext) > 0:
        nexttrack = playnext[0]
        playnext = playnext[1:]
    else:
        if len(playlist) > 0:
            nexttrack = playlist[0]
            playlist = playlist[1:]
            # Make sure playlist is not empty
            if len(playlist) == 0:
                get_related_songs(nexttrack["id"])

    if nexttrack:
        nexttrack = get_stream_model(nexttrack["id"])
        _play(nexttrack)

def on_prev():
    # just do nothing :)
    return


def on_pause():
    Player.pause()


def _call(url, param=None):
    # print('call radio with path=%s, param=%s', path, param)
    if param:
        param['key'] = yt_key
        url += '?' + urlencode(param)
    print("call youtube with url: " + url)
    response = Helper.downloadString(url)
    json_data = json.loads(response)
    return json_data