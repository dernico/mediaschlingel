from urllib import urlencode
from Helper import Helper
import json


TracksUrl = "http://8tracks.com"
ApiKey = "asdasd"
ApiVersion = 3
PlayToken = None

def popular():
    path = "mix_sets/all:popular.json"
    params = {"include": "mixes"}
    result = _call(path, params)
    return result

def get_track(id):
    path = "sets/{0}/play.json".format(PlayToken)
    params = {"mix_id": id}
    result = _call(path, params)
    print(result)
    return CurrentMix["set"]["track"]

def next(id):
    path = "sets/{0}/next.json".format(PlayToken)
    params = {"mix_id": id}
    result = _call(path, params)
    print(result)

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
getPlayToken()