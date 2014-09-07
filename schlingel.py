# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib
import os
from os import curdir, sep
import json

import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket

from aplayer import APlayer
#from mpdplayer import APlayer
import Streams
from apis import eighttracks
from apis import youtube
from Factory import TracksModelFactory

from tornado.options import define, options

from Helper.Helper import grab_cover
from Config import getMediaDirs, getOutputDir

from tornado import gen, web, httpclient

define("port", default=8000, help="run on the given port", type=int)

publicpath = "public"
debugMode = False

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #user_json = self.get_secure_cookie("chatdemo_user")
        #if not user_json: return None
        return None

class MainHandler(BaseHandler):
    index = None

    def get(self):
        global publicpath
        f = open(curdir + sep + publicpath + sep + 'index.html')
        self.index = f.read()
        f.close()
        self.write(self.index)
        self.flush()

class MediaHandler(BaseHandler):
    
    def get(self, id):
        self.streamFile(id)
        #tornado.ioloop.IOLoop.current().add_callback(self.streamFile, id=id)

    
    def streamFile(self, id):
        id = int(id)
        media = Player.walker.getMedia()[id]
        if(media):
            
            self.set_header("Content-Type", 'audio/mpeg')
            with open(media.Path, 'rb') as mediafile:
                
                total = os.path.getsize(media.Path)
                self.set_header("Content-Length", str(total))

                for line in mediafile:
                    self.write(line)
                self.flush()
                return
                '''
                range = self.request.headers.get('range', None)
                if range:
                    parts = range.replace("bytes=", "").split("-"); 
                    partialstart = parts[0]; 
                    partialend = parts[1]; 

                    total = os.path.getsize(media.Path)
                    start = int(partialstart)
                    end = total - 1
                    if partialend:
                        end = int(partialend)
                    print("start: " + str(start) + " end: " + str(end) + " total: " + str(total))
                    self.set_header("Content-Range", "bytes " + str(start) + "-" + str(end) + "/" + str(total))
                    self.set_header("Accept-Ranges", "bytes")
                    self.set_header("Content-Length", str((end-start)+1))
                    self.set_header('Transfer-Encoding', 'chunked')
                    self.set_header("Connection", "close")
                    self.set_status(206)
                    mediafile.seek(start)
                    self.write(mediafile.read(end)+"0")
                else:
                    #for line in mediafile:
                        #self.write(line)
                    b = mediafile.read(1024)
                    while len(b) > 0:
                        self.write(b)
                        b = mediafile.read(1024)

            self.flush()
'''

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
        for mediadir in getMediaDirs():
            grab_cover(mediadir, getOutputDir())

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
        files = Player.filterMedia(term, start, end)
        self.write(files)
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
        self.handle()
    def post(self):
        self.handle()

    def handle(self):
        searchTerm = self.get_argument("search", None)
        albumCount = self.get_argument("albumCount", 10)
        albumPage = self.get_argument("albumPage", 1)
        albumCount = int(albumCount)
        albumPage = int(albumPage)
        albums = Player.walker.getAlbums(searchTerm, albumPage, albumCount)
        self.write({"albums": albums})
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
        streams = Streams.getStreams()
        self.write(streams)
        self.flush()

class HandleAddStream(BaseHandler):

    def post(self):
        path = self.get_argument('item', None)
        Streams.addStream(path)


class HandleRemoveStream(BaseHandler):

    def post(self):
        id = self.get_argument('id', None)
        if id:
            Streams.removeStream(int(id))

class HandleDiscover(BaseHandler):
    def get(self):
        Player.walker.discoverSchlingel()


class HandleRadioSearch(BaseHandler):
    def get(self):
        result = {}
        
        term = self.get_argument('search', None)
        result["result"] = Streams.search(term)

        self.write(result)
        self.flush()

class HandleRadioRecommendations(BaseHandler):
    def get(self):
        result = {}
        result["recommendations"] = Streams.recommendations()

        self.write(result)
        self.flush()


class HandleRadioTop(BaseHandler):
    def get(self):
        result = {}
        result["top"] = Streams.top()

        self.write(result)
        self.flush()

class HandleRadioMostWanted(BaseHandler):
    def get(self):
        result = {}
        result["mostWanted"] = Streams.mostWanted()

        self.write(result)
        self.flush()

class HandlePlayRadio(BaseHandler):
    def post(self,):
        
        id = self.get_argument('id', None)
        if not id is None:
            station = Streams.getByStationID(id)
            Player.playStreamModel(station)

        self.write(Player.getinfo())
        self.flush()


class HandleSaveRadio(BaseHandler):
    def post(self):
        #station = self.get_argument('item', None)
        #if station is not None:
        #    stationJson = json.loads(station)
        Streams.saveLastRadioResult()
        
        self.write({})
        self.flush()


class HandleTracksTag(BaseHandler):
    def get(self):
        self.handleRequest()

    def post(self):
        self.handleRequest()

    def handleRequest(self):
        tag = self.get_argument("tag", None)
        result = None
        if tag:
            result = eighttracks.tags(tag)
        
        if result:
            self.write(result)
            self.flush()

class HandleTracksExplorer(BaseHandler):
    def get(self):
        self.handleRequest()
        
    def post(self):
        self.handleRequest()

    def handleRequest(self):
        tags = self.get_argument("tags", None)
        result = None
        if tags:
            result = eighttracks.explore(tags)
        
        if result:
            self.write(result)
            self.flush()

class HandleTracksSearch(BaseHandler):
    def get(self):
        search = self.get_argument("search", None)
        if(search):
            mixes = eighttracks.search(search)
            self.write(mixes)
            self.flush()

class HandleTracksPlay(BaseHandler):
    def post(self):
        mix = self.get_argument("mix", None)
        if mix:
            mix = json.loads(mix)
            mix = TracksModelFactory.create_mix_from_post(mix)
            Player.playMix(mix)
            self.write(Player.getinfo())
            self.flush()
        else:
            print("cant get mix from post")

class HandleTracksPageing(BaseHandler):
    def get(self):
        page_to = self.get_argument("page_to")
        if page_to:
            mixes = eighttracks.page_to(page_to)
            self.write(mixes)
            self.flush()
        else:
            prit("no page_to parameter was found")

class HandleYouTubeSearch(BaseHandler):
    def get(self):
        q = self.get_argument("search", None)
        if q:
            result = {}
            result["result"] = youtube.search(q)
            self.write(result)
            self.flush()


class HandleYouTubePlay(BaseHandler):
    def get(self):
        self.play()

    def post(self):
        self.play()

    def play(self):
        id = self.get_argument("id", None)
        if id:
            result = {}
            streamModel = youtube.get_stream_model(id)
            Player.playStreamModel(streamModel)
            self.write(Player.getinfo())
            self.flush()

class HandleWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "Websocket is open and ready to connect :)"
        Player.addWatchCurrentSubscriber(self.sendCurrentInfo)

    def sendCurrentInfo(self):
        data = {
            "type": "info",
            "data": Player.getinfo()
        }
        self.write_message(data)

    def on_message(self, msg):
        self.write_message()

    def on_close(self):
        print "Websocket is closed"

class HandleRestartSchlingel(BaseHandler):
    def get(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        #python = sys.executable
        #os.execl(python, python, * sys.argv)
        os.execl(sys.executable, *([sys.executable]+sys.argv))

class CustomStaticFileHandler(tornado.web.StaticFileHandler):
    global debugMode
    def set_extra_headers(self, path):
        # Disable cache
        if debugMode:
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

Player = APlayer()

def main():
    global publicpath
    global debugMode

    print "Starte Server"
    try:
        import gobject
        gobject.threads_init()
    except Exception:   
        print "Could not load gobject"

    #Player.run()
    Player.start()
    client = ""
    if len(sys.argv) > 1:
        client = "_" + sys.argv[1]
    publicpath = os.path.join(os.path.dirname(__file__), "public" + client)
    print("publicpath: {}".format(publicpath))

    debugArg = sys.argv[len(sys.argv) - 1]
    if(debugArg == "debug"):
        debugMode = True

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
            (r"/api/music/removeStream", HandleRemoveStream),
            (r"/api/music/grabcover", CoverGrabberHandler),
            (r"/api/music/discover", HandleDiscover),
            (r"/api/music/radio/search", HandleRadioSearch),
            (r"/api/music/radio/recommendations", HandleRadioRecommendations),
            (r"/api/music/radio/top", HandleRadioTop),
            (r"/api/music/radio/mostWanted", HandleRadioMostWanted),
            (r"/api/music/playRadio", HandlePlayRadio),
            (r"/api/music/saveRadio", HandleSaveRadio),
            (r"/api/8tracks/tags", HandleTracksTag),
            (r"/api/8tracks/play", HandleTracksPlay),
            (r"/api/8tracks/search", HandleTracksSearch),
            (r"/api/8tracks/explore", HandleTracksExplorer),
            (r"/api/8tracks/page", HandleTracksPageing),
            (r"/api/youtube/search", HandleYouTubeSearch),
            (r"/api/youtube/play", HandleYouTubePlay),
            (r"/api/restartSchlingel", HandleRestartSchlingel),
            (r"/websocket", HandleWebSocket),
            (r"/(.*)", CustomStaticFileHandler, dict(path=publicpath))
        ]
    )
    app.listen(options.port)
    print "Und los .."
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
    tornado.ioloop.IOLoop.instance().start()
    print "Schliessen"

def try_exit():
    return

def signal_handler(signum, frame):
    print "Got Signal. Try exiting ... " + str(signum)
    tornado.ioloop.IOLoop.instance().stop()
    os._exit(1)

if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGINT, signal_handler)
        main()
    except KeyboardInterrupt:
        print "Try exiting ... "
        os._exit(1)
        print "exiting not working"
