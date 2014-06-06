try:
    import pygst
    pygst.require('0.10')
    import gst
    import gobject
except Exception:
    print "Could not load pygst"

import sys
from walker import Walker
import threading
from random import choice
from Config import getMediaDirs

class APlayer(threading.Thread):

    player = None
    mainloop = None

    def __init__(self):
        self.volume = 5.0
        self.isPlaying = False
        self.isRandom = False
        self.walker = Walker()
        self.currentlyPlaying = {}
        self.nextId = []
        self.setVolume(self.volume)

        try:
            self.pipeline = gst.Pipeline
            self.player = gst.element_factory_make("playbin2", "player")
            pulse = gst.element_factory_make("pulsesink", "pulse")
            fakesink = gst.element_factory_make("fakesink", "fakesink")

            bus = self.player.get_bus()
            bus.add_signal_watch_full(1)
            bus.connect("message", self.on_message)
            #output = gst.parse_bin_from_description("alsasink", ghost_unconnected_pads=True)
            self.player.set_property("audio-sink", pulse)
            self.player.set_property("video-sink", fakesink)

            self.mainloop = gobject.MainLoop()
        except Exception, e:
            print "Could not set any off the gstreamer stuff and also no mainloop :/"
            print "Error: {0}".format(str(e))

        threading.Thread.__init__(self)

    def _set_state(self, state):
        try:
            self.player.set_state(state)
        except Exception, e:
            print "Could not set state {0}. Err {1}".format(state, str(e))

    def _set_property(self, prop, val):
        try:
            self.player.set_property(prop, val)
        except:
            print "Could not set property {0} to {1}".format(prop,val)

    def _set_state_NULL(self):
        try:
            self._set_state(gst.STATE_NULL)
        except Exception, e:
            print "Set State NULL not possible: {0}".format(str(e))

    def _set_state_Playing(self):
        try:
            self._set_state(gst.STATE_PLAYING)
        except Exception, e:
            print "Set State Playing not possible: {0}".format(str(e))

    def _set_state_Paused(self):
        try:
            self._set_state(gst.STATE_PAUSED)
        except Exception, e:
            print "Set State Pause not possible: {0}".format(str(e))

    def stop(self):
        self._set_state_NULL()
        self._stop.set()

    def run(self):
        print "Start Mainloop"
        
        for dir in getMediaDirs():
            self.walker.walk(dir)
        self.walker.discoverSchlingel()
        #self.walker.walkShares()
        if self.mainloop:
            self.mainloop.run()
        else:
            print "No Mainloop is set. Its None"

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
        self._set_state_NULL()
        #self._set_property('uri', 'file://' + media.Path)
        self._set_property('uri', media.WebPath)
        self.currentlyPlaying = media
        self.play()

        print "play " + media.WebPath

    def playStream(self, stream):
        print "try playing " + stream
        self._set_state_NULL()
        self._set_property('uri', stream)
        s = self.walker.getStream(stream)
        self.currentlyPlaying = {}
        self.currentlyPlaying['path'] = s["stream"]
        self.currentlyPlaying['title'] = s["format"]
        self.currentlyPlaying['cover'] = s["image"]
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
        self._set_state_Playing()
        self.isPlaying = True

    def pausePlay(self):
        self._set_state_Paused()
        self.isPlaying = False

    def playNext(self):
        print "play next ..."
        self._set_state_NULL()
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
            self._set_state_NULL()
            self.isPlaying = False

    def playPrev(self):
        print "play prev ..."
        self._set_state_NULL()
        nextid = self.currentlyPlaying["id"] - 1
        if nextid < 0:
            nextid = 0
        if nextid:
            self.playId(nextid)
        else:
            print "Leider keine id gefunden"
            self._set_state_NULL()
            self.isPlaying = False

    def search(self, term):
        return self.walker.filterMedia(term)

    #def getVolume(self):
    #    return 10 * self.player.get_property('volume')

    def setVolume(self, vol):
        vol = vol / 10
        print "Volume: " + str(vol)
        self._set_property('volume', vol)

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
