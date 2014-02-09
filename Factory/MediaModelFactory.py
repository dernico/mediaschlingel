# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import mutagen
import os
import hashlib
from Model.MediaModel import MediaModel

_ARTIST = "TPE1"
_ALBUM = "TALB"
_TITLE = "TIT2"
_COVER = "APIC:"

class MediaModelFactory():

    #def __init__(self):

    def createMediaModel(self, id, path, file, coverdir):
        filepath = os.path.join(path, file)
        audiofile = mutagen.File(filepath)
        tags = audiofile.tags

        model = MediaModel()
        #for key in tags:
        #    print "Key " + key + " Value: " + str(audiofile.tags[key])

        #print "------------------"

        model.Artist = ""
        model.Album = ""
        model.Title = ""

        if tags is not None and _ARTIST in tags:
            model.Artist = str(tags[_ARTIST])
            #artist = artist.decode("cp1252").encode('utf-8')
        if tags is not None and _ALBUM in tags:
            model.Album = str(tags[_ALBUM])
            #album = album.decode("cp1252").encode('utf-8')
        if tags is not None and _TITLE in tags:
            model.Title = str(tags[_TITLE])
            #title = title.decode("cp1252").encode('utf-8')

        if model.Title is None or model.Title is "":
            model.Title = file
        if model.Album is None or model.Album is "":
            model.Album = path

        model.Cover = self.getCoverName(model.Album)
        model.ID = id
        model.Filepath = filepath

        if tags is not None and _COVER in tags:
            #covername = base64.b64encode(album) + ".jpg"
            coverpath = os.path.join(coverdir, model.Cover)
            if not os.path.exists(coverpath):
                try:
                    print "Try write Coverpath: " + coverpath + " for Album " + model.Album
                    with open(coverpath, 'wb') as img:
                        img.write(tags[_COVER].data)
                except Exception, e:
                    print "Cover could not be written to " + coverpath, e
        return model

    def getCoverName(self, album):
        return hashlib.sha224(album).hexdigest() + ".jpg"
