# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import mutagen
import os
from Helper import Helper
from Model.MediaModel import MediaModel

_ARTIST = "TPE1"
_ALBUM = "TALB"
_TITLE = "TIT2"
_COVER = "APIC:"

class MediaModelFactory():

    def createMediaModelFromJson(self, id, json):
        model = MediaModel()
        model.ID = id
        model.IsLocal = False
        model.Album = json["album"]
        model.Artist = json["artist"]
        model.Cover = json["cover"]
        model.Title = json["title"]
        model.WebPath = json["webpath"]
        model.IsNext = False
        return model

    def createMediaModel(self, id, path, file, coverdir, ipAddress, isLocal=False):
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
        model.IsLocal = isLocal
        model.IsNext = False

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

        covername = self.getCoverName(model.Album)
        model.Cover = 'http://' + ipAddress + ":8000/Cover/" + covername
        model.ID = id
        model.Path = filepath
        model.WebPath = "http://" + ipAddress + ":8000/mediafile/" + str(id)

        if tags is not None and _COVER in tags:
            #covername = base64.b64encode(album) + ".jpg"
            coverpath = os.path.join(coverdir, covername)
            if not os.path.exists(coverpath):
                try:
                    print "Try write Coverpath: " + coverpath + " for Album " + model.Album
                    with open(coverpath, 'wb') as img:
                        img.write(tags[_COVER].data)
                except Exception, e:
                    print "Cover could not be written to " + coverpath, e
        return model

    def getCoverName(self, album):
        return Helper.hash_string(album) + ".jpg"
