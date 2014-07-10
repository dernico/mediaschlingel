from mpd import MPDClient


import sys
from walker import Walker
import threading
from random import choice
from Config import getMediaDirs
import Streams

class APlayer(threading.Thread):

    mpd = None
    mainloop = None

    def __init__(self):
        self.volume = 0
        self.isPlaying = False
        self.isRandom = False
        self.walker = Walker()
        self.currentlyPlaying = {}
        self.nextId = []
        self.currentPlaylist = ""
        self.watchCurrentSubscriber = []
        self.timer = None

        try:
            self.mpd = MPDClient()
            self.mpd.timeout = 10;
            self.mpd.idletimeout = None
            self.walker.setMPD(self)
        except Exception, e:
            print "Problem with setting up the mpd stuff"
            print "Error: {0}".format(str(e))

        threading.Thread.__init__(self)

    def stop(self):
        self.mpd.close()
        self.mpd.disconnect()
        self._stop.set()


    def loadAndConnect(self):

        Streams.loadStreams()
        for dir in getMediaDirs():
            self.walker.walk(dir)
        self.walker.discoverSchlingel()

        try:
            self.mpd.connect("localhost", 6600)
            self.mpd.consume(1)
            self.mpd.single(1)
            self.mpd.stop()
            self.setVolume()
        except Exception, e:
            print "Error {0}".format(str(e))
        print self.mpd.mpd_version
        #self.setVolume(self.volume)


    def run(self):
        print "Start Mainloop"
        self.loadAndConnect()
        #self.walker.walkShares()
        if self.mainloop:
            self.mainloop.run()
        else:
            print "No Mainloop is set. Its None"

    def quit(self):
        self.mpd.close()
        self.mpd.disconnect()
        threading.Event().set()
        #self.mainloop.quit()


    def playing(self):
        return self.isPlaying

    def setNext(self, nextid):
        self.nextId.append(int(nextid))

    def watchCurrentSongFunc(self):
        current = None
        try:
            current = self.mpd.currentsong()
            if current and current["file"]:
                #print current
                self.watchCurrentSong()
            else:
                self.playNext()
        except Exception, e:
            print "Error {0}".format(str(e))

        #for infoCallback in self.watchCurrentSubscriber:
        #    infoCallback()

    def watchCurrentSong(self):
        self.stopWatchCurrentSong()
        self.timer = threading.Timer(2, self.watchCurrentSongFunc)
        self.timer.start()

    def stopWatchCurrentSong(self):
        if self.timer is not None:
            self.timer.cancel()

    def addWatchCurrentSubscriber(self, callback):
        self.watchCurrentSubscriber.append(callback)

    def plaympd(self, path):
        try:
            self.mpd.clear()
            self.mpd.add(path)
            self.mpd.play(0)
        except Exception, e:
            print "Error {0}".format(str(e))

    def playId(self, id):
        print "Try play id " + str(id)
        media = self.walker.getMedia()[id]
        self.plaympd(media.WebPath)
        
        self.watchCurrentSong()

        self.currentlyPlaying = media
        print "play " + media.WebPath

    def playStream(self, stream):
        self.stopWatchCurrentSong()
        print "try playing " + stream
        s = Streams.getStream(stream)
        self.plaympd(s.Stream)
        self.currentlyPlaying = {}
        self.currentlyPlaying['path'] = s.Stream
        self.currentlyPlaying['title'] = s.Format
        self.currentlyPlaying['cover'] = s.Image
        self.play()

        print "play " + stream

    def tryStream(self, s):
        self.stopWatchCurrentSong()
        print "try playing " + s.Stream
        self.plaympd(s.Stream)
        self.currentlyPlaying = {}
        self.currentlyPlaying['path'] = s.Stream
        self.currentlyPlaying['title'] = s.Format
        self.currentlyPlaying['cover'] = s.Image
        self.play()

        print "checkout Stream: " + s.Stream

    def getinfo(self):
        self.currentlyPlaying['IsPlaying'] = self.isPlaying
        self.currentlyPlaying['IsRandom'] = self.isRandom
        self.currentlyPlaying['Volume'] = self.volume
        return self.currentlyPlaying

    def toggleRandom(self):
        if self.isRandom:
            self.isRandom = False
        else:
            self.isRandom = True

    def play(self):
        try:
            self.mpd.pause(0)
        except Exception, e:
            print "Error: {0}".format(str(e))
        self.isPlaying = True

    def pausePlay(self):
        try:
            self.mpd.pause(1)
        except Exception, e:
            print "Error: {0}".format(str(e))
        self.isPlaying = False

    def playNext(self):
        print "play next ..."
        nextid = 0
        if len(self.nextId) > 0:
            nextid = self.nextId[0]
            self.nextId = self.nextId[1:]
        elif self.isRandom:
            nextid = choice(self.walker.getMedia())["id"]
        else:
            nextid = self.currentlyPlaying["id"] + 1

        if nextid >= len(self.walker.getMedia()):
            nextid = 0
        if nextid:
            self.playId(nextid)
        else:
            print "Leider keine id gefunden"
            self.isPlaying = False

    def playPrev(self):
        print "play prev ..."
        nextid = self.currentlyPlaying["id"] - 1
        if nextid < 0:
            nextid = 0
        if nextid:
            self.playId(nextid)
        else:
            print "Leider keine id gefunden"
            self.isPlaying = False

    def search(self, term):
        return self.walker.filterMedia(term)

    #def getVolume(self):
    #    return 10 * self.player.get_property('volume')

    def setVolume(self):
        status = self.mpd.status()
        if status is not None and status["volume"] is not None:
            self.volume = int(status["volume"])

    def setMpdVolume(self, vol):
        #vol = vol / 10
        print "Volume: " + str(vol)
        try:
            self.mpd.setvol(vol)
        except Exception, e:
            print("Error: {0}", str(e))

    def volUp(self):
        if self.volume < 100:
            self.volume += 5
            self.setMpdVolume(self.volume)

    def volDown(self):
        if self.volume > 0:
            self.volume -= 5
            self.setMpdVolume(self.volume)

    def filterMedia(self, term, start, end):
        media = self.walker.filterMedia(term)
        count = len(media)
        media = media[start:end]
        for m in media:
            if m.ID in self.nextId:
                m.IsNext = True;
        return {
            'count': count,
            'list': media
        }


#play_uri('file:///home/nico/dev/python/schlingel/skit.mp3')
#player = APlayer()
#player.playStream()
