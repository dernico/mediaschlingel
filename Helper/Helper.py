# -*- coding: utf-8 -*-
import urllib2
import socket
import hashlib

try:
    import cover_grabber
    from cover_grabber.os.media_dir_walker import MediaDirWalker
except:
    print "Could not load Cover Grabber. Pls install from libs folder"

def grab_cover(mediadir, outputdir, overwrite = False):
    media_walker = MediaDirWalker(mediadir, outputdir, overwrite).do_walk_path()

def hash_string(toHash):
    return hashlib.sha224(toHash).hexdigest()

def getIpAdress():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

def downloadString(url, callback=None):
    content = None
    try:
        c = urllib2.urlopen(url, timeout=5)
        content = c.read();
    except Exception as ex:
        #print "Error: {0}".format(str(ex))
        content = None

    if callback: callback(content)
    else: return content

def parsem3u(content):
    lines = content.split('\n')
    for line in lines:
        if line.startswith('http'):
            stream = ""
            if '.m3u' in line:
                filecontent = downloadString(line)
                stream = parsePls(filecontent)
                #for url in nexturls:
                    #urls.append(url)
            elif '.pls' in line:
                filecontent = downloadString(line)
                stream = parsePls(filecontent)
                #for url in nexturls:
                #    urls.append(url)

            return stream



def parsePls(content):
    lines = content.spint('\n')
    for line in lines:
        line = line.lowercase()
        if line.startswith('file'):
            tmp = line.split('=')
            if len(tmp) == 2:
                return tmp[1]
