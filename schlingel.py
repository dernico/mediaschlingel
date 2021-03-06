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

from aplayer import Player
#from mpdplayer import Player
from apis import Streams
from apis import eighttracks
from apis import youtube
from apis import tunein
from apis import deezer
from Factory import TracksModelFactory
from Factory import StreamModelFactory

from tornado.options import define, options

from Helper.Helper import grab_cover
from Config import getMediaDirs, getOutputDir

from tornado import gen, web, httpclient

define("port", default=8000, help="run on the given port", type=int)

publicpath = "public"
debugMode = False


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get_current_user(self):
        return ""
        #return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    index = None

    def get(self):
        #if not self.current_user:
        #    self.redirect("/login")
        #    return
        #print("Hello " + self.current_user)
        global publicpath
        f = open(publicpath + sep + 'index.html')
        self.index = f.read()
        f.close()
        self.write(self.index)
        self.flush()

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user","/")
        self.redirect("/")



class MediaHandler(BaseHandler):
    def get(self, id):
        self.streamFile(id)
        #tornado.ioloop.IOLoop.current().add_callback(self.streamFile, id=id)


    def streamFile(self, id):
        id = int(id)
        media = Player.walker.getMedia()[id]

        if (media):

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
        print("test")
        coverpath = os.path.join(Player.walker.getCoverDir(), cover)
        if not os.path.exists(coverpath):
            print("cover not found: " + coverpath)
            coverpath = os.path.join(curdir, publicpath, "nopic.jpg")
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
    def get(self):
        self.handle()

    def post(self):
        self.handle()

    def handle(self):
        files = Player.playNext()
        self.write(Player.getinfo())
        self.flush()


class HandlePrev(BaseHandler):
    def get(self):
        self.handle()

    def post(self):
        self.handle()

    def handle(self):
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
        #print "Handle playStream"
        print("play stream was called")
        stream = self.get_argument('stream', None)
        if stream is not None:
            print("now playing stream")
            Player.playStream(stream)
        else:
            print("stream was not set")
            #if not Player.playing():
            #    Player.play()
            #    print "Play"

        self.write(Player.getinfo())
        self.flush()


class HandlePause(BaseHandler):
    def get(self):
        self.handle()

    def post(self):
        self.handle()

    def handle(self):
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
        #print "Suche nach: " + term
        term = urllib.unquote(term)
        #print "Umgeformt nach: " + term
        result = Player.search(term)
        self.write(result)
        self.flush()


class HandleVolumeUp(BaseHandler):
    def get(self):
        self.handle()

    def post(self):
        self.handle()

    def handle(self):
        Player.volUp()
        info = Player.getinfo()
        self.write(info)
        self.flush()


class HandleVolumeDown(BaseHandler):
    def get(self):
        self.handle()

    def post(self):
        self.handle()

    def handle(self):
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
        Player.walker.init()


class HandleTuneinPlay(BaseHandler):
    def post(self):
        item = self.get_argument('item', None)
        if not item is None:
            item = json.loads(item)
            tunein.play(item)

        self.write(Player.getinfo())
        self.flush()

class HandleTuneinSearch(BaseHandler):
    def get(self):
        result = {}

        term = self.get_argument('search', None)
        result["result"] = tunein.search(term)

        self.write(result)
        self.flush()


class HandleTuneinCategories(BaseHandler):
    def get(self):
        result = {}

        term = self.get_argument('categorie', "")
        result["result"] = tunein.categories(term)

        self.write(result)
        self.flush()


class HandleTuneinStations(BaseHandler):
    def get(self):
        result = {}

        term = self.get_argument('station_id', "")
        result["result"] = tunein.stations(term)

        self.write(result)
        self.flush()


class HandleTuneinSave(BaseHandler):
    def post(self):
        item = self.get_argument('item', None)
        if item:
            tunein.save(item)

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
        if (search):
            mixes = eighttracks.search(search)
            self.write(mixes)
            self.flush()


class HandleTracksPlay(BaseHandler):
    def post(self):
        mix = self.get_argument("mix", None)
        if mix:
            mix = json.loads(mix)
            mix = TracksModelFactory.create_mix_from_post(mix)
            eighttracks.playMix(mix)
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
            print("no page_to parameter was found")


class HandleYouTubeSearch(BaseHandler):
    def get(self):
        q = self.get_argument("search", None)
        pageToken = self.get_argument("pageToken", None)
        if q:
            result = {}
            result = youtube.search(q, pageToken)
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
            #streamModel = youtube.get_stream_model(id)
            #Player.playStreamModel(streamModel)
            youtube.play(id)
            self.write(Player.getinfo())
            self.flush()


class HandleYoutTubeAddToPlaylist(BaseHandler):
    def get(self):
        self.add()

    def post(self):
        self.add()

    def add(self):
        trackString = self.get_argument("track", None)
        if trackString:
            track = json.loads(trackString)
            youtube.add_to_playlist(track)


class HandleYouTubePlaylist(BaseHandler):
    def get(self):
        self.playlist()

    def post(self):
        self.playlist()

    def playlist(self):
        result = youtube.get_playlist()
        self.write(result)
        self.flush()


class HandleYouTubeRelated(BaseHandler):
    def get(self, *args, **kwargs):
        video_id = self.get_argument("id", None)
        if video_id:
            result = youtube.get_related_songs(video_id)
            self.write(result)
        self.flush()

class HandleDeezerSearch(BaseHandler):
    def get(self):
        q = self.get_argument("q", None)
        #pageToken = self.get_argument("pageToken", None)
        if q:
            result = {}
            result = deezer.search(q)
            self.write(result)
            self.flush()

class HandleDeezerPlay(BaseHandler):
    def get(self):
        self.play()

    def post(self):
        self.play()

    def play(self):
        item = self.get_argument("item", None)
        if item:
            deezer.play(json.loads(item))
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
        os.execl(sys.executable, *([sys.executable] + sys.argv))

class HandleUpload(BaseHandler):
    def post(self):
        fileinfo = self.request.files['nexttrack'][0]

        fname = fileinfo['filename']
        mediadir = getMediaDirs()[0]
        filepath = os.path.join(mediadir, fname)

        model = None
        if not os.path.exists(filepath):
            fh = open(filepath, 'w')
            fh.write(fileinfo['body'])
            model = Player.walker.addFile(mediadir, fname, True, True)
        else:
            model = Player.walker.filterMedia(filepath)
        Player.setNext(model.ID)
        Player.playNext()
        self.finish(Player.getinfo())


class CheckAndPlayFile(BaseHandler):
    def get(self):
        filename = self.get_argument("filename", None)
        if filename:
            mediadir = getMediaDirs()[0]
            filepath = os.path.join(mediadir, filename)

            model = None
            result = Player.walker.filterMedia(filepath)
            if len(result) > 0:
                model = result[0]
            if model:
                print "filename - " + filepath + " - exists."
                Player.setNext(model.ID)
                Player.playNext()
                self.finish(Player.getinfo())
            else:
                print "filename - " + filepath + " - does not exist"
                self.finish("false")


class CustomStaticFileHandler(tornado.web.StaticFileHandler):
    global debugMode

    def set_extra_headers(self, path):
        # Disable cache
        #if debugMode:
        self.set_header('Cache-Control', 'no-store, no-bcache, must-revalidate, max-age=0')


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
    if len(sys.argv) > 1 and sys.argv[1] != "debug":
        client = "_" + sys.argv[1]
    publicpath = os.path.join(os.path.dirname(__file__), "public" + client)
    print("publicpath: {}".format(publicpath))

    debugArg = sys.argv[len(sys.argv) - 1]
    if (debugArg == "debug"):
        debugMode = True

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/Cover/([^/]+)", CoverHandler),
            (r"/mediafile/([^/]+)", MediaHandler),
            (r"/api/music/upload", HandleUpload),
            (r"/api/music/checkandplay", CheckAndPlayFile),
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


            (r"/api/tunein/search", HandleTuneinSearch),
            (r"/api/tunein/play", HandleTuneinPlay),
            (r"/api/tunein/categories", HandleTuneinCategories),
            (r"/api/tunein/stations", HandleTuneinStations),
            (r"/api/tunein/save", HandleTuneinSave),

            (r"/api/8tracks/tags", HandleTracksTag),
            (r"/api/8tracks/play", HandleTracksPlay),
            (r"/api/8tracks/search", HandleTracksSearch),
            (r"/api/8tracks/explore", HandleTracksExplorer),
            (r"/api/8tracks/page", HandleTracksPageing),

            (r"/api/youtube/search", HandleYouTubeSearch),
            (r"/api/youtube/play", HandleYouTubePlay),
            (r"/api/youtube/addplaylist", HandleYoutTubeAddToPlaylist),
            (r"/api/youtube/related", HandleYouTubeRelated),
            (r"/api/youtube/playlist", HandleYouTubePlaylist),

            (r"/api/deezer/search", HandleDeezerSearch),
            (r"/api/deezer/play", HandleDeezerPlay),

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



'''
old code - maybe useful later if radio.de has open api

 ...
(r"/api/music/radio/search", HandleRadioSearch),
(r"/api/music/radio/recommendations", HandleRadioRecommendations),
(r"/api/music/radio/categories", HandleRadioCategories),
(r"/api/music/radio/top", HandleRadioTop),
(r"/api/music/radio/mostWanted", HandleRadioMostWanted),
(r"/api/music/radio/bycategorie", HandleRadioStationsByCategories),
(r"/api/music/playRadio", HandlePlayRadio),
...

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

class HandleRadioCategories(BaseHandler):
    def get(self):
        type = self.get_argument('categorieType', None)
        if type:
            result = {
                "categories": Streams.get_categories(type)
            }
            self.write(result)

class HandleRadioStationsByCategories(BaseHandler):
    def get(self):
        type = self.get_argument('categorieType', None)
        categorie = self.get_argument('categorie', None)
        if categorie and type:
            result = {
                "stations": Streams.get_stations_by_category(type, categorie)
            }
            self.write(result)

class HandlePlayRadio(BaseHandler):
    def post(self, ):
        id = self.get_argument('id', None)
        if not id is None:
            station = Streams.getByStationID(id)
            Player.playStreamModel(station)

        self.write(Player.getinfo())
        self.flush()
'''
