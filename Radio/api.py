from urllib import urlencode
from Helper import Helper
import json

RadioUrl = "http://radio.de/info"

def get_recommendation_stations():
    path = 'broadcast/editorialreccomendationsembedded'
    return __api_call(path)

def get_top_stations():
    path = 'menu/broadcastsofcategory'
    param = {'category': '_top'}
    return __api_call(path, param)

def get_station_by_station_id(station_id):
    path = 'broadcast/getbroadcastembedded'
    param = {'broadcast': str(station_id)}
    return __api_call(path, param)

def get_search(term):
    if term is None: return None
    path = ''
    param = {'search': term}
    return __api_call(path, param)

def _get_most_wanted( num_entries=25):
        if not isinstance(num_entries, int):
            raise TypeError('Need int')
        path = 'account/getmostwantedbroadcastlists'
        param = {'sizeoflists': str(num_entries)}
        stations_lists = self.__api_call(path, param)
        return stations_lists

def __api_call(path, param=None):
        print('__api_call started with path=%s, param=%s',
                     path, param)
        url = '%s/%s' % (RadioUrl, path)
        if param:
            url += '?%s' % urlencode(param)
        response = Helper.downloadString(url)
        json_data = json.loads(response)
        return json_data