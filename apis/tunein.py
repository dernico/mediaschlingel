# Used many of the code from: https://github.com/kingosticks/mopidy-tunein/blob/master/mopidy_tunein/tunein.py


try:
    import xml.etree.cElementTree as elementtree
except ImportError:
    import xml.etree.ElementTree as elementtree

import re
import urlparse
from urllib import urlencode
from Helper import Helper
from Factory import StreamModelFactory
from aplayer import Player
from apis import Streams

import json
#import Config


def search(searchterm):
    result = singelton.search(searchterm);
    streams = []
    for item in result:
        stream = StreamModelFactory.createFromTunein(item)
        streams.append(stream)
    return streams

def play(item):
    model = StreamModelFactory.createFromStreamJson(item)
    parseUrl = True
    tuneurls = singelton.tune(model.Id, parseUrl)
    if len(tuneurls) > 0:
        model.Stream = tuneurls[0];
        _play(model)


def _play(s):
    #Player.on_media_end = on_media_end
    Player.play_next = on_next
    Player.play_prev = on_prev
    #Player.on_pause = on_pause

    Player.currentlyPlaying = {}
    Player.currentlyPlaying['webpath'] = s.Stream
    Player.currentlyPlaying['name'] = s.Name
    Player.currentlyPlaying['title'] = s.Format
    Player.currentlyPlaying['cover'] = s.Image
    Player.currentlyPlaying['type'] = Player.streamType
    Player.playPath(s.Stream)

def on_next():
    #do nothing
    next = True

def on_prev():
    #do nothing
    prev = True

def save(item):
    json_item = json.loads(item)
    model = StreamModelFactory.createFromStreamJson(json_item)
    tuneurls = singelton.tune(model.Id, True)
    if len(tuneurls) > 0:
        model.Stream = tuneurls[0];
    Streams.writeModelToFile(model)

tuneInUri = 'http://opml.radiotime.com/'
tuneInBrowseUri = tuneInUri + 'Browse.ashx'


def parse_m3u(url):

    urls = []
    m3u_content = Helper.downloadString(url)
    for line in m3u_content.split("\n"):
        if not line.startswith('#') \
        and line.strip() \
        and line.startswith("http"):
            urls.append(line)
    return urls

    # Copied from mopidy.audio.playlists
    # Mopidy version expects a header but it's not always present
    #for line in data.readlines():
    #    if not line.startswith('#') and line.strip():
    #        yield line.strip()


def parse_pls(url):
    urls = []
    pls_content = Helper.downloadString(url)
    for line in pls_content.split("\n"):
        if 'File' in line:
            url = line.split("=")[1]
            urls.append(url)
    return urls
'''
    # Copied from mopidy.audio.playlists
    try:
        print(data)
        cp = configparser.RawConfigParser()
        cp.readfp(data)
    except configparser.Error:
        return

    for section in cp.sections():
        if section.lower() != 'playlist':
            continue
        for i in xrange(cp.getint(section, 'numberofentries')):
            try:
                # TODO: Remove this horrible hack
                if cp.get(section, 'length%d' % (i+1)) == '-1':
                    yield cp.get(section, 'file%d' % (i+1))
            except configparser.NoOptionError:
                yield cp.get(section, 'file%d' % (i+1))
'''

def fix_asf_uri(uri):
    return re.sub(r'http://(.+\?mswmext=\.asf)', r'mms://\1', uri, re.I)


def parse_old_asx(data):
    print("parse old asx")
    try:
        cp = configparser.RawConfigParser()
        cp.readfp(data)
    except configparser.Error:
        return
    for section in cp.sections():
        if section.lower() != 'reference':
            continue
        for option in cp.options(section):
            if option.lower().startswith('ref'):
                uri = cp.get(section, option).lower()
                yield fix_asf_uri(uri)


def parse_new_asx(data):
    print("parse new asx")
    # Copied from mopidy.audio.playlists
    try:
        for event, element in elementtree.iterparse(data):
            element.tag = element.tag.lower()  # normalize
    except elementtree.ParseError:
        return

    for ref in element.findall('entry/ref[@href]'):
        yield fix_asf_uri(ref.get('href', '').strip())

    for entry in element.findall('entry[@href]'):
        yield fix_asf_uri(entry.get('href', '').strip())


def parse_asx(url):
    urls = []
    data = Helper.downloadString(url)

    m = re.search(r'\<[Rr]ef.*\"(http.*)\"', data, re.I)
    url = m.group(1)
    print("Found asx url: " + url)
    urls.append(url)

    return urls

    if b'asx' in data.getvalue()[0:50].lower():
        url = parse_new_asx(data)
        urls.append(url)
    else:
        url = parse_old_asx(data)
        urls.append(url)

    return urls

'''
def find_playlist_parser(extension, content_type):
    extension_map = {'.asx': parse_asx,
                     '.m3u': parse_m3u,
                     '.pls': parse_pls}
    content_type_map = {'video/x-ms-asf': parse_asx,
                        'application/x-mpegurl': parse_m3u,
                        'audio/x-scpls': parse_pls}

    parser = extension_map.get(extension, None)
    if not parser and content_type:
        # Annoying case where the url gave us no hints so try and work it out
        # from the header's content-type instead.
        # This might turn out to be server-specific...
        parser = content_type_map.get(content_type.lower(), None)
    return parser
'''

def _call(url, param=None):
    # print('call radio with path=%s, param=%s', path, param)
    if param:
        param['key'] = yt_key
        url += '?' + urlencode(param)
    print("call tunein with url: " + url)
    response = Helper.downloadString(url)
    json_data = json.loads(response)
    return json_data



class TuneIn(object):
    """Wrapper for the TuneIn API."""

    def __init__(self, timeout):
        self._base_uri = 'http://opml.radiotime.com/%s'
        self._timeout = timeout / 1000.0
        self._stations = {}

    def reload(self):
        self._stations.clear()
        self._tunein.clear()
        self._get_playlist.clear()

    def _flatten(self, data):
        results = []
        for item in data:
            if 'children' in item:
                results.extend(item['children'])
            else:
                results.append(item)
        return results

    def _filter_results(self, data, section_name=None, map_func=None):
        results = []

        def grab_item(item):
            if 'guide_id' not in item:
                return
            if map_func:
                station = map_func(item)
            elif item.get('type', 'link') == 'link':
                results.append(item)
                return
            else:
                station = item
            self._stations[station['guide_id']] = station
            results.append(station)

        for item in data:
            if section_name is not None:
                section_key = item.get('key', '').lower()
                if section_key.startswith(section_name.lower()):
                    for child in item['children']:
                        grab_item(child)
            else:
                grab_item(item)
        return results

    def categories(self, category=''):
        if category == 'location':
            args = '&id=r0'  # Annoying special case
        elif category == 'language':
            args = '&c=lang'
            return []  # TuneIn's API is a mess here, cba
        else:
            args = '&c=' + category

        # Take a copy so we don't modify the cached data
        results = list(self._tunein('Browse.ashx', args))
        if category in ('podcast', 'local'):
            # Flatten the results!
            results = self._filter_results(self._flatten(results))
        elif category == '':
            trending = {'text': 'Trending',
                        'key': 'trending',
                        'type': 'link',
                        'URL': self._base_uri % 'Browse.ashx?c=trending'}
            # Filter out the language root category for now
            results = [x for x in results if x['key'] != 'language']
            results.append(trending)
        else:
            results = self._filter_results(results)
        return results

    def locations(self, location):
        args = '&id=' + location
        results = self._tunein('Browse.ashx', args)
        # TODO: Support filters here
        return [x for x in results if x.get('type', '') == 'link']

    def _browse(self, section_name, guide_id):
        args = '&id=' + guide_id
        results = self._tunein('Browse.ashx', args)
        return self._filter_results(results, section_name)

    def featured(self, guide_id):
        return self._browse('Featured', guide_id)

    def local(self, guide_id):
        return self._browse('Local', guide_id)

    def stations(self, guide_id):
        return self._browse('Station', guide_id)

    def related(self, guide_id):
        return self._browse('Related', guide_id)

    def shows(self, guide_id):
        return self._browse('Show', guide_id)

    def episodes(self, guide_id):
        args = '&c=pbrowse&id=' + guide_id
        results = self._tunein('Tune.ashx', args)
        return self._filter_results(results, 'Topic')

    def _map_listing(self, listing):
        # We've already checked 'guide_id' exists
        url_args = 'Tune.ashx?id=%s' % listing['guide_id']
        return {'text': listing.get('name', '???'),
                'guide_id': listing['guide_id'],
                'type': 'audio',
                'subtext': listing.get('slogan', ''),
                'URL': self._base_uri % url_args}

    def _station_info(self, station_id):
        args = '&c=composite&detail=listing&id=' + station_id
        results = self._tunein('Describe.ashx', args)
        listings = self._filter_results(results, 'Listing', self._map_listing)
        if listings:
            return listings[0]

    def parse_stream_url(self, url):
        extension = urlparse.urlparse(url).path[-4:]
        print('Using TuneIn extension parsing: %s , extension %s', \
            url, extension)
        if extension in ['.mp3', '.wma']:
            return [url]  # Catch these easy ones
        elif extension == '.pls':
            return parse_pls(url)
        elif extension == '.m3u':
            return parse_m3u(url)
        #elif extension == '.asx':
        #    return parse_asx(url)
        else:
            return [url]

        # old code from mopidy tunein 
        results = []
        playlist, content_type = self._get_playlist(url)
        if playlist:
            parser = find_playlist_parser(extension, content_type)
            if parser:
                print("parse_stream_url " + playlist)
                #playlist_data = StringIO.StringIO(playlist)
                #results = [u for u in parser(playlist_data) if u is not None]

        if not results:
            print(
                'Parsing failure, possibly malformed playlist: %s' % playlist)
        else:
            print('TuneIn found URI: %s', results[0])
        return results

    def tune(self, station_id, parse_url=True):
        print('Tuning station id %s' % station_id)
        args = '&id=' + station_id
        for stream in self._tunein('Tune.ashx', args):
            if 'url' in stream:
                # TODO Cache these playable stream urls?
                if parse_url:
                    return self.parse_stream_url(stream['url'])
                else:
                    return [stream['url']]

        print('Failed to tune station id %s' % station_id)
        return []

    def station(self, station_id):
        if station_id in self._stations:
            station = self._stations[station_id]
        else:
            station = self._station_info(station_id)
            self._stations['station_id'] = station
        return station

    def search(self, query):
        # "Search.ashx?query=" + query + filterVal
        if not query:
            print('Empty search query')
            return []
        print('Searching for "%s"' % query)
        #args = '&query=' + query
        args ={
            "query": query
        }
        args = "&" + urlencode(args)
        search_results = self._tunein('Search.ashx', args)
        results = []
        for item in self._flatten(search_results):
            # use only audio and filter out wma
            # wma is not playable from gstreamer
            if item.get('type', '') == 'audio' \
            and not 'wma' in item.get('formats',''):
                # Only return stations
                self._stations[item['guide_id']] = item
                results.append(item)

        return results

    def _tunein(self, variant, args):
        uri = (self._base_uri % variant) + '?render=json' + args
        print('TuneIn request: %s', uri)
        try:
            data = _call(uri)
            if (data['head']['status'] != '200'):
                print("Error requesting tunein")
            return data['body']
        except Exception as e:
            print('TuneIn request failed: %s', e)
        return {}

    def _get_playlist(self, uri):
        try:
            # Defer downloading the body until know it's not a stream
            response = _call(uri)
            response.raise_for_status()
            content_type = response.headers.get('content-type', 'audio/mpeg')
            content_type = content_type.split(';')[0]
            print('Content type: %s', content_type)
            if content_type == 'audio/mpeg':
                print('Found streaming audio at %s' % uri)
                data = None
            else:
                data = response.content.decode('utf-8', errors='ignore')
            response.close()
            return (data, content_type)
        except Exception as e:
            print('TuneIn playlist request failed: %s', e)
        return (None, None)

singelton = TuneIn(3000)