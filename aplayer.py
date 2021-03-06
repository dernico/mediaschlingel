try:
    import gi
    gi.require_version('Gst', '1.0')
    #import gst
    #import gobject
    from gi.repository import GObject,Gtk
    from gi.repository import Gst as gst
except Exception:
    print "Could not load pygst"

from walker import Walker
import threading
from random import choice
from apis import Streams
import subprocess

from Player.DeezerPlayer import Player as dz_player


class Base_Player(threading.Thread):

    player = None
    mainloop = None
    on_media_end = None
    play_next = None
    play_prev = None
    on_pause = None
    on_play = None

    def __init__(self):

        self.localType = "local"
        self.streamType = "stream"
        self.eightTacksType = "8tracks"
        self.volume = 5.0
        self.isPlaying = False
        self.isRandom = False
        self.walker = Walker()
        self.currentlyPlaying = {}
        self.nextId = []
        #self.setVolume(self.volume)
        self.setDefaultMediaHandling()

        try:
            #self.pipeline = gst.Pipeline
            #self.player = gst.element_factory_make("playbin2", "player")
            #self.player = gst.element_factory_make("playbin", "player")
            #self.player = gst.element_factory_make("pulsesink", "player")
            #fakesink = gst.element_factory_make("fakesink", "fakesink")

            #bus = self.player.get_bus()
            #bus.add_signal_watch_full(1)
            #bus.connect("message", self.on_message)
            #output = gst.parse_bin_from_description("alsasink", ghost_unconnected_pads=True)
            #self.player.set_property("audio-sink", pulse)
            #self.player.set_property("video-sink", fakesink)

            self.mainloop = GObject.MainLoop()


            #GObject.threads_init()
            gst.init(None)
            self.pipeline = gst.Pipeline()
            #self.player = gst.ElementFactory.make('autoaudiosink', 'audio_sink')

            #self.pipeline.add(self.player)
            
            #bus = self.pipeline.get_bus()
            #bus.add_signal_watch_full(1)
            #bus.connect("message", self.on_message)

            self.player = gst.ElementFactory.make("playbin", "player")
            fakesink = gst.ElementFactory.make("fakesink","fakesink")
            self.player.set_property("video-sink",fakesink)
            bus = self.player.get_bus()
            #bus.add_signal_watch()
            bus.add_signal_watch_full(1)
            bus.connect("message",self.on_message)

        except Exception, e:
            print "Could not set any off the gstreamer stuff and also no mainloop :/"
            print "Error: {0}".format(str(e))

        threading.Thread.__init__(self)

    def default_media_end(self, player):
        # if(self.currentlyPlaying['type'] is "8tracks"):
        #     mix_id = self.currentlyPlaying['mix_id']
        #     track = eighttracks.next(mix_id)
        #     if track:
        #         self._playTrack(mix_id, track)
        # else:
        self.playNext()

    def _set_state(self, state):
        try:
            self.player.set_state(state)
            #self.pipeline.set_state(state)
        except Exception, e:
            print "Could not set state {0}. Err {1}".format(state, str(e))

    def _set_property(self, prop, val):
        try:
            self.player.set_property(prop, val)
            #self.pipeline.set_property(prop, val)
        except:
            print "Could not set property {0} to {1}".format(prop,val)

    def _set_state_NULL(self):
        try:
            self._set_state(gst.State.NULL)
        except Exception, e:
            print "Set State NULL not possible: {0}".format(str(e))

    def _set_state_Playing(self):
        try:
            self._set_state(gst.State.PLAYING)
        except Exception, e:
            print "Set State Playing not possible: {0}".format(str(e))

    def _set_state_Paused(self):
        try:
            self._set_state(gst.State.PAUSED)
            #self._set_state(gst.STATE_PAUSED)
        except Exception, e:
            print "Set State Pause not possible: {0}".format(str(e))

    def stop(self):
        self._set_state_NULL()
        #self._stop.set()

    def run(self):
        print "Start Mainloop"
        
        #self.walker.walkShares()
        if self.mainloop:
            self.mainloop.run()
        else:
            print "No Mainloop is set. Its None"

    def quit(self):
        threading.Event().set()
        #self.mainloop.quit()

class APlayer(Base_Player):

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MessageType.EOS:
            #print("Player got message MESSAGE_EOS")
            if self.on_media_end:
                self.on_media_end(self)

        elif t == gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print "Error: {0} {1}".format(err, debug)
            self.playNext()

    def playing(self):
        return self.isPlaying

    def setNext(self, nextid):
        self.nextId.append(int(nextid))

    def setDefaultMediaHandling(self):
        dz_player.exit()
        self.on_media_end = self.default_media_end
        self.play_next = self._playNext
        self.play_prev = self._playPrev
        self.on_pause = self._on_pause
        self.on_play = self._play


    def playId(self, id):
        print "Try play id " + str(id)
        self.setDefaultMediaHandling()
        media = self.walker.getById(id)
        self._set_state_NULL()
        if media.IsLocal:
            self._set_property('uri', 'file://' + media.Path)
            print "play " + media.Path
        else:
            self._set_property('uri', media.WebPath)
            print "play " + media.WebPath
        self.currentlyPlaying = media
        self.currentlyPlaying['type'] = self.localType
        self.play()

    def playStream(self, stream):
        print "try playing " + stream
        self.setDefaultMediaHandling()
        self._set_state_NULL()
        self._set_property('uri', stream)
        s = Streams.getStream(stream)
        self.currentlyPlaying = {}
        if s is None:
            self.currentlyPlaying['webpath'] = stream
            self.currentlyPlaying['title'] = "Unknown"
            self.currentlyPlaying['cover'] = ""
            self.currentlyPlaying['type'] = self.streamType  
        else:
            self.currentlyPlaying['webpath'] = s["stream"]
            self.currentlyPlaying['title'] = s["name"]
            self.currentlyPlaying['cover'] = s["image"]
            self.currentlyPlaying['type'] = self.streamType
        self.play()


    def playStreamModel(self, s):
        print "try playing " + s.Stream
        self.setDefaultMediaHandling()
        self._set_state_NULL()
        self._set_property('uri', s.Stream)
        self.currentlyPlaying = {}
        self.currentlyPlaying['webpath'] = s.Stream
        self.currentlyPlaying['name'] = s.Name
        self.currentlyPlaying['title'] = s.Name
        self.currentlyPlaying['cover'] = s.Image
        self.currentlyPlaying['type'] = self.streamType
        self.play()

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
        if self.on_play:
            self.on_play()

    def _play(self):
        if self.currentlyPlaying is not None \
             and self.currentlyPlaying['type'] is self.streamType \
             and self.currentlyPlaying['webpath'] is not None:
            
            print "checkout Stream: " + self.currentlyPlaying['webpath']
            self._set_state_NULL()
            self._set_property('uri', self.currentlyPlaying['webpath'])

        self._set_property('volume', 1.0)
        self._set_state_Playing()
        self.isPlaying = True

    def playPath(self, path):
        self._set_state_NULL()
        self._set_property('uri', path)
        self._set_state_Playing()
        self.isPlaying = True

    def pausePlay(self):
        if(self.on_pause):
            self.on_pause()

    def _on_pause(self):
        if self.currentlyPlaying['type'] is self.streamType:
            self.stop()
        else:
            self.pause()

    def pause(self):
        self._set_state_Paused()
        self.isPlaying = False

    def stop(self):
        self._set_state_NULL()
        self.isPlaying = False

    def playNext(self):
        if self.play_next:
            self.play_next()

    def _playNext(self):
        print "play next ..."

        self._set_state_NULL()
        nextid = 0
        if len(self.nextId) > 0:
            nextid = self.nextId[0]
            self.nextId = self.nextId[1:]
        elif self.isRandom:
            if len(self.walker.getFiltered()) > 0:
                nextid = choice(self.walker.getFiltered())["id"]
            else:
                nextid = choice(self.walker.getMedia())["id"]
        else:
            nextid = self.walker.getNextId()

        if nextid >= len(self.walker.getMedia()):
            nextid = 0
        if nextid:
            self.playId(nextid)
        else:
            print "Leider keine id gefunden"
            self._set_state_NULL()
            self.isPlaying = False

    def playPrev(self):
        if self.play_prev:
            self.play_prev()

    def _playPrev(self):
        print "play prev ..."

        if self.currentlyPlaying['type'] is "8tracks":
            return
        
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
        #vol = vol / 10
        vol = vol * 10
        print "Volume: " + str(vol)
        #self._set_property('volume', vol)

        if (vol <= 100) and (vol >= 0):
            subprocess.call(["amixer", "-qD", "pulse", "sset", "Master", str(vol)+"%"])

    def volUp(self):
        if self.volume < 10:
            #if self.volume < 1:
            #    self.volume += 0.1
            #else:
            #    self.volume += 1
            self.volume += 0.2
            self.volume = float("{0:.2f}".format(self.volume))
            self.setVolume(self.volume)

    def volDown(self):
        if self.volume > 0.0:
            #if self.volume <= 1:
            #    self.volume -= 0.1
            #else:
            #    self.volume -= 1
            self.volume -= 0.2
            self.volume = float("{0:.2f}".format(self.volume))
            self.setVolume(self.volume)


    def filterMedia(self, term, start, end):
        media = self.walker.filterMedia(term)
        count = len(media)
        media = media[start:end]
        for m in media:
            if m.ID in self.nextId:
                m.IsNext = True
        return {
            'count': count,
            'list': media
        }

Player = APlayer()