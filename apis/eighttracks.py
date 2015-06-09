from threading import Timer
import urllib
from urllib import urlencode
from Helper import Helper
from Factory import TracksModelFactory as factory
import json
import Config
import aplayer

TracksUrl = "http://8tracks.com"
ApiKey = Config.getTracksApiKey()
ApiVersion = 3
PlayToken = None
CurrentMix = None
CurrentTrack = None
PerPage = 12
LastMixPath = None
LastMixParams = None
tracksTimer = None


def tags(tag):
    global LastMixParams
    global LastMixPath

    # tag = urllib.quote_plus(tag)
    print(tag)
    path = "mix_sets/{0}.json".format(tag)
    params = {"include": "mixes+pagination"}
    LastMixParams = params
    LastMixPath = path
    result = _call(path, params)
    return create_mixes_result(result)


def search(keyword):
    global LastMixParams
    global LastMixPath

    keyword = urllib.quote_plus(keyword)
    # path = "mix_sets/keyword:{0}:popular.json".format(keyword)
    path = "mix_sets/{0}.json".format(keyword)
    params = {"include": "mixes+pagination"}
    LastMixParams = params
    LastMixPath = path
    result = _call(path, params)
    return create_mixes_result(result)


def create_mixes_result(result):
    mixes = {"mixes": [], "pageing": {
        "currentPage": 0,
        "nextPage": 0,
        "perPage": PerPage,
        "prevPage": 0,
        "totalMixes": 0,
        "totalPages": 0
    }}
    if "mix_set" in result:
        mix_set = result["mix_set"]
        if len(mix_set["mixes"]) > 0:
            if "pagination" in result["mix_set"]:
                pageing = result["mix_set"]["pagination"]

                mixes["pageing"]["currentPage"] = pageing["current_page"]
                mixes["pageing"]["nextPage"] = pageing["next_page"]
                mixes["pageing"]["perPage"] = pageing["per_page"]
                mixes["pageing"]["prevPage"] = pageing["previous_page"]
                mixes["pageing"]["totalMixes"] = pageing["total_entries"]
                mixes["pageing"]["totalPages"] = pageing["total_pages"]

            for mix in result["mix_set"]["mixes"]:
                mixes["mixes"].append(factory.create_mix_from_tracks(mix))
    return mixes


def get_track(mix):
    getPlayToken()
    global CurrentMix
    global CurrentTrack
    CurrentMix = mix

    path = "sets/{0}/play.json".format(PlayToken)
    params = {"mix_id": mix.ID}
    result = _call(path, params)
    set_current_track(result)
    return CurrentTrack["track"]


def next(mix_id, callings=0):
    global CurrentTrack

    if callings > 2:
        # try next mix
        mix = next_mix(CurrentMix.ID)
        print("called next 3 times. Try next mix")
        return get_track(mix)

    if CurrentTrack["at_last_track"]:
        print("I am at the End of the Current Mix. Get Next mix in line ...")
        nextMix = next_mix(mix_id)
        return get_track(nextMix)

    path = "sets/{0}/next.json".format(PlayToken)
    params = {"mix_id": mix_id}
    result = _call(path, params)
    if result:
        set_current_track(result)
        if "track_file_stream_url" in CurrentTrack["track"]:
            if CurrentTrack["track"]["track_file_stream_url"]:
                return CurrentTrack["track"]

    next(mix_id, callings + 1)


def next_mix(mix_id):
    path = "sets/{0}/next_mix.json".format(PlayToken)
    params = {"mix_id": mix_id}
    result = _call(path, params)
    CurrentMix = factory.create_mix_from_tracks(result["next_mix"])
    return CurrentMix


def skip(mix_id):
    global CurrentTrack

    if CurrentTrack["skip_allowed"]:
        path = "sets/{0}/skip.json".format(PlayToken)
        params = {"mix_id": mix_id}
        result = _call(path, params)
        if result == None or result["status"] is "403 Forbidden":
            return next(mix_id)
        else:
            set_current_track(result)
            return CurrentTrack["track"]
    else:
        print("Skip is not allowed. play next mix.")
        return next(mix_id)


def report(track_id, mix_id):
    print("Report track")
    path = "sets/{0}/report.json".format(PlayToken)
    params = {"track_id": track_id, "mix_id": mix_id}
    _call(path, params)


def page_to(page_nr):
    global PerPage
    global LastMixParams
    LastMixParams["page"] = page_nr
    LastMixParams["per_page"] = PerPage
    result = _call(LastMixPath, LastMixParams)
    return create_mixes_result(result)


def _call(path, param=None):
    if param is None:
        param = {}

    param["api_key"] = ApiKey
    param["api_version"] = ApiVersion

    url = '{0}/{1}'.format(TracksUrl, path)
    if param:
        url += '?' + urlencode(param)
    print('call radio with url=%s', url)
    response = Helper.downloadString(url)
    # print("Response: " + response)
    if response:
        json_data = json.loads(response)
        return json_data
    else:
        return None


def set_current_track(result):
    global CurrentTrack

    if not "set" in result:
        if CurrentMix is None:
            return
        next(CurrentMix.ID)
        return
    CurrentTrack = result["set"]
    CurrentTrack["track"]["cover"] = CurrentMix.Cover


def getPlayToken():
    global PlayToken
    path = "sets/new.json"
    if PlayToken is None:
        result = _call(path)
        PlayToken = result["play_token"]
        print("Playtoken: %s", PlayToken)


def playMix(mix):
    print "try playing 8Track id" + mix.ID
    track = get_track(mix)
    _play(track)


def _play(track):
    global tracksTimer

    set_mediahandling()

    cancleTracksTimer()
    # track_id = Player.currentlyPlaying['track_id']
    # mix_id = Player.currentlyPlaying['mix_id']

    if track["id"] is None:
        next(CurrentMix.ID)

    print("start tracks timer")
    tracksTimer = Timer(30.0, lambda: report(CurrentTrack["track"]["id"], CurrentMix.ID))
    tracksTimer.start()

    stream_url = track["track_file_stream_url"]
    name = track["name"]
    title = track["release_name"]
    track_id = track["id"]
    cover = track["cover"]

    aplayer.Player.currentlyPlaying = {
        'webpath': stream_url,
        'name': name,
        'title': title,
        'album': name,
        'cover': cover,
        'track_id': track_id,
        'mix_id': CurrentMix.ID,
        'type': "8tracks"
    }
    aplayer.Player.playPath(stream_url)


def cancleTracksTimer():
    global tracksTimer
    print("cancle Tracks Timer")
    if tracksTimer:
        tracksTimer.cancel()
    tracksTimer = None


def set_mediahandling():
    aplayer.Player.on_media_end = on_media_end
    aplayer.Player.play_next = on_next
    aplayer.Player.play_prev = on_prev
    aplayer.Player.on_pause = on_pause


def on_media_end(player):
    track = next(CurrentMix.ID)
    _play(track)


def on_next():
    track = next(CurrentMix.ID)
    _play(track)


def on_prev():
    return


def on_pause():
    aplayer.Player.pause()

    # Get a playtoken when lib gets loaded
    #getPlayToken()