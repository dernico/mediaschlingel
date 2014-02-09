import pygst
pygst.require('0.10')
import gst
import sys
from walker import Walker
import threading
from random import choice
import gobject

class APlayer(threading.Thread):
#class APlayer():
    def __init__(self):
        self.pipeline = gst.Pipeline
        self.player = gst.element_factory_make("playbin2", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch_full(1)
        bus.connect("message", self.on_message)
        self.volume = 5.0
        self.isPlaying = False
        self.isRandom = False
        self.walker = Walker()
        self.currentlyPlaying = {}
        threading.Thread.__init__(self)
        #self._stop = threading.Event()
        self.nextId = []
        self.setVolume(self.volume)
        self.mainloop = gobject.MainLoop()
        #gobject.threads_init()
        #context = mainloop.get_context()


    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self._stop.set()

    def run(self):
        print "Start Mainloop"
        self.walker.walk()
        #self.walker.walkShares()
        self.mainloop.run()

    def quit(self):
        threading.Event().set()
        #self.mainloop.quit()

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            print "Song vorbei .."
            self.playNext()

        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print >> sys.stderr, "Error: {0} {1}".format(err, debug)
            self.playNext()
        return self.isPlaying

    def playing(self):
        return self.isPlaying

    def setNext(self, nextid):
        self.nextId.append(int(nextid))

    def playId(self, id):
        print "Try play id " + str(id)
        media = self.walker.getMedia()[id]
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property('uri', 'file://' + media.Filepath)
        self.currentlyPlaying = media
        self.play()

        print "play " + media.Filepath

    def playStream(self, stream):
        print "try playing " + stream
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property('uri', stream)
        self.currentlyPlaying = {}
        self.currentlyPlaying['path'] = stream
        self.currentlyPlaying['title'] = stream
        self.play()

        print "play " + stream

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
        self.player.set_state(gst.STATE_PLAYING)
        self.isPlaying = True

    def pausePlay(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.isPlaying = False

    def playNext(self):
        print "play next ..."
        self.player.set_state(gst.STATE_NULL)
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
            self.player.set_state(gst.STATE_NULL)
            self.isPlaying = False

    def playPrev(self):
        print "play prev ..."
        self.player.set_state(gst.STATE_NULL)
        nextid = self.currentlyPlaying["id"] - 1
        if nextid < 0:
            nextid = 0
        if nextid:
            self.playId(nextid)
        else:
            print "Leider keine id gefunden"
            self.player.set_state(gst.STATE_NULL)
            self.isPlaying = False

    def search(self, term):
        return self.walker.filterMedia(term)

    #def getVolume(self):
    #    return 10 * self.player.get_property('volume')

    def setVolume(self, vol):
        vol = vol / 10
        print "Volume: " + str(vol)
        self.player.set_property('volume', vol)

    def volUp(self):
        if self.volume < 10:
            self.volume += 1
            self.setVolume(self.volume)

    def volDown(self):
        if self.volume > 0:
            self.volume -= 1
            self.setVolume(self.volume)


#play_uri('file:///home/nico/dev/python/schlingel/skit.mp3')
#player = APlayer()
#player.playStream()
