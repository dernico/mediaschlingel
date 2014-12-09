try:
    import pygst
    pygst.require('0.10')
    import gst
    import gobject
except Exception:
    print "Could not load pygst"

from walker import Walker
import threading
from random import choice
import Streams
import subprocess


class Base_Player(threading.Thread):

    player = None
    mainloop = None
    on_media_end = None
    play_next = None
    play_prev = None
    on_pause = None

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
        self.setVolume(self.volume)
        self.setDefaultMediaHandling()

        try:
            self.pipeline = gst.Pipeline
            self.player = gst.element_factory_make("playbin2", "player")
            #pulse = gst.element_factory_make("pulsesink", "pulse")
            #fakesink = gst.element_factory_make("fakesink", "fakesink")

            bus = self.player.get_bus()
            bus.add_signal_watch_full(1)
            bus.connect("message", self.on_message)
            #output = gst.parse_bin_from_description("alsasink", ghost_unconnected_pads=True)
            #self.player.set_property("audio-sink", pulse)
            #self.player.set_property("video-sink", fakesink)

            self.mainloop = gobject.MainLoop()
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
        if t == gst.MESSAGE_EOS:
            if self.on_media_end:
                self.on_media_end(self)

        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: {0} {1}".format(err, debug)
            self.playNext()
        return self.isPlaying

    def playing(self):
        return self.isPlaying

    def setNext(self, nextid):
        self.nextId.append(int(nextid))

    def setDefaultMediaHandling(self):
        self.on_media_end = self.default_media_end
        self.play_next = self._playNext
        self.play_prev = self._playPrev
        self.on_pause = self._on_pause


    def playId(self, id):
        print "Try play id " + str(id)
        self.setDefaultMediaHandling()
        media = self.walker.getMedia()[id]
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
        self.currentlyPlaying['webpath'] = s["stream"]
        self.currentlyPlaying['title'] = s["format"]
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
        self.currentlyPlaying['title'] = s.Format
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
        if self.currentlyPlaying['type'] is self.streamType and self.currentlyPlaying['webpath'] is not None:
            print "checkout Stream: " + self.currentlyPlaying['webpath']
            self._set_state_NULL()
            self._set_property('uri', self.currentlyPlaying['webpath'])

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

    def get_master_volume(self):
        proc = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE)
        amixer_stdout = proc.communicate()[0].split('\n')[4]
        proc.wait()

        find_start = amixer_stdout.find('[') + 1
        find_end = amixer_stdout.find('%]', find_start)

        return float(amixer_stdout[find_start:find_end])

    def set_master_volume(self, volume):
        val = float(int(volume))

        proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
        proc.wait()

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

#play_uri('file:///home/nico/dev/python/schlingel/skit.mp3')
#player = APlayer()
#player.playStream()



Player = APlayer()