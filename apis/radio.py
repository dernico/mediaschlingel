from urllib import urlencode
from Helper import Helper
import json

RadioUrl = "http://radio.de/info"
searchCache = {}

searchCache["test"] = [
{
    "id": 18978,
    "image": "/keinbild.jpg",
    "name": "Radio 1",
    "genre": "hip hop"
},
{
    
    "id": 27879,
    "image": "/keinbild.jpg",
    "name": "Radio 1",
    "genre": "hip hop"
}
]

def getRecommendations():
    path = 'broadcast/editorialreccomendationsembedded'
    return _call(path)

def getTop():
    path = 'menu/broadcastsofcategory'
    param = {'category': '_top'}
    return _call(path, param)

def getByStationID(station_id):
    path = 'broadcast/getbroadcastembedded'
    id = str(station_id)
    param = {'broadcast': id}
    return _call(path, param)

def search(term):
    if term is None: return None
    if term in searchCache:
        print "Cache Hit for: {0}".format(term)
        return searchCache[term]
    path = 'index/searchembeddedbroadcast'
    param = {
        'q': term.encode("utf-8"),
        'start' : '0',
        'rows' : 200
    }
    searchCache[term] = _call(path, param)
    return searchCache[term]

def getMostWanted( num_entries=25):
        if not isinstance(num_entries, int):
            raise TypeError('Need int')
        path = 'account/getmostwantedbroadcastlists'
        param = {'sizeoflists': str(num_entries)}
        stations_lists = _call(path, param)
        return stations_lists

def _call(path, param=None):
        #print('call radio with path=%s, param=%s', path, param)
        url = '{0}/{1}'.format(RadioUrl, path)
        if param:
            url += '?' + urlencode(param)
        print("call radio with url: " + url)
        response = Helper.downloadString(url)
        json_data = json.loads(response)
        return json_data