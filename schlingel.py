# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib
import os
from os import curdir, sep

import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web

from aplayer import APlayer

from tornado.options import define, options

from Helper.Helper import grab_cover
from Config import getMediaDir, getOutputDir

define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #user_json = self.get_secure_cookie("chatdemo_user")
        #if not user_json: return None
        return None

class MainHandler(BaseHandler):
    index = None

    def get(self):
        #if(self.index is None):
        f = open(curdir + sep + 'public' + sep + 'index.html')
        self.index = f.read()
        f.close()
        self.write(self.index)
        self.flush()

class MediaHandler(BaseHandler):
    def get(self, id):
        id = int(id)
        media = Player.walker.getMedia()[id]
        if(media):
            self.set_header("Content-Type", 'audio/mpeg')
            with open(media.Path, 'rb') as mediafile:
                for line in mediafile:
                    self.write(line)
                self.flush()


class CoverHandler(BaseHandler):

    def get(self, cover):
        coverpath = os.path.join(Player.walker.getCoverDir(), cover)
        if not os.path.exists(coverpath):
            coverpath = os.path.join(curdir, "public", "schlingel.jpg")
        print "Send Cover " + coverpath
        self.set_header("Content-Type", 'image/jpeg')
        with open(coverpath, 'rb') as cover:
            self.write(cover.read())
            self.flush()

class CoverGrabberHandler(BaseHandler):

    def get(self):
        grab_cover(getMediaDir(), getOutputDir())

class HandlePlayPause(BaseHandler):

    def get(self):
        print 'Is Playing: ' + str(Player.playing())
        if Player.playing():
            Player.pausePlay()
            print 'Pause Play'
        else:
            Player.play()
            print 'Play'

class HandleList(BaseHandler):

    def get(self):
        term = self.get_argument("filter", None)
        start = int(self.get_argument("skip", 25))
        end = start + int(self.get_argument("top", 0))
        term = urllib.unquote(term)
        files = Player.walker.filterMedia(term)
        self.write({
            'count': len(files),
            'list': files[start:end]
        })
        self.flush()

class HandleListComplete(BaseHandler):
    def get(self):
        files = Player.walker.getLocalMedia()
        self.write({
            'count': len(files),
            'list': files    
        })

class HandleAlbums(BaseHandler):

    def get(self):
        self.write(Player.walker.getAlbums())
        self.flush()

class HandleVote(BaseHandler):
    def get(self):
        print "Handle set Next"
        id = self.get_argument("id", None)
        if id is not None:
            print 'Next Media ID is ' + id
            Player.setNext(id);

class HandleNext(BaseHandler):
    def post(self):
        files = Player.playNext()
        self.write(Player.getinfo())
        self.flush()

class HandlePrev(BaseHandler):
    def post(self):
        files = Player.playPrev()
        self.write(Player.getinfo())
        self.flush()

class HandleInfo(BaseHandler):
    def get(self):
        print "Handle info"
        info = ''
        if Player is not None and Player.getinfo() is not None:
            info = Player.getinfo()
        self.write(info)
        self.flush()

class HandlePlay(BaseHandler):
    def get(self):
        self.play()
    def post(self):
        self.play()

    def play(self):
        print "Handle play"
        id = self.get_argument('id', None)
        if id is not None:
            _id = int(id)
            Player.playId(_id)
        else:
            if not Player.playing():
                Player.play()
                print "Play"

        self.write(Player.getinfo())
        self.flush()

class HandlePlayStream(BaseHandler):
    def get(self):
        self.play()

    def post(self):
        self.play()

    def play(self):
        print "Handle playStream"
        stream = self.get_argument('stream', None)
        if stream is not None:
            Player.playStream(stream)
        else:
            if not Player.playing():
                Player.play()
                print "Play"

        self.write(Player.getinfo())
        self.flush()

class HandlePause(BaseHandler):
    def post(self):
        if Player.playing():
            Player.pausePlay()
            self.write(Player.getinfo())
            self.flush()
            print "Pause"

class HandleToggleRandom(BaseHandler):
    def get(self):
        self.toggleRandom()

    def post(self):
        self.toggleRandom()

    def toggleRandom(self):
        Player.toggleRandom()
        self.write(Player.getinfo())
        self.flush()
        print "Toggle Random"

class HandleSearch(BaseHandler):
    def get(self):
        term = self.path.split('/')[3]
        print "Suche nach: " + term
        term = urllib.unquote(term)
        print "Umgeformt nach: " + term
        result = Player.search(term)
        self.write(result)
        self.flush()

class HandleVolumeUp(BaseHandler):
    def post(self):
        Player.volUp()
        info = Player.getinfo()
        self.write(info)
        self.flush()

class HandleVolumeDown(BaseHandler):
    def post(self):
        Player.volDown()
        info = Player.getinfo()
        self.write(info)
        self.flush()

class HandleGetStreams(BaseHandler):
    def get(self):
        streams = Player.walker.getStreams()
        self.write(streams)
        self.flush()

class HandleAddStream(BaseHandler):

    def post(self):
        path = self.get_argument('item', None)
        Player.walker.addStream(path)

class HandleDiscover(BaseHandler):
    def get(self):
        Player.walker.discoverSchlingel()

from Radio import api
class HandleRadio(BaseHandler):
    def get(self):
        topstations = api.get_top_stations()
        result = {}
        result["topstations"] = topstations
        self.write(result)
        self.flush()

class CustomStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

Player = APlayer()

def main():
    print "Starte Server"
    try:
        import gobject
        gobject.threads_init()
    except Exception:
        print "Could not load gobject"

    #Player.run()
    Player.start()
    public = os.path.join(os.path.dirname(__file__), "public")
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/Cover/([^/]+)", CoverHandler),
            (r"/mediafile/([^/]+)", MediaHandler),
            (r"/api/music/playpause", HandlePlayPause),
            (r"/api/music/playStream", HandlePlayStream),
            (r"/api/music/play", HandlePlay),
            (r"/api/music/info", HandleInfo),
            (r"/api/music/list", HandleList),
            (r"/api/music/listcomplete", HandleListComplete),
            (r"/api/music/albums", HandleAlbums),
            (r"/api/music/vote", HandleVote),
            (r"/api/music/next", HandleNext),
            (r"/api/music/toggleRandom", HandleToggleRandom),
            (r"/api/music/prev", HandlePrev),
            (r"/api/music/pause", HandlePause),
            (r"/api/music/volumeUp", HandleVolumeUp),
            (r"/api/music/volumeDown", HandleVolumeDown),
            (r"/api/music/streams", HandleGetStreams),
            (r"/api/music/addListenPls", HandleAddStream),
            (r"/api/music/grabcover", CoverGrabberHandler),
            (r"/api/music/discover", HandleDiscover),
            (r"/api/music/radio", HandleRadio),
            (r"/(.*)", CustomStaticFileHandler, dict(path=public))
        ]
    )
    app.listen(options.port)
    print "Und los .."
    tornado.ioloop.IOLoop.instance().start()
    print "Schliessen"

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Try exiting ... "
        os._exit(os.EX_OK)
        print "exiting not working"
