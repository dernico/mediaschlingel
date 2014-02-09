import sys
import os
import smb.smbclient
import socket
import json
from Factory.MediaModelFactory import MediaModelFactory
from Config import getOutputDir

from os import curdir, sep


class Walker:
    def __init__(self):
        self.allowdFiles = ['.mp3', '.m4a']
        self.mediafiles = []
        self.media_albums = None
        self.streams = []
        self.factory = MediaModelFactory()
        self.smb = smb.smbclient.SambaClient(server="111.1111.111.11",
                    share="folder",
                    username="xxx",
                    password="xxxx",
                    domain="WORKGROUP")
        #self.ipAdress = self.getIpAdress()

    def getCoverDir(self):
        return getOutputDir()


    def getIpAdress(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def walk(self, dir='/home/nico/Music'):
        for path, directories, files in os.walk(dir):
            for directory in directories:
                self.walk(directory)
            for filename in files:
                self.addFile(path, filename)

    def walkShares(self, dir="/Musik"):
        for file in self.smb.listdir(dir):
            _file = os.path.join(dir, file)
            if self.smb.isdir(_file):
                self.walkShares(_file)
            #elif self.smb.isfile(file):
            else:
                #file, ext = os.path.splitext(file)
                #path, filename = os.path.split(file)
                self.addFile(dir, file)

    def addFile(self, path, file):
        #print "Path: " + path + "   Datei: " + file
        name, ext = os.path.splitext(file)

        for extension in self.allowdFiles:
            if extension == ext:
                #model = MediaModel(len(self.mediafiles), path, file, self.getCoverDir())
                model = self.factory.createMediaModel(len(self.mediafiles), path, file, self.getCoverDir())
                self.mediafiles.append(model)

    def getAlbums(self):
        if self.media_albums is None:
            self.media_albums = {}
            for media in self.mediafiles:
                if(not media["album"] in self.media_albums):
                    self.media_albums[media["album"]] = []

                self.media_albums[media["album"]].append(media)

        return self.media_albums

    def getMedia(self):
        return self.mediafiles

    def filterMedia(self, term):
        if term == "":
            return self.mediafiles

        #term = unicode(term, "utf-8")
        terms = term.lower().split(" ")
        result = []

        for media in self.mediafiles:

            foundCount = 0
            path = media.Filepath.lower()
            artist = media.Artist.lower()
            title = media.Title.lower()
            album = media.Album.lower()

            #title = title.decode("utf-8")
            #title = unicode(title, "utf-8")
            #title = title.encode("utf-8")
            #title = unicode(title)

            for term in terms:
                term = term.strip()
                term = term.encode("utf-8")

                #print str(type(term)) + " " + term
                #print str(type(title)) + " " + title
                if term is "":
                    break

                if (term in title
                    or term in artist
                    or term in album
                    or term in path):
                    foundCount = foundCount + 1

            if foundCount == len(terms):

                result.append(media)

        return result

    def getStreams(self):
        if len(self.streams) == 0:
            curdir = os.getcwd()
            dir = os.path.join(curdir, "Streams")
            for path, directories, files in os.walk(dir):
                for filename in files:
                    filepath = os.path.join(dir, filename)
                    with open(filepath) as filecontent:
                        #content = filecontent.read()
                        jsonContent = json.load(filecontent)
                        self.streams.append(jsonContent)
        data = {}
        data["streams"] = self.streams
        return data































import os
import sys
from UserDict import UserDict

def stripnulls(data):
    "strip whitespace and nulls"
    return data.replace("\00", "").strip()

class FileInfo(UserDict):
    "store file metadata"
    def __init__(self, filename=None):
        UserDict.__init__(self)
        self["name"] = filename

class MP3FileInfo(FileInfo):
    "store ID3v1.0 MP3 tags"
    tagDataMap = {"title"   : (  3,  33, stripnulls),
                  "artist"  : ( 33,  63, stripnulls),
                  "album"   : ( 63,  93, stripnulls),
                  "year"    : ( 93,  97, stripnulls),
                  "comment" : ( 97, 126, stripnulls),
                  "genre"   : (127, 128, ord)}

    def __parse(self, filename):
        "parse ID3v1.0 tags from MP3 file"
        self.clear()
        try:
            fsock = open(filename, "rb", 0)
            try:
                fsock.seek(-128, 2)
                tagdata = fsock.read(128)
            finally:
                fsock.close()
            print "Pos 3: " + tagdata[:3]
            if tagdata[:3] == "TAG":
                for tag, (start, end, parseFunc) in self.tagDataMap.items():
                    value = parseFunc(tagdata[start:end])
                    print "Tag: " + tag  + " Value: " + value
                    self[tag] = parseFunc(tagdata[start:end])
        except IOError:
            print "IOError"
            pass

    def __setitem__(self, key, item):
        if key == "name" and item:
            self.__parse(item)
        FileInfo.__setitem__(self, key, item)

def listDirectory(directory, fileExtList):
    "get list of file info objects for files of particular extensions"
    fileList = [os.path.normcase(f)
                for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f)
               for f in fileList
                if os.path.splitext(f)[1] in fileExtList]
    def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):
        "get file info class from filename extension"
        subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]
        return hasattr(module, subclass) and getattr(module, subclass) or FileInfo
    return [getFileInfoClass(f)(f) for f in fileList]
