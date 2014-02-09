# -*- coding: utf-8 -*-
#Copyright Jon Berg , turtlemeat.com

import sys
import cgi
import gobject
import threading
import json
import urllib
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from aplayer import APlayer

Player = APlayer()


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            path = self.path.split('?')[0]
            print "PFAD: " + path
            if path == '/':
                path = '/index.html'
            if path.endswith(".html"):
                self.sendfile(path,'text/html')
            elif path.endswith(".js"):
                self.sendfile(path,'application/javascript')
            elif path.endswith(".css"):
                self.sendfile(path, 'text/css')
            elif path.endswith(".ttf"):
                self.sendfile(path, 'application/x-font-ttf')
            elif path.startswith('/api'):
                self.handleApi()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write("Content Type von %s wird nicht unterstüzt" %
                    self.path)
                return
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        global rootnode
        try:
            self.handleApi()
#            ctype, pdict = cgi.parse_header(
#                self.headers.getheader('content-type'))
#            if ctype == 'multipart/form-data':
#                query = cgi.parse_multipart(self.rfile, pdict)
#            self.send_response(301)

#            self.end_headers()
#            upfilecontent = query.get('upfile')
#            print "filecontent", upfilecontent[0]
#            self.wfile.write("<HTML>POST OK.<BR><BR>")
#            self.wfile.write(upfilecontent[0])

        except:
            pass

    def sendfile(self, path, contentType):
        #note that this potentially makes every file on your computer readable
        # by the internet
        f = open(curdir + sep + 'public' + path)

        self.send_response(200)
        self.send_header('Content-type', contentType)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()

    def sendjson(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data))

    def sendSuccess(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hat jeklappt :)')

    def getQuery(self):
        query = self.path.split('?')[1].split('&')
        params = {}
        for q in query:
            q = q.split("=")
            params[q[0]] = q[1]
        return params

    def handleApi(self):
        if self.path.startswith('/api/music/playpause'):
            print 'Is Playing: ' + str(Player.playing())
            if Player.playing():
                Player.pausePlay()
                print 'Pause Play'
            else:
                Player.play()
                print 'Play'
            self.sendSuccess()

        elif self.path.startswith('/api/music/list'):
            params = self.getQuery()
            term = params["filter"]
            start = int(params["skip"])
            end = start + int(params["top"])
            term = urllib.unquote(term)
            files = Player.walker.filterMedia(term)
            self.sendjson({
                'count': len(files),
                'list': files[start:end]
            })

        elif self.path.startswith('/api/music/vote'):
            print "Handle set Next"
            query = self.getQuery()
            if 'id' in query and query['id'] != '':
                print 'Next Media ID is ' + query['id']
                Player.setNext(query['id'])

        elif self.path.startswith('/api/music/next'):
            files = Player.playNext()
            self.sendjson(Player.getinfo())

        elif self.path.startswith('/api/music/prev'):
            files = Player.playPrev()
            self.sendjson(Player.getinfo())

        elif self.path.startswith('/api/music/info'):
            print "Handle info"
            info = ''
            if Player is not None and Player.getinfo() is not None:
                info = Player.getinfo()
            self.sendjson(info)

        elif self.path.startswith('/api/music/play'):
            print "Handle play"
            query = self.getQuery()
            if 'id' in query and query['id'] != '':
                _id = int(query['id'])
                Player.playId(_id)
                self.sendjson(Player.getinfo())
            else:
                if not Player.playing():
                    Player.play()
                    print "Play"

        elif self.path.startswith('/api/music/pause'):
            if Player.playing():
                Player.pausePlay()
                print "Pause"

        elif self.path.startswith('/api/music/toggleRandom'):
            if Player.playing():
                Player.pausePlay()
                print "Pause"

        elif self.path.startswith('/api/playStream'):
            Player.playStream()

        elif self.path.startswith('/api/search/'):
            term = self.path.split('/')[3]
            print "Suche nach: " + term
            term = urllib.unquote(term)
            print "Umgeformt nach: " + term
            result = Player.search(term)
            self.sendjson(result)


class MyWebServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        self.server.shutdown()
        self._stop.set()

    def run(self):
        try:
            self.server = HTTPServer(('', 8000), MyHandler)
            print 'started httpserver...'
            self.server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down server'
            self.server.socket.close()

if __name__ == '__main__':
    server = MyWebServer()
    try:
        #Player.start()
        Player.run()
        server.start()
        mainloop = gobject.MainLoop()
        gobject.threads_init()
        context = mainloop.get_context()
        mainloop.run()

        while 1:
            # Handle commands here
            print "woop woop"
            context.iteration(True)
    except KeyboardInterrupt:
        print "Go exit .. close Threads .."
        #Player.stop()
        server.stop()
        print "Threads closed .. Bye"
        sys.exit()
