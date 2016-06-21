import urllib2
import json
from Factory.MediaModelFactory import MediaModelFactory
import Config
from thread import allocate_lock
from threading import Thread
from Helper import Helper
from subprocess import *

class Walker:
    def __init__(self):
        self.player = None
        self.allowdFiles = ['.mp3', '.m4a', '.wma', '.ogg']
        self.mediafiles = []
        self.currentId = 0
        self.currentFiltered = []
        self.media_albums = None
        self.mediafactory = MediaModelFactory()
        self.ipAdress = Helper.getIpAdress()
        self.lock = allocate_lock()
        self.init()

    def init(self):
        

        t = Thread(target = self.walkMusicfolder)
        t.start()


        t = Thread(target = self.walkShares)
        t.start()

        self.discoverSchlingel()

    def mount(self, path, user, password, mntPath):
        '''
        try:
            unmountString = "umount {0}".format(path)
            check_call(unmountString, shell=True)
        except Exception, e:
            print("Error Unmounting " + path + " Error: " + str(e))
        '''

        try:
            mountString = "mount -t cifs -o user={1}%{2} {0} {3}".format(path, user, password, mntPath)
            #check_call(mountString, shell=True)
            self.timeout_command(mountString, 3)
        except Exception, e:
            print("Error Mounting " + path + " Error: " + str(e))

    def timeout_command(self, command, timeout):
        """call shell-command and either return its output or kill it
        if it doesn't normally exit within timeout seconds and return None"""
        import subprocess, datetime, os, time, signal
        start = datetime.datetime.now()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while process.poll() is None:
          time.sleep(0.1)
          now = datetime.datetime.now()
          if (now - start).seconds> timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return None
        return process.stdout.read()

    def mount_shares(self):
        shares = []
        for share in Config.get_shares():
            mntName = Helper.hash_string(share["path"])
            mntPath = os.path.join(os.curdir, "mnt", mntName)
            if os.path.exists(mntPath) == False:
                try:
                    os.makedirs(mntPath)
                except Exception, e:
                    print("Could not create Mountpath. Error: " + str(e))
            
            self.mount(share["path"], share["user"], share["password"], mntPath)
            share["mntPath"] = mntPath
            shares.append(share)
        return shares

    def getCoverDir(self):
        return Config.getOutputDir()

    def walk(self, dir):
        if os.path.exists(dir):
            print "Search {0} for media".format(dir)
            for path, directories, files in os.walk(dir):
                for directory in directories:
                    self.walk(directory)
                for filename in files:
                    self.addFile(path, filename, True)


    def addFile(self, path, file, isLocal=False, addId3=False):
        #print "Path: " + path + "   Datei: " + file
        name, ext = os.path.splitext(file)

        for extension in self.allowdFiles:
            if extension == ext:
                model = self.mediafactory.createMediaModelFromFile(len(self.mediafiles), path, file, self.ipAdress, isLocal)
                if(addId3):
                    self.mediafactory.addId3Informations(model, self.ipAdress, self.getCoverDir())
                self.appendMediaFile(model)
                return model


    def appendMediaFile(self, mediafile):
        self.lock.acquire()
        #print "No Lock add data"
        self.mediafiles.append(mediafile)
        self.lock.release()


    def walkMusicfolder(self):
        print("Read music dirs")
        for _dir in Config.getMediaDirs():
            self.walk(_dir)

        print("Add Id3 Tag Informations")
        for mediaModel in self.mediafiles:
            self.mediafactory.addId3Informations(mediaModel, self.ipAdress, self.getCoverDir())

    def walkShares(self):
        print("Read Shares")
        shares = self.mount_shares()
        for share in shares:
            self.walk(share["mntPath"])
            #self.walk(share["mntPath"])
        print("Add Id3 Tag Informations")
        for mediaModel in self.mediafiles:
            self.mediafactory.addId3Informations(mediaModel, self.ipAdress, self.getCoverDir())


    def getAlbums(self, filter, albumPage, albumCount):
        #if self.media_albums is None:
        self.media_albums = {}
        for media in self.mediafiles:
            if(not media.Album in self.media_albums):
                self.media_albums[media["album"]] = []

            self.media_albums[media["album"]].append(media)

        result = []
        if not filter is None and not filter is "": 
            result = []
            for album in self.media_albums:
                if filter.lower() in album.lower():
                    result.append({
                    "album": album,
                    "cover": self.mediafactory.getCoverPath(self.ipAdress, album),
                    "tracks": self.media_albums[album]
                })
        else:
            for album in self.media_albums:
                result.append({
                    "album": album,
                    "cover": self.mediafactory.getCoverPath(self.ipAdress, album),
                    "tracks": self.media_albums[album]
                })

        end = albumPage * albumCount
        start = end - albumCount
        return result[start:end]

    def getLocalMedia(self):
        result = []
        for media in self.mediafiles:
            if media.IsLocal:
                result.append(media)
        return result

    def getMedia(self):
        return self.mediafiles

    def getById(self, id):
        self.currentId = id
        return self.mediafiles[id]

    def getFiltered(self):
        return self.currentFiltered

    def getNextId(self):
        if len(self.currentFiltered) > 0:
            self.currentFiltered = self.currentFiltered[1:]
            self.currentId = self.currentFiltered[0]["id"]
            return self.currentId
        else:
            return self.currentId + 1

    def containsMediaWebPath(self, webpath):
        self.lock.acquire()
        found = False
        for media in self.mediafiles:
            if(media.WebPath == webpath):
                found = True
                break
        self.lock.release()

    def filterMedia(self, term):
        if term == "":
            return self.mediafiles

        terms = term.lower().split(" ")
        result = []

        for media in self.mediafiles:

            foundCount = 0
            path = media.Path.lower()
            artist = media.Artist.lower()
            title = media.Title.lower()
            album = media.Album.lower()

            for term in terms:
                term = term.strip()
                term = term.encode("utf-8")

                if term is "":
                    break

                if (term in title
                    or term in artist
                    or term in album
                    or term in path):
                    foundCount = foundCount + 1

            if foundCount == len(terms):

                result.append(media)

        self.currentFiltered = result
        return result


    def discoverSchlingel(self):
        print "Start Discovering. My ip is {0}".format(self.ipAdress)
        tmp = self.ipAdress.split('.')
        ipparts = tmp[0:3]
        baseIp = ".".join(ipparts)
        for i in range(0, 27):
            start = i * 10
            end = ((i+1) * 10)-1
            if(end > 254):
                end = 254
            #print "Starte Threads from {0} to {1}".format(start, end)
            t = Thread(target = self.downloadRange, args=(baseIp, start, end))
            t.start()

    def downloadRange(self, baseIp, start, end):
        for i in range(start, end):
            index = str(i)
            ip = baseIp + "." + index
            if(self.ipAdress != ip):
                testUrl = "http://" + ip + ":8000/api/music/listcomplete"
                #print "download content from: {0}".format(testUrl)
                Helper.downloadString(testUrl, self.discoverFinished)


    def discoverFinished(self, url, data):
        if data != None and data != "":
            print "Find some Stuff from: " + url
            result = data
            if isinstance(result, basestring):
                result = json.loads(result)
            if isinstance(result, str):
                result = json.loads(result)
            list = result["list"]
            for external in list:
                mediaModel = self.mediafactory.createMediaModelFromJson(len(self.mediafiles), external)
                if not self.containsMediaWebPath(mediaModel.WebPath):
                    self.appendMediaFile(mediaModel)


















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
