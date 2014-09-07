from urllib import urlencode
from Helper import Helper
from Factory.StreamModelFactory import StreamModelFactory
import json
import Config


yt_api_endpoint = 'https://www.googleapis.com/youtube/v3/'
yt_key = Config.getYoutubeApiKey()


def search(q):
    query = {
        'part': 'id,snippet',
        'maxResults': 15,
        'type': 'video',
        'q': q,
        'key': yt_key
    }
    result = _call(yt_api_endpoint+'search', param=query)
    #return result
    tracks = []
    for item in result['items']:
        try:
            if item["id"]["kind"] == "youtube#video":
                track = {}
                track["title"] = item["snippet"]["title"]
                track["id"] = item["id"]["videoId"]
                track["description"] = item["snippet"]["description"]
                track["thumbnail"] = item["snippet"]["thumbnails"]["high"]["url"]
                '''
                video = pafy.new(track["id"])
                audio = video.getbestaudio()
                if not audio:
                    audio = video.getbest()
                    print("video: " + audio.title + " " + audio.mediatype)
                track["stream"] = audio.url
                '''
            	tracks.append(track)
        except Exception as e:
            print(str(e))
    return tracks
    
def get_stream_model(id):
    factory = StreamModelFactory()
    return factory.createFromYouTube(id)


def _call(url, param=None):
        #print('call radio with path=%s, param=%s', path, param)
        if param:
            url += '?' + urlencode(param)
        print("call radio with url: " + url)
        response = Helper.downloadString(url)
        json_data = json.loads(response)
        return json_data