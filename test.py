import smb.smbclient
#import pygst
#pygst.require('0.10')
#import gst
#import gobject
import os
from walker import MP3FileInfo
from mutagen.mp3 import EasyMP3 as mp3
import mutagen


filepath = '/home/nico/Music/9th_Wonder_And_Buckshot-Chemistry-2005-FU/02-9th_wonder_and_buckshot-hes_back.mp3'


title = ""
album = ""
artist = ""


e = mutagen.File(filepath, easy=True)

title = e["title"][0]

print title

'''
info = MP3FileInfo(filepath)


if "artist" in info:
    artist = info["artist"].decode("cp1252").encode('utf-8')
if "album" in info:
    album = info["album"].decode("cp1252").encode('utf-8')
if "title" in info:
    title = info["title"].decode("cp1252").encode('utf-8')

print "Title: " + title
print "Album: " + album
print "Artist: " + artist
'''

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
