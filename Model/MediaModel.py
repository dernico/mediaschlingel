# -*- coding: utf-8 -*-

class MediaModel(dict):

    @property
    def ID(self):
        return self['id']

    @ID.setter
    def ID(self, value):
        self['id'] = value

    @property
    def Title(self):
        return self['title']

    @Title.setter
    def Title(self, value):
        self['title'] = value

    @property
    def Artist(self):
        return self['artist']

    @Artist.setter
    def Artist(self, value):
        self['artist'] = value

    @property
    def Album(self):
        return self['album']

    @Album.setter
    def Album(self, value):
        self['album'] = value

    @property
    def Cover(self):
        return self['cover']

    @Cover.setter
    def Cover(self, value):
        self['cover'] = value

    @property
    def WebPath(self):
        return self['webpath']

    @WebPath.setter
    def WebPath(self, value):
        self['webpath'] = value

    @property
    def Path(self):
        return self.path

    @Path.setter
    def Path(self, value):
        self.path = value

    @property
    def IsLocal(self):
        return self['islocal']

    @IsLocal.setter
    def IsLocal(self, value):
        self['islocal'] = value

    @property
    def IsNext(self):
        return self['isnext']

    @IsNext.setter
    def IsNext(self, value):
        self['isnext'] = value

    def __init__(self):
        self.path = ""
        self.ID = ""
        self.Title = ""
        self.Artist = ""
        self.Album = ""
        self.Cover = ""
        self.WebPath = ""
        self.IsLocal = False
        self.IsNext = False


    def toDict(self):
        return {
            'id': self.id,
            'artist': self.artist,
            'album': self.album,
            'title': self.title,
            'path': self.filepath,
            'WebPath': '',
            'covername': self.covername
        }