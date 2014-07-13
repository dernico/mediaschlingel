import urllib
from urllib import urlencode
from Helper import Helper
from Factory import TracksModelFactory as factory
import json
import Config

TracksUrl = "http://8tracks.com"
ApiKey = Config.getTracksApiKey()
ApiVersion = 3
PlayToken = None
CurrentMix = None
CurrentTrack = None

def tags(tag):
    path = "mix_sets/{0}.json".format(tag)
    params = {"include": "mixes"}
    result = _call(path, params)
    mixes = {"mixes": []}
    for mix in result["mix_set"]["mixes"]:
        mixes["mixes"].append(factory.create_mix_from_tracks(mix))
    return mixes

def search(keyword):
    keyword = urllib.quote_plus(keyword)
    path = "mix_sets/keyword:{0}.json".format(keyword)
    params = {"include": "mixes"}
    result = _call(path, params)
    mixes = {"mixes": []}
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
    CurrentTrack = result["set"]
    CurrentTrack["track"]["cover"] = CurrentMix.Cover
    return CurrentTrack["track"]

def next(mix_id):
    global CurrentTrack

    if CurrentTrack["at_last_track"] == True:
        print("I am at the End of the Current Mix. Get Next mix in line ...")
        mix_id = next_mix_id(mix_id)

    path = "sets/{0}/next.json".format(PlayToken)
    params = {"mix_id": mix_id}
    result = _call(path, params)
    CurrentTrack = result["set"]
    CurrentTrack["track"]["cover"] = CurrentMix.Cover
    return CurrentTrack["track"]

def next_mix_id(mix_id):
    path = "sets/{0}/next_mix.json".format(PlayToken)
    params = {"mix_id": mix_id}
    result = _call(path, params)
    CurrentMix = factory.create_mix_from_tracks(result["next_mix"])
    return CurrentMix.ID

def skip(mix_id):
    global CurrentTrack

    if CurrentTrack["skip_allowed"] == True:
        path = "sets/{0}/skip.json".format(PlayToken)
        params = {"mix_id": mix_id}
        result = _call(path, params)
        if(result["status"] is "403 Forbidden"):
            return None
        else:
            CurrentTrack = result["set"]
            CurrentTrack["track"]["cover"] = CurrentMix.Cover
            return CurrentTrack["track"]
    else:
        print("Skip is not allowed")
        return None

def report(track_id, mix_id):
    print("Report track")
    path = "sets/{0}/report.json".format(PlayToken)
    params = {"track_id": track_id, "mix_id":mix_id}
    _call(path, params)

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
        #print("Response: " + response)
        json_data = json.loads(response)
        return json_data



def getPlayToken():
    global PlayToken
    path = "sets/new.json"
    if PlayToken is None:
        result = _call(path)
        PlayToken = result["play_token"]
        print("Playtoken: %s", PlayToken)

#Get a playtoken when lib gets loaded
#getPlayToken()