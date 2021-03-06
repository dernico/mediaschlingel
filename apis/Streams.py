import os
from Factory import StreamModelFactory
from os import curdir
from apis import radio
import json

streams = []
streamDir = os.path.join(curdir, "Streams")
lastRadioResult = None


def loadStreams():
    global streams
    if len(streams) == 0:
        for path, directories, files in os.walk(streamDir):
            for filename in files:
                filepath = os.path.join(streamDir, filename)
                with open(filepath) as filecontent:
                    # content = filecontent.read()
                    streamModel = StreamModelFactory.createFromJson(len(streams), json.load(filecontent))
                    streams.append(streamModel)


def getStreams():
    global streams
    if len(streams) == 0:
        loadStreams()
    data = {}
    data["streams"] = streams
    return data


def getStream(stream):
    global streams
    if len(streams) == 0:
        loadStreams()
    if (len(streams) > 0):
        for s in streams:
            if (s["stream"] == stream):
                return s
    return None


def addStream(path):
    global streams
    if len(streams) == 0:
        loadStreams()
    if path is None or path == "": return

    if '.m3u' in path:
        content = Helper.downloadString(path)
        print "Content m3u: {0}".format(content)
        url = Helper.parsem3u(content)
        path = url
    elif '.pls' in path:
        content = Helper.downloadString(path)
        print "Content pls: {0}".format(content)
        url = Helper.parsePls(content)
        path = url

    stream = streamfactory.createFromUrl(len(streams), path)
    writeModelToFile(stream)


def getStreamById(id):
    for stream in streams:
        if stream.Id == id:
            return stream

def removeStreamFromList(id):
    stream_to_delete = None
    for stream in streams:
        if stream.Id == id:
            stream_to_delete = stream
            break
    if stream_to_delete:
        print("Entferne Stream mit ID %s aus der Liste", str(id))
        streams.remove(stream_to_delete)


def removeStream(id):
    global streams
    stream = getStreamById(id)
    streamfile = getStreamFileName(stream)
    print("Try to delete streamfile: {}", streamfile)
    os.remove(streamfile)
    removeStreamFromList(id)


def getStreamFileName(streamModel):
    streamfile = streamModel.Stream
    streamfile = streamfile.replace(':', '').replace('/', '_')
    streamfile = os.path.join(streamDir, streamfile) + ".json"
    return streamfile


def writeModelToFile(streamModel):
    global streams
    streamfile = getStreamFileName(streamModel)
    print "Try write new Streamfile: {0}".format(streamfile)
    if not os.path.exists(streamfile):
        try:
            with open(streamfile, 'a') as file:
                file.write(json.dumps(streamModel))
                print "Added file {0}".format(streamfile)
                streams = []
        except Exception as ex:
            print "Error: {0}".format(str(ex))


'''
Excample of one entry:
{
    bitrate: 128
    broadcastType: 1
    country: "Russland"
    currentTrack: "Snoop Dogg Pres Doggys Angels - Keep Ya Head Up"
    genresAndTopics: "Hip-Hop, Rap"
    id: 6564
    name: "Radio Hip-Hop"
    picture1Name: "t100.png"
    picture1TransName: "t100.png"
    picture7Url: ""
    pictureBaseURL: "http://static.radio.de/images/broadcasts/ee/6e/6564/"
    playable: "FREE"
    rank: 1119
    rating: 4.7
    streamContentFormat: "MP3"
    subdomain: "radiohip-hop"
}

'''


def search(term):
    result = radio.search(term)
    return result


def getByStationID(station_id):
    global lastRadioResult
    station = radio.getByStationID(station_id)
    lastRadioResult = streamfactory.createFromRadio(len(streams), station)
    return lastRadioResult


def saveLastRadioResult():
    writeModelToFile(lastRadioResult)


def recommendations():
    return radio.getRecommendations()


def top():
    return radio.getTop()


def mostWanted():
    return radio.getMostWanted()


def get_categories(type):
    return radio.get_categories(type)


def get_stations_by_category(type, categorie):
    return radio.get_stations_by_category(type, categorie)