import smb.smbclient
#import pygst
#pygst.require('0.10')
#import gst
#import gobject

from mpdplayer import APlayer
from mpd import MPDClient
from walker import Walker

player = APlayer()
walker = Walker()
walker.walk("C:\\Users\\Nico\\Music")
#player.init()

_mpd = MPDClient()
_mpd.connect("localhost", 6600)
print _mpd.mpd_version
_mpd.clear()
mediaFiles = walker.getMedia()

print "{0} Files found".format(len(mediaFiles))
'''
for media in mediaFiles:
    #media.Path = media.Path.replace("\\", "\\\\")
    media.Path = media.Path.replace("\\", "/")
    #media.Path = "file:///" + media.Path
    media.Path = "file://localhost/" + media.Path
    print "Add media {0}".format(media.WebPath)
    _mpd.add(media.WebPath)
    #_mpd.playlistadd("files",media.WebPath)
'''
_mpd.add(mediaFiles[3].WebPath)
_mpd.play(0)
#_mpd.load("files")

#for info in _mpd.playlistinfo():
#    print info


print "current Song: "
print _mpd.currentsong()
print "Status:"
print _mpd.status()
#_mpd.setvol(50)
#print "Status:"
#print _mpd.status()

#mpd.playlistadd("streams", "http://173.192.32.198:80")


#smb://asrock/Netzordner/Musik/Stay Thirsty Episode 6.mp3

#player = gst.element_factory_make("playbin2", "player")
#player.set_state(gst.STATE_NULL)
#player.set_property('uri', 'file:////asrock/Netzordner/Musik/Stay Thirsty Episode 6.mp3')
#player.set_property('uri', 'smb://asrock/Netzordner/Musik/Stay Thirsty Episode 6.mp3')
#player.set_property('uri', 'file:///home/nico/dev/python/schlingel/chiddy_busty.mp3')
#player.set_state(gst.STATE_PLAYING)

#mainloop = gobject.MainLoop()
#mainloop.run()









#print "Start Scanning"
#smb = smb.smbclient.SambaClient(server="192.168.2.124",
#    share="netzordner",
#    username="nico",
#    password="ro07",
#    domain="WORKGROUP")

#for file in smb.listdir('/'):
#    if smb.isdir(file):
#        print "Found Directory: " + file
#    elif smb.isfile(file):
#        print "Found File: " + file
